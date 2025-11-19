from supabase import Client
from dtos import (
    CreateBlockDTO,
    UpdateBlockDTO,
    BlockResponseDTO,
    UpdatePinnedBlocksDTO,
    BlockType
)
from repositories.block_repository import BlockRepository
from mappers.block_mapper import BlockMapper

class BlockService:
    @staticmethod
    def get_blocks(
        client: Client,
        user_id: str,
        locale: str = "en",
        block_type: str | None = None,
        workspace_type: str | None = None,
        organization_id: str | None = None,
        company_id: str | None = None,
        published: bool | None = None,
        search_query: str | None = None
    ) -> list[BlockResponseDTO]:
        blocks = BlockRepository.get_blocks(
            client,
            user_id,
            block_type,
            workspace_type,
            organization_id,
            company_id,
            published,
            search_query
        )

        return [BlockMapper.entity_to_response_dto(b, locale) for b in blocks]

    @staticmethod
    def get_block_by_id(
        client: Client,
        block_id: str,
        locale: str = "en"
    ) -> BlockResponseDTO | None:
        block = BlockRepository.get_block_by_id(client, block_id)
        if not block:
            return None

        return BlockMapper.entity_to_response_dto(block, locale)

    @staticmethod
    def create_block(
        client: Client,
        user_id: str,
        data: CreateBlockDTO,
        locale: str = "en"
    ) -> BlockResponseDTO:
        workspace_type = "user"
        if data.organization_id:
            workspace_type = "organization"
        elif data.company_id:
            workspace_type = "company"

        title_dict = BlockMapper.ensure_localized_dict(data.title, locale)
        description_dict = BlockMapper.ensure_localized_dict(data.description, locale) if data.description else None
        content_dict = BlockMapper.ensure_localized_dict(data.content, locale)

        block = BlockRepository.create_block(
            client,
            user_id,
            data.type.value,
            title_dict,
            description_dict,
            content_dict,
            data.published,
            data.organization_id,
            data.company_id,
            workspace_type
        )

        return BlockMapper.entity_to_response_dto(block, locale)

    @staticmethod
    def update_block(
        client: Client,
        block_id: str,
        data: UpdateBlockDTO,
        locale: str = "en"
    ) -> BlockResponseDTO | None:
        block_type = data.type.value if data.type else None
        title_dict = BlockMapper.ensure_localized_dict(data.title, locale) if data.title else None
        description_dict = BlockMapper.ensure_localized_dict(data.description, locale) if data.description else None
        content_dict = BlockMapper.ensure_localized_dict(data.content, locale) if data.content else None

        block = BlockRepository.update_block(
            client,
            block_id,
            block_type,
            title_dict,
            description_dict,
            content_dict,
            data.published
        )

        if not block:
            return None

        return BlockMapper.entity_to_response_dto(block, locale)

    @staticmethod
    def delete_block(client: Client, block_id: str) -> bool:
        return BlockRepository.delete_block(client, block_id)

    @staticmethod
    def get_block_types() -> list[str]:
        return [bt.value for bt in BlockType]

    @staticmethod
    def get_pinned_blocks(
        client: Client,
        user_id: str,
        locale: str = "en"
    ) -> list[BlockResponseDTO]:
        pinned_ids = BlockRepository.get_pinned_block_ids(client, user_id)

        if not pinned_ids:
            return []

        blocks = []
        for block_id in pinned_ids:
            block = BlockRepository.get_block_by_id(client, block_id)
            if block:
                blocks.append(block)

        return [BlockMapper.entity_to_response_dto(b, locale) for b in blocks]

    @staticmethod
    def update_pinned_blocks(
        client: Client,
        user_id: str,
        data: UpdatePinnedBlocksDTO
    ) -> dict:
        for block_id in data.block_ids:
            block = BlockRepository.get_block_by_id(client, block_id)
            if not block:
                raise ValueError(f"Block {block_id} not found")

        pinned_ids = BlockRepository.update_pinned_blocks(client, user_id, data.block_ids)
        return {"pinned_blocks": pinned_ids}
