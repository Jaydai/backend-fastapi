"""Service for getting template metadata with version summaries."""

from supabase import Client
from dtos import TemplateMetadataDTO, VersionSummary
from repositories.templates import get_template_metadata as repo_get_template_metadata
from repositories.templates.versions import get_versions_summary
from utils.localization import localize_object


def get_template_metadata(
    client: Client,
    locale: str,
    template_id: str
) -> TemplateMetadataDTO | None:
    """
    Get template metadata with list of version summaries (no content).

    This is optimized for the initial template detail page load:
    - Fetches template metadata (no content)
    - Fetches all version summaries (no content)
    - Localizes all text fields

    Args:
        client: Supabase client
        locale: Locale for localization (e.g., "en", "fr")
        template_id: UUID of the template

    Returns:
        TemplateMetadataDTO with version summaries, or None if not found
    """
    # Get template metadata (no content)
    template = repo_get_template_metadata(client, template_id)

    if not template:
        return None

    # Get all version summaries for this template
    versions_data = get_versions_summary(client, template_id)

    # Convert to DTOs with localization
    versions = [
        VersionSummary(
            id=v.id,
            name=localize_object(v.name, locale),
            slug=v.slug,
            is_current=v.is_current,
            created_at=v.created_at,
            author_id=v.author_id
        )
        for v in versions_data
    ]

    # Localize template title and description
    title = localize_object(template.title, locale) if isinstance(template.title, dict) else template.title
    description = localize_object(template.description, locale) if isinstance(template.description, dict) else template.description

    return TemplateMetadataDTO(
        id=template.id,
        title=title,
        description=description,
        folder_id=template.folder_id,
        organization_id=template.organization_id,
        user_id=template.user_id,
        workspace_type=template.workspace_type,
        created_at=template.created_at,
        updated_at=template.updated_at,
        tags=template.tags or [],
        usage_count=template.usage_count or 0,
        current_version_id=template.current_version_id,
        is_free=template.is_free,
        is_published=template.is_published,
        versions=versions
    )
