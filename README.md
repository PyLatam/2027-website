# PyCon Latam 2027 — Website

Landing page for **PyCon Latam 2027**, in Punta Cana, Dominican Republic.

The site is a single announcement screen, bilingual (Spanish primary, English
secondary), built as a static bundle and hosted on GitHub Pages.

> The official dates have not been announced yet. Until they are, the page
> deliberately says only what the key art says.

## Stack

TypeScript · React 19 · Vite 7 · CSS Modules · GitHub Actions → GitHub Pages

No CSS framework, no illustration library: every shape on the page is
hand-authored SVG.

## Getting started

```bash
npm install
npm run dev
```

## Scripts

| Command             | What it does                              |
| ------------------- | ----------------------------------------- |
| `npm run dev`       | Dev server with HMR                       |
| `npm run typecheck` | `tsc --noEmit`                            |
| `npm run lint`      | Type-aware ESLint                         |
| `npm run format`    | Prettier, write mode                      |
| `npm run build`     | Type-check and emit `dist/`               |
| `npm run preview`   | Serve `dist/` at the production base path |

## Deployment

Pushing to `main` builds and publishes to GitHub Pages
(`.github/workflows/deploy.yml`). Enable **Settings → Pages → Source: GitHub
Actions** once, and the rest is automatic.

The Vite `base` is resolved at build time: `/` when `public/CNAME` exists
(custom domain), `/<repo>/` otherwise.

## Contributing

Read [AGENTS.md](./AGENTS.md) — it covers scope, the language policy, the
architecture and the design tokens.

## License

See [LICENSE](./LICENSE).
