## 1. Cache partagé (anti-spam du lien de connexion)

- [x] 1.1 Remplacer `LocMemCache` par `DatabaseCache` (table `django_cache`) dans `config/settings.py`, en mettant à jour le commentaire
- [x] 1.2 Ajouter un test qui vérifie que la limite d'un lien par email et par minute s'appuie sur le cache partagé : une deuxième demande dans la minute n'envoie pas d'email, et une demande après expiration en renvoie un
- [x] 1.3 Lancer la suite de tests complète et vérifier qu'elle passe avec le nouveau backend

## 2. Serveur d'application

- [x] 2.1 Ajouter `gunicorn` aux dépendances avec `uv add gunicorn` (met à jour `pyproject.toml` et `uv.lock`)
- [x] 2.2 Vérifier en local que `gunicorn config.wsgi` sert le site avec `DEBUG=false` et des statiques collectés

## 3. Image Docker et démarrage

- [x] 3.1 Créer `.dockerignore` (`.venv`, `.env`, `db.sqlite3*`, `.git`, `staticfiles`, `__pycache__`, `openspec`, `.claude`)
- [x] 3.2 Créer `start.sh` (exécutable, `set -e`) : `migrate --noinput`, `createcachetable`, `purge_unused_accounts` non bloquant (erreur journalisée), puis `exec gunicorn config.wsgi` sur `0.0.0.0:$PORT` avec 2 workers `gthread` × 4 threads par défaut et les logs d'accès sur la sortie standard
- [x] 3.3 Créer le `Dockerfile` : `python:3.12-slim`, uv copié depuis son image officielle, `uv sync --frozen --no-dev` avant la copie du code, `.venv/bin` dans le `PATH`, `collectstatic --noinput` avec `DEBUG=false` et une `SECRET_KEY` factice passée inline (pas en `ENV`), `CMD` sur `start.sh`
- [x] 3.4 Tester l'image en local : `docker build`, puis `docker run` avec un volume monté sur `/data`, `DATABASE_PATH=/data/db.sqlite3`, `DEBUG=false`, `SECURE_SSL_REDIRECT=false`. Vérifier les logs de démarrage, la mise en forme des pages, et que les données survivent à un redémarrage du conteneur
- [x] 3.5 Vérifier que l'image ne contient ni `.env`, ni base locale, ni la `SECRET_KEY` factice dans ses variables d'environnement (`docker inspect`)

## 4. Documentation

- [x] 4.1 Ajouter au README une section « Déploiement sur Railway » : création du service depuis GitHub, volume sur `/data`, liste des variables (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `SITE_URL`, `DATABASE_PATH`, SMTP), domaine `*.up.railway.app`, ce que fait `start.sh`, réglage des workers par `WEB_CONCURRENCY`
- [x] 4.2 Documenter les opérations ponctuelles via `railway ssh` (création du superutilisateur, premier quartier dans l'admin) et préciser que `railway run` n'a pas accès au volume
- [x] 4.3 Mettre à jour la section « Configuration » du README et `.env.example` (`DATABASE_PATH=/data/db.sqlite3` en prod, `collectstatic` désormais fait au build)
- [x] 4.4 Lister dans le README les sujets reportés avant l'ouverture à des testeurs : sauvegardes, pages légales, SPF/DKIM/DMARC, HSTS, limite par IP, suivi des erreurs

## 5. Mise en ligne (manuelle, sur Railway)

- [ ] 5.1 Créer le service Railway depuis le dépôt, attacher le volume `/data`, renseigner les variables et générer le domaine public
- [ ] 5.2 Vérifier le premier déploiement dans les logs, créer le superutilisateur et un quartier via `railway ssh` et l'admin
- [ ] 5.3 Recette : recevoir un lien de connexion par email, se connecter, compléter le profil, publier un objet, redéployer et constater que l'objet est toujours présent
