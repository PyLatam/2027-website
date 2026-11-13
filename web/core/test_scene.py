"""The scene port against golden output from the React site.

`web/golden/*.json` is produced by `web/golden/generate.mjs` from the real
TypeScript in `legacy-react/` and committed, so these tests need no Node.
"Identical" means byte-identical, except for the ids React's `useId`
generates, which are normalised before comparing.
"""

import hashlib
import json
import math
import re
from collections import Counter
from functools import cache
from pathlib import Path
from typing import Any

from django.conf import settings
from django.template import Context, Template
from django.test import SimpleTestCase

from core import decor
from core.decor.shapes import ASSETS, DECOR_SHAPES
from core.dictionary import ES
from core.svg import (
    canopy_blobs,
    create_random,
    js_fixed2,
    js_hypot,
    js_round,
    js_str,
    namespace_svg_ids,
    ribbon_path,
    svg_inner_markup,
    svg_view_box,
)

GOLDEN = Path(settings.BASE_DIR) / "golden"
CSS = Path(settings.BASE_DIR) / "static" / "css"

REACT_UID = re.compile(r"_R_[0-9a-z]+_")
"""`useId` on the server, as React 19 prints it (`_R_0_`, `_R_1l_`, …)."""
DJANGO_UID = re.compile(r"\bsvg\d+\b")
"""`core.templatetags.decor` uids (`svg1`, `svg2`, …)."""
TEST_UID = "svgtest"

ID_ATTR = re.compile(r"""\bid=["']([^"']+)["']""")
REFERENCE = re.compile(r"""url\(#([^)]+)\)|href=["']#([^"']+)["']""")


@cache
def golden(name: str) -> Any:
    return json.loads((GOLDEN / f"{name}.json").read_text(encoding="utf-8"))


def normalise_ids(markup: str, uid: re.Pattern[str]) -> str:
    """Replace each distinct uid with `UID<n>`, numbered by first appearance."""
    order: dict[str, int] = {}

    def label(match: re.Match[str]) -> str:
        return f"UID{order.setdefault(match.group(), len(order))}"

    return uid.sub(label, markup)


def collapse(markup: str) -> str:
    """Drop whitespace between tags (template indentation) and at the ends."""
    return re.sub(r">\s+<", "><", markup).strip()


def strip_css(css: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"/\*.*?\*/", "", css, flags=re.S)).strip()


class IdIntegrityMixin(SimpleTestCase):
    def assert_ids_resolve(self, markup: str) -> None:
        """Every id is unique and every `url(#…)`/`href="#…"` points at one."""
        ids = Counter(ID_ATTR.findall(markup))
        duplicates = [i for i, n in ids.items() if n > 1]
        self.assertEqual(duplicates, [], "duplicate ids")
        references = {a or b for a, b in REFERENCE.findall(markup)}
        self.assertEqual(sorted(references - set(ids)), [], "dangling references")


class NumberTests(SimpleTestCase):
    """The JS number rules every SVG coordinate goes through."""

    def test_to_string_matches_js(self) -> None:
        for value, expected in golden("numbers")["toString"]:
            with self.subTest(value=value):
                self.assertEqual(js_str(value), expected)

    def test_to_fixed_2_matches_js(self) -> None:
        for value, expected in golden("numbers")["toFixed2"]:
            with self.subTest(value=value):
                self.assertEqual(js_fixed2(value), expected)

    def test_math_round_matches_js(self) -> None:
        for value, expected in golden("numbers")["round"]:
            with self.subTest(value=value):
                self.assertEqual(js_round(value), expected)

    def test_hypot_matches_v8_bit_for_bit(self) -> None:
        for x, y, expected in golden("numbers")["hypot"]:
            with self.subTest(x=x, y=y):
                self.assertEqual(js_hypot(x, y), expected)

    def test_documented_pitfalls(self) -> None:
        self.assertEqual(js_fixed2(0.125), "0.13")  # Python's format gives 0.12.
        self.assertEqual(js_fixed2(-0.001), "0")  # Not "-0".
        self.assertEqual(js_str(3.0), "3")
        self.assertEqual(js_str(1e-7), "1e-7")
        self.assertEqual(js_round(2.5), 3)  # Python's round gives 2.
        self.assertEqual(js_round(-2.5), -2)
        self.assertEqual(math.copysign(1, js_round(-0.4)), -1)  # -0, like JS.


