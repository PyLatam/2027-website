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
| 3   | Scene                | Hero type, `BrandMark`/`BrandShape`, and `src/lib/svg/` ported with the same PRNG; SVG identical except generated ids |
| 4   | Visual parity        | Pixel diff at 320, 390, 768, 1024, 1280, 1366, 1440, 1920, 2560 + landscape phones, `es`/`en`; zero horizontal overflow; same surf gap |
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
  - The skip link targets `#content`, as in React. The id sat on `<main>`
    until Phase 3 moved it to the hero `<section>`.
  - Django-only key: `footer.social` ("Redes sociales" / "Social media") for
    the social list's `aria-label`, which React hardcodes in English.
  - Verified with Playwright at 390, 768, 1440 and 1920 wide, in both
    languages: switcher and footer bounding boxes are identical to React, with
    zero horizontal overflow.
  - **Hosting note:** the cookie and `Accept-Language` steps need a server. A
    static export would serve the default (Spanish) unless the visitor uses
    `?lang=`. Factor this into the pending hosting decision.
- **Phase 3 — done.** Scene: hero type, every decor component and the SVG
  generators, as a full Python port. The page now renders the whole scene
  server-side, without JavaScript.
  - `core/svg/` ports `src/lib/svg/`: `prng.py` (Mulberry32), `ribbon.py`,
    `canopy.py`, `markup.py`, plus `numbers.py`, the single place JS number
    rules live: `js_str` (`String(n)`), `js_fixed2`
    (`Number(n.toFixed(2)).toString()`), `js_round` (`Math.round`) and
    `js_hypot` (V8's `Math.hypot`).
  - `core/decor/` ports `components/decor/` as pure functions that return
    the markup `react-dom/server` produces (same attribute order, closing
    tags, `data-*="true"`). `core/assets/` holds byte-identical copies of
    `src/assets/` (logo and the eight catalogue shapes). The tags in
    `core/templatetags/decor.py` hand each instance a uid (`svg1`, `svg2`, …)
    that plays `useId`'s role; it restarts on every render, so the page is
    stable across requests.
  - The hero is `landing/templates/landing/hero.html` and `hero_decor.html`.
    `id="content"` moved from `<main>` to the hero `<section>`.
    `hero.css`/`hero-decor.css` follow the prefix rule: `.hero` and `.layer`
    become `.hero` and `.hero-decor`, every other class and keyframe becomes
    `hero-*`/`hero-decor-*`.
  - No new dictionary keys: the hero uses the existing `hero.*` and
    `logo.alt`. The hardcoded durations in the CSS (`9s`, `13s`, `900ms`) and
    the hero's `drop-shadow` colour come verbatim from the React modules.
  - Python takes only `class_name` (and `color` on `brand_shape`), not
    React's `style` prop: nothing in the scene passes one.
  - **Golden files.** `web/golden/generate.mjs` loads the real TS/TSX through
    Vite's SSR loader and writes `web/golden/*.json`: JS number formatting
    (856 values, incl. `toFixed` ties and `-0`), 807 `Math.hypot` results,
    PRNG sequences for 14 seeds (negative, fractional, ≥ 2³²), 54
    `ribbonPath` spines (every spine in the scene, edge cases, 40 random),
    6 `canopyBlobs` calls, 35 rendered components (every catalogue shape,
    every prop the scene uses, the full `HeroDecor` and `Hero` in both
    languages), asset hashes, and the hero CSS Modules compiled with the
    Django class names. Regenerate with `node web/golden/generate.mjs` (from
    the repo root, in WSL, nvm loaded). It only reads `legacy-react/`.
  - **Tests** (`core/test_scene.py`): everything above compared exactly;
    component markup byte for byte with uids normalised; `Hero`/`HeroDecor`
    after also dropping whitespace between tags (template indentation); every
    id on the page unique and every `url(#…)`/`href="#…"` resolving; each
    instance getting its own ids; the ported CSS equal to the compiled modules
    once comments and whitespace are dropped; every decor item with its own
    `width`.
  - **Finding:** V8's `Math.hypot` differs from Python's `math.hypot` in the
    last bit for about a third of inputs. It changes no rounded digit in the
    current scene, but `js_hypot` ports V8's algorithm and is tested bit for
    bit, so a future spine cannot drift.
  - Verified with Playwright against the React preview at 390×844, 768×1024,
    1440×900, 1920×1080, 320×568, 1280×800, 2560×1440 and 844×390, with
    animations frozen: the hero, emblem, each headline line and every decor
    piece have identical bounding boxes; zero horizontal overflow; the gap
    from the dates line to the top of the surf is identical (the surf starts
    above the dates line at every size except 320×568 and 2560×1440, where
    the gap is 34 and 39 px, equal on both sites). Pixel diff ≤ 0.06%, all in
    the footer copyright line (antialiasing) and one palm pixel.
  - **Dev note:** after adding a module under `templatetags/`, restart
    `runserver`; its autoreloader does not register new tag libraries.

  Porting pitfalls, kept for reference (all handled and tested):
  - `Math.round` rounds halves towards +∞; Python's `round` rounds half to
    even. Port the JS rule.
  - `Number(n.toFixed(2)).toString()` (`ribbon.ts`) rounds exact ties up
    (`0.125` → `0.13`; Python's `f"{0.125:.2f}"` gives `0.12`) and turns
    `-0.00` into `0`. Needs a dedicated helper.
  - JS prints `3` where Python prints `3.0`. Every number written into SVG
    goes through one JS-compatible formatter.
  - Mulberry32 (`random.ts`) relies on 32-bit `>>>` and `Math.imul`; mask
    with `0xFFFFFFFF` and emulate `imul`.
  - `Math.hypot` / `Math.cos` may differ from Python by one ulp; the golden
    tests below catch any case where that changes a rounded digit.
  - **Verification:** a Node script generates golden JSON from the real
    TypeScript generators (PRNG sequences, `ribbonPath`, `canopyBlobs`, each
    decor component's markup). The JSON is committed under `web/`, so the
    Python tests need no Node and outlive `legacy-react/`.
  - **"Identical" excludes generated ids.** `useId` ids depend on React's
    internals and are not reproduced. Tests compare markup with ids
    normalised, and separately check that every id is unique and every
    `url(#…)`/`href="#…"` reference resolves.
- **Phase 4 — done.** Visual parity: the two sites render pixel-identical
  screenshots at every size checked, in both languages.
  - `web/golden/compare.py` is the versioned check. It drives Playwright at
    both running sites (React preview and a Django `runserver`; it starts
    neither). For each size and language it measures horizontal overflow, the
    boxes of the hero, inner column, emblem, `<h1>` and each line, every decor
    piece, the switcher and the footer, the visible text of the headline,
    switcher and footer, and the gap from the bottom of the dates line to the
    top of the visible surf bands. Then it diffs the full-page screenshots
    pixel by pixel inside Chromium (no Pillow), attributing every differing
    pixel to the smallest measured box that contains it. It writes React,
    Django, diff and side-by-side PNGs plus `report.json`, and exits 1 on any
    failed check. Run and options: the module docstring.
  - Sizes: 320×568, 375×667, 390×844, 667×375, 768×1024, 844×390, 1024×768,
    1280×800, 1366×768, 1440×900, 1920×1080, 2560×1440, each in `es` and
    `en` (24 cases).
  - **Result:** 24/24 identical: zero differing pixels, zero horizontal
    overflow, every box within 0.5 px (in practice exact), same text, same
    surf gap on both sites.
  - **Fixed in `web/`:** the language switcher had whitespace text nodes
    between its links (`textContent` "ES EN" vs React's "ESEN"). It had no
    visual effect in a flex row, but it was a DOM difference. Now wrapped in
    `{% spaceless %}`.
  - **The Phase 3 copyright diff is antialiasing, not markup or CSS.** The
    serialised HTML, computed styles and `lang` match exactly. React renders
    `© {year} {name}. {rights}` as six text nodes; the template gives one.
    Chromium rounds each node's advance on its own, so glyphs move by
    0.015–0.03 px and roughly 35–340 antialiased pixels change. Splitting
    Django's text into the same six nodes gives a byte-identical screenshot.
    The script merges adjacent text nodes (`Node.normalize()`) on both pages
    before the screenshot; `--keep-text-nodes` shows the raw difference.
  - **The Phase 3 palm pixels were rasteriser noise.** The palms and the sand
    (`will-change: transform`) rasterised differently from one load to the
    next, even with the page diffed against itself. Chromium now runs with
    `--disable-partial-raster` and the animation clock stopped through CDP
    before navigation. With that, repeated loads are identical, so the pixel
    threshold is zero.
  - Surf gap per size (both sites; negative = surf starts above the dates
    line). This metric is the top of the visible wave bands' geometry, which
    is stricter than Phase 3's: 320×568 +74.7, 375×667 +63.6, 390×844 +26.6,
    667×375 −13.8, 768×1024 −10.9, 844×390 +26.9, 1024×768 +69.1,
    1280×800 −8.4, 1366×768 −21.7, 1440×900 −5.8, 1920×1080 −9.6,
    2560×1440 +59.7. The positive gaps belong to the React layout and the
    port reproduces them. Closing them would be a design change for both
    sites, not a parity fix.
  - **Dev note:** in this WSL setup Playwright is only in uv's offline cache
    for a non-3.14 Python, so run the script from outside `web/` (where
    `.python-version` pins 3.14) with
    `uv run --offline --no-project --with playwright==1.65.1 python -I …/compare.py --chromium …`.
    Start `vite preview` with `setsid`, or it dies with the shell.
- **Phase 5 — next.** Cut-over and cleanup, blocked on the hosting decision.

## Decision log

| Date       | Decision                                                                 | Status      |
| ---------- | ------------------------------------------------------------------------ | ----------- |
| 2026-11-12 | Move the React site to `legacy-react/`, build Django in `web/`           | Decided     |
| 2026-11-12 | Django runs **locally only** for now; nothing in `web/` is deployed      | Decided     |
| 2026-11-12 | `deploy.yml` only fires on `legacy-react/**` changes, so it stays separate | Decided     |
| 2026-11-12 | Production hosting for Django (static export to GitHub Pages vs. server) | **Pending** |
| 2026-11-12 | Full Python port of the scene, not hybrid (`django-vite` serving React)  | Decided     |
| 2026-11-12 | Scene parity means identical SVG except React-generated (`useId`) ids    | Decided     |

### Pending: hosting

GitHub Pages only serves static files, so it cannot run Django. Options:

- **Static export.** Django renders the page to HTML at build time (e.g.
  `django-distill` or a management command) and the output keeps deploying to
  GitHub Pages under the same domain. No running server, no cost.
- **Server.** A real host (Fly.io, Render, a VPS…). Needed only once the site
  gains dynamic features (registration, CFP, an admin for the committee).

Until this is decided, production keeps deploying `legacy-react/` and nothing
in `web/` may assume either option.

### Decided: full Python port of the scene

The scene is static SVG with no interaction, and the generators are about 220
lines of pure arithmetic. A hybrid would keep Node in the build permanently
and complicate the hosting decision for no user-facing gain. Rendering the
scene server-side also means it appears without JavaScript, which the React
site cannot do. The cost is careful numeric porting; see the Phase 3 pitfalls
under Progress.
