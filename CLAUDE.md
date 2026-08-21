# CLAUDE.md

**Read [AGENTS.md](./AGENTS.md) first.** It is the single source of truth for
this repository: scope, language policy, architecture, design tokens and the
non-negotiables. This file only records what is specific to working here with
Claude Code, so the two documents cannot drift apart.

## The three things most likely to trip you up

1. **Scope is intentionally tiny.** This landing page says only what the
   official key art says: "PyCon Latam 2027 / Nos vemos en Punta Cana,
   República Dominicana". The dates are not public yet. Do not helpfully add an
   agenda, speakers, a countdown or a registration form — inventing details
   about a real conference is a defect, not a feature.

2. **Two languages, two registers.** The site is bilingual (Spanish primary,
   English secondary); the _codebase_ is English-only. Comments, identifiers,
   commit messages and Markdown are English. Spanish lives in
   `src/i18n/dictionary.ts` and in the `<noscript>` fallback of `index.html`.

3. **Verify visually, at several sizes.** CSS here is tuned against real
   screenshots, not guessed. After any layout or typography change:

   ```bash
   npm run build && npm run preview   # http://localhost:4173/2027-website/
   ```

   then capture at least 390×844, 768×1024, 1440×900 and 1920×1080 and look at
   them. Check for horizontal overflow and for a dead band opening up between
   the headline and the surf.

## Verification loop

```bash
npm run typecheck && npm run lint && npx prettier --check . && npm run build
```

CI runs exactly these four. Run them before reporting a change as done.

## House style

- Add copy by adding a key to the `es` dictionary — the `Messages` type then
  forces the `en` translation to exist. Never inline a user-facing string.
- Never hardcode a colour, font or duration; read a token from
  `src/styles/tokens.css`. The five brand colours come from the official logo.
- **Never redraw the logo, and never redraw supplied artwork.** `BrandMark`
  inlines the designer's mark; `BrandShape` inlines the supplied leaves, corals
  and dots. Check the catalogue in `src/components/decor/shapes.ts` _before_
  drawing anything new.
- Scenery with no supplied artwork builds on the generators in `src/lib/svg/`
  (`ribbonPath`, `canopyBlobs`) rather than hand-written path
  data, and goes in `src/components/decor/` as pure components that take
  `className`/`style` and know nothing about where they sit.
- Every decor item must set its own `width` in `HeroDecor.module.css`. Forget it
  and the fallback in `.item` keeps it small instead of covering the page —
  but that fallback is a safety net, not a size.
- Randomness in artwork is always seeded (`createRandom`). `Math.random()` in a
  shape is a bug: it makes the scene reshuffle on every render.
- Prefer editing a token or a `clamp()` over adding a new media query.
