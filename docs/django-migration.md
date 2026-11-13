# Django migration

Plan and decision log for porting the landing page from React + Vite to
Django, keeping the page visually identical.

## Layout during the migration

```
2027-website/
├── legacy-react/   # The current React site. Still what production deploys.
├── web/            # The Django port (in progress).
├── assets/         # Untouched designer deliverables, shared by both.
└── docs/           # This file.
```

`legacy-react/` is the reference the port is compared against. It is deleted
once the Django site reaches parity and takes over production.

## Phases

| #   | Phase                | Done when                                                                                          |
| --- | -------------------- | -------------------------------------------------------------------------------------------------- |
| 0   | Move the React site  | Site lives in `legacy-react/`; CI and deploy run from there; build unchanged                       |
| 1   | Django skeleton      | `web/` runs locally; `landing` view; `<head>` (meta, OG, hreflang, JSON-LD) and dictionary ported  |
| 2   | Language and shell   | Remembered choice + `Accept-Language`; language switcher, footer, social icons; skip link works    |
| 3   | Scene                | Hero type, `BrandMark`/`BrandShape`, and `src/lib/svg/` ported with the same PRNG; SVG identical   |
| 4   | Visual parity        | Pixel diff at 320, 390, 768, 1280, 1440, 1920, 2560; zero horizontal overflow; no dead band        |
| 5   | Cut-over and cleanup | Hosting chosen, CI/deploy switched, AGENTS.md/CLAUDE.md rewritten, `legacy-react/` removed         |

### Rules while both sites exist

- `legacy-react/` is the **frozen reference**. Change it only to fix
  production, and mirror the same fix in `web/`.
- `web/static/css/tokens.css` and `global.css` are verbatim copies. Edit
  tokens in both places until the cut-over, or parity diffs become meaningless.
- Message keys in `web/core/dictionary.py` match `dictionary.ts` one to one,
  except for keys only Django needs (listed under Progress).

### Progress

- **Phase 0 — done.** React site in `legacy-react/`; its CI checks pass from there.
- **Phase 1 — done.** `web/` runs locally (see `web/README.md`). The `<head>`
  is ported and now localised server-side (title, description, OG, JSON-LD
  follow `?lang=`). The dictionary was ported early because the head needs it;
  two keys were added (`meta.ogDescription`, `meta.eventDescription`) for copy
  the React site had hardcoded in Spanish only. The body is a placeholder.
- **Phase 2 — next.** Remembered language choice (cookie, replacing the React
  site's `localStorage`), `Accept-Language`, language switcher as plain links,
  footer with social icons. Sources: `legacy-react/src/i18n/detectLocale.ts`,
  `legacy-react/src/components/ui/{LanguageSwitcher,Footer,SocialIcons}.tsx`.

## Decision log

| Date       | Decision                                                                 | Status      |
| ---------- | ------------------------------------------------------------------------ | ----------- |
| 2026-11-12 | Move the React site to `legacy-react/`, build Django in `web/`           | Decided     |
| 2026-11-12 | Django runs **locally only** for now; nothing in `web/` is deployed      | Decided     |
| 2026-11-12 | `deploy.yml` only fires on `legacy-react/**` changes, so it stays separate | Decided     |
| 2026-11-12 | Production hosting for Django (static export to GitHub Pages vs. server) | **Pending** |
| 2026-11-12 | Full Python port of the scene vs. hybrid (`django-vite` serving React)   | **Pending** |

### Pending: hosting

GitHub Pages only serves static files, so it cannot run Django. Options:

- **Static export.** Django renders the page to HTML at build time (e.g.
  `django-distill` or a management command) and the output keeps deploying to
  GitHub Pages under the same domain. No running server, no cost.
- **Server.** A real host (Fly.io, Render, a VPS…). Needed only once the site
  gains dynamic features (registration, CFP, an admin for the committee).

Until this is decided, production keeps deploying `legacy-react/` and nothing
in `web/` may assume either option.
