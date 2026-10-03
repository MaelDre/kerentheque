FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Dépendances d'abord, pour profiter du cache Docker tant que uv.lock ne change pas.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .

# La SECRET_KEY factice ne sert qu'à collectstatic et n'est pas conservée dans l'image.
RUN DEBUG=false SECRET_KEY=collectstatic-only python manage.py collectstatic --noinput

CMD ["./start.sh"]
