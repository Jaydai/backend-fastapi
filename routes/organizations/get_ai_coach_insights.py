"""Get AI Coach insights for organization"""

import logging
from datetime import datetime, timedelta
from typing import Any

from fastapi import HTTPException, Request

from . import router

logger = logging.getLogger(__name__)


@router.get("/{organization_id}/ai-coach/insights")
async def get_ai_coach_insights(request: Request, organization_id: str):
    """
    Get AI Coach insights for an organization including:
    - Quality score
    - Theme/intent distribution
    - Top performing prompts
    - Personalized recommendations
    """
    try:
        client = request.state.supabase_client

        # Get all users in this organization first
        org_members_response = (
            client.table("organization_members").select("user_id").eq("organization_id", organization_id).execute()
        )

        if not org_members_response.data:
            # No members in organization, return empty insights
            return {
                "quality_score": 0,
                "quality_trend": "stable",
                "theme_distribution": [],
                "intent_distribution": [],
                "top_prompts": [],
                "recommendations": [
                    {
                        "type": "improvement",
                        "title": "Start Using Jaydai",
                        "description": "Begin creating prompts to unlock AI-powered insights and recommendations.",
                    }
                ],
                "total_prompts": 0,
                "avg_quality_change": 0,
            }

        user_ids = [member["user_id"] for member in org_members_response.data]

        # Get all enriched chats for organization members (last 90 days)
        cutoff_date = datetime.now() - timedelta(days=90)
        chats_response = (
            client.table("enriched_chats")
            .select(
                "id, chat_provider_id, theme, intent, quality_score, clarity_score, context_score, specificity_score, created_at, user_id"
            )
            .in_("user_id", user_ids)
            .gte("created_at", cutoff_date.isoformat())
            .order("created_at", desc=True)
            .limit(1000)
            .execute()
        )

        if not chats_response.data:
            # Return default insights if no data
            return {
                "quality_score": 0,
                "quality_trend": "stable",
                "theme_distribution": [],
                "intent_distribution": [],
                "top_prompts": [],
                "recommendations": [
                    {
                        "type": "improvement",
                        "title": "Start Using Jaydai",
                        "description": "Begin creating prompts to unlock AI-powered insights and recommendations.",
                    }
                ],
                "total_prompts": 0,
                "avg_quality_change": 0,
            }

        chats = chats_response.data
        total_prompts = len(chats)

        # Calculate overall quality score
        quality_scores = [c.get("quality_score", 0) or 0 for c in chats if c.get("quality_score") is not None]
        avg_quality = round(sum(quality_scores) / len(quality_scores)) if quality_scores else 0

        # Calculate quality trend (compare recent vs older chats)
        mid_point = len(chats) // 2
        recent_quality = (
            sum(quality_scores[:mid_point]) / mid_point if mid_point > 0 and len(quality_scores) >= mid_point else 0
        )
        older_quality = (
            sum(quality_scores[mid_point:]) / (len(quality_scores) - mid_point)
            if len(quality_scores) > mid_point
            else 0
        )

        quality_change = round(recent_quality - older_quality) if older_quality > 0 else 0
        quality_trend = "up" if quality_change > 2 else "down" if quality_change < -2 else "stable"

        # Calculate theme distribution
        theme_counts: dict[str, int] = {}
        for chat in chats:
            theme = chat.get("theme", "Other") or "Other"
            theme_counts[theme] = theme_counts.get(theme, 0) + 1

        theme_distribution = [
            {"theme": theme, "count": count, "percentage": round((count / total_prompts) * 100, 1)}
            for theme, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
        ]

        # Calculate intent distribution
        intent_counts: dict[str, int] = {}
        for chat in chats:
            intent = chat.get("intent", "Other") or "Other"
            intent_counts[intent] = intent_counts.get(intent, 0) + 1

        intent_distribution = [
            {"intent": intent, "count": count, "percentage": round((count / total_prompts) * 100, 1)}
            for intent, count in sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)
        ]

        # Get top performing chats
        top_chats_data = sorted(
            [c for c in chats if c.get("quality_score") is not None],
            key=lambda x: x.get("quality_score", 0),
            reverse=True,
        )[:5]

        # Format top prompts (without full content for now)
        top_prompts = [
            {
                "id": chat["id"],
                "content": f"{chat.get('theme', 'Chat')} - {chat.get('intent', 'interaction')}",
                "quality_score": chat.get("quality_score", 0),
                "usage_count": 0,  # We don't track usage count currently
                "theme": chat.get("theme", "Other") or "Other",
                "intent": chat.get("intent", "Other") or "Other",
            }
            for chat in top_chats_data
        ]

        # Generate recommendations based on data
        recommendations: list[dict[str, Any]] = []

        # Quality-based recommendations
        if avg_quality < 50:
            recommendations.append(
                {
                    "type": "improvement",
                    "title": "Enhance Prompt Quality",
                    "description": "Your average prompt quality is below 50. Focus on adding more context, clear instructions, and specific examples to improve results.",
                }
            )
        elif avg_quality >= 80:
            recommendations.append(
                {
                    "type": "strength",
                    "title": "Excellent Prompt Quality!",
                    "description": "Your team consistently creates high-quality prompts. Keep up the great work!",
                }
            )

        # Trend-based recommendations
        if quality_trend == "down":
            recommendations.append(
                {
                    "type": "warning",
                    "title": "Quality Trending Down",
                    "description": "Recent prompts show lower quality scores. Consider reviewing best practices with your team.",
                }
            )
        elif quality_trend == "up":
            recommendations.append(
                {
                    "type": "strength",
                    "title": "Improving Prompt Quality",
                    "description": "Your recent prompts show higher quality scores. Great progress!",
                }
            )

        # Theme diversity recommendation
        if len(theme_distribution) < 3:
            recommendations.append(
                {
                    "type": "improvement",
                    "title": "Diversify Use Cases",
                    "description": "Your prompts focus on limited themes. Explore different use cases to maximize AI value across your organization.",
                }
            )

        # Team activity recommendation
        if total_prompts >= 100:
            recommendations.append(
                {
                    "type": "strength",
                    "title": "Active Team",
                    "description": f"Your team has created {total_prompts} prompts. Great collaboration and AI adoption!",
                }
            )

        # Default recommendation if none generated
        if not recommendations:
            recommendations.append(
                {
                    "type": "improvement",
                    "title": "Keep Creating",
                    "description": "Continue using Jaydai to unlock more personalized insights and recommendations.",
                }
            )

        return {
            "quality_score": avg_quality,
            "quality_trend": quality_trend,
            "theme_distribution": theme_distribution,
            "intent_distribution": intent_distribution,
            "top_prompts": top_prompts,
            "recommendations": recommendations,
            "total_prompts": total_prompts,
            "avg_quality_change": quality_change,
        }

    except Exception as e:
        logger.error(f"Error getting AI coach insights for organization {organization_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get AI coach insights: {str(e)}")
