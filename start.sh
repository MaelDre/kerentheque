#!/bin/sh
# Lancé à chaque démarrage du conteneur : ces étapes ont besoin de la base, donc du volume,
# qui n'est pas accessible pendant le build ni dans la commande de pré-déploiement de Railway.
set -e

python manage.py migrate --noinput
python manage.py createcachetable

# Une purge ratée ne doit pas empêcher le site de démarrer.
python manage.py purge_unused_accounts || echo "Échec de purge_unused_accounts, démarrage poursuivi." >&2

exec gunicorn config.wsgi \
    --bind "0.0.0.0:${PORT:-8000}" \
    --workers "${WEB_CONCURRENCY:-2}" \
    --worker-class gthread \
    --threads "${GUNICORN_THREADS:-4}" \
    --access-logfile -
