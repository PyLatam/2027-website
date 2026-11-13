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
| `core/locales.py`        | `i18n/locales.ts`, `detectLocale.ts` | Locales; `?lang=` > cookie > `Accept-Language` > `es` |
| `core/middleware.py`     | `persistLocale` (localStorage) | Sets `request.locale`, remembers `?lang=` in a cookie |
| `core/context_processors.py` | `LocaleProvider`, `Footer.tsx` | Shell context: locale, switcher options, social links |
| `core/dictionary.py`     | `i18n/dictionary.ts`           | All user-facing copy (`es` is the reference)        |
| `core/content.py`        | `content/event.ts`             | Event facts: dates, venue, URLs                     |
| `core/seo.py`            | JSON-LD in `index.html`        | Structured data                                     |
| `core/templatetags/`     | `i18n/useTranslation.ts`       | `{% t "key" %}`                                     |
| `core/svg/`              | `lib/svg/`                     | PRNG, `ribbon_path`, `canopy_blobs`, SVG inlining, JS number rules |
| `core/decor/`            | `components/decor/`            | Decor shapes as pure functions returning SVG markup |
| `core/assets/`           | `assets/`                      | Logo and decor SVGs, byte-identical copies          |
| `core/templatetags/decor.py` | `useId` + JSX              | `{% brand_shape %}`, `{% palm_tree %}`, …; one uid per instance |
| `landing/`               | `features/hero/`, `app/`       | The page view; `hero.html`, `hero_decor.html`       |
| `golden/`                | the TypeScript itself          | `generate.mjs` + the JSON the scene tests compare against |
| `templates/base.html`    | `index.html`                   | Document `<head>`                                   |
| `templates/shell/`       | `components/ui/`               | Language switcher and footer partials               |
| `templates/icons/`       | `components/ui/SocialIcons.tsx` | Social icon SVGs, path data verbatim               |
| `static/css/`            | `styles/`, `*.module.css`      | `tokens.css`/`global.css` verbatim; one file per component, `prefix-*` classes |

The scene must stay identical to React's. After changing a generator or a
decor component in either site, regenerate the golden files from the repo
root (inside WSL, with nvm loaded) and run the tests:

```bash
node web/golden/generate.mjs
```

After adding a module under `templatetags/`, restart `runserver`; it does not
pick up new tag libraries on its own.

Copy goes in `core/dictionary.py`: add the key to `ES`, then to `EN` (a test
fails if they differ). Never inline user-facing text in a template.
