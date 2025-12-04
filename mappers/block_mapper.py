from domains.entities import Block, BlockSummary
from dtos import BlockResponseDTO, BlockSummaryResponseDTO
from services.locale_service import LocaleService


class BlockMapper:
    @staticmethod
    def entity_to_response_dto(block: Block, locale: str = LocaleService.DEFAULT_LOCALE) -> BlockResponseDTO:
        return BlockResponseDTO(
            id=block.id,
            type=block.type,
            title=LocaleService.localize_string(block.title, locale),
            description=LocaleService.localize_string(block.description, locale) if block.description else None,
            content=LocaleService.localize_string(block.content, locale),
            published=block.published,
            user_id=block.user_id,
            organization_id=block.organization_id,
            workspace_type=block.workspace_type,
            created_at=block.created_at,
            updated_at=block.updated_at,
            usage_count=block.usage_count,
        )

    @staticmethod
    def entity_to_summary_dto(block: BlockSummary, locale: str = LocaleService.DEFAULT_LOCALE) -> BlockSummaryResponseDTO:
        return BlockSummaryResponseDTO(
            id=block.id,
            title=LocaleService.localize_string(block.title, locale),
            type=block.type,
            description=LocaleService.localize_string(block.description, locale) if block.description else None,
            usage_count=block.usage_count,
            organization_image_url=block.organization_image_url,
            organization_id=block.organization_id,
        )
