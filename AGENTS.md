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

### Brand sources

| File                                          | What it is                                             |
| --------------------------------------------- | ------------------------------------------------------ |
| `assets/pcw.jpeg`                             | The announcement key art the whole scene derives from  |
| `assets/Logo Pycon Punta Cana.svg`            | The official mark, as delivered                        |
| `assets/LOGO_Pycon Punta Cana y elementos.ai` | Full lockups (mark + wordmark), 4 artboards            |
| `assets/Recurso 1.zip`                        | The loose decorative elements, as delivered            |
| `src/assets/pycon-latam-rd-mark.svg`          | Verbatim copy of the mark, the one the site imports    |
| `src/assets/decor/*.svg`                      | The loose elements, normalised for the web (see below) |

`assets/` holds the untouched designer deliverables — never edit them.
`src/assets/` holds the build-facing copies.

Note the official lockup reads **"PyCon Latam RD · Punta Cana"**, while the key
art reads **"PyCon Latam 2027"**. The page follows the key art, because that is
the announcement. Confirm with the committee before changing it.

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

There is **no CSS framework and no icon/illustration library**. The logo and
every leaf, coral and dot cluster are the design team's own SVGs; only the
scenery with no supplied artwork — water, sand, jungle, palm trees, circuit
traces — is generated from the primitives in `src/lib/svg/`. Keep it that way:
the page ships as one self-contained bundle with no third-party requests except
Google Fonts.

---

## 4. Architecture

```
src/
├── app/            # Application shell: layout, skip link, toolbar
├── assets/         # Brand files imported by the build (the logo)
├── components/
│   ├── decor/      # Presentational SVG shapes. No text, no state, no i18n.
│   └── ui/         # Reusable interactive controls
├── content/        # Event facts (dates, venue, URLs) — locale independent
├── features/
│   └── hero/       # The one feature this site currently has
├── i18n/           # Locale detection, dictionary, provider, hook
├── lib/            # Framework-free helpers (`cx`) and `svg/` generators
├── styles/         # tokens.css (design system) + global.css (reset)
└── types/          # Cross-cutting types
```

**Dependency rule — imports point inwards only:**

```
features/  →  components/  →  lib/svg, styles, types
    ↓             ↓
  i18n  ←──── content
```

- `lib/svg/*` is pure TypeScript: it takes numbers and returns path strings.
  It imports nothing from React and touches no DOM, so it is the easiest layer
  to reason about and the first place to look when a shape is wrong.
- `components/decor/*` never imports from `features/` or `i18n/`. They are
  dumb shapes that accept `className`/`style` and let the parent place them.
- `features/*` owns composition and layout. It is the only layer allowed to
  position decorations, and `HeroDecor` is where the scene's paint order lives.
- Adding a section means adding `src/features/<section>/` plus its dictionary
  keys — never editing `Hero` to smuggle new content in.

Import with the `@/` alias (`@/i18n/useTranslation`), not deep relative paths.

### Official artwork first

**Before drawing anything, check whether the design team already supplied it.**
The catalogue lives in `src/components/decor/shapes.ts`:

| Name              | What it is                                    |
| ----------------- | --------------------------------------------- |
| `leaf-frond-01`   | Upright palm frond (also the palm-tree crown) |
| `leaf-frond-02`   | Horizontal frond                              |
| `leaf-frond-trio` | Three fronds as one composition               |
| `coral-staghorn`  | Fat branching coral                           |
| `coral-fan`       | Fine sea fan                                  |
| `coral-branch`    | Small branching coral                         |
| `sea-rock`        | Offshore rock (see the note in that file)     |
| `dot-cluster`     | Five brand-coloured dots                      |

`sea-rock` and `dot-cluster` are in the catalogue but not in the current scene —
they are delivered artwork kept discoverable for future sections, not dead code
to delete.

Render one with `<BrandShape name="coral-fan" color="var(--c-aqua-500)" />`.

Single-colour files were rewritten to `fill="currentColor"`, so `color` tints
them; multi-colour files keep the brand colours they shipped with. Ids are
namespaced per instance, which is what lets the same shape appear more than once
without its clip paths fighting.

To add artwork: drop the normalised file in `src/assets/decor/` and register it
in `shapes.ts`. Never redraw one of these by hand.

### The beach, and why it looks right

