"""Django settings for the PyCon Latam 2027 site.

The site is a static, bilingual landing page: no database, no auth, no
sessions. Everything that varies between machines comes from the environment.

Production runs on Fly.io behind its TLS-terminating proxy, under gunicorn,
with WhiteNoise serving static files (see web/fly.toml, web/Dockerfile and
docs/django-migration.md). Local development keeps `runserver` defaults.
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def _env_flag(name: str, default: bool) -> bool:
    return os.environ.get(name, "1" if default else "0").lower() in {"1", "true", "yes"}


# Local development defaults. Production must set real values.
DEBUG = _env_flag("DJANGO_DEBUG", default=True)
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
if not SECRET_KEY:
    if not DEBUG:
        # The repository is public: falling back to a key written here would
        # hand it to everyone. Production gets it from `flyctl secrets`.
        raise ImproperlyConfigured("DJANGO_SECRET_KEY must be set when DJANGO_DEBUG=0.")
    SECRET_KEY = "django-insecure-local-development-only"  # noqa: S105
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
# Test deploys must not compete with the real site in search results.
NOINDEX = _env_flag("DJANGO_NOINDEX", default=False)

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "core",
    "landing",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Right after SecurityMiddleware, as WhiteNoise's docs require.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.NoIndexMiddleware",
    "core.middleware.LocaleMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "core.context_processors.site",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# No database: the site has no persistent state.
DATABASES: dict[str, dict[str, object]] = {}

# Locale handling is the site's own (core.locales + core.middleware): `?lang=`,
# then a remembered-choice cookie, then `Accept-Language`, then Spanish.
# Django's gettext machinery is not used.
LANGUAGE_CODE = "es"
USE_I18N = False
TIME_ZONE = "America/Santo_Domingo"
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Hashed, compressed file names need `collectstatic` (run in the Docker build),
# so local development and the test suite keep the plain storage.
STORAGES = {
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if DEBUG
            else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        ),
    },
}

if not DEBUG:
    # Fly's proxy terminates TLS and redirects HTTP (`force_https` in fly.toml);
    # it tells Django the original scheme through this header.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    # One hour while the site lives on fly.dev; raise it at the cut-over.
    SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_HSTS_SECONDS", "3600"))
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
    CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
