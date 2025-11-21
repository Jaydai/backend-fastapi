"""
Tests for the centralized LocaleService.

This ensures the locale management is working correctly across the application.
"""
import pytest
import sys
from pathlib import Path
import importlib.util

# Direct import to avoid openai dependency issue
spec = importlib.util.spec_from_file_location(
    "locale_service",
    Path(__file__).parent.parent / "services" / "locale_service.py"
)
locale_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(locale_module)
LocaleService = locale_module.LocaleService


class MockRequest:
    """Mock FastAPI Request for testing."""
    def __init__(self, headers: dict):
        self.headers = headers


class TestLocaleServiceExtraction:
    """Test locale extraction from headers."""

    def test_extract_from_x_locale_header(self):
        """Should prioritize X-Locale header."""
        request = MockRequest(headers={"X-Locale": "fr", "Accept-Language": "en"})
        locale = LocaleService.extract_locale_from_request(request)
        assert locale == "fr"

    def test_extract_from_accept_language_header(self):
        """Should fallback to Accept-Language header when X-Locale not present."""
        request = MockRequest(headers={"Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8"})
        locale = LocaleService.extract_locale_from_request(request)
        assert locale == "fr"

    def test_extract_with_no_headers(self):
        """Should return default locale when no headers present."""
        request = MockRequest(headers={})
        locale = LocaleService.extract_locale_from_request(request)
        assert locale == "en"

    def test_extract_with_invalid_locale(self):
        """Should return default locale for unsupported locales."""
        request = MockRequest(headers={"X-Locale": "de"})  # German not supported
        locale = LocaleService.extract_locale_from_request(request)
        assert locale == "en"

    def test_extract_with_complex_accept_language(self):
        """Should parse complex Accept-Language header correctly."""
        request = MockRequest(headers={"Accept-Language": "fr-CA,fr;q=0.9,en-US;q=0.8,en;q=0.7"})
        locale = LocaleService.extract_locale_from_request(request)
        assert locale == "fr"


class TestLocaleServiceValidation:
    """Test locale validation."""

    def test_validate_supported_locale_en(self):
        """Should validate English locale."""
        assert LocaleService.validate_locale("en") == "en"

    def test_validate_supported_locale_fr(self):
        """Should validate French locale."""
        assert LocaleService.validate_locale("fr") == "fr"

    def test_validate_unsupported_locale(self):
        """Should return default for unsupported locale."""
        assert LocaleService.validate_locale("de") == "en"
        assert LocaleService.validate_locale("es") == "en"

    def test_validate_none_locale(self):
        """Should return default for None."""
        assert LocaleService.validate_locale(None) == "en"

    def test_validate_empty_locale(self):
        """Should return default for empty string."""
        assert LocaleService.validate_locale("") == "en"

    def test_validate_case_insensitive(self):
        """Should handle case-insensitive validation."""
        assert LocaleService.validate_locale("EN") == "en"
        assert LocaleService.validate_locale("FR") == "fr"


class TestLocaleServiceLocalization:
    """Test string localization."""

    def test_localize_dict_with_requested_locale(self):
        """Should return value for requested locale."""
        value = {"en": "Hello", "fr": "Bonjour"}
        result = LocaleService.localize_string(value, "fr")
        assert result == "Bonjour"

    def test_localize_dict_with_fallback_to_default(self):
        """Should fallback to default locale when requested not available."""
        value = {"en": "Hello"}
        result = LocaleService.localize_string(value, "fr")
        assert result == "Hello"

    def test_localize_dict_with_fallback_to_any(self):
        """Should fallback to any available locale when default not available."""
        value = {"fr": "Bonjour"}
        result = LocaleService.localize_string(value, "es")  # Neither es nor en available
        assert result == "Bonjour"

    def test_localize_plain_string(self):
        """Should return plain string as-is."""
        result = LocaleService.localize_string("Hello", "fr")
        assert result == "Hello"

    def test_localize_none_value(self):
        """Should return empty string for None."""
        result = LocaleService.localize_string(None, "en")
        assert result == ""

    def test_localize_empty_dict(self):
        """Should return empty string for empty dict."""
        result = LocaleService.localize_string({}, "en")
        assert result == ""

    def test_localize_dict_with_empty_values(self):
        """Should skip empty values and return first non-empty."""
        value = {"en": "", "fr": "Bonjour"}
        result = LocaleService.localize_string(value, "en")
        assert result == "Bonjour"


class TestLocaleServiceEnsureDict:
    """Test conversion to localized dict format."""

    def test_ensure_localized_dict_with_value(self):
        """Should create dict with specified locale."""
        result = LocaleService.ensure_localized_dict("Hello", "en")
        assert result == {"en": "Hello"}

    def test_ensure_localized_dict_with_different_locale(self):
        """Should create dict with specified locale."""
        result = LocaleService.ensure_localized_dict("Bonjour", "fr")
        assert result == {"fr": "Bonjour"}

    def test_ensure_localized_dict_with_none(self):
        """Should create dict with empty string for None."""
        result = LocaleService.ensure_localized_dict(None, "en")
        assert result == {"en": ""}


class TestLocaleServiceObjectLocalization:
    """Test object and list localization."""

    def test_localize_object_dict(self):
        """Should localize specific fields in a dict."""
        obj = {
            "id": 1,
            "title": {"en": "Hello", "fr": "Bonjour"},
            "description": {"en": "World", "fr": "Monde"}
        }
        result = LocaleService.localize_object(obj, "fr", ["title", "description"])
        assert result["title"] == "Bonjour"
        assert result["description"] == "Monde"
        assert result["id"] == 1

    def test_localize_object_with_missing_field(self):
        """Should handle missing fields gracefully."""
        obj = {"id": 1, "title": {"en": "Hello", "fr": "Bonjour"}}
        result = LocaleService.localize_object(obj, "fr", ["title", "missing_field"])
        assert result["title"] == "Bonjour"
        assert "missing_field" not in result

    def test_localize_list(self):
        """Should localize all objects in a list."""
        items = [
            {"id": 1, "title": {"en": "Hello", "fr": "Bonjour"}},
            {"id": 2, "title": {"en": "World", "fr": "Monde"}}
        ]
        result = LocaleService.localize_list(items, "fr", ["title"])
        assert len(result) == 2
        assert result[0]["title"] == "Bonjour"
        assert result[1]["title"] == "Monde"

    def test_localize_empty_list(self):
        """Should handle empty list."""
        result = LocaleService.localize_list([], "en", ["title"])
        assert result == []


class TestLocaleServiceHelpers:
    """Test helper methods."""

    def test_get_supported_locales(self):
        """Should return list of supported locales."""
        locales = LocaleService.get_supported_locales()
        assert "en" in locales
        assert "fr" in locales
        assert len(locales) == 2

    def test_is_locale_supported_true(self):
        """Should return True for supported locales."""
        assert LocaleService.is_locale_supported("en") is True
        assert LocaleService.is_locale_supported("fr") is True

    def test_is_locale_supported_false(self):
        """Should return False for unsupported locales."""
        assert LocaleService.is_locale_supported("de") is False
        assert LocaleService.is_locale_supported("es") is False

    def test_is_locale_supported_case_insensitive(self):
        """Should handle case-insensitive check."""
        assert LocaleService.is_locale_supported("EN") is True
        assert LocaleService.is_locale_supported("FR") is True
