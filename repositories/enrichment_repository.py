"""
Repository for enrichment data access
Database operations only - no business logic
"""
import logging
from supabase import Client
from domains.entities.enrichment_entities import EnrichedChat, EnrichedMessage, QualityMetrics, FeedbackDetail, RiskCategory, RiskIssue
from typing import Optional

logger = logging.getLogger(__name__)


class EnrichmentRepository:

    @staticmethod
    def save_enriched_chat(client: Client, user_id: str, enriched_chat: EnrichedChat) -> Optional[EnrichedChat]:
        """
        Save enriched chat to database
        Returns None if chat already exists (duplicate), otherwise returns the saved chat
        """
        # Check if already exists
        existing = client.table("enriched_chats") \
            .select("id") \
            .eq("user_id", user_id) \
            .eq("chat_provider_id", enriched_chat.chat_provider_id) \
            .execute()

        if existing.data:
            logger.info(f"Chat {enriched_chat.chat_provider_id} already enriched")
            return None

        # Prepare data for insert
        data = {
            "user_id": user_id,
            "chat_id": enriched_chat.chat_id,
            "chat_provider_id": enriched_chat.chat_provider_id,
            "message_provider_id": enriched_chat.message_provider_id,
            "is_work_related": enriched_chat.is_work_related,
            "theme": enriched_chat.theme,
            "intent": enriched_chat.intent,
            "raw_response": enriched_chat.raw_response,
            "processing_time_ms": enriched_chat.processing_time_ms,
            "model_used": enriched_chat.model_used
        }

        # Add quality metrics if present
        if enriched_chat.quality_metrics:
            data.update({
                "quality_score": enriched_chat.quality_metrics.quality_score,
                "clarity_score": enriched_chat.quality_metrics.clarity_score,
                "context_score": enriched_chat.quality_metrics.context_score,
                "specificity_score": enriched_chat.quality_metrics.specificity_score,
                "actionability_score": enriched_chat.quality_metrics.actionability_score
            })

        # Add feedback if present
        if enriched_chat.feedback:
            data.update({
                "feedback_summary": enriched_chat.feedback.summary,
                "feedback_strengths": enriched_chat.feedback.strengths,
                "feedback_improvements": enriched_chat.feedback.improvements,
                "improved_prompt_example": enriched_chat.feedback.improved_prompt_example
            })

        response = client.table("enriched_chats").insert(data).execute()
        print("response🙏🏻🙏🏻🙏🏻", response)

        if not response.data:
            return None

        # Map back to entity
        row = response.data[0]
        return EnrichmentRepository._map_chat_row_to_entity(row)

    @staticmethod
    def save_enriched_message(client: Client, user_id: str, enriched_message: EnrichedMessage) -> Optional[EnrichedMessage]:
        """
        Save enriched message to database
        Returns None if message already exists (duplicate), otherwise returns the saved message
        """
        # Check if already exists
        existing = client.table("enriched_messages") \
            .select("id") \
            .eq("user_id", user_id) \
            .eq("message_provider_id", enriched_message.message_provider_id) \
            .execute()

        if existing.data:
            logger.info(f"Message {enriched_message.message_provider_id} already enriched")
            return None

        # Prepare risk categories for JSON storage
        risk_categories_json = {}
        for category_name, category_detail in enriched_message.risk_categories.items():
            risk_categories_json[category_name] = {
                "level": category_detail.level,
                "score": category_detail.score,
                "detected": category_detail.detected,
                "details": category_detail.details
            }

        # Prepare detected issues for JSON storage
        detected_issues_json = []
        for issue in enriched_message.detected_issues:
            detected_issues_json.append({
                "category": issue.category,
                "severity": issue.severity,
                "description": issue.description,
                "details": issue.details
            })

        data = {
            "user_id": user_id,
            "message_provider_id": enriched_message.message_provider_id,
            "overall_risk_level": enriched_message.overall_risk_level,
            "overall_risk_score": enriched_message.overall_risk_score,
            "risk_categories": risk_categories_json,
            "risk_summary": enriched_message.risk_summary,
            "detected_issues": detected_issues_json,
            "user_whitelist": enriched_message.user_whitelist
        }

        response = client.table("enriched_messages").insert(data).execute()

        if not response.data:
            return None

        row = response.data[0]
        return EnrichmentRepository._map_message_row_to_entity(row)

    @staticmethod
    def get_enriched_chat(client: Client, user_id: str, chat_provider_id: str) -> Optional[EnrichedChat]:
        """Retrieve enriched chat by chat_provider_id"""
        response = client.table("enriched_chats") \
            .select("*") \
            .eq("user_id", user_id) \
            .eq("chat_provider_id", chat_provider_id) \
            .execute()

        if not response.data:
            return None

        return EnrichmentRepository._map_chat_row_to_entity(response.data[0])

    @staticmethod
    def get_enriched_message(client: Client, user_id: str, message_provider_id: str) -> Optional[EnrichedMessage]:
        """Retrieve enriched message by message_provider_id"""
        response = client.table("enriched_messages") \
            .select("*") \
            .eq("user_id", user_id) \
            .eq("message_provider_id", message_provider_id) \
            .execute()

        if not response.data:
            return None

        return EnrichmentRepository._map_message_row_to_entity(response.data[0])

    @staticmethod
    def get_risky_messages(
        client: Client,
        user_id: str,
        days: int,
        min_risk_level: str,
        limit: int
    ) -> list[EnrichedMessage]:
        """Get risky messages for a user within date range"""
        from datetime import datetime, timedelta

        cutoff_date = datetime.now() - timedelta(days=days)

        # Risk level hierarchy
        risk_hierarchy = {
            "critical": ["critical"],
            "high": ["critical", "high"],
            "medium": ["critical", "high", "medium"],
            "low": ["critical", "high", "medium", "low"]
        }

        risk_levels = risk_hierarchy.get(min_risk_level, ["critical", "high", "medium"])

        response = client.table("enriched_messages") \
            .select("*") \
            .eq("user_id", user_id) \
            .in_("overall_risk_level", risk_levels) \
            .eq("user_whitelist", False) \
            .gte("created_at", cutoff_date.isoformat()) \
            .order("overall_risk_score", desc=True) \
            .limit(limit) \
            .execute()

        if not response.data:
            return []

        return [EnrichmentRepository._map_message_row_to_entity(row) for row in response.data]

    @staticmethod
    def get_rated_chats(
        client: Client,
        user_id: str,
        days: int,
        min_quality: Optional[float],
        max_quality: Optional[float],
        order_by: str,
        limit: int
    ) -> list[EnrichedChat]:
        """Get rated chats for a user within date range"""
        from datetime import datetime, timedelta

        cutoff_date = datetime.now() - timedelta(days=days)

        query = client.table("enriched_chats") \
            .select("*") \
            .eq("user_id", user_id) \
            .gte("created_at", cutoff_date.isoformat())

        if min_quality is not None:
            query = query.gte("quality_score", min_quality)

        if max_quality is not None:
            query = query.lte("quality_score", max_quality)

        # Order by
        if order_by == "quality_asc":
            query = query.order("quality_score", desc=False)
        elif order_by == "quality_desc":
            query = query.order("quality_score", desc=True)
        elif order_by == "recent":
            query = query.order("created_at", desc=True)

        query = query.limit(limit)
        response = query.execute()

        if not response.data:
            return []

        return [EnrichmentRepository._map_chat_row_to_entity(row) for row in response.data]

    @staticmethod
    def whitelist_message(client: Client, user_id: str, message_provider_id: str) -> bool:
        """Mark a message as whitelisted (not risky)"""
        response = client.table("enriched_messages") \
            .update({"user_whitelist": True}) \
            .eq("user_id", user_id) \
            .eq("message_provider_id", message_provider_id) \
            .execute()

        return len(response.data) > 0

    @staticmethod
    def override_chat_quality(client: Client, user_id: str, chat_provider_id: str, quality_score: int) -> bool:
        """Override chat quality score with user assessment"""
        response = client.table("enriched_chats") \
            .update({
                "user_override_quality": True,
                "user_quality_score": quality_score
            }) \
            .eq("user_id", user_id) \
            .eq("chat_provider_id", chat_provider_id) \
            .execute()

        return len(response.data) > 0

    # Helper methods for mapping DB rows to entities

    @staticmethod
    def _map_chat_row_to_entity(row: dict) -> EnrichedChat:
        """Map database row to EnrichedChat entity"""
        quality_metrics = None
        if row.get("quality_score") is not None:
            quality_metrics = QualityMetrics(
                quality_score=row.get("quality_score", 0),
                clarity_score=row.get("clarity_score", 0),
                context_score=row.get("context_score", 0),
                specificity_score=row.get("specificity_score", 0),
                actionability_score=row.get("actionability_score", 0)
            )

        feedback = None
        if row.get("feedback_summary"):
            feedback = FeedbackDetail(
                summary=row["feedback_summary"],
                strengths=row.get("feedback_strengths", []),
                improvements=row.get("feedback_improvements", []),
                improved_prompt_example=row.get("improved_prompt_example")
            )

        return EnrichedChat(
            id=row.get("id"),
            created_at=row.get("created_at"),
            user_id=row.get("user_id"),
            chat_id=row.get("chat_id"),
            chat_provider_id=row.get("chat_provider_id"),
            message_provider_id=row.get("message_provider_id"),
            is_work_related=row.get("is_work_related", False),
            theme=row.get("theme"),
            intent=row.get("intent"),
            quality_metrics=quality_metrics,
            feedback=feedback,
            raw_response=row.get("raw_response"),
            processing_time_ms=row.get("processing_time_ms"),
            model_used=row.get("model_used"),
            user_override_quality=row.get("user_override_quality", False),
            user_quality_score=row.get("user_quality_score")
        )

    @staticmethod
    def _map_message_row_to_entity(row: dict) -> EnrichedMessage:
        """Map database row to EnrichedMessage entity"""
        # Parse risk categories from JSON
        risk_categories = {}
        if row.get("risk_categories"):
            for category_name, category_data in row["risk_categories"].items():
                risk_categories[category_name] = RiskCategory(
                    level=category_data.get("level", "none"),
                    score=category_data.get("score", 0.0),
                    detected=category_data.get("detected", False),
                    details=category_data.get("details")
                )

        # Parse detected issues from JSON
        detected_issues = []
        if row.get("detected_issues"):
            for issue_data in row["detected_issues"]:
                detected_issues.append(RiskIssue(
                    category=issue_data.get("category", ""),
                    severity=issue_data.get("severity", "low"),
                    description=issue_data.get("description", ""),
                    details=issue_data.get("details")
                ))

        return EnrichedMessage(
            id=row.get("id"),
            created_at=row.get("created_at"),
            user_id=row.get("user_id"),
            message_provider_id=row.get("message_provider_id"),
            overall_risk_level=row.get("overall_risk_level", "none"),
            overall_risk_score=row.get("overall_risk_score", 0.0),
            risk_categories=risk_categories,
            risk_summary=row.get("risk_summary", []),
            detected_issues=detected_issues,
            user_whitelist=row.get("user_whitelist", False)
        )


