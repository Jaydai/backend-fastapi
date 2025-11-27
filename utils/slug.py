"""Slug generation utilities for database entities."""

import re


def generate_version_slug(version_name: str, version_number: int | None = None) -> str:
    """
    Generate a URL-friendly slug from a version name.

    Examples:
        "Version 2.0" -> "v2-0"
        "Beta Release" -> "beta-release"
        "1.5 Draft" -> "1-5-draft"

    Args:
        version_name: The human-readable version name
        version_number: Optional version number to prefix (for uniqueness)

    Returns:
        A URL-friendly slug
    """
    # Convert to lowercase
    slug = version_name.lower()

    # Replace spaces and special characters with hyphens
    slug = re.sub(r"[^a-z0-9]+", "-", slug)

    # Remove leading/trailing hyphens
    slug = slug.strip("-")

    # Collapse multiple consecutive hyphens
    slug = re.sub(r"-+", "-", slug)

    # Prefix with version number if provided
    if version_number is not None:
        slug = f"v{version_number}-{slug}" if slug else f"v{version_number}"

    # Ensure the slug is not empty
    if not slug:
        slug = "version"

    return slug


def ensure_unique_slug(base_slug: str, existing_slugs: list[str]) -> str:
    """
    Ensure a slug is unique by appending a number if necessary.

    Args:
        base_slug: The desired slug
        existing_slugs: List of existing slugs to check against

    Returns:
        A unique slug
    """
    if base_slug not in existing_slugs:
        return base_slug

    # Try appending numbers until we find a unique slug
    counter = 2
    while True:
        candidate = f"{base_slug}-{counter}"
        if candidate not in existing_slugs:
            return candidate
        counter += 1
