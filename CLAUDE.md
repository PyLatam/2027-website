# CLAUDE.md

**Read [AGENTS.md](./AGENTS.md) first.** It is the single source of truth for
this repository: scope, language policy, architecture, design tokens and the
non-negotiables. This file only records what is specific to working here with
Claude Code, so the two documents cannot drift apart.

## Migration in progress: React → Django

Read [docs/django-migration.md](./docs/django-migration.md) for the plan,
current phase and decision log.

| Folder          | What it is                                                      |
| --------------- | --------------------------------------------------------------- |
| `legacy-react/` | The React site. Production. Frozen reference for the port.      |
| `web/`          | The Django port. **Local only, never deployed.**                |

- Production hosting for Django is **not decided**. Do not assume a static
  export or a server, and do not add a Django deploy workflow.
- `deploy.yml` only fires on `legacy-react/**`. Keep it that way.
- Never push or deploy without being asked: the user reviews everything locally
  first.
- Unless a rule says otherwise, `src/…` paths below are relative to
  `legacy-react/`. Each rule has a Django counterpart under "House style".

## Environment

The repo lives in WSL (`~/2027-website`) and is opened from Windows through
`\\wsl.localhost\Ubuntu\…`. Git refuses that path ("dubious ownership"),
and Node is installed via nvm, so run tooling inside WSL:

```powershell
wsl -d Ubuntu -- bash -lc "cd ~/2027-website && git status"
wsl -d Ubuntu -- bash -lc "source ~/.nvm/nvm.sh && cd ~/2027-website/legacy-react && npm run build"
wsl -d Ubuntu -- bash -lc "cd ~/2027-website/web && uv run python manage.py runserver"
```

## The three things most likely to trip you up

1. **Scope is intentionally tiny.** This landing page says only what the
   official key art says: "PyCon Latam 2027 / Nos vemos en Punta Cana,
   República Dominicana", plus the confirmed dates (26 – 29 August 2027). Do
   not helpfully add an agenda, speakers, a countdown or a registration form —
   inventing details about a real conference is a defect, not a feature. The
   migration ports the page as it is; it adds nothing.

2. **Two languages, two registers.** The site is bilingual (Spanish primary,
   English secondary); the _codebase_ is English-only. Comments, identifiers,
   commit messages and Markdown are English. Spanish lives in
   `src/i18n/dictionary.ts` and the `<noscript>` of `index.html` (React), and
   in `web/core/dictionary.py` (Django).

3. **Verify visually, at several sizes.** CSS here is tuned against real
   screenshots, not guessed. After any layout or typography change, run both
   sites side by side:

   ```bash
   cd legacy-react && npm run build && npm run preview   # http://localhost:4173/
   cd web && uv run python manage.py runserver           # http://127.0.0.1:8000/
   ```

   then capture at least 390×844, 768×1024, 1440×900 and 1920×1080 and look at
   them. Check for horizontal overflow and for a dead band opening up between
   the headline and the surf.

## Verification loop

React (`legacy-react/`). CI runs exactly these four:

```bash
npm run typecheck && npm run lint && npx prettier --check . && npm run build
```

Django (`web/`). Not in CI yet:

```bash
uv run ruff format --check . && uv run ruff check . && uv run python manage.py check && uv run python manage.py test
```

Run the loop for every site you touched before reporting a change as done.

## House style

- Add copy by adding a key to the `es` dictionary — the `Messages` type then
  forces the `en` translation to exist. Never inline a user-facing string.
  **Django:** add the key to `ES` and `EN` in `web/core/dictionary.py` (a test
  fails if they differ) and render it with `{% t "key" %}`.
- Never hardcode a colour, font or duration; read a token from
  `src/styles/tokens.css`. The five brand colours come from the official logo.
  **Django:** `web/static/css/tokens.css` is a verbatim copy; change both.
- Event facts (dates, venue, URLs) live in `src/content/event.ts`; **Django:**
  `web/core/content.py`. Templates never inline them.
- **Never redraw the logo, and never redraw supplied artwork.** `BrandMark`
  inlines the designer's mark; `BrandShape` inlines the supplied leaves, corals
  and dots. Check the catalogue in `src/components/decor/shapes.ts` _before_
  drawing anything new. **Django:** include the same SVG files verbatim.
- Scenery with no supplied artwork builds on the generators in `src/lib/svg/`
  (`ribbonPath`, `canopyBlobs`) rather than hand-written path
  data, and goes in `src/components/decor/` as pure components that take
  `className`/`style` and know nothing about where they sit. **Django:** the
  Python port must produce byte-identical SVG output.
- Every decor item must set its own `width` in `HeroDecor.module.css`. Forget it
  and the fallback in `.item` keeps it small instead of covering the page —
  but that fallback is a safety net, not a size.
- Randomness in artwork is always seeded (`createRandom`). `Math.random()` in a
  shape is a bug: it makes the scene reshuffle on every render. In Python,
  `random` is equally a bug — port the same PRNG.
- CSS Modules become plain CSS with a per-component prefix (`App.module.css` →
  `app.css` with `.app-*`).
- Prefer editing a token or a `clamp()` over adding a new media query.
