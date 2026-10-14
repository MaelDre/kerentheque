## Context

L'application est déjà configurée par variables d'environnement (`config/settings.py`). SQLite y est déjà réglé en WAL + `IMMEDIATE`, avec un chemin configurable (`DATABASE_PATH`). WhiteNoise sert les statiques avec un manifeste compressé quand `DEBUG=False`, et les en-têtes de sécurité HTTPS s'activent quand `DEBUG=False`. Les dépendances sont gérées par uv (`pyproject.toml`, `uv.lock`, Python 3.12).

Contraintes Railway qui orientent les choix :
- Le volume n'est monté **qu'au lancement du conteneur**. Il n'est disponible ni pendant le build, ni dans la commande de pré-déploiement.
- Un service avec volume tourne avec **un seul replica**, et chaque redéploiement entraîne une courte coupure.
- Le volume est monté avec l'utilisateur root comme propriétaire.
- Railway fournit le port d'écoute dans la variable `PORT` et termine le TLS devant l'application, qui reçoit `X-Forwarded-Proto`.

## Goals / Non-Goals

**Goals:**
- Un `git push` sur `main` suffit pour reconstruire et redéployer l'application, sans étape manuelle.
- Une image identique en local et sur Railway (`docker build` / `docker run` pour tester avant de pousser).
- Une limite anti-spam correcte quel que soit le nombre de processus gunicorn.

**Non-Goals:**
- Fichier de configuration Railway (`railway.toml`) : Railway détecte le `Dockerfile` tout seul, et les réglages du service (volume, variables) se font dans l'interface.
- Optimisation de la taille de l'image (build multi-étapes poussé, image distroless).
- Utilisateur non-root dans le conteneur (voir décision 5).

## Decisions

### 1. Gunicorn, 2 workers `gthread` × 4 threads, réglables par variable
`gunicorn config.wsgi` écoute sur `0.0.0.0:$PORT`, avec les logs d'accès sur la sortie standard. Par défaut, 2 workers de 4 threads, ce qui suffit largement pour quelques utilisateurs. Les réglages se changent sans rebuild grâce aux variables que gunicorn lit nativement (`WEB_CONCURRENCY`, ou `GUNICORN_CMD_ARGS`).
- *Alternative* : uvicorn/ASGI. Écartée, l'application est entièrement synchrone.
- *Alternative* : 1 seul worker. Écartée : avec `DatabaseCache`, plusieurs workers ne posent plus de problème, et un deuxième worker évite qu'une requête lente bloque tout le site.

### 2. `DatabaseCache` plutôt que `LocMemCache`
`CACHES` utilise `django.core.cache.backends.db.DatabaseCache` avec une table `django_cache`, dans la même base SQLite. Le seul usage du cache est la limite d'un lien par email et par minute (`cache.add` dans `accounts/views.py`). Avec ce backend, la limite est partagée entre les workers et survit aux redémarrages, comme l'exige la spec `user-accounts`. La table se crée avec `manage.py createcachetable` (sans effet si elle existe déjà). Le lanceur de tests Django la crée aussi pour la base de test : les tests existants (`cache.clear()`) restent valables.
- *Alternative* : `FileBasedCache` sur le volume. Écartée : rien de plus simple, et ça ajoute des fichiers à gérer.
- *Alternative* : Redis. Écartée : un service de plus à payer et à maintenir pour un seul compteur.
- *Coût* : une écriture SQLite par demande de lien, ce qui est négligeable.

### 3. Image : `python:3.12-slim` + uv, collectstatic au build
- uv est copié depuis son image officielle, puis `uv sync --frozen --no-dev` installe les dépendances exactement selon `uv.lock` dans `.venv`, ajouté au `PATH`.
- Les dépendances sont copiées et installées **avant** le code, pour profiter du cache Docker.
- `collectstatic --noinput` tourne au build avec `DEBUG=false` (nécessaire pour générer le manifeste WhiteNoise). Il reçoit aussi une `SECRET_KEY` factice passée uniquement à cette commande, car `settings.py` refuse de démarrer sans clé quand `DEBUG=False`. Cette clé n'est ni conservée dans l'image ni utilisée à l'exécution.
- `.dockerignore` exclut `.venv`, `.env`, `db.sqlite3*`, `.git`, `staticfiles`, `__pycache__`, `openspec` et `.claude`. Ainsi, aucune base locale ni aucun secret n'entre dans l'image.

