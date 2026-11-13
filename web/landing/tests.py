import json
import re

from django.test import SimpleTestCase

from core.content import EVENT


class IndexViewTests(SimpleTestCase):
    def test_renders_in_spanish_by_default(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<html lang="es-419">')
        self.assertContains(response, "Saltar al contenido")
        self.assertContains(response, '<meta property="og:locale" content="es_419" />')

    def test_renders_in_english_with_lang_param(self) -> None:
        response = self.client.get("/", {"lang": "en"})
        self.assertContains(response, '<html lang="en">')
        self.assertContains(response, "Skip to content")
        self.assertContains(response, '<meta property="og:locale" content="en_US" />')

    def test_json_ld_is_valid_and_matches_the_event(self) -> None:
        html = self.client.get("/").content.decode()
        match = re.search(
            r'<script type="application/ld\+json">(.*?)</script>', html, flags=re.DOTALL
        )
        assert match is not None
        data = json.loads(match.group(1))
        self.assertEqual(data["@type"], "Event")
        self.assertEqual(data["startDate"], EVENT.dates.start)
        self.assertEqual(data["endDate"], EVENT.dates.end)
        self.assertEqual(data["url"], EVENT.canonical_url)

    def test_hreflang_alternates_cover_every_locale(self) -> None:
        response = self.client.get("/")
        for code in ("es", "en", "x-default"):
            self.assertContains(response, f'hreflang="{code}"')
