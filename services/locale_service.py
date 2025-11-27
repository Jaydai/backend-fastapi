"""Centralized locale management service."""

import logging
from typing import Any

from fastapi import Request

logger = logging.getLogger(__name__)


class LocaleService:
    """Centralized service for locale management and localization."""

    SUPPORTED_LOCALES = ["en", "fr"]
    DEFAULT_LOCALE = "fr"

    @staticmethod
    def extract_locale_from_request(request: Request) -> str:
        """Extract and validate locale from request headers (X-Locale or Accept-Language)."""
        locale = request.headers.get("X-Locale")

        if not locale:
            accept_language = request.headers.get("Accept-Language")
            if accept_language:
                locale = accept_language.split(",")[0].split("-")[0].split(";")[0].strip()

        return LocaleService.validate_locale(locale)

    @staticmethod
    def validate_locale(locale: str | None) -> str:
        """Validate locale code against supported locales."""
        if not locale:
            return LocaleService.DEFAULT_LOCALE

        locale = locale.lower().strip()
        return locale if locale in LocaleService.SUPPORTED_LOCALES else LocaleService.DEFAULT_LOCALE

    @staticmethod
    def localize_string(value: dict[str, str] | str | None, locale: str = DEFAULT_LOCALE) -> str:
        """Extract localized string from multilingual value."""
        if value is None:
            return ""

        if isinstance(value, str):
            return value

        if isinstance(value, dict):
            if locale in value and value[locale]:
                return value[locale]

            if LocaleService.DEFAULT_LOCALE in value and value[LocaleService.DEFAULT_LOCALE]:
                return value[LocaleService.DEFAULT_LOCALE]

            for fallback_locale in LocaleService.SUPPORTED_LOCALES:
                if fallback_locale in value and value[fallback_locale]:
                    return value[fallback_locale]

            for val in value.values():
                if val:
                    return val

            return ""

        return ""

    @staticmethod
    def ensure_localized_dict(value: str | None, locale: str = DEFAULT_LOCALE) -> dict[str, str]:
        """Convert a plain string to a localized dict format."""
        if value is None:
            return {locale: ""}
        return {locale: value}

    @staticmethod
    def localize_object(obj: dict | Any, locale: str, fields: list[str]) -> dict:
        """Localize specific fields in an object."""
        if not isinstance(obj, dict):
            obj = obj.__dict__ if hasattr(obj, "__dict__") else {}

        result = obj.copy()
        for field in fields:
            if field in result:
                result[field] = LocaleService.localize_string(result[field], locale)

        return result

    @staticmethod
    def localize_list(items: list[dict | Any], locale: str, fields: list[str]) -> list[dict]:
        """Localize specific fields in a list of objects."""
        return [LocaleService.localize_object(item, locale, fields) for item in items]

    @staticmethod
    def get_supported_locales() -> list[str]:
        """Get list of supported locale codes."""
        return LocaleService.SUPPORTED_LOCALES.copy()

    @staticmethod
    def is_locale_supported(locale: str) -> bool:
        """Check if a locale is supported."""
        return locale.lower() in LocaleService.SUPPORTED_LOCALES
