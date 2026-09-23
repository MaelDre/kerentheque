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
pointer vers un disque persistant. Lancez aussi `collectstatic` au déploiement.