class PrngTests(SimpleTestCase):
    def test_sequences_match_create_random(self) -> None:
        for case in golden("prng"):
            with self.subTest(seed=case["seed"]):
                next_value = create_random(case["seed"])
                self.assertEqual([next_value() for _ in case["values"]], case["values"])

    def test_same_seed_same_sequence(self) -> None:
        a, b = create_random(21), create_random(21)
        self.assertEqual([a() for _ in range(10)], [b() for _ in range(10)])


class RibbonTests(SimpleTestCase):
    def test_paths_match_ribbon_path(self) -> None:
        for index, case in enumerate(golden("ribbon")):
            with self.subTest(index=index):
                self.assertEqual(ribbon_path(case["spine"]), case["d"])


class CanopyTests(SimpleTestCase):
    def test_blobs_match_canopy_blobs(self) -> None:
        for case in golden("canopy"):
            options = case["options"]
            with self.subTest(seed=options["seed"]):
                blobs = canopy_blobs(
                    seed=options["seed"],
                    count=options["count"],
                    start=tuple(options["from"]),
                    end=tuple(options["to"]),
                    min_radius=options["minRadius"],
                    max_radius=options["maxRadius"],
                    scatter=options["scatter"],
                )
                self.assertEqual(
                    [blob._asdict() for blob in blobs],
                    [{"cx": b["cx"], "cy": b["cy"], "r": b["r"]} for b in case["blobs"]],
                )


class MarkupHelperTests(SimpleTestCase):
    def test_view_box_matches(self) -> None:
        for name, expected in golden("markup")["helpers"]["viewBox"]:
            with self.subTest(name=name):
                self.assertEqual(svg_view_box(DECOR_SHAPES[name]), expected)

    def test_namespaced_inner_markup_matches(self) -> None:
        for name, expected in golden("markup")["helpers"]["namespace"]:
            with self.subTest(name=name):
                self.assertEqual(
                    namespace_svg_ids(svg_inner_markup(DECOR_SHAPES[name]), "UID"), expected
                )

    def test_view_box_fallback(self) -> None:
        self.assertEqual(svg_view_box("<svg></svg>"), "0 0 100 100")


class AssetTests(SimpleTestCase):
    def test_artwork_is_a_verbatim_copy(self) -> None:
        """Never redraw the supplied artwork: the files match React's byte for byte."""
        for relative, digest in golden("assets").items():
            with self.subTest(file=relative):
                data = (ASSETS / relative).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), digest)

    def test_catalogue_matches_the_files(self) -> None:
        expected = {Path(p).stem for p in golden("assets") if p.startswith("decor/")}
        self.assertEqual(set(DECOR_SHAPES), expected)


class ComponentMarkupTests(IdIntegrityMixin):
    """Each decor component against `react-dom/server` output, prop for prop."""

    def assert_same(self, key: str, markup: str) -> None:
        expected = golden("markup")["components"][key]
        self.assertEqual(
            normalise_ids(markup, re.compile(re.escape(TEST_UID))),
            normalise_ids(expected, REACT_UID),
        )
        self.assert_ids_resolve(markup)

    def test_brand_mark(self) -> None:
        self.assert_same("BrandMark/es", decor.brand_mark(title=ES["logo.alt"], uid=TEST_UID))
        self.assert_same(
            "BrandMark/class",
            decor.brand_mark(title='A & "B"', uid=TEST_UID, class_name="x y"),
        )

    def test_brand_shapes(self) -> None:
        for name in DECOR_SHAPES:
            with self.subTest(name=name):
                self.assert_same(f"BrandShape/{name}", decor.brand_shape(name, uid=TEST_UID))
                self.assert_same(
                    f"BrandShape/{name}/color",
                    decor.brand_shape(
                        name, uid=TEST_UID, color="var(--c-aqua-500)", class_name="item"
                    ),
                )

    def test_circuit_traces(self) -> None:
        self.assert_same("CircuitTraces", decor.circuit_traces())
        self.assert_same("CircuitTraces/class", decor.circuit_traces(class_name="traces left"))

    def test_palm_tree(self) -> None:
        self.assert_same(
            "PalmTree",
            decor.palm_tree(trunk_color="var(--c-aqua-600)", crown_color="var(--c-aqua-600)"),
        )
        self.assert_same(
            "PalmTree/flip8",
            decor.palm_tree(
                trunk_color="var(--c-ocean-400)",
                crown_color="var(--c-ocean-400)",
                fronds=8,
                flip=True,
                class_name="palm",
            ),
        )
        for fronds in (1, 2, 3, 5, 12):
            with self.subTest(fronds=fronds):
                self.assert_same(
                    f"PalmTree/fronds{fronds}",
                    decor.palm_tree(trunk_color="red", crown_color="blue", fronds=fronds),
                )

    def test_sand_cove(self) -> None:
        self.assert_same("SandCove", decor.sand_cove(uid=TEST_UID))
        self.assert_same("SandCove/seed7", decor.sand_cove(uid=TEST_UID, seed=7, class_name="sand"))

    def test_sea_rock(self) -> None:
        self.assert_same("SeaRock", decor.sea_rock(class_name="rock"))

    def test_shoreline(self) -> None:
        self.assert_same("Shoreline", decor.shoreline(class_name="shore"))


