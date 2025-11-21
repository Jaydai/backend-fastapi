from fastapi import Request
from dataclasses import asdict, is_dataclass
from services.locale_service import LocaleService


def extract_locale_from_request(request: Request) -> str:
    """
    Extract locale from request headers.

    Args:
        request: FastAPI Request object

    Returns:
        Locale string (e.g., "en", "fr")
    """
    # Try to get from custom header first
    locale = request.headers.get("X-Locale") or request.headers.get("Accept-Language")

    if locale:
        # Parse Accept-Language header (e.g., "en-US,en;q=0.9,fr;q=0.8")
        if "," in locale:
            locale = locale.split(",")[0]
        if "-" in locale:
            locale = locale.split("-")[0]
        locale = locale.lower()[:2]

    # Default to English if not found or invalid
    return locale if locale in ["en", "fr"] else "en"


def ensure_localized_field(value: str | dict[str, str], locale: str) -> dict[str, str]:
    """
    Ensure a field is in localized format.

    Args:
        value: String or dict value
        locale: Current locale

    Returns:
        Dict with locale keys
    """
    if isinstance(value, dict):
        return value
    elif isinstance(value, str):
        return {locale: value}
    else:
        return {}


def get_localized_value(field: str | dict[str, str], locale: str = LocaleService.DEFAULT_LOCALE, fallback: str = None) -> str:
    """
    Get localized value from a field.

    Args:
        field: String or dict field
        locale: Desired locale
        fallback: Fallback value if not found

    Returns:
        Localized string value
    """
    if isinstance(field, str):
        return field
    elif isinstance(field, dict):
        # Try requested locale first
        if locale in field:
            return field[locale]
        # Then try fallback chain: "custom", "en", "fr", then first available
        return (
            field.get("custom") or
            field.get("en") or
            field.get("fr") or
            next(iter(field.values()), fallback or "")
        )
    return fallback or ""


def localize_object(obj: dict | object, locale: str, fields: list) -> dict:
    """
    Transform localized fields in an object to strings based on locale.

    Args:
        obj: The object (dict or Pydantic model) to transform
        locale: The target locale (e.g., "en", "fr")
        fields: List of field names to localize

    Returns:
        Transformed dict with localized fields as strings
    """
    # Convert to dict based on object type
    if is_dataclass(obj):
        obj_dict = asdict(obj)
    elif hasattr(obj, 'model_dump'):
        obj_dict = obj.model_dump()
    elif hasattr(obj, 'dict'):
        obj_dict = obj.dict()
    elif isinstance(obj, dict):
        obj_dict = obj.copy()
    else:
        return obj

    # Transform specified fields only if they exist and are not None
    for field in fields:
        if field in obj_dict and obj_dict[field] is not None:
            # Only localize if it's a dict (localized field) or string
            field_value = obj_dict[field]
            if isinstance(field_value, dict) or isinstance(field_value, str):
                obj_dict[field] = get_localized_value(field_value, locale)

    return obj_dict


def localize_list(items: list, locale: str, fields: list) -> list:
    """
    Transform a list of objects with localized fields.

    Args:
        items: List of objects to transform
        locale: The target locale
        fields: List of field names to localize

    Returns:
        List of transformed dicts
    """
    return [localize_object(item, locale, fields) for item in items]
