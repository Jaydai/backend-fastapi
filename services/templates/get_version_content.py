"""Service for getting version content by slug."""

from supabase import Client
from dtos import VersionContentDTO
from repositories.templates.versions import get_version_by_slug
from utils.localization import localize_object


def get_version_content(
    client: Client,
    locale: str,
    template_id: str,
    slug: str
) -> VersionContentDTO | None:
    """
    Get full version content by slug.

    This is called when a specific version is selected or when
    loading the default (current) version.

    Args:
        client: Supabase client
        locale: Locale for localization (e.g., "en", "fr")
        template_id: UUID of the template
        slug: URL-friendly slug of the version

    Returns:
        VersionContentDTO with full content, or None if not found
    """
    version = get_version_by_slug(client, template_id, slug)

    if not version:
        return None

    # Localize text fields
    name = localize_object(version.name, locale) if isinstance(version.name, dict) else version.name
    content = localize_object(version.content, locale) if isinstance(version.content, dict) else version.content
    change_notes = localize_object(version.change_notes, locale) if isinstance(version.change_notes, dict) else version.change_notes

    return VersionContentDTO(
        id=version.id,
        template_id=version.template_id,
        name=name,
        slug=version.slug,
        content=content,
        change_notes=change_notes,
        author_id=version.author_id,
        created_at=version.created_at,
        updated_at=version.updated_at,
        status=version.status,
        is_current=version.is_current,
        is_published=version.is_published,
        optimized_for=version.optimized_for
    )