### 4. Script de démarrage `start.sh` : migrate → createcachetable → purge → gunicorn
Ces étapes ont besoin de la base, donc du volume. Elles ne peuvent tourner qu'au lancement du conteneur. Le script :
1. `migrate --noinput` : **bloquant** (`set -e`). Si une migration échoue, le conteneur s'arrête et Railway garde le déploiement précédent en échec visible, ce qui correspond à la spec « l'application ne démarre pas ».
2. `createcachetable` : bloquant.
3. `purge_unused_accounts` : **non bloquant**. En cas d'échec, l'erreur est écrite dans les logs et le démarrage continue. Une purge ratée ne doit pas rendre le site indisponible.
4. `exec gunicorn …` : `exec` fait de gunicorn le processus principal, pour qu'il reçoive bien le signal d'arrêt de Railway.

Le chemin par défaut `DATABASE_PATH` reste inchangé dans les settings. En prod, la variable est réglée sur `/data/db.sqlite3`, et les fichiers `-wal`/`-shm` se créent à côté, sur le volume.
- *Alternative* : enchaîner les commandes directement dans le `CMD` du Dockerfile. Écartée, c'est moins lisible et la purge serait difficile à rendre non bloquante.

### 5. Le conteneur tourne en root
Le volume Railway appartient à root. Un utilisateur non-root obligerait à définir `RAILWAY_RUN_UID=0`, ce qui revient au même, ou à faire un `chown` au démarrage, ce qui nécessite d'être root de toute façon. Pour cette itération, l'image tourne en root et gunicorn hérite de cet utilisateur.
- *Alternative à reprendre plus tard* : démarrer en root, faire `chown` sur `/data`, puis passer à un utilisateur dédié (`gosu`/`setpriv`) avant de lancer gunicorn.

### 6. Opérations ponctuelles via `railway ssh`
`railway run` exécute une commande **sur la machine locale** avec les variables Railway : il n'a donc pas accès au volume. La création du superutilisateur et les commandes de maintenance passent par `railway ssh`, qui ouvre un shell dans le conteneur, puis `python manage.py createsuperuser`. Le README le précise.

## Risks / Trade-offs

- [Perte ou corruption du fichier SQLite, sans sauvegarde] → Accepté pour l'itération 1 : les données sont celles du développeur. Le sujet des sauvegardes (Litestream ou `.backup` avant `migrate`) est à traiter avant l'itération 2.
- [Migration qui échoue en production] → Le conteneur refuse de démarrer, ce qui rend l'erreur visible dans les logs. On corrige, puis on redéploie, ou on revient au commit précédent sur Railway. Sans sauvegarde, une migration qui *réussit mais détruit des données* ne se rattrape pas : il faut relire les migrations destructrices.
- [Coupure à chaque déploiement] → Accepté (un seul replica imposé par le volume) : quelques secondes, acceptable pour une alpha.
- [Emails classés en spam (pas de SPF/DKIM)] → Accepté pour l'itération 1 : le développeur vérifie son dossier spam. Le domaine d'envoi est à configurer avant l'itération 2.
- [HSTS de 1 an sur `*.up.railway.app`] → Sans conséquence sur un sous-domaine Railway : la directive ne couvre que ce nom d'hôte et ses propres sous-domaines, et le préchargement est impossible. À revoir avec le domaine personnalisé.
- [Conteneur en root] → Surface d'attaque un peu plus grande. Accepté pour cette itération, avec une alternative identifiée (décision 5).
- [`SECRET_KEY` factice au build] → Aucun risque si elle n'est passée qu'à la commande `collectstatic` (variable inline dans le `RUN`, pas `ENV`), et donc absente de l'image finale.

## Migration Plan

1. Sur Railway : créer un service depuis le dépôt GitHub `MaelDre/kerentheque`, branche `main`, et attacher un volume monté sur `/data`.
2. Renseigner les variables d'environnement : `SECRET_KEY` (aléatoire), `DEBUG=false`, `ALLOWED_HOSTS=<app>.up.railway.app`, `CSRF_TRUSTED_ORIGINS=https://<app>.up.railway.app`, `SITE_URL=https://<app>.up.railway.app`, `DATABASE_PATH=/data/db.sqlite3`, et les paramètres SMTP. Générer le domaine public `*.up.railway.app` dans l'onglet réseau.
3. Premier déploiement : vérifier dans les logs l'enchaînement migrate → createcachetable → purge → gunicorn.
4. `railway ssh` → `python manage.py createsuperuser`, puis créer au moins un quartier dans l'admin.
5. Vérification manuelle : demander un lien de connexion, le recevoir, se connecter, compléter le profil, ajouter un objet, redéployer et constater que l'objet est toujours là.

Retour arrière : redéployer un déploiement précédent depuis l'interface Railway. Le volume est conservé. Attention, une migration déjà appliquée n'est pas annulée automatiquement.
