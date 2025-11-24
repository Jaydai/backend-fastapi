"""
Template Service - Business Logic Layer
Handles all template-related operations with permission checking and validation
"""
from supabase import Client
from fastapi import HTTPException, status

from dtos import (
    CreateTemplateDTO,
    UpdateTemplateDTO,
    CreateVersionDTO,
    TemplateVersionResponseDTO,
    TemplateTitleResponseDTO,
    TemplateResponseDTO,
    UsageResponseDTO,
    TemplateCountsResponseDTO,
    TemplateMetadataDTO,
    VersionContentDTO,
)
from repositories import TemplateRepository, TemplateVersionRepository, PermissionRepository
from services import PermissionService
from domains.enums import PermissionEnum
from mappers.template_mapper import TemplateMapper
from utils import localize_object


class TemplateService:
    # ==================== TEMPLATE OPERATIONS ====================

    @staticmethod
    def get_templates_titles(
        client: Client,
        locale: str = "en",
        user_id: str | None = None,
        organization_id: str | None = None,
        folder_id: str | None = None,
        published_only: bool | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[TemplateTitleResponseDTO]:
        """Get template titles with filtering and localization"""
        # SECURITY FIX: Always pass user_id to repository for proper filtering
        # RLS policies at database level provide additional security layer
        filter_user_id = user_id
        filter_org_id = organization_id
        filter_folder_id = folder_id

        templates = TemplateRepository.get_templates_titles(
            client,
            user_id=filter_user_id,
            organization_id=filter_org_id,
            folder_id=filter_folder_id,
            published_only=published_only,
            limit=limit,
            offset=offset
        )

        return [
            TemplateTitleResponseDTO(**localize_object(template.__dict__, locale, ["title"]))
            for template in templates
        ]

    @staticmethod
    def get_template_by_id(
        client: Client,
        template_id: str,
        locale: str = "en"
    ) -> TemplateResponseDTO | None:
        """Get complete template with versions and comments"""
        template = TemplateRepository.get_template_by_id(client, template_id)
        if not template:
            return None

        versions = TemplateVersionRepository.get_versions(client, template_id)
        comments = []  # TODO: Implement comments

        return TemplateMapper.entity_to_response_dto(template, versions, locale)

    @staticmethod
    def get_template_metadata(
        client: Client,
        template_id: str,
        locale: str = "en"
    ) -> TemplateMetadataDTO | None:
        """Get template metadata without content (optimized for initial load)"""
        template = TemplateRepository.get_template_metadata(client, template_id)
        if not template:
            return None

        versions_data = TemplateVersionRepository.get_versions_summary(client, template_id)

        # Convert to DTOs with localization
        from domains.entities import VersionSummary
        versions = [
            VersionSummary(
                id=v.id,
                name=localize_object(v.name, locale),
                slug=v.slug,
                is_current=v.is_current
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

    @staticmethod
    def create_template(
        client: Client,
        user_id: str,
        data: CreateTemplateDTO,
        locale: str = "en"
    ) -> TemplateResponseDTO:
        """Create a new template with initial version"""
        workspace_type = "organization" if data.organization_id else "user"

        title_dict = TemplateMapper.ensure_localized_dict(data.title, locale)
        description_dict = TemplateMapper.ensure_localized_dict(data.description, locale) if data.description else None
        content_dict = TemplateMapper.ensure_localized_dict(data.content, locale)

        template = TemplateRepository.create_template(
            client,
            user_id,
            title_dict,
            description_dict,
            data.folder_id,
            data.organization_id,
            data.tags,
            workspace_type
        )

        try:
            version = TemplateVersionRepository.create_version(
                client,
                template.id,
                user_id,
                content_dict,
                name="1.0",
                change_notes=None,
                status="draft" if workspace_type != "user" else "published",
                optimized_for=data.optimized_for
            )

            TemplateRepository.update_template(client, template.id, current_version_id=version.id)

        except Exception as e:
            TemplateRepository.delete_template(client, template.id)
            raise Exception(f"Failed to create template version: {str(e)}")

        return TemplateService.get_template_by_id(client, template.id, locale)

    @staticmethod
    def update_template(
        client: Client,
        template_id: str,
        data: UpdateTemplateDTO,
        locale: str = "en"
    ) -> TemplateResponseDTO | None:
        """Update template metadata and optionally create/update version"""
        template = TemplateRepository.get_template_by_id(client, template_id)
        if not template:
            return None

        title_dict = TemplateMapper.ensure_localized_dict(data.title, locale) if data.title else None
        description_dict = TemplateMapper.ensure_localized_dict(data.description, locale) if data.description else None

        content_updated = data.content is not None
        status_updated = data.status is not None

        if content_updated or status_updated:
            if data.version_id:
                version_update_data = {}
                if content_updated:
                    version_update_data["content"] = TemplateMapper.ensure_localized_dict(data.content, locale)
                if status_updated:
                    version_update_data["status"] = data.status

                version = TemplateVersionRepository.update_version(
                    client,
                    data.version_id,
                    template_id,
                    content=version_update_data.get("content"),
                    status=version_update_data.get("status")
                )

                if not version:
                    return None
            else:
                if content_updated:
                    content_dict = TemplateMapper.ensure_localized_dict(data.content, locale)
                    version = TemplateVersionRepository.create_version(
                        client,
                        template_id,
                        template.user_id,
                        content_dict,
                        change_notes=None,
                        status=data.status or "draft"
                    )
                    TemplateRepository.update_template(
                        client,
                        template_id,
                        title=title_dict,
                        description=description_dict,
                        folder_id=data.folder_id,
                        tags=data.tags,
                        current_version_id=version.id
                    )

        if not content_updated and not status_updated:
            TemplateRepository.update_template(
                client,
                template_id,
                title=title_dict,
                description=description_dict,
                folder_id=data.folder_id,
                tags=data.tags,
                current_version_id=data.current_version_id
            )

        if data.is_pinned is not None:
            TemplateRepository.update_pinned_status(client, template.user_id, template_id, data.is_pinned)

        return TemplateService.get_template_by_id(client, template_id, locale)

    @staticmethod
    def delete_template(client: Client, template_id: str) -> bool:
        """Delete a template"""
        return TemplateRepository.delete_template(client, template_id)

    @staticmethod
    def increment_usage(client: Client, template_id: str) -> UsageResponseDTO:
        """Increment usage count for a template"""
        new_count = TemplateRepository.increment_usage(client, template_id)
        return UsageResponseDTO(usage_count=new_count)

    @staticmethod
    def search_templates(
        client: Client,
        user_id: str,
        query: str,
        locale: str = "en",
        tags: list[str] | None = None,
        include_public: bool = True,
        limit: int = 50,
        offset: int = 0
    ) -> list[TemplateTitleResponseDTO]:
        """Search templates by query and tags"""
        templates = TemplateRepository.search_templates(
            client,
            user_id,
            query,
            tags,
            include_public,
            limit,
            offset
        )
        return [TemplateMapper.entity_to_list_item_dto(t, locale) for t in templates]

    @staticmethod
    def get_templates_counts(client: Client, user_id: str) -> TemplateCountsResponseDTO:
        """Get template counts for user and all their organizations"""
        user_counts = TemplateRepository.get_user_templates_count(client, user_id)
        user_all_roles = PermissionRepository.get_user_all_roles(client, user_id)

        organization_counts = {}
        for role in user_all_roles:
            if role.organization_id:
                organization_counts[role.organization_id] = TemplateRepository.get_organization_templates_count(
                    client, role.organization_id
                )

        return TemplateCountsResponseDTO(
            user_counts=user_counts,
            organization_counts=organization_counts
        )

    # ==================== VERSION OPERATIONS ====================

    @staticmethod
    def get_versions(
        client: Client,
        template_id: str,
        locale: str = "en"
    ) -> list[TemplateVersionResponseDTO]:
        """Get all versions for a template"""
        versions = TemplateVersionRepository.get_versions(client, template_id)
        return [TemplateMapper.version_entity_to_dto(v, locale) for v in versions]

    @staticmethod
    def get_version_by_slug(
        client: Client,
        template_id: str,
        slug: str,
        locale: str = "en"
    ) -> VersionContentDTO | None:
        """Get full version content by slug"""
        version = TemplateVersionRepository.get_version_by_slug(client, template_id, slug)
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

    @staticmethod
    def create_version(
        client: Client,
        template_id: str,
        user_id: str,
        data: CreateVersionDTO,
        locale: str = "en"
    ) -> TemplateVersionResponseDTO:
        """Create a new version for a template"""
        if data.copy_from_version_id:
            source_version = TemplateVersionRepository.get_version_by_id(client, data.copy_from_version_id)
            if not source_version:
                return None
            content_dict = source_version.content
        else:
            content_dict = TemplateMapper.ensure_localized_dict(data.content, locale) if data.content else {locale: ""}

        change_notes_dict = TemplateMapper.ensure_localized_dict(data.change_notes, locale) if data.change_notes else None

        version = TemplateVersionRepository.create_version(
            client,
            template_id,
            user_id,
            content_dict,
            name=data.name,
            change_notes=change_notes_dict,
            status=data.status or "draft",
            optimized_for=data.optimized_for
        )

        return TemplateMapper.version_entity_to_dto(version, locale)

    @staticmethod
    def update_version(
        client: Client,
        user_id: str,
        template_id: str,
        version_id: int,
        content: dict[str, str] | None = None,
        change_notes: dict[str, str] | None = None,
        status_val: str | None = None,
        is_current: bool | None = None,
        is_published: bool | None = None,
        optimized_for: list[str] | None = None,
        locale: str = "en"
    ) -> TemplateVersionResponseDTO:
        """Update a template version with permission checking"""
        # Check if version exists and belongs to this template
        version = TemplateVersionRepository.get_version_by_id(client, version_id)
        if not version or version.template_id != template_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template version not found"
            )

        # Check if user has permission (template owner or organization admin)
        template = TemplateRepository.get_template_by_id(client, template_id)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template not found"
            )

        # Check if user is the template owner
        has_permission = template.user_id == user_id

        # If template belongs to an organization, check organization permissions
        if not has_permission and template.organization_id:
            has_permission = PermissionService.user_has_permission_in_organization(
                client,
                user_id,
                PermissionEnum.TEMPLATE_UPDATE,
                template.organization_id
            )

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to update this template version"
            )

        # Build update data, excluding None values
        update_dict = {}
        if content is not None:
            update_dict["content"] = content
        if change_notes is not None:
            update_dict["change_notes"] = change_notes
        if status_val is not None:
            update_dict["status"] = status_val
        if is_current is not None:
            update_dict["is_current"] = is_current
        if is_published is not None:
            update_dict["is_published"] = is_published
        if optimized_for is not None:
            update_dict["optimized_for"] = optimized_for

        if not update_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No update data provided"
            )

        # If setting as current, handle it through set_default_version
        if update_dict.get("is_current") is True:
            TemplateVersionRepository.set_default_version(client, template_id, version_id)
            # Remove from update_dict as it's already handled
            del update_dict["is_current"]

        # Perform the update if there are remaining fields
        if update_dict:
            updated_version = TemplateVersionRepository.update_version(
                client,
                version_id,
                template_id,
                content=update_dict.get("content"),
                status=update_dict.get("status")
            )
        else:
            # Just refetch the version
            updated_version = TemplateVersionRepository.get_version_by_id(client, version_id)

        if not updated_version:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update version"
            )

        return TemplateMapper.version_entity_to_dto(updated_version, locale)

    @staticmethod
    def set_default_version(
        client: Client,
        user_id: str,
        template_id: str,
        version_id: int
    ) -> dict:
        """Set a version as the default/current version"""
        # Check if version exists and belongs to this template
        version = TemplateVersionRepository.get_version_by_id(client, version_id)
        if not version or version.template_id != template_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template version not found"
            )

        # Check if user has permission (template owner or organization admin)
        template = TemplateRepository.get_template_by_id(client, template_id)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template not found"
            )

        # Check if user is the template owner
        has_permission = template.user_id == user_id

        # If template belongs to an organization, check organization permissions
        if not has_permission and template.organization_id:
            has_permission = PermissionService.user_has_permission_in_organization(
                client,
                user_id,
                PermissionEnum.TEMPLATE_UPDATE,
                template.organization_id
            )

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to update this template"
            )

        # Perform the update
        TemplateVersionRepository.set_default_version(client, template_id, version_id)

        return {
            "success": True,
            "message": f"Version {version.name} set as default",
            "data": {
                "template_id": template_id,
                "current_version_id": version_id
            }
        }

    @staticmethod
    def delete_version(
        client: Client,
        user_id: str,
        template_id: str,
        version_id: int
    ) -> dict:
        """Delete a template version with permission checking"""
        # Check if version exists and belongs to this template
        version = TemplateVersionRepository.get_version_by_id(client, version_id)
        if not version or version.template_id != template_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template version not found"
            )

        # Prevent deletion of the current/default version
        if version.is_current:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete the current version. Please set another version as current first."
            )

        # Check if user has permission (template owner or organization admin)
        template = TemplateRepository.get_template_by_id(client, template_id)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template not found"
            )

        # Check if user is the template owner
        has_permission = template.user_id == user_id

        # If template belongs to an organization, check organization permissions
        if not has_permission and template.organization_id:
            has_permission = PermissionService.user_has_permission_in_organization(
                client,
                user_id,
                PermissionEnum.TEMPLATE_DELETE,
                template.organization_id
            )

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this template version"
            )

        # Perform the deletion
        success = TemplateVersionRepository.delete_version(client, template_id, version_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete template version"
            )

        return {
            "success": True,
            "message": f"Version {version.name} deleted successfully",
            "deleted_version_id": version_id
        }
