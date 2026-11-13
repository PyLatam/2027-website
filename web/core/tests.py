from django.test import RequestFactory, SimpleTestCase

from core.dictionary import DICTIONARIES, ES, interpolate, translate
from core.locales import resolve_locale


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

    def test_query_parameter_wins(self) -> None:
        self.assertEqual(resolve_locale(self.factory.get("/", {"lang": "en"})), "en")

    def test_unknown_or_missing_falls_back_to_spanish(self) -> None:
        self.assertEqual(resolve_locale(self.factory.get("/", {"lang": "fr"})), "es")
        self.assertEqual(resolve_locale(self.factory.get("/")), "es")
