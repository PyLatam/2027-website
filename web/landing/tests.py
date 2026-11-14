import json
import os
import re
import subprocess
import sys
from pathlib import Path

from django.test import SimpleTestCase, override_settings

from core.content import EVENT
from core.locales import LOCALE_COOKIE


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

    def test_skip_link_targets_an_element_that_exists(self) -> None:
        html = self.client.get("/").content.decode()
        self.assertIn('href="#content"', html)
        self.assertEqual(html.count('id="content"'), 1)


class RememberedLocaleTests(SimpleTestCase):
    def test_lang_param_is_remembered_in_a_cookie(self) -> None:
        response = self.client.get("/", {"lang": "en"})
        cookie = response.cookies[LOCALE_COOKIE]
        self.assertEqual(cookie.value, "en")
        self.assertTrue(cookie["max-age"])
        self.assertTrue(cookie["httponly"])
        self.assertEqual(cookie["samesite"], "Lax")

    def test_remembered_choice_applies_without_the_param(self) -> None:
        self.client.get("/", {"lang": "en"})
        response = self.client.get("/", headers={"accept-language": "es"})
        self.assertContains(response, '<html lang="en">')

    def test_new_choice_replaces_the_old_one(self) -> None:
        self.client.get("/", {"lang": "en"})
        self.client.get("/", {"lang": "es"})
        self.assertContains(self.client.get("/"), '<html lang="es-419">')

    def test_no_cookie_without_an_explicit_choice(self) -> None:
        response = self.client.get("/", headers={"accept-language": "en"})
        self.assertContains(response, '<html lang="en">')
        self.assertNotIn(LOCALE_COOKIE, response.cookies)

    def test_unsupported_lang_param_is_not_remembered(self) -> None:
        response = self.client.get("/", {"lang": "fr"})
        self.assertNotIn(LOCALE_COOKIE, response.cookies)

    def test_response_varies_on_cookie_and_accept_language(self) -> None:
        vary = self.client.get("/")["Vary"]
        self.assertIn("Cookie", vary)
        self.assertIn("Accept-Language", vary)


class LanguageSwitcherTests(SimpleTestCase):
    def options(self, lang: str) -> list[str]:
        html = self.client.get("/", {"lang": lang}).content.decode()
        return re.findall(r'<a\s[^>]*class="language-switcher-option"[^>]*>.*?</a>', html, re.S)

    def test_one_plain_link_per_locale(self) -> None:
        options = self.options("es")
        self.assertEqual(len(options), 2)
        self.assertIn('href="?lang=es"', options[0])
        self.assertIn('href="?lang=en"', options[1])
        self.assertIn(">ES</a>", options[0])
        self.assertIn(">EN</a>", options[1])

    def test_current_locale_is_marked(self) -> None:
        for lang, current in (("es", 0), ("en", 1)):
            with self.subTest(lang=lang):
                options = self.options(lang)
                self.assertIn('aria-current="true"', options[current])
                self.assertNotIn('aria-current="true"', options[1 - current])

    def test_labels_are_localised(self) -> None:
        es = self.options("es")
        self.assertIn('aria-label="Cambiar idioma a English"', es[1])
        en = self.options("en")
        self.assertIn('aria-label="Switch language to Español"', en[0])

    def test_switcher_sits_in_the_toolbar(self) -> None:
        self.assertContains(
            self.client.get("/"), 'class="language-switcher app-toolbar" role="group"'
        )


class FooterTests(SimpleTestCase):
    def test_social_links_come_from_content(self) -> None:
        response = self.client.get("/")
        for url in (
            EVENT.social.x,
            EVENT.social.instagram,
            EVENT.social.linkedin,
            EVENT.social.facebook,
        ):
            with self.subTest(url=url):
                self.assertContains(response, f'href="{url}"', count=1)

    def test_every_social_link_has_an_icon(self) -> None:
        html = self.client.get("/").content.decode()
        self.assertEqual(html.count('class="footer-social-link"'), 4)
        self.assertEqual(
            html.count('<svg viewBox="0 0 24 24" fill="currentColor" class="footer-icon"'), 4
        )

    def test_copy_is_localised(self) -> None:
        es = self.client.get("/", {"lang": "es"})
        self.assertContains(es, f"&copy; {EVENT.year} {EVENT.name}. Todos los derechos reservados.")
        self.assertContains(es, 'aria-label="Instagram de PyCon Latam"')
        self.assertContains(es, 'aria-label="Redes sociales"')
        en = self.client.get("/", {"lang": "en"})
        self.assertContains(en, "All rights reserved.")
        self.assertContains(en, 'aria-label="PyCon Latam on Instagram"')
        self.assertContains(en, 'aria-label="Social media"')


class ProductionSettingsTests(SimpleTestCase):
    def test_production_refuses_to_start_without_a_secret_key(self) -> None:
        env = {**os.environ, "DJANGO_DEBUG": "0", "DJANGO_SECRET_KEY": ""}
        result = subprocess.run(  # noqa: S603
            [sys.executable, "-c", "import config.settings"],
            cwd=Path(__file__).resolve().parent.parent,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DJANGO_SECRET_KEY must be set", result.stderr)


class NoIndexTests(SimpleTestCase):
    def test_no_robots_header_by_default(self) -> None:
        self.assertNotIn("X-Robots-Tag", self.client.get("/").headers)

    @override_settings(NOINDEX=True)
    def test_test_deploys_ask_search_engines_to_skip_them(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.headers["X-Robots-Tag"], "noindex, nofollow")
