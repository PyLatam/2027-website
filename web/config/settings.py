"""Django settings for the PyCon Latam 2027 site.

The site is a static, bilingual landing page: no database, no auth, no
sessions. Everything that varies between machines comes from the environment.

For now it runs locally only. Production hosting (static export vs. a server)
has not been decided, so nothing here may assume either. See
docs/django-migration.md.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _env_flag(name: str, default: bool) -> bool:
    return os.environ.get(name, "1" if default else "0").lower() in {"1", "true", "yes"}


# Local development defaults. Production must set real values.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-local-development-only")
DEBUG = _env_flag("DJANGO_DEBUG", default=True)
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "core",
    "landing",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# No database: the site has no persistent state.
DATABASES: dict[str, dict[str, object]] = {}

# Locale handling is the site's own (core.locales), driven by `?lang=`;
# Django's gettext machinery is not used.
LANGUAGE_CODE = "es"
USE_I18N = False
TIME_ZONE = "America/Santo_Domingo"
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