class TemplateTagTests(IdIntegrityMixin):
    def render(self, source: str) -> str:
        return Template("{% load decor %}" + source).render(Context())

    def test_each_instance_gets_its_own_ids(self) -> None:
        html = self.render('<div>{% brand_shape "sea-rock" %}{% brand_shape "sea-rock" %}</div>')
        expected = golden("markup")["components"]["BrandShape/twice"]
        self.assertEqual(normalise_ids(html, DJANGO_UID), normalise_ids(expected, REACT_UID))
        self.assert_ids_resolve(html)

    def test_ids_restart_on_every_render(self) -> None:
        source = '{% brand_shape "sea-rock" %}'
        self.assertEqual(self.render(source), self.render(source))

    def test_unknown_shape_fails_loudly(self) -> None:
        with self.assertRaises(KeyError):
            self.render('{% brand_shape "not-a-shape" %}')


class HeroTests(IdIntegrityMixin):
    """The whole hero, rendered by Django, against the React `Hero`."""

    def hero(self, lang: str) -> str:
        html = self.client.get("/", {"lang": lang}).content.decode()
        match = re.search(r'<section class="hero".*?</section>', html, flags=re.S)
        assert match is not None
        return match.group()

    def test_hero_matches_react(self) -> None:
        for lang in ("es", "en"):
            with self.subTest(lang=lang):
                expected = golden("markup")["components"][f"Hero/{lang}"]
                self.assertEqual(
                    collapse(normalise_ids(self.hero(lang), DJANGO_UID)),
                    collapse(normalise_ids(expected, REACT_UID)),
                )

    def test_scene_matches_hero_decor(self) -> None:
        match = re.search(
            r'<div class="hero-decor".*</div>(?=\s*<div class="hero-inner")',
            self.hero("es"),
            flags=re.S,
        )
        assert match is not None
        expected = golden("markup")["components"]["HeroDecor"]
        self.assertEqual(
            collapse(normalise_ids(match.group(), DJANGO_UID)),
            collapse(normalise_ids(expected, REACT_UID)),
        )

    def test_page_ids_are_unique_and_resolve(self) -> None:
        for lang in ("es", "en"):
            with self.subTest(lang=lang):
                self.assert_ids_resolve(self.client.get("/", {"lang": lang}).content.decode())

    def test_skip_link_targets_the_hero(self) -> None:
        self.assertIn('id="content"', self.hero("es"))

    def test_copy_comes_from_the_dictionary(self) -> None:
        self.assertIn('aria-label="PyCon Latam RD logo, Punta Cana"', self.hero("en"))
        self.assertIn(">August 26 – 29, 2027</span>", self.hero("en"))
        self.assertIn(">26 – 29 de agosto, 2027</span>", self.hero("es"))


class CssTests(SimpleTestCase):
    """The hero CSS matches the compiled CSS Modules, renamed to Django classes."""

    def test_css_matches_the_modules(self) -> None:
        for name, compiled in golden("css").items():
            with self.subTest(file=name):
                ported = (CSS / name).read_text(encoding="utf-8")
                self.assertEqual(strip_css(ported), strip_css(compiled))

    def test_every_decor_item_sets_its_own_width(self) -> None:
        """`.hero-decor-item`'s width is a fallback, not a size."""
        html = self.client.get("/").content.decode()
        css = (CSS / "hero-decor.css").read_text(encoding="utf-8")
        items = re.findall(r'class="hero-decor-item ([a-z-]+)', html)
        self.assertTrue(items)
        for class_name in set(items):
            with self.subTest(item=class_name):
                rule = re.search(rf"\.{class_name} \{{([^}}]*)\}}", css)
                assert rule is not None
                self.assertRegex(rule.group(1), r"(?m)^\s*width:")
