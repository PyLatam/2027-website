# PyCon Latam 2027 — Website

Landing page for **PyCon Latam 2027**, 26 – 29 August 2027 in Punta Cana,
Dominican Republic. Live at [2027.pylatam.org](https://2027.pylatam.org).

The site is a single announcement screen, bilingual (Spanish primary, English
secondary). It deliberately says only what the official key art says, plus the
confirmed dates.

## Migration in progress: React → Django

The site is being ported from React to Django, keeping it visually identical.
Plan, phases and decision log: [docs/django-migration.md](./docs/django-migration.md).

| Folder          | What it is                                                   |
| --------------- | ------------------------------------------------------------ |
| `legacy-react/` | The React site. **Production.** Frozen reference for the port |
| `web/`          | The Django port. Test deploy on fly.dev, not on the domain yet |
| `assets/`       | Untouched designer deliverables, shared by both               |
| `docs/`         | Migration plan and decision log                               |

Status: phases 0–4 are done. The Django site renders the full scene
server-side and is pixel-identical to React at every checked size, in both
languages. Next is phase 5, the cut-over to [Fly.io](https://fly.io) (one
always-on Machine, SQLite on a volume), after which `legacy-react/` is removed.

## React site (`legacy-react/`)

TypeScript · React 19 · Vite 7 · CSS Modules · GitHub Actions → GitHub Pages

No CSS framework, no illustration library: every shape on the page is
hand-authored SVG.

```bash
cd legacy-react
npm install
npm run dev
```

| Command             | What it does                              |
| ------------------- | ----------------------------------------- |
| `npm run dev`       | Dev server with HMR                       |
| `npm run typecheck` | `tsc --noEmit`                            |
| `npm run lint`      | Type-aware ESLint                         |
| `npm run format`    | Prettier, write mode                      |
| `npm run build`     | Type-check and emit `dist/`               |
| `npm run preview`   | Serve `dist/` at the production base path |

## Django site (`web/`)

Python 3.14 · Django · [uv](https://docs.astral.sh/uv/) · plain CSS · no
JavaScript

```bash
cd web
uv sync
uv run python manage.py runserver   # http://127.0.0.1:8000/  (?lang=en for English)
```

Layout, checks and the golden/parity tooling: [web/README.md](./web/README.md).

## Deployment

Pushing to `main` builds `legacy-react/` and publishes it to GitHub Pages
(`.github/workflows/deploy.yml`, which only fires on `legacy-react/**`). The
Vite `base` is resolved at build time: `/` when `public/CNAME` exists (custom
domain), `/<repo>/` otherwise.

Pushing to `main` changes in `web/` runs the Django checks and deploys to a
Fly.io test app, <https://pyconlat-2027-test.fly.dev/>
(`.github/workflows/fly-deploy.yml`, which only fires on `web/**`). The test
app is marked `noindex`; `2027.pylatam.org` stays on GitHub Pages until the
phase 5 cut-over. It needs a `FLY_API_TOKEN` Actions secret: a deploy token
scoped to that app (`flyctl tokens create deploy -a pyconlat-2027-test`).

There is no staging environment: previews run on a local `runserver` shared
through ngrok.

## Contributing

Read [AGENTS.md](./AGENTS.md) — it covers scope, the language policy, the
architecture and the design tokens.

## License

See [LICENSE](./LICENSE).
