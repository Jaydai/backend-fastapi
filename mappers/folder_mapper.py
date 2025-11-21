from domains.entities import Folder, Template
from dtos import FolderResponseDTO, FolderWithItemsDTO

class FolderMapper:
    @staticmethod
    def localize_string(value: dict[str, str] | str | None, locale: str = "en") -> str:
        if value is None:
            return ""
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            return value.get(locale) or value.get("en") or list(value.values())[0] if value else ""
        return ""

    @staticmethod
    def ensure_localized_dict(value: str | None, locale: str = "en") -> dict[str, str]:
        if value is None:
            return {locale: ""}
        return {locale: value}

    @staticmethod
    def entity_to_response_dto(folder: Folder, locale: str = "en") -> FolderResponseDTO:
        return FolderResponseDTO(
            id=folder.id,
            title=FolderMapper.localize_string(folder.title, locale),
            description=FolderMapper.localize_string(folder.description, locale) if folder.description else None,
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
        locale: str = "en"
    ) -> FolderWithItemsDTO:
        from mappers.template_mapper import TemplateMapper

        folder_dtos = [FolderMapper.entity_to_response_dto(f, locale) for f in folders]
        template_dtos = [TemplateMapper.entity_to_list_item_dto(t, locale) for t in templates]

        return FolderWithItemsDTO(
            folders=folder_dtos,
            templates=template_dtos
        )
