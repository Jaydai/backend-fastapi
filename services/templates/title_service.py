"""Template title service - handles business logic for template list operations"""
from supabase import Client
from dtos import TemplateTitleResponseDTO
from repositories.templates import TemplateBaseRepository
from services.permissions import UserPermissionsService
from utils import localize_object

class TemplateTitleService:
    """Service for template title operations (list views)"""

    @staticmethod
    def get_titles(
        client: Client,
        locale: str = "en",
        organization_id: str | None = None,
        folder_ids: list[str] | None = None,
        published: bool | None = None,
        user_id: str | None = None,
        workspace_type: str | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[TemplateTitleResponseDTO]:
        """
        Get template titles with optional filtering and permission checks.

        Args:
            client: Supabase client
            locale: Locale for localization
            organization_id: Filter by organization (performs access check if user_id provided)
            folder_ids: Filter by folder IDs
            published: Filter by published status
            user_id: User ID for permission checks and workspace filtering
            workspace_type: Workspace type for filtering (user, organization, all)
            limit: Max results
            offset: Pagination offset
        """
        # Build permission filter if user_id and workspace_type provided
        or_conditions = None
        if user_id and workspace_type:
            filter_result = UserPermissionsService.build_workspace_filter_conditions(
                client, user_id, workspace_type, organization_id
            )

            if filter_result["type"] == "none":
                return []
            elif filter_result["type"] == "or":
                or_conditions = filter_result["conditions"]
                organization_id = None  # Clear org_id as we're using OR conditions
            elif filter_result["type"] == "organization":
                organization_id = filter_result["org_id"]
            elif filter_result["type"] == "organizations":
                # Build OR conditions for multiple orgs
                or_conditions = [f"organization_id.eq.{org_id}" for org_id in filter_result["org_ids"]]
                organization_id = None
            elif filter_result["type"] == "user":
                user_id = user_id  # Use user filter
                organization_id = None

        # Fetch from repository
        templates = TemplateBaseRepository.get_templates_titles(
            client,
            organization_id=organization_id,
            folder_ids=folder_ids,
            published=published,
            user_id=user_id if not or_conditions else None,
            or_conditions=or_conditions,
            limit=limit,
            offset=offset
        )

        # Localize and convert to DTOs
        return [
            TemplateTitleResponseDTO(**localize_object(template.__dict__, locale, ["title"]))
            for template in templates
        ]
