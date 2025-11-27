from domains.entities import Folder, Template
from dtos import FolderResponseDTO, FolderWithItemsDTO
from services.locale_service import LocaleService

class FolderMapper:
    @staticmethod
    def entity_to_response_dto(folder: Folder, locale: str = LocaleService.DEFAULT_LOCALE) -> FolderResponseDTO:
        return FolderResponseDTO(
            id=folder.id,
            title=LocaleService.localize_string(folder.title, locale),
            description=LocaleService.localize_string(folder.description, locale) if folder.description else None,
            user_id=folder.user_id,
            organization_id=folder.organization_id,
            parent_folder_id=folder.parent_folder_id,
            workspace_type=folder.workspace_type,
            created_at=folder.created_at,
            updated_at=folder.updated_at
        )

    @staticmethod
    def folder_with_items_to_dto(
        folders: list[Folder],
        templates: list[Template],
        locale: str = LocaleService.DEFAULT_LOCALE,
        total_count: int = 0,
        has_more: bool = False
    ) -> FolderWithItemsDTO:
        from mappers.template_mapper import TemplateMapper

        folder_dtos = [FolderMapper.entity_to_response_dto(f, locale) for f in folders]
        template_dtos = [TemplateMapper.entity_to_list_item_dto(t, locale) for t in templates]

        return FolderWithItemsDTO(
            folders=folder_dtos,
            templates=template_dtos,
            total_count=total_count,
            has_more=has_more
        )
