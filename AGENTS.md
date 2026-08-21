# AGENTS.md

Working agreement for humans and AI agents contributing to the **PyCon Latam
2027** website.

Read this before changing anything. `CLAUDE.md` points here — this file is the
single source of truth.

---

## 1. What this site is

A one-screen announcement. As of today the organising committee has confirmed
exactly two facts:

- **Where:** Punta Cana, Dominican Republic
- **When:** to be announced

The landing page therefore says only what the official key art says, in two
languages:

| Spanish (primary)            | English                    |
| ---------------------------- | -------------------------- |
| PyCon Latam 2027             | PyCon Latam 2027           |
| Nos vemos en **Punta Cana,** | See you in **Punta Cana,** |
| República Dominicana         | Dominican Republic         |

**Do not add sections** (agenda, speakers, tickets, sponsors, CFP, countdown)
until the committee provides the content. Placeholder or invented information
about a real conference is worse than an empty page.

The key art this design derives from is `assets/pcw.jpeg`.

---

## 2. Language policy

- The site is **bilingual: Spanish and English. Spanish is primary** — it is
  the default and the fallback for every unresolved locale.
- **All code, comments, commit messages, documentation and `.md` files are
  written in English.** Only the strings in `src/i18n/dictionary.ts` and the
  static fallbacks in `index.html` are user-facing Spanish.
- Never inline user-facing text in a component. Add a key to the `es`
  dictionary; TypeScript will then force you to add the `en` translation. That
  is the mechanism that keeps translations from drifting.

---

## 3. Stack

| Concern    | Choice                                                                          | Why                                                        |
| ---------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Language   | TypeScript (strict + `noUncheckedIndexedAccess` + `exactOptionalPropertyTypes`) | Content-driven site; type errors should catch missing copy |
| UI         | React 19                                                                        | Room to grow into a multi-section conference site          |
| Build      | Vite 7                                                                          | Static output, no server, fits GitHub Pages                |
| Styling    | CSS Modules + custom properties                                                 | Scoped styles, zero runtime, tokens shared everywhere      |
| Deployment | GitHub Actions → GitHub Pages                                                   | Repo-native, no external service                           |

There is **no CSS framework and no icon/illustration library**. Every shape on
the page is hand-authored SVG in `src/components/decor/`. Keep it that way: the
whole page ships as one small self-contained bundle.

---

## 4. Architecture

```
src/
├── app/            # Application shell: layout, skip link, toolbar
├── components/
│   ├── decor/      # Presentational SVG shapes. No text, no state, no i18n.
│   └── ui/         # Reusable interactive controls
├── content/        # Event facts (dates, venue, URLs) — locale independent
├── features/
│   └── hero/       # The one feature this site currently has
├── i18n/           # Locale detection, dictionary, provider, hook
├── styles/         # tokens.css (design system) + global.css (reset)
└── types/          # Cross-cutting types
```

**Dependency rule — imports point inwards only:**

```
features/  →  components/  →  styles, types
    ↓             ↓
  i18n  ←──── content
```

- `components/decor/*` never imports from `features/` or `i18n/`. They are
  dumb shapes that accept `className`/`style` and let the parent place them.
- `features/*` owns composition and layout. It is the only layer allowed to
  position decorations.
- Adding a section means adding `src/features/<section>/` plus its dictionary
  keys — never editing `Hero` to smuggle new content in.

Import with the `@/` alias (`@/i18n/useTranslation`), not deep relative paths.

---

## 5. Design system

`src/styles/tokens.css` is the single source of truth for colour, type, space
and motion. The palette is sampled from the key art.

**Components must never hardcode a colour, radius, duration or font.** Read a
token. Raw ramp values are `--c-*`; components consume semantic roles
(`--color-accent`, `--color-brand`, …) so the ramp can be retuned in one place.

Typography:

- `--font-script` (Kaushan Script) — "PyCon Latam 2027", "República Dominicana"
- `--font-display` (Kanit 800 italic) — "Nos vemos en", "Punta Cana,"
- `--font-ui` (Outfit) — everything else

Sizes are fluid `clamp()` expressions that blend `vw` **and** `vh`, because the
page must fill a 1080p desktop and a portrait tablet equally well. Never add a
fixed `px` font size.

---

## 6. Non-negotiables

- **Responsive everywhere.** The page is verified at 320, 390, 768, 1280, 1440,
  1920 and 2560 wide, plus landscape phones. There must be **zero horizontal
  overflow** at any width, and no dead band between the headline and the surf.
- **Accessible.** The headline is a single `<h1>` with a visually-hidden full
  sentence; the decorative line breaks are `aria-hidden`. Decoration is inert.
  Keep the skip link, the visible focus ring, and `prefers-reduced-motion`
  support.
- **Static.** No runtime data fetching, no analytics, no third-party scripts.
  Google Fonts is the only external request.
- **Client-side routing is not available.** GitHub Pages serves the built
  `dist/` as-is; the language is a `?lang=` query parameter, not a path segment.

---

## 7. Commands

```bash
npm install
npm run dev        # local dev server
npm run typecheck  # tsc --noEmit
npm run lint       # eslint (type-aware)
npm run format     # prettier --write
npm run build      # tsc --build && vite build
npm run preview    # serve dist/ at the production base path
```

Before opening a PR, all of `typecheck`, `lint`, `prettier --check .` and
`build` must pass — CI runs exactly those.

---

## 8. Deployment

`.github/workflows/deploy.yml` builds on every push to `main` and publishes
`dist/` to GitHub Pages.

The Vite `base` is resolved at build time:

- `public/CNAME` present → base `/` (custom domain, e.g. `2027.pylatam.org`)
- otherwise → base `/<repo>/` (project site)

To move to a custom domain: add `public/CNAME`, then update the absolute URLs
in `index.html` (`canonical`, `hreflang`, `og:url`, `og:image`) and
`EVENT.canonicalUrl` in `src/content/event.ts`.

`public/.nojekyll` must stay — without it GitHub Pages hides `_`-prefixed build
assets.

---

## 9. When the dates are announced

1. Fill `EVENT.dates.start` / `.end` in `src/content/event.ts`.
2. Replace the `WebSite` JSON-LD in `index.html` with an `Event` node so the
   page becomes eligible for event rich results.
3. Only then consider surfacing the dates in the hero — and ask the committee
   first, since the current design is deliberately word-for-word the key art.
