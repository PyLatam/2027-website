from django.http import HttpRequest
from django.test import RequestFactory, SimpleTestCase

from core.dictionary import DICTIONARIES, ES, interpolate, translate
from core.locales import LOCALE_COOKIE, resolve_locale


class DictionaryTests(SimpleTestCase):
    def test_every_locale_has_exactly_the_spanish_keys(self) -> None:
        for locale, messages in DICTIONARIES.items():
            with self.subTest(locale=locale):
                self.assertEqual(set(messages), set(ES))

    def test_no_message_is_empty(self) -> None:
        for locale, messages in DICTIONARIES.items():
            for key, value in messages.items():
                with self.subTest(locale=locale, key=key):
                    self.assertTrue(value.strip())

    def test_interpolate_fills_known_and_keeps_unknown_placeholders(self) -> None:
        self.assertEqual(interpolate("{a} y {b}", {"a": "uno"}), "uno y {b}")

    def test_missing_key_fails_loudly(self) -> None:
        with self.assertRaises(KeyError):
            translate("es", "does.not.exist")


class ResolveLocaleTests(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def request(
        self,
        lang: str | None = None,
        cookie: str | None = None,
        accept: str | None = None,
    ) -> HttpRequest:
        request = self.factory.get(
            "/",
            {"lang": lang} if lang is not None else {},
            **({"HTTP_ACCEPT_LANGUAGE": accept} if accept is not None else {}),
        )
        if cookie is not None:
            request.COOKIES[LOCALE_COOKIE] = cookie
        return request

    def test_query_parameter_beats_everything(self) -> None:
        self.assertEqual(resolve_locale(self.request(lang="en", cookie="es", accept="es")), "en")
        self.assertEqual(resolve_locale(self.request(lang="es", cookie="en", accept="en")), "es")

    def test_remembered_choice_beats_accept_language(self) -> None:
        self.assertEqual(resolve_locale(self.request(cookie="en", accept="es-MX")), "en")
        self.assertEqual(resolve_locale(self.request(cookie="es", accept="en-US")), "es")

    def test_accept_language_is_used_without_a_choice(self) -> None:
        self.assertEqual(resolve_locale(self.request(accept="en-US,en;q=0.9")), "en")

    def test_accept_language_matches_on_the_base_subtag(self) -> None:
        self.assertEqual(resolve_locale(self.request(accept="EN-gb")), "en")
        self.assertEqual(resolve_locale(self.request(accept="es-419")), "es")

    def test_accept_language_skips_unsupported_languages(self) -> None:
        self.assertEqual(resolve_locale(self.request(accept="fr-FR, pt;q=0.9, en;q=0.5")), "en")

    def test_accept_language_honours_quality_values(self) -> None:
        self.assertEqual(resolve_locale(self.request(accept="es;q=0.4, en;q=0.8")), "en")
        # q=0 means "not acceptable".
        self.assertEqual(resolve_locale(self.request(accept="en;q=0, fr")), "es")

    def test_invalid_query_and_cookie_fall_through(self) -> None:
        self.assertEqual(resolve_locale(self.request(lang="fr", cookie="de", accept="en")), "en")

    def test_malformed_accept_language_falls_back_to_spanish(self) -> None:
        self.assertEqual(resolve_locale(self.request(accept=";;, ,q=x;en;q=abc")), "es")

    def test_nothing_known_falls_back_to_spanish(self) -> None:
        self.assertEqual(resolve_locale(self.request()), "es")
        self.assertEqual(resolve_locale(self.request(accept="*")), "es")
