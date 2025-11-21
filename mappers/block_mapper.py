from domains.entities import Block
from dtos import BlockResponseDTO

class BlockMapper:
    @staticmethod
    def localize_string(value: dict[str, str] | str | None, locale: str = "en") -> str:
        if value is None:
            return ""
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            return value.get(locale) or value.get("custom") or value.get("en") or list(value.values())[0] if value else ""
        return ""

    @staticmethod
    def ensure_localized_dict(value: str | None, locale: str = "en") -> dict[str, str]:
        if value is None:
            return {"custom": ""}
        return {"custom": value}

    @staticmethod
    def entity_to_response_dto(block: Block, locale: str = "en") -> BlockResponseDTO:
        return BlockResponseDTO(
            id=block.id,
            type=block.type,
            title=BlockMapper.localize_string(block.title, locale),
            description=BlockMapper.localize_string(block.description, locale) if block.description else None,
            content=BlockMapper.localize_string(block.content, locale),
            published=block.published,
            user_id=block.user_id,
            organization_id=block.organization_id,
            workspace_type=block.workspace_type,
            created_at=block.created_at,
            updated_at=block.updated_at,
            usage_count=block.usage_count
        )
