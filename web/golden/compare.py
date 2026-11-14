"""Visual parity check: the Django port against the frozen React site.

Both sites must already be running; this script only drives a browser at them:

    # legacy-react/
    npm run build && npm run preview                      # http://localhost:4173/
    # web/
    uv run python manage.py runserver 127.0.0.1:8001      # any free port

    # web/  (Playwright is not a project dependency; uv provides it on the fly)
    uv run --no-project --with playwright python -I golden/compare.py \\
        --django http://127.0.0.1:8001/ --out /tmp/parity

For every viewport and language it loads both pages in a fresh browser context
with the animation clock stopped, waits for the web fonts, freezes the
animations (finite ones jump to their end state, the infinite floats go back
to rest) and then:

- measures horizontal overflow;
- compares the boxes of the hero, its inner column, the emblem, the <h1> and
  each of its lines, every decor piece, the language switcher and the footer;
- compares the visible text of the headline lines, switcher and footer;
- measures the gap from the bottom of the dates line to the top of the surf
  (negative means the surf starts above the dates line);
- diffs the two full-page screenshots pixel by pixel and attributes every
  differing pixel to the smallest measured box that contains it.

Two things make the pixel diff exact rather than "close enough":

- Chromium runs with `--disable-partial-raster`. Without it the decor pieces
  with `will-change: transform` (the palms, the sand) rasterise slightly
  differently from one load to the next, so even a page diffed against itself
  shows a few dozen pixels.
- Adjacent text nodes are merged (`Node.normalize()`) on both pages before the
  screenshot. React renders `© {year} {name}. {rights}` as six text nodes
  where Django's template gives one; Chromium rounds each node's advance on
  its own, which moves glyphs by up to 0.03 px and changes ~100 antialiased
  pixels. The text and markup are the same, so the merge removes noise, not a
  difference. `--keep-text-nodes` turns it off.

With both, identical pages give identical screenshots, so the default pixel
threshold is zero.

The diff runs inside Chromium (canvas), so Playwright is the only dependency.
Screenshots, diff images, side-by-side images and `report.json` go to `--out`.
The exit status is 1 if any case fails a check.
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

from playwright.sync_api import Browser, sync_playwright

# Width x height. The widths AGENTS.md promises plus common laptop sizes,
# landscape phones and a short portrait phone.
VIEWPORTS: tuple[tuple[int, int], ...] = (
    (320, 568),
    (375, 667),
    (390, 844),
    (667, 375),
    (768, 1024),
    (844, 390),
    (1024, 768),
    (1280, 800),
    (1366, 768),
    (1440, 900),
    (1920, 1080),
    (2560, 1440),
)
LANGS: tuple[str, ...] = ("es", "en")

# A box may differ by this much (CSS px) before it counts as a mismatch.
BOX_TOLERANCE = 0.5
# A pixel counts as "strong" when a channel differs by more than this (0-255).
# Glyph antialiasing produces scattered strong pixels too, which is why each
# differing pixel is also attributed to an element.
STRONG_DELTA = 64
# Fail when more than this share of the page differs at all (`--max-diff`).
MAX_DIFF_RATIO = 0.0
CHROMIUM_ARGS = ["--disable-partial-raster"]

HEADLINE_LINES = ("eyebrow", "lead", "city", "country", "dates")
# Classes that say how a decor piece moves, not which piece it is.
GENERIC_CLASSES = {"item", "float", "float-slow"}

FREEZE_JS = """
() => {
  for (const animation of document.getAnimations()) {
    const end = animation.effect?.getComputedTiming().endTime;
    if (Number.isFinite(end)) animation.finish();
    else animation.cancel();
  }
}
"""

# Structural selectors only: React's CSS Module class names are hashed, so the
# two DOMs are matched by shape (ids, tags, aria-hidden, order), not by class.
MEASURE_JS = """
() => {
  const box = (el) => {
    const r = el.getBoundingClientRect();
    return [r.x + scrollX, r.y + scrollY, r.width, r.height];
  };
  const text = (el) => el.textContent.replace(/\\s+/g, ' ').trim();
  const doc = document.documentElement;
  const hero = document.getElementById('content');
  const decor = hero.querySelector(':scope > [aria-hidden="true"]');
  const inner = hero.querySelector(':scope > :not([aria-hidden="true"])');
  const h1 = hero.querySelector('h1');
  const lines = [...h1.querySelectorAll(':scope > span[aria-hidden="true"]')];
  const main = document.querySelector('main');
  const switcher = main.previousElementSibling;
  const footer = document.querySelector('footer');
  const copyright = footer.querySelector('span');
  const social = footer.querySelector('ul');

  const boxes = [
    { name: 'hero', box: box(hero) },
    { name: 'hero-inner', box: box(inner) },
    { name: 'emblem', box: box(inner.querySelector(':scope > svg')) },
    { name: 'h1', box: box(h1) },
    ...lines.map((el, i) => ({ name: `line-${i}`, box: box(el), text: text(el) })),
    ...[...decor.children].map((el, i) => ({
      name: `decor-${i}`, cls: el.getAttribute('class') ?? '', box: box(el),
    })),
    { name: 'switcher', box: box(switcher), text: text(switcher) },
    { name: 'footer', box: box(footer) },
    { name: 'footer-copyright', box: box(copyright), text: text(copyright) },
    { name: 'footer-social', box: box(social) },
  ];

  const surf = [...decor.querySelectorAll('[data-wide-bands], [data-compact-bands]')]
    .filter((g) => getComputedStyle(g).display !== 'none')
    .map((g) => g.getBoundingClientRect().top);
  const datesBottom = lines[lines.length - 1].getBoundingClientRect().bottom;

  const fonts = new Set(
    [...document.fonts].filter((f) => f.status === 'loaded')
      .map((f) => `${f.family.replace(/"/g, '')} ${f.weight}`),
  );

  return {
    overflowX: Math.max(doc.scrollWidth, document.body.scrollWidth) - doc.clientWidth,
    pageHeight: doc.scrollHeight,
    surfGap: Math.min(...surf) - datesBottom,
    fonts: [...fonts].sort(),
    boxes,
  };
}
"""

# Runs on about:blank. Compares two PNGs, paints a diff image (differences in
# red over a faded copy of the React shot) and a React | Django | diff strip.
DIFF_JS = """
async ({ a, b, regions, strongDelta }) => {
  const load = async (data) => {
    const img = new Image();
    img.src = 'data:image/png;base64,' + data;
    await img.decode();
    return img;
  };
  const [ia, ib] = await Promise.all([load(a), load(b)]);
  const w = Math.max(ia.width, ib.width);
  const h = Math.max(ia.height, ib.height);
  const pixels = (img) => {
    const c = new OffscreenCanvas(w, h);
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#ff00ff';
    ctx.fillRect(0, 0, w, h);
    ctx.drawImage(img, 0, 0);
    return ctx.getImageData(0, 0, w, h).data;
  };
  const pa = pixels(ia);
  const pb = pixels(ib);
  const out = new ImageData(w, h);
  const counts = {};
  let any = 0, strong = 0, maxDelta = 0;
  let x0 = w, y0 = h, x1 = -1, y1 = -1;
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      const i = (y * w + x) * 4;
      const d = Math.max(
        Math.abs(pa[i] - pb[i]), Math.abs(pa[i + 1] - pb[i + 1]), Math.abs(pa[i + 2] - pb[i + 2]),
      );
      if (d === 0) {
        const g = 200 + ((pa[i] + pa[i + 1] + pa[i + 2]) / 3) * 0.2;
        out.data[i] = out.data[i + 1] = out.data[i + 2] = g;
        out.data[i + 3] = 255;
        continue;
      }
      any++;
      if (d > strongDelta) strong++;
      if (d > maxDelta) maxDelta = d;
      if (x < x0) x0 = x;
      if (y < y0) y0 = y;
      if (x > x1) x1 = x;
      if (y > y1) y1 = y;
      out.data[i] = 255;
      out.data[i + 1] = out.data[i + 2] = d > strongDelta ? 0 : 120;
      out.data[i + 3] = 255;
      const hit = regions.find(([, rx, ry, rw, rh]) =>
        x >= rx && x < rx + rw && y >= ry && y < ry + rh);
      const key = hit ? hit[0] : 'page';
      counts[key] ??= [0, 0];
      counts[key][0]++;
      if (d > strongDelta) counts[key][1]++;
    }
  }
  const png = async (canvas) => {
    const blob = await canvas.convertToBlob({ type: 'image/png' });
    const bytes = new Uint8Array(await blob.arrayBuffer());
    let s = '';
    for (let i = 0; i < bytes.length; i += 0x8000) {
      s += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
    }
    return btoa(s);
  };
  const diff = new OffscreenCanvas(w, h);
  diff.getContext('2d').putImageData(out, 0, 0);
  const gap = 16;
  const side = new OffscreenCanvas(w * 3 + gap * 2, h);
  const sctx = side.getContext('2d');
  sctx.fillStyle = '#ffffff';
  sctx.fillRect(0, 0, side.width, h);
  sctx.drawImage(ia, 0, 0);
  sctx.drawImage(ib, w + gap, 0);
  sctx.drawImage(diff, (w + gap) * 2, 0);
  return {
    width: w, height: h,
    sizes: [[ia.width, ia.height], [ib.width, ib.height]],
    any, strong, maxDelta,
    bbox: x1 < 0 ? null : [x0, y0, x1 - x0 + 1, y1 - y0 + 1],
    regions: counts,
    diffPng: await png(diff),
    sidePng: await png(side),
  };
}
"""


def decor_label(classes: str) -> str:
    """Name a decor piece from its classes, the same way on both sites.

    React: `_leafTopLeft_x1y2 _float_a3b4`; Django:
    `hero-decor-leaf-top-left hero-decor-float`. Both give `leaf-top-left`.
    """
    names = []
    for token in classes.split():
        module = re.match(r"^_([A-Za-z][A-Za-z0-9]*)_", token)
        if module:
            name = re.sub(r"(?<!^)([A-Z])", r"-\1", module.group(1)).lower()
        else:
            name = token.removeprefix("hero-decor-").removeprefix("hero-")
        if name not in GENERIC_CLASSES:
            names.append(name)
    return " ".join(names)


def capture(
    browser: Browser, url: str, width: int, height: int, merge_text: bool = True
) -> tuple[dict[str, Any], bytes]:
    """Load one page in a fresh context and return its measurements and screenshot."""
    context = browser.new_context(
        viewport={"width": width, "height": height},
        device_scale_factor=1,
        reduced_motion="no-preference",
    )
    try:
        page = context.new_page()
        # Stop the animation clock before the page loads. Pieces with
        # `will-change: transform` are rasterised as layers; if they sway while
        # loading, their final raster depends on timing and the same page can
        # differ from itself by a few pixels.
        cdp = context.new_cdp_session(page)
        cdp.send("Animation.enable")
        cdp.send("Animation.setPlaybackRate", {"playbackRate": 0})
        page.goto(url, wait_until="networkidle")
        page.wait_for_selector("#content h1")
        page.evaluate("document.fonts.ready.then(() => undefined)")
        page.evaluate(FREEZE_JS)
        if merge_text:
            page.evaluate("document.body.normalize()")
        # Two frames, so layout settles after the animations are gone.
        page.evaluate("new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))")
        metrics = page.evaluate(MEASURE_JS)
        shot = page.screenshot(full_page=True, animations="disabled", caret="hide")
        return metrics, shot
    finally:
        context.close()


def with_lang(url: str, lang: str) -> str:
    return f"{url}{'&' if '?' in url else '?'}lang={lang}"


def compare_boxes(react: dict[str, Any], django: dict[str, Any]) -> list[dict[str, Any]]:
    """Every measured element whose box, text or identity differs."""
    problems: list[dict[str, Any]] = []
    rb = {b["name"]: b for b in react["boxes"]}
    db = {b["name"]: b for b in django["boxes"]}
    for name in sorted(set(rb) ^ set(db)):
        problems.append({"name": name, "issue": "missing on one site"})
    for name in [b["name"] for b in django["boxes"] if b["name"] in rb]:
        r, d = rb[name], db[name]
        if "cls" in d and decor_label(r["cls"]) != decor_label(d["cls"]):
            problems.append(
                {
                    "name": name,
                    "issue": "different piece",
                    "react": decor_label(r["cls"]),
                    "django": decor_label(d["cls"]),
                }
            )
        delta = max(abs(a - b) for a, b in zip(r["box"], d["box"], strict=True))
        if delta > BOX_TOLERANCE:
            problems.append(
                {
                    "name": name,
                    "issue": "box",
                    "delta": delta,
                    "react": r["box"],
                    "django": d["box"],
                }
            )
        if r.get("text") != d.get("text"):
            problems.append(
                {"name": name, "issue": "text", "react": r.get("text"), "django": d.get("text")}
            )
    return problems


def region_list(django: dict[str, Any]) -> list[list[Any]]:
    """Measured boxes, smallest first, so a pixel goes to the most specific one."""
    regions = []
    for b in django["boxes"]:
        label = b["name"]
        if "cls" in b:
            label = f"{b['name']} ({decor_label(b['cls'])})"
        x, y, w, h = b["box"]
        regions.append([label, x, y, w, h])
    return sorted(regions, key=lambda r: r[3] * r[4])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--react", default="http://localhost:4173/")
    parser.add_argument("--django", default="http://127.0.0.1:8001/")
    parser.add_argument("--out", type=Path, default=Path(tempfile.gettempdir()) / "pycon-parity")
    parser.add_argument("--chromium", help="Chromium executable, if not Playwright's own")
    parser.add_argument(
        "--only", nargs="*", default=[], help="Limit to sizes such as 390x844 (default: all)"
    )
    parser.add_argument("--langs", nargs="*", default=list(LANGS))
    parser.add_argument(
        "--max-diff",
        type=float,
        default=MAX_DIFF_RATIO,
        help="Share of pixels allowed to differ (default: 0)",
    )
    parser.add_argument(
        "--keep-text-nodes",
        action="store_true",
        help="Do not merge adjacent text nodes before the screenshot",
    )
    args = parser.parse_args()
    merge_text = not args.keep_text_nodes

    viewports = [v for v in VIEWPORTS if not args.only or f"{v[0]}x{v[1]}" in args.only]
    args.out.mkdir(parents=True, exist_ok=True)
    report: list[dict[str, Any]] = []
    failed = False

    with sync_playwright() as pw:
        launch: dict[str, Any] = {"args": CHROMIUM_ARGS}
        if args.chromium:
            launch["executable_path"] = args.chromium
        browser = pw.chromium.launch(**launch)
        canvas = browser.new_page()
        for width, height in viewports:
            for lang in args.langs:
                case = f"{width}x{height}-{lang}"
                react, react_png = capture(
                    browser, with_lang(args.react, lang), width, height, merge_text
                )
                django, django_png = capture(
                    browser, with_lang(args.django, lang), width, height, merge_text
                )
                diff = canvas.evaluate(
                    DIFF_JS,
                    {
                        "a": base64.b64encode(react_png).decode(),
                        "b": base64.b64encode(django_png).decode(),
                        "regions": region_list(django),
                        "strongDelta": STRONG_DELTA,
                    },
                )
                (args.out / f"{case}-react.png").write_bytes(react_png)
                (args.out / f"{case}-django.png").write_bytes(django_png)
                (args.out / f"{case}-diff.png").write_bytes(base64.b64decode(diff.pop("diffPng")))
                (args.out / f"{case}-side.png").write_bytes(base64.b64decode(diff.pop("sidePng")))

                problems = compare_boxes(react, django)
                ratio = diff["any"] / (diff["width"] * diff["height"])
                checks = {
                    "overflow": react["overflowX"] == 0 and django["overflowX"] == 0,
                    "boxes": not problems,
                    "surf gap": abs(react["surfGap"] - django["surfGap"]) <= BOX_TOLERANCE,
                    "page size": diff["sizes"][0] == diff["sizes"][1],
                    "fonts": react["fonts"] == django["fonts"],
                    "pixels": ratio <= args.max_diff,
                }
                ok = all(checks.values())
                failed |= not ok
                report.append(
                    {
                        "case": case,
                        "ok": ok,
                        "checks": checks,
                        "overflowX": [react["overflowX"], django["overflowX"]],
                        "surfGap": [react["surfGap"], django["surfGap"]],
                        "fonts": [react["fonts"], django["fonts"]],
                        "problems": problems,
                        "pixels": {**diff, "ratio": ratio},
                    }
                )
                regions = ", ".join(
                    f"{name} {n}/{s}"
                    for name, (n, s) in sorted(diff["regions"].items(), key=lambda kv: -kv[1][0])
                )
                print(
                    f"{'ok  ' if ok else 'FAIL'} {case:<14}"
                    f" overflow {react['overflowX']}/{django['overflowX']}"
                    f"  boxes {len(problems)} off"
                    f"  surf gap {react['surfGap']:.1f}/{django['surfGap']:.1f}"
                    f"  pixels {diff['any']} ({ratio:.4%}), strong {diff['strong']},"
                    f" max delta {diff['maxDelta']}"
                    + (f"  [{regions}]" if regions else "")
                    + "".join(f"\n       ! {name}" for name, good in checks.items() if not good)
                )
        browser.close()

    (args.out / "report.json").write_text(json.dumps(report, indent=2))
    print(f"\n{len(report)} cases, {'FAILED' if failed else 'all ok'}. Output: {args.out}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
