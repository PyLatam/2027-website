# Production image for the Django site, deployed to Fly.io (see fly.toml).
# Build context: this directory (web/).

FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.13 /uv /usr/local/bin/uv

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Dependencies first, so code changes reuse this layer.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .

# Hashed static files for WhiteNoise. The key is a throwaway: collectstatic
# needs settings to load, not a real secret.
RUN DJANGO_DEBUG=0 DJANGO_SECRET_KEY=collectstatic-only \
    python manage.py collectstatic --noinput

# gunicorn's control socket lives under the user's home, so it needs one.
RUN useradd --system --create-home app
USER app

EXPOSE 8000

CMD ["gunicorn", "config.wsgi", "--bind", "0.0.0.0:8000", "--workers", "2", "--access-logfile", "-"]
