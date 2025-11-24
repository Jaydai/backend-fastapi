"""
Enrichment Service - Business logic layer (REFACTORED with utilities)
Orchestrates classification, risk assessment, and data persistence
"""

import asyncio
import logging

from dtos.enrichment_dto import (
    ChatEnrichmentRequestDTO,
    ChatEnrichmentResponseDTO,
    EnrichMessageRequestDTO,
    EnrichMessageResponseDTO,
    QualityMetricsDTO,
    RatedChatDTO,
    RiskCategoryDetailDTO,
    RiskyMessageDTO,
)
from repositories.enrichment_repository import EnrichmentRepository
from services.enrichment import classification_service, risk_assessment_service
from supabase import Client
from utils.enrichment import (
    classification_to_enriched_chat,
    classification_to_response_dto,
    risk_assessment_to_enriched_message,
    risk_assessment_to_response_dto,
    truncate_message,
)

logger = logging.getLogger(__name__)


class EnrichmentService:
    """Business logic for enrichment operations"""

    @staticmethod
    def enrich_chat(
        client: Client,
        user_id: Optional[str],
        request: ChatEnrichmentRequestDTO
    ) -> ChatEnrichmentResponseDTO:
        """Enrich a single chat with classification and quality assessment"""
        # Truncate messages for AI processing
        user_message = truncate_message(request.user_message)
        assistant_response = truncate_message(request.assistant_response) if request.assistant_response else None

        # Call classification service
        classification_result = classification_service.classify_chat(user_message, assistant_response)

        # Use user_id from request payload if available (ChatEnrichmentBatchItemDTO), otherwise from auth
        effective_user_id = getattr(request, 'user_id', None) or user_id

        # Convert to entity and save (only if user_id is provided)
        if effective_user_id:
            enriched_chat = classification_to_enriched_chat(classification_result, request)
            EnrichmentRepository.save_enriched_chat(client, effective_user_id, enriched_chat)

        # Return response DTO
        return classification_to_response_dto(classification_result)

    @staticmethod
    async def enrich_chat_batch(
        client: Client,
        user_id: Optional[str],
        requests: list[ChatEnrichmentRequestDTO]
    ) -> list[dict]:
        """Enrich multiple chats in parallel"""
        tasks = [EnrichmentService._enrich_chat_async(client, user_id, req) for req in requests]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Format results with success/error indicators
        return [
            {
                "success": not isinstance(result, Exception),
                "data": result if not isinstance(result, Exception) else None,
                "error": str(result) if isinstance(result, Exception) else None,
                "chat_provider_id": requests[i].chat_provider_id,
            }
            for i, result in enumerate(results)
        ]

    @staticmethod
    async def _enrich_chat_async(client: Client, user_id: Optional[str], request: ChatEnrichmentRequestDTO):
        """Async wrapper for enrich_chat"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, EnrichmentService.enrich_chat, client, user_id, request)

    @staticmethod
    def enrich_message(
        client: Client,
        user_id: Optional[str],
        request: EnrichMessageRequestDTO
    ) -> EnrichMessageResponseDTO:
        """Enrich a single message with risk assessment"""
        # Call risk assessment service
        risk_result = risk_assessment_service.assess_message_risk(
            content=request.content, role=request.role, context=request.context
        )

        # Use user_id from request payload if available, otherwise from auth
        effective_user_id = request.user_id or user_id

        # Convert to entity and save (only if user_id is provided)
        if effective_user_id:
            enriched_message = risk_assessment_to_enriched_message(risk_result, request)
            EnrichmentRepository.save_enriched_message(client, effective_user_id, enriched_message)

        # Return response DTO
        return risk_assessment_to_response_dto(risk_result)

    @staticmethod
    def enrich_message_batch(
        client: Client,
        user_id: Optional[str],
        requests: list[EnrichMessageRequestDTO]
    ) -> list[dict]:
        """Enrich multiple messages sequentially"""
        results = []

        for request in requests:
            try:
                result = EnrichmentService.enrich_message(client, user_id, request)
                results.append(
                    {"success": True, "data": result, "error": None, "message_provider_id": request.message_provider_id}
                )
            except Exception as e:
                logger.error(f"Failed to enrich message {request.message_provider_id}: {e}")
                logger.error(f"Exception type: {type(e).__name__}, Exception args: {e.args}")
                import traceback
                logger.error(f"Traceback: {traceback.format_exc()}")
                results.append({
                    "success": False,
                    "data": None,
                    "error": str(e),
                    "message_provider_id": request.message_provider_id
                })

        return results

    @staticmethod
    def get_risky_messages(
        client: Client, user_id: str, days: int, min_risk_level: str, limit: int
    ) -> list[RiskyMessageDTO]:
        """Get risky messages for a user"""
        enriched_messages = EnrichmentRepository.get_risky_messages(client, user_id, days, min_risk_level, limit)

        # Transform to DTOs
        return [
            RiskyMessageDTO(
                message_provider_id=msg.message_provider_id,
                risk_level=msg.overall_risk_level,
                risk_score=msg.overall_risk_score,
                risk_categories={
                    name: RiskCategoryDetailDTO(
                        level=cat.level, score=cat.score, detected=cat.detected, details=cat.details
                    )
                    for name, cat in msg.risk_categories.items()
                },
                risk_summary=msg.risk_summary,
                content_preview="[Content preview]",  # TODO: Join with messages table
                created_at=msg.created_at,
                user_whitelist=msg.user_whitelist,
            )
            for msg in enriched_messages
        ]

    @staticmethod
    def get_rated_chats(
        client: Client,
        user_id: str,
        days: int,
        min_quality: float | None,
        max_quality: float | None,
        order_by: str,
        limit: int,
    ) -> list[RatedChatDTO]:
        """Get rated chats for a user"""
        enriched_chats = EnrichmentRepository.get_rated_chats(
            client, user_id, days, min_quality, max_quality, order_by, limit
        )

        # Transform to DTOs
        return [
            RatedChatDTO(
                chat_provider_id=chat.chat_provider_id,
                quality_score=chat.quality_metrics.quality_score if chat.quality_metrics else 0,
                theme=chat.theme or "unknown",
                intent=chat.intent or "unknown",
                quality_metrics=QualityMetricsDTO(
                    quality_score=chat.quality_metrics.quality_score if chat.quality_metrics else 0,
                    clarity_score=chat.quality_metrics.clarity_score if chat.quality_metrics else 0,
                    context_score=chat.quality_metrics.context_score if chat.quality_metrics else 0,
                    specificity_score=chat.quality_metrics.specificity_score if chat.quality_metrics else 0,
                    actionability_score=chat.quality_metrics.actionability_score if chat.quality_metrics else 0,
                ),
                content_preview="[Content preview]",  # TODO: Join with messages table
                created_at=chat.created_at,
                user_override_quality=chat.user_override_quality,
                user_quality_score=chat.user_quality_score,
            )
            for chat in enriched_chats
        ]

    @staticmethod
    def whitelist_message(client: Client, user_id: str, message_provider_id: str) -> bool:
        """Mark a message as whitelisted"""
        return EnrichmentRepository.whitelist_message(client, user_id, message_provider_id)

    @staticmethod
    def override_chat_quality(client: Client, user_id: str, chat_provider_id: str, quality_score: int) -> bool:
        """Override chat quality score"""
        return EnrichmentRepository.override_chat_quality(client, user_id, chat_provider_id, quality_score)
