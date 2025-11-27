from turtle import pu
from supabase import Client
from dtos import (
    VersionSlugResponseDTO
)
from domains.entities import VersionSummary
from repositories import TemplateVersionRepository


class TemplateVersionService:
    @staticmethod
    def get_version_by_slug(
        client: Client,
        template_id: str,
        slug: str
    ) -> list[VersionSlugResponseDTO]:
        return TemplateVersionRepository.get_version_by_slug(client, template_id, slug)

    def get_versions_summary(
        client: Client,
        template_id: str,
        published: bool | None = None
    ) -> list[VersionSummary]:
        return TemplateVersionRepository.get_versions_summary(client, template_id, published)