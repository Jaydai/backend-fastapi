"""
Aggregation Utilities for Audit Data
Handles statistical calculations and data aggregation
"""

from collections import Counter, defaultdict
from datetime import datetime

from config.enrichment_config import enrichment_config
from domains.entities.audit_entities import (
    IntentStats,
    QualityStats,
    RiskStats,
    RiskyPrompt,
    ThemeStats,
    TopPrompt,
    TopUser,
    UsageStats,
)


def aggregate_quality_stats(quality_data: dict) -> QualityStats:
    """
    Aggregate quality statistics from raw data
    Calculates averages, distributions, and trends
    """
    current_scores = [
        row.get("quality_score", 0) for row in quality_data.get("current", []) if row.get("quality_score") is not None
    ]

    if not current_scores:
        return QualityStats(average_score=0.0, total_rated=0)

    # Calculate statistics
    avg_score = sum(current_scores) / len(current_scores)
    sorted_scores = sorted(current_scores)
    median_score = sorted_scores[len(sorted_scores) // 2] if sorted_scores else 0

    # Calculate distribution using quality buckets
    distribution = _calculate_quality_distribution(current_scores)

    # Calculate trend
    trend_change = _calculate_quality_trend(current_scores, quality_data.get("trend", []))

    return QualityStats(
        average_score=round(avg_score, 2),
        median_score=median_score,
        distribution=distribution,
        total_rated=len(current_scores),
        trend_change=round(trend_change, 2) if trend_change is not None else None,
    )


def aggregate_risk_stats(risk_data: list) -> RiskStats:
    """
    Aggregate risk statistics from raw data
    Counts risk levels and detected issue types
    """
    if not risk_data:
        return RiskStats()

    # Count risk levels
    risk_level_counts = Counter(row.get("overall_risk_level", "none") for row in risk_data)

    # Count detected issue types
    pii_count, credentials_count, sensitive_count = _count_detected_issues(risk_data)

    # Calculate average risk score
    risk_scores = [row.get("overall_risk_score", 0) for row in risk_data if row.get("overall_risk_score")]
    avg_risk_score = sum(risk_scores) / len(risk_scores) if risk_scores else 0.0

    return RiskStats(
        total_messages_assessed=len(risk_data),
        critical_count=risk_level_counts.get("critical", 0),
        high_count=risk_level_counts.get("high", 0),
        medium_count=risk_level_counts.get("medium", 0),
        low_count=risk_level_counts.get("low", 0),
        none_count=risk_level_counts.get("none", 0),
        pii_detected_count=pii_count,
        credentials_detected_count=credentials_count,
        sensitive_data_count=sensitive_count,
        average_risk_score=round(avg_risk_score, 2),
    )


def aggregate_usage_stats(usage_data: dict) -> UsageStats:
    """
    Aggregate usage statistics from raw data
    Calculates totals, unique users, work percentages
    """
    messages = usage_data.get("messages", [])
    work_classification = usage_data.get("work_classification", [])

    total_prompts = len(messages)
    unique_users = len({msg.get("user_id") for msg in messages if msg.get("user_id")})

    work_related_count = sum(1 for row in work_classification if row.get("is_work_related"))
    personal_count = len(work_classification) - work_related_count

    work_percentage = (work_related_count / len(work_classification) * 100) if work_classification else 0.0
    avg_prompts_per_user = total_prompts / unique_users if unique_users > 0 else 0.0

    return UsageStats(
        total_prompts=total_prompts,
        total_chats=len(work_classification),
        active_users=unique_users,
        work_related_count=work_related_count,
        personal_count=personal_count,
        work_percentage=round(work_percentage, 2),
        average_prompts_per_user=round(avg_prompts_per_user, 2),
    )


def aggregate_theme_stats(theme_data: dict) -> ThemeStats:
    """
    Aggregate theme distribution statistics
    Calculates top themes with counts and trend changes
    """
    current_themes = [row.get("theme") for row in theme_data.get("current", []) if row.get("theme")]
    trend_themes = [row.get("theme") for row in theme_data.get("trend", []) if row.get("theme")]

    theme_counts = Counter(current_themes)
    total = len(current_themes)

    # Build top themes list
    top_themes = _build_top_themes_list(theme_counts, total)

    # Calculate trend changes
    trend_change = _calculate_theme_trends(theme_counts, Counter(trend_themes), total, len(trend_themes))

    return ThemeStats(top_themes=top_themes, total_categorized=total, trend_change=trend_change)


def aggregate_intent_stats(intent_data: list) -> IntentStats:
    """
    Aggregate intent distribution statistics
    Groups by intent with average quality scores
    """
    if not intent_data:
        return IntentStats()

    # Group by intent and calculate average quality
    intent_quality = defaultdict(lambda: {"count": 0, "total_quality": 0})

    for row in intent_data:
        intent = row.get("intent")
        quality = row.get("quality_score")

        if intent and quality is not None:
            intent_quality[intent]["count"] += 1
            intent_quality[intent]["total_quality"] += quality

    # Build top intents list
    top_intents = [
        {
            "intent": intent,
            "count": data["count"],
            "avg_quality": round(data["total_quality"] / data["count"], 2) if data["count"] > 0 else 0,
        }
        for intent, data in sorted(intent_quality.items(), key=lambda x: x[1]["count"], reverse=True)[:10]
    ]

    return IntentStats(top_intents=top_intents, total_categorized=len(intent_data))


def aggregate_top_users(top_users_data: dict) -> list[TopUser]:
    """
    Aggregate top users by activity
    Combines message counts, quality scores, and risk data
    """
    messages = top_users_data.get("messages", [])
    quality = top_users_data.get("quality", [])
    risks = top_users_data.get("risks", [])

    # Aggregate by user_id
    user_stats = defaultdict(
        lambda: {"total_prompts": 0, "quality_scores": [], "work_prompts": 0, "high_risk_messages": 0}
    )

    # Count messages
    for msg in messages:
        uid = msg.get("user_id")
        if uid:
            user_stats[uid]["total_prompts"] += 1

    # Add quality data
    for q in quality:
        uid = q.get("user_id")
        if uid:
            score = q.get("quality_score")
            if score is not None:
                user_stats[uid]["quality_scores"].append(score)
            if q.get("is_work_related"):
                user_stats[uid]["work_prompts"] += 1

    # Add risk data
    for r in risks:
        uid = r.get("user_id")
        if uid:
            user_stats[uid]["high_risk_messages"] += 1

    # Build TopUser list
    top_users = []
    for user_id, stats in sorted(user_stats.items(), key=lambda x: x[1]["total_prompts"], reverse=True)[:10]:
        avg_quality = (sum(stats["quality_scores"]) / len(stats["quality_scores"])) if stats["quality_scores"] else 0

        top_users.append(
            TopUser(
                user_id=user_id,
                email="user@example.com",  # TODO: Fetch from auth
                name=None,
                total_prompts=stats["total_prompts"],
                average_quality=round(avg_quality, 2),
                work_prompts=stats["work_prompts"],
                high_risk_messages=stats["high_risk_messages"],
            )
        )

    return top_users


def aggregate_top_prompts(top_prompts_data: dict) -> list[TopPrompt]:
    """
    Aggregate top quality prompts
    Joins chat data with message content
    """
    chats = top_prompts_data.get("chats", [])
    messages = top_prompts_data.get("messages", [])

    # Build message content map
    message_map = {msg.get("message_provider_id"): msg.get("content", "") for msg in messages}

    top_prompts = []
    for chat in chats[:10]:
        msg_provider_id = chat.get("message_provider_id")
        content = message_map.get(msg_provider_id, "")
        content_preview = content[:200] if content else "[No content]"

        top_prompts.append(
            TopPrompt(
                chat_provider_id=chat.get("chat_provider_id", ""),
                message_provider_id=msg_provider_id,
                quality_score=chat.get("quality_score", 0),
                theme=chat.get("theme", "unknown"),
                intent=chat.get("intent", "unknown"),
                content_preview=content_preview,
                created_at=datetime.fromisoformat(chat.get("created_at")) if chat.get("created_at") else datetime.now(),
            )
        )

    return top_prompts


def aggregate_risky_prompts(risky_prompts_data: dict) -> list[RiskyPrompt]:
    """
    Aggregate riskiest prompts
    Joins risk data with message content and user info
    """
    risks = risky_prompts_data.get("risks", [])
    messages = risky_prompts_data.get("messages", [])
    users = risky_prompts_data.get("users", [])

    # Build message content map
    message_map = {msg.get("message_provider_id"): msg.get("content", "") for msg in messages}

    # Build user info map
    user_map = {user.get("user_id"): user for user in users}

    risky_prompts = []
    for risk in risks:
        msg_provider_id = risk.get("message_provider_id")
        content_full = message_map.get(msg_provider_id, "")
        content_preview = content_full[:200] if content_full else "[No content]"

        # Extract risk categories
        risk_categories = _extract_risk_category_names(risk.get("risk_categories", {}))

        # Get user info
        user_id = risk.get("user_id")
        user_info = user_map.get(user_id, {})

        risky_prompts.append(RiskyPrompt(
            message_provider_id=msg_provider_id,
            risk_level=risk.get("overall_risk_level", "none"),
            risk_score=risk.get("overall_risk_score", 0.0),
            risk_categories=risk_categories,
            content_preview=content_preview,
            content_full=content_full if content_full else "[No content]",
            created_at=datetime.fromisoformat(risk.get("created_at")) if risk.get("created_at") else datetime.now(),
            user_whitelist=risk.get("user_whitelist", False),
            user_email=user_info.get("email"),
            user_name=user_info.get("name")
        ))

    return risky_prompts


# ==================== PRIVATE HELPER FUNCTIONS ====================


def _calculate_quality_distribution(scores: list[int]) -> dict[str, int]:
    """Calculate quality score distribution by bucket"""
    distribution = {"excellent": 0, "good": 0, "medium": 0, "poor": 0}
    for score in scores:
        bucket = enrichment_config.get_quality_bucket(score)
        distribution[bucket] += 1
    return distribution


def _calculate_quality_trend(current_scores: list, trend_data: list) -> float | None:
    """Calculate quality trend percentage change"""
    if not current_scores:
        return None

    trend_scores = [row.get("quality_score", 0) for row in trend_data if row.get("quality_score") is not None]

    if not trend_scores:
        return None

    current_avg = sum(current_scores) / len(current_scores)
    trend_avg = sum(trend_scores) / len(trend_scores)

    return ((current_avg - trend_avg) / trend_avg * 100) if trend_avg > 0 else 0


def _count_detected_issues(risk_data: list) -> tuple[int, int, int]:
    """Count PII, credentials, and sensitive data detections"""
    pii_count = 0
    credentials_count = 0
    sensitive_count = 0

    for row in risk_data:
        issues = row.get("detected_issues", [])
        if not isinstance(issues, list):
            continue

        for issue in issues:
            if not isinstance(issue, dict):
                continue
            category = issue.get("category", "").lower()
            if "pii" in category:
                pii_count += 1
            elif "security" in category or "credential" in category:
                credentials_count += 1
            elif "confidential" in category or "data_leakage" in category:
                sensitive_count += 1

    return pii_count, credentials_count, sensitive_count


def _build_top_themes_list(theme_counts: Counter, total: int) -> list[dict]:
    """Build top themes list with percentages"""
    return [
        {"theme": theme, "count": count, "percentage": round(count / total * 100, 2) if total > 0 else 0}
        for theme, count in theme_counts.most_common(10)
    ]


def _calculate_theme_trends(
    current_counts: Counter, trend_counts: Counter, current_total: int, trend_total: int
) -> dict:
    """Calculate per-theme percentage changes"""
    trend_change = {}

    for theme, current_count in current_counts.items():
        current_pct = current_count / current_total * 100 if current_total > 0 else 0
        trend_count = trend_counts.get(theme, 0)
        trend_pct = trend_count / trend_total * 100 if trend_total > 0 else 0
        change = current_pct - trend_pct
        trend_change[theme] = round(change, 2)

    return trend_change


def _extract_risk_category_names(risk_categories: dict) -> list[str]:
    """Extract names of detected risk categories"""
    detected = []
    for cat_name, cat_data in risk_categories.items():
        if isinstance(cat_data, dict) and cat_data.get("detected") is True:
            detected.append(cat_name)
    return detected
