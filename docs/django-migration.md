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
- **Phase 2 — done.** Language and shell.
  - Locale is resolved server-side in `detectLocale.ts` order: `?lang=` >
    remembered choice > `Accept-Language` (q-values honoured, base subtag
    matched) > Spanish. `core.middleware.LocaleMiddleware` sets
    `request.locale`, stores a valid `?lang=` in the `pyconlatam.locale`
    cookie (same name as the React `localStorage` key; one year, `HttpOnly`,
    `SameSite=Lax`) and adds `Vary: Cookie, Accept-Language`.
  - Shell context (locale, switcher options, social links) comes from
    `core.context_processors.site`; the partials are
    `templates/shell/{language_switcher,footer}.html`.
  - The language switcher is plain `?lang=` links, no JavaScript. The current
    language carries `aria-current="true"` instead of `aria-pressed`, which is
    only valid on buttons. CSS: `language-switcher.css`, plus
    `text-decoration: none` because the options are now links.
  - The footer and social icons are ported in `footer.css`. The icon SVGs in
    `templates/icons/` have the same path data as `SocialIcons.tsx`, checked
    by script. URLs come from `core.content`.
  - The skip link targets `#content`, as in React. Until Phase 3 the id sits
    on `<main>`; it then moves to the hero `<section>`, where React has it.
  - Django-only key: `footer.social` ("Redes sociales" / "Social media") for
    the social list's `aria-label`, which React hardcodes in English.
  - Verified with Playwright at 390, 768, 1440 and 1920 wide, in both
    languages: switcher and footer bounding boxes are identical to React, with
    zero horizontal overflow.
  - **Hosting note:** the cookie and `Accept-Language` steps need a server. A
    static export would serve the default (Spanish) unless the visitor uses
    `?lang=`. Factor this into the pending hosting decision.
- **Phase 3 — next.** Scene: hero type, `BrandMark`/`BrandShape`, and the
  `src/lib/svg/` generators with the same PRNG.

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