`SandCove` mixes two geometries on purpose, and confusing them is what makes a
beach look wrong:

- **The waterline** (`EDGE`) is local and diagonal. Only the foam follows it.
- **The far shore** — golden sand, jungle, pale hill — runs **horizontally**.
  It is the distance, so it follows the horizon, not the local waterline.

Everything is clipped to the sand region, so no dune and no crown can end up
floating on the water. The palms are drawn on top, planted so their trunks
disappear into the canopy.

### The geometry primitives

For the scenery with no supplied artwork:

| Primitive           | Produces                        | Used by                                             |
| ------------------- | ------------------------------- | --------------------------------------------------- |
| `ribbonPath(spine)` | A tapered, variable-width band  | `SeaRock` currents, `PalmTree` trunk + crown blades |
| `canopyBlobs(opts)` | Overlapping crowns along a line | The jungle inside `SandCove`                        |

Anything random is seeded (`createRandom`) so the artwork renders identically on
every machine and every reload. **Never call `Math.random()` in a shape.**

### The brand mark

`BrandMark` inlines `src/assets/pycon-latam-rd-mark.svg` verbatim. It is
deliberately not redrawn, re-coloured or tokenised — to update the logo, replace
that file.

---

## 5. Design system

`src/styles/tokens.css` is the single source of truth for colour, type, space
and motion.

The five brand colours are taken **verbatim from the official mark** and every
ramp is built around them, so nothing on the page can drift away from the logo:

| Token              | Value     | Role               |
| ------------------ | --------- | ------------------ |
| `--c-brand-blue`   | `#31add0` | Ocean, script type |
| `--c-brand-yellow` | `#fec822` | Sun, sand          |
| `--c-brand-teal`   | `#48bab7` | Palms, reef        |
| `--c-brand-coral`  | `#ea5363` | Headline, coral    |
| `--c-brand-orange` | `#ee8827` | Accent fronds      |

**Components must never hardcode a colour, radius, duration or font.** Read a
token. Raw ramp values are `--c-*`; components consume semantic roles
(`--color-accent`, `--color-brand`, …) so the ramp can be retuned in one place.

Typography:

**The brand font is Freehand 521 BT** (Bitstream), which is commercial and not
on Google Fonts. The site uses the closest free stand-ins for the two roles the
key art puts it in. If the licence is ever bought, swap the two families in
`tokens.css` and nothing else changes.

- `--font-script` (Yellowtail) — "PyCon Latam 2027", "República Dominicana",
  and the dates line, which is one step smaller via `--script-size`
- `--font-display` (Courgette) — "Nos vemos en", "Punta Cana,"
- `--font-ui` (Outfit) — everything else

Courgette is lighter than the key art's display weight, so the two display lines
carry `-webkit-text-stroke: var(--display-stroke)`. That is a deliberate
substitute for a heavier cut, not a decoration — keep it if you change sizes.

Sizes are fluid `clamp()` expressions that blend `vw` **and** `vh`, because the
page must fill a 1080p desktop and a portrait tablet equally well. Never add a
fixed `px` font size.

---

## 6. Non-negotiables

- **Decoration never touches the type.** The copy column is centred and at most
  `--content-max` wide; no decorative piece may drift into the band it occupies.
  The text paints on top, so this is about legibility, not z-order.
- **Less is more.** The scene is a frame for four lines of type, not an
  illustration contest. If an element does not read at a glance, cut it — that
  is why there is no dot cluster, no fifth coral and no wet-sand band.
- **Every decor item sets its own `width`** in `HeroDecor.module.css`. The
  fallback in `.item` is a safety net that keeps a forgotten one small instead
  of stretching it across the page — it is not a size.
- **Responsive everywhere.** The page is verified at 320, 390, 768, 1280, 1440,
  1920 and 2560 wide, plus landscape phones. There must be **zero horizontal
  overflow** at any width, and no dead band between the headline and the surf.
- **Accessible.** The headline is a single `<h1>` with a visually-hidden full
  sentence; the decorative line breaks are `aria-hidden`. Decoration is inert.
  Keep the skip link, the visible focus ring, and `prefers-reduced-motion`
  support.
- **Static.** No runtime data fetching, no analytics, no third-party scripts.
  Google Fonts is the only external request.
- **Deterministic artwork.** Seeded randomness only, so a redeploy never
  silently reshuffles the reef.
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
