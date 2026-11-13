# web/ — Django port

The PyCon Latam 2027 landing page, being ported from `../legacy-react/`.
Plan and decisions: [../docs/django-migration.md](../docs/django-migration.md).

**Local only.** Nothing here is deployed, and production hosting has not been
decided yet.

## Run it

Requires [uv](https://docs.astral.sh/uv/) (it installs Python 3.14 if needed).

```bash
cd web
uv sync
uv run python manage.py runserver   # http://127.0.0.1:8000/  (?lang=en for English)
```

## Verify

```bash
uv run ruff format --check . && uv run ruff check . && uv run python manage.py check && uv run python manage.py test
```

## Layout

| Path                     | Mirrors (in legacy-react/src/) | What it holds                                       |
| ------------------------ | ------------------------------ | --------------------------------------------------- |
| `config/`                | —                              | Settings and root URLs                              |
| `core/locales.py`        | `i18n/locales.ts`              | Supported locales and request locale resolution     |
| `core/dictionary.py`     | `i18n/dictionary.ts`           | All user-facing copy (`es` is the reference)        |
| `core/content.py`        | `content/event.ts`             | Event facts: dates, venue, URLs                     |
| `core/seo.py`            | JSON-LD in `index.html`        | Structured data                                     |
| `core/templatetags/`     | `i18n/useTranslation.ts`       | `{% t "key" %}`                                     |
| `landing/`               | `features/hero/`, `app/`       | The page view and template                          |
| `templates/base.html`    | `index.html`                   | Document `<head>`                                   |
| `static/css/`            | `styles/`, `*.module.css`      | `tokens.css` and `global.css` copied verbatim       |

Copy goes in `core/dictionary.py`: add the key to `ES`, then to `EN` (a test
fails if they differ). Never inline user-facing text in a template.
