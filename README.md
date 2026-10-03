# Kerentheque

Application web de prêt d'objets entre habitants d'un même secteur : chacun liste
les objets qu'il accepte de prêter, et les autres membres peuvent demander à entrer
en contact avec le propriétaire. Le prêt se déroule ensuite hors de l'application.

Stack : Django 5.2, SQLite, templates rendus côté serveur, Pico CSS.

## Démarrage en local

Prérequis : Python 3.12+ et [uv](https://docs.astral.sh/uv/).

```sh
cp .env.example .env              # DEBUG=true suffit en local
uv sync
uv run --env-file .env python manage.py migrate
uv run --env-file .env python manage.py createcachetable
uv run --env-file .env python manage.py createsuperuser
uv run --env-file .env python manage.py runserver
```

- Le site est sur http://localhost:8000 et l'admin sur http://localhost:8000/admin/.
- Pour tester rapidement, chargez des données de démonstration (quartiers, deux membres
  `alice@example.com` et `bernard@example.com`, quelques objets) :
  `uv run --env-file .env python manage.py load_demo_data`
- Sinon, avant la première inscription, créez au moins un quartier dans l'admin
  (Comptes › Quartiers). Une liste de catégories par défaut est créée par les migrations.
- En local, les emails (dont les liens de connexion) sont affichés dans la console
  du serveur.

## Tests

```sh
uv run --env-file .env python manage.py test
```

## Maintenance

Supprimer les comptes créés lors d'une demande de lien mais jamais utilisés :

```sh
uv run --env-file .env python manage.py purge_unused_accounts
```

## Configuration

Toutes les variables d'environnement sont documentées dans `.env.example`.
En production (`DEBUG=false`), `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`,
`SITE_URL` et les paramètres SMTP doivent être renseignés. `DATABASE_PATH` doit
pointer vers un disque persistant. Les fichiers statiques sont collectés au build de
l'image Docker.

## Déploiement sur Railway

L'application est livrée sous forme d'image Docker (`Dockerfile`). La base SQLite
est stockée sur un volume Railway persistant.

### Mise en place (une fois)

1. Créer un service depuis le dépôt GitHub, branche `main`. Railway détecte le
   `Dockerfile` et redéploie à chaque push.
2. Attacher un volume au service, monté sur `/data`.
3. Renseigner les variables du service :

   | Variable | Valeur |
   |---|---|
   | `SECRET_KEY` | longue valeur aléatoire (`python -c "import secrets; print(secrets.token_urlsafe(50))"`) |
   | `DEBUG` | `false` |
   | `ALLOWED_HOSTS` | `<app>.up.railway.app` |
   | `CSRF_TRUSTED_ORIGINS` | `https://<app>.up.railway.app` |
   | `SITE_URL` | `https://<app>.up.railway.app` |
   | `DATABASE_PATH` | `/data/db.sqlite3` |
   | `DEFAULT_FROM_EMAIL`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS` | paramètres SMTP (SMTP sortant autorisé sur le plan Pro) |

4. Générer le domaine public (`*.up.railway.app`) dans l'onglet *Networking* du service.

### À chaque démarrage

`start.sh` applique les migrations, crée la table de cache, purge les comptes jamais
utilisés, puis lance gunicorn sur `$PORT`. Ces étapes tournent au démarrage et non
dans la commande de pré-déploiement, qui n'a pas accès au volume. Si une migration
échoue, le conteneur ne démarre pas : l'erreur est visible dans les logs du déploiement.

Gunicorn tourne par défaut avec 2 workers de 4 threads, réglables par les variables
`WEB_CONCURRENCY` et `GUNICORN_THREADS`. Avec le volume, le service n'a qu'une seule
instance : chaque redéploiement provoque une courte coupure.

Le conteneur tourne en root, propriétaire du volume. Si l'image passe un jour à un
utilisateur non-root, il faudra définir `RAILWAY_RUN_UID=0` ou changer le propriétaire
de `/data` au démarrage.

### Opérations ponctuelles

Elles se font dans le conteneur, avec `railway ssh` (après `railway link`).
`railway run` exécute la commande sur votre machine avec les variables Railway, sans
accès au volume : il ne convient pas ici.

```sh
railway ssh
python manage.py createsuperuser
```

Ensuite, créer au moins un quartier dans l'admin (`/admin/`, Comptes › Quartiers)
avant la première inscription.

### Tester l'image en local

```sh
docker build -t kerentheque .
docker run --rm -p 8000:8000 -v kerentheque-data:/data \
  -e DEBUG=false -e SECRET_KEY=test -e ALLOWED_HOSTS=localhost \
  -e SECURE_SSL_REDIRECT=false -e DATABASE_PATH=/data/db.sqlite3 kerentheque
```

### Avant d'ouvrir le site à des testeurs

Sujets volontairement reportés lors de la première mise en ligne :

- sauvegardes de la base (aucune pour l'instant : Litestream, ou copie `.backup` avant `migrate`) ;
- pages légales et politique de confidentialité, encore provisoires ;
- domaine d'envoi des emails avec SPF, DKIM et DMARC (risque de spam), et domaine personnalisé ;
- durée HSTS à réduire au départ sur un domaine personnalisé (`SECURE_HSTS_SECONDS`) ;
- limite des demandes de lien de connexion par adresse IP ;
- purge planifiée des comptes inutilisés (aujourd'hui seulement au démarrage) ;
- suivi des erreurs (Sentry), intégration continue, healthcheck.
