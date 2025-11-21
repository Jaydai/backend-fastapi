"""
Repository for audit data access with async parallel queries
Database operations only - no business logic
"""
import logging
from supabase import Client
from datetime import datetime, timedelta
from typing import Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


class AuditRepository:
    """
    Repository for organization audit queries
    Uses async execution for performance optimization
    """

    @staticmethod
    def get_organization_member_ids(client: Client, organization_id: str) -> list[str]:
        """Get all user IDs for organization members"""
        response = client.table("users_metadata") \
            .select("user_id") \
            .contains("organization_ids", [organization_id]) \
            .execute()

        if not response.data:
            return []

        return [row["user_id"] for row in response.data]

    @staticmethod
    async def get_quality_stats_async(
        client: Client,
        user_ids: list[str],
        start_date: datetime,
        end_date: datetime
    ) -> dict:
        """Get quality statistics with trend comparison (async)"""
        loop = asyncio.get_event_loop()

        def _fetch():
            # Current period stats
            current_response = client.table("enriched_chats") \
                .select("quality_score, clarity_score, context_score, specificity_score, actionability_score") \
                .in_("user_id", user_ids) \
                .gte("created_at", start_date.isoformat()) \
                .lte("created_at", end_date.isoformat()) \
                .execute()

            # Previous period for trend (7 days before start_date)
            trend_start = start_date - timedelta(days=7)
            trend_end = start_date

            trend_response = client.table("enriched_chats") \
                .select("quality_score") \
                .in_("user_id", user_ids) \
                .gte("created_at", trend_start.isoformat()) \
                .lt("created_at", trend_end.isoformat()) \
                .execute()

            return {
                "current": current_response.data,
                "trend": trend_response.data
            }

        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, _fetch)

        return result

    @staticmethod
    async def get_risk_stats_async(
        client: Client,
        user_ids: list[str],
        start_date: datetime,
        end_date: datetime
    ) -> dict:
        """Get risk statistics (async)"""
        loop = asyncio.get_event_loop()

        def _fetch():
            response = client.table("enriched_messages") \
                .select("overall_risk_level, overall_risk_score, detected_issues") \
                .in_("user_id", user_ids) \
                .gte("created_at", start_date.isoformat()) \
                .lte("created_at", end_date.isoformat()) \
                .execute()

            return response.data

        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, _fetch)

        return result

    @staticmethod
    async def get_usage_stats_async(
        client: Client,
        user_ids: list[str],
        start_date: datetime,
        end_date: datetime
    ) -> dict:
        """Get usage statistics (async)"""
        loop = asyncio.get_event_loop()

        def _fetch():
            # Total messages/chats
            messages_response = client.table("messages") \
                .select("id, user_id") \
                .in_("user_id", user_ids) \
                .gte("created_at", start_date.isoformat()) \
                .lte("created_at", end_date.isoformat()) \
                .execute()

            # Work-related stats
            work_response = client.table("enriched_chats") \
                .select("is_work_related") \
                .in_("user_id", user_ids) \
                .gte("created_at", start_date.isoformat()) \
                .lte("created_at", end_date.isoformat()) \
                .execute()

            return {
                "messages": messages_response.data,
                "work_classification": work_response.data
            }

        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, _fetch)

        return result

    @staticmethod
    async def get_theme_stats_async(
        client: Client,
        user_ids: list[str],
        start_date: datetime,
        end_date: datetime
    ) -> dict:
        """Get theme distribution stats with trends (async)"""
        loop = asyncio.get_event_loop()

        def _fetch():
            # Current period
            current_response = client.table("enriched_chats") \
                .select("theme") \
                .in_("user_id", user_ids) \
                .gte("created_at", start_date.isoformat()) \
                .lte("created_at", end_date.isoformat()) \
                .not_.is_("theme", "null") \
                .execute()

            # Previous period for trend
            trend_start = start_date - timedelta(days=7)
            trend_end = start_date

            trend_response = client.table("enriched_chats") \
                .select("theme") \
                .in_("user_ids", user_ids) \
                .gte("created_at", trend_start.isoformat()) \
                .lt("created_at", trend_end.isoformat()) \
                .not_.is_("theme", "null") \
                .execute()

            return {
                "current": current_response.data,
                "trend": trend_response.data
            }

        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, _fetch)

        return result

    @staticmethod
    async def get_intent_stats_async(
        client: Client,
        user_ids: list[str],
        start_date: datetime,
        end_date: datetime
    ) -> dict:
        """Get intent distribution stats with quality (async)"""
        loop = asyncio.get_event_loop()

        def _fetch():
            response = client.table("enriched_chats") \
                .select("intent, quality_score") \
                .in_("user_id", user_ids) \
                .gte("created_at", start_date.isoformat()) \
                .lte("created_at", end_date.isoformat()) \
                .not_.is_("intent", "null") \
                .execute()

            return response.data

        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, _fetch)

        return result

    @staticmethod
    async def get_top_users_async(
        client: Client,
        user_ids: list[str],
        start_date: datetime,
        end_date: datetime,
        limit: int = 10
    ) -> list[dict]:
        """Get top users by activity with quality and risk metrics (async)"""
        loop = asyncio.get_event_loop()

        def _fetch():
            # Get message counts per user
            messages_response = client.table("messages") \
                .select("user_id") \
                .in_("user_id", user_ids) \
                .gte("created_at", start_date.isoformat()) \
                .lte("created_at", end_date.isoformat()) \
                .execute()

            # Get quality scores per user
            quality_response = client.table("enriched_chats") \
                .select("user_id, quality_score, is_work_related") \
                .in_("user_id", user_ids) \
                .gte("created_at", start_date.isoformat()) \
                .lte("created_at", end_date.isoformat()) \
                .execute()

            # Get risk levels per user
            risk_response = client.table("enriched_messages") \
                .select("user_id, overall_risk_level") \
                .in_("user_id", user_ids) \
                .gte("created_at", start_date.isoformat()) \
                .lte("created_at", end_date.isoformat()) \
                .in_("overall_risk_level", ["high", "critical"]) \
                .execute()

            return {
                "messages": messages_response.data,
                "quality": quality_response.data,
                "risks": risk_response.data
            }

        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, _fetch)

        return result

    @staticmethod
    async def get_top_prompts_async(
        client: Client,
        user_ids: list[str],
        start_date: datetime,
        end_date: datetime,
        limit: int = 10
    ) -> list[dict]:
        """Get highest quality prompts (async)"""
        loop = asyncio.get_event_loop()

        def _fetch():
            # Get top quality chats
            chats_response = client.table("enriched_chats") \
                .select("chat_provider_id, message_provider_id, quality_score, theme, intent, created_at") \
                .in_("user_id", user_ids) \
                .gte("created_at", start_date.isoformat()) \
                .lte("created_at", end_date.isoformat()) \
                .not_.is_("quality_score", "null") \
                .order("quality_score", desc=True) \
                .limit(limit) \
                .execute()

            # Get message content for these chats
            if chats_response.data:
                message_ids = [chat["message_provider_id"] for chat in chats_response.data if chat.get("message_provider_id")]

                if message_ids:
                    messages_response = client.table("messages") \
                        .select("provider_id, content") \
                        .in_("provider_id", message_ids) \
                        .execute()

                    return {
                        "chats": chats_response.data,
                        "messages": messages_response.data
                    }

            return {
                "chats": chats_response.data,
                "messages": []
            }

        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, _fetch)

        return result

    @staticmethod
    async def get_riskiest_prompts_async(
        client: Client,
        user_ids: list[str],
        start_date: datetime,
        end_date: datetime,
        limit: int = 10
    ) -> list[dict]:
        """Get highest risk prompts (async)"""
        loop = asyncio.get_event_loop()

        def _fetch():
            # Get top risk messages
            risks_response = client.table("enriched_messages") \
                .select("message_provider_id, overall_risk_level, overall_risk_score, risk_categories, created_at, user_whitelist") \
                .in_("user_id", user_ids) \
                .gte("created_at", start_date.isoformat()) \
                .lte("created_at", end_date.isoformat()) \
                .in_("overall_risk_level", ["medium", "high", "critical"]) \
                .order("overall_risk_score", desc=True) \
                .limit(limit) \
                .execute()

            # Get message content
            if risks_response.data:
                message_ids = [risk["message_provider_id"] for risk in risks_response.data]

                messages_response = client.table("messages") \
                    .select("provider_id, content") \
                    .in_("provider_id", message_ids) \
                    .execute()

                return {
                    "risks": risks_response.data,
                    "messages": messages_response.data
                }

            return {
                "risks": risks_response.data,
                "messages": []
            }

        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, _fetch)

        return result

    @staticmethod
    async def fetch_all_audit_data_parallel(
        client: Client,
        user_ids: list[str],
        start_date: datetime,
        end_date: datetime
    ) -> dict:
        """
        Fetch all audit data in parallel for maximum performance
        This is the main entry point for audit repository
        """
        # Execute all queries in parallel
        results = await asyncio.gather(
            AuditRepository.get_quality_stats_async(client, user_ids, start_date, end_date),
            AuditRepository.get_risk_stats_async(client, user_ids, start_date, end_date),
            AuditRepository.get_usage_stats_async(client, user_ids, start_date, end_date),
            AuditRepository.get_theme_stats_async(client, user_ids, start_date, end_date),
            AuditRepository.get_intent_stats_async(client, user_ids, start_date, end_date),
            AuditRepository.get_top_users_async(client, user_ids, start_date, end_date),
            AuditRepository.get_top_prompts_async(client, user_ids, start_date, end_date),
            AuditRepository.get_riskiest_prompts_async(client, user_ids, start_date, end_date),
            return_exceptions=True
        )

        # Unpack results
        quality_data, risk_data, usage_data, theme_data, intent_data, top_users_data, top_prompts_data, risky_prompts_data = results

        return {
            "quality": quality_data if not isinstance(quality_data, Exception) else {"current": [], "trend": []},
            "risk": risk_data if not isinstance(risk_data, Exception) else [],
            "usage": usage_data if not isinstance(usage_data, Exception) else {"messages": [], "work_classification": []},
            "themes": theme_data if not isinstance(theme_data, Exception) else {"current": [], "trend": []},
            "intents": intent_data if not isinstance(intent_data, Exception) else [],
            "top_users": top_users_data if not isinstance(top_users_data, Exception) else {},
            "top_prompts": top_prompts_data if not isinstance(top_prompts_data, Exception) else {"chats": [], "messages": []},
            "risky_prompts": risky_prompts_data if not isinstance(risky_prompts_data, Exception) else {"risks": [], "messages": []}
        }
