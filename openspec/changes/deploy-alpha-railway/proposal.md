## Why

Kerentheque ne tourne aujourd'hui qu'en local. Avant de la faire tester par un premier utilisateur, le développeur veut la mettre en ligne et vérifier lui-même son fonctionnement dans des conditions réelles (HTTPS, emails envoyés, données conservées entre deux déploiements). Il manque pour cela un serveur d'application adapté à la production et une image déployable sur Railway. De plus, la limite anti-spam du lien de connexion est stockée en mémoire, ce qui ne tient plus avec plusieurs processus.

## What Changes

- Ajout de `gunicorn` comme serveur d'application de production.
- Ajout d'un `Dockerfile` qui installe les dépendances avec uv et collecte les fichiers statiques au build.
- Ajout d'un script de démarrage qui, à chaque lancement, applique les migrations, crée la table de cache, purge les comptes inutilisés, puis lance gunicorn. Ces étapes ne peuvent pas aller dans la commande de pré-déploiement de Railway, qui n'a pas accès au volume.
- Base SQLite placée sur un volume Railway persistant (`DATABASE_PATH`), conservée d'un déploiement à l'autre.
- Le cache Django passe de la mémoire du processus (`LocMemCache`) à la base de données (`DatabaseCache`). La limite d'un lien de connexion par email et par minute est ainsi partagée entre tous les processus et survit aux redémarrages.
- README complété avec la procédure de déploiement sur Railway : variables d'environnement, volume, utilisateur du conteneur, création du superutilisateur, premier quartier.

**Hors périmètre** (reporté à une itération ultérieure) : sauvegardes de la base, pages légales et de confidentialité définitives, SPF/DKIM/DMARC et domaine personnalisé, réduction de la durée HSTS, limite des demandes par adresse IP, purge planifiée (cron), suivi des erreurs (Sentry), intégration continue, endpoint de healthcheck. Le site est servi sur une URL `*.up.railway.app`, avec les inscriptions ouvertes.

## Capabilities

### New Capabilities
- `deployment`: exécution de l'application en production : démarrage avec un serveur d'application, mise à jour automatique du schéma de base au lancement, persistance des données entre les déploiements, fichiers statiques servis par l'application.

### Modified Capabilities
- `user-accounts`: la limite d'un lien de connexion par email et par minute, déjà implémentée, devient une exigence. Elle MUST valoir pour toute l'application, quel que soit le nombre de processus, et survivre aux redémarrages.

## Impact

- **Dépendances** : ajout de `gunicorn` (`pyproject.toml`, `uv.lock`).
- **Code** : `config/settings.py` (`CACHES`).
- **Nouveaux fichiers** : `Dockerfile`, `.dockerignore`, script de démarrage.
- **Documentation** : `README.md`, `.env.example`.
- **Infrastructure** : un service Railway (plan Pro) avec un volume monté sur `/data`. Le SMTP sortant est autorisé sur ce plan.
- **Exploitation** : courte indisponibilité à chaque redéploiement (un seul replica, à cause du volume).
