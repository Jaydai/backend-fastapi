"""
Audit Time-Series Service - Business logic for time-series audit data
Handles adoption curves, risk timelines, quality evolution, etc.
"""
import logging
from supabase import Client
from datetime import datetime, timedelta
from typing import Optional, List
from collections import defaultdict

from repositories.team_repository import TeamRepository
from dtos.audit_dto import (
    AdoptionCurveResponseDTO,
    AdoptionCurveDataDTO,
    RiskTimelineResponseDTO,
    RiskTimelineDataDTO,
    RiskTimelineDataPointDTO,
    QualityTimelineResponseDTO,
    QualityTimelineDataDTO,
    QualityTimelineDataPointDTO,
    TimeSeriesDataPointDTO,
    ThemeTimelineResponseDTO,
    ThemeDistributionDTO,
    IntentTimelineResponseDTO,
    IntentDistributionDTO
)

logger = logging.getLogger(__name__)


def _calculate_date_range(start_date: str | None, end_date: str | None, days: int):
    """Calculate start and end datetime from parameters"""
    if end_date:
        end_dt = datetime.fromisoformat(end_date)
    else:
        end_dt = datetime.now()

    if start_date:
        start_dt = datetime.fromisoformat(start_date)
    else:
        start_dt = end_dt - timedelta(days=days)

    return start_dt, end_dt


def _get_date_trunc_sql(granularity: str) -> str:
    """Get SQL date truncation expression based on granularity"""
    if granularity == "week":
        return "DATE_TRUNC('week', created_at)"
    elif granularity == "month":
        return "DATE_TRUNC('month', created_at)"
    else:  # day
        return "DATE_TRUNC('day', created_at)"


def _get_user_ids_for_teams(client: Client, organization_id: str, team_ids: List[str] | None) -> List[str]:
    """Get user IDs filtered by teams, or all organization members if no teams specified"""
    if not team_ids or len(team_ids) == 0:
        # Get all organization members
        response = client.table("user_organization_roles") \
            .select("user_id") \
            .eq("organization_id", organization_id) \
            .execute()
        return [row["user_id"] for row in response.data] if response.data else []

    # Get users in specified teams
    user_ids_set = set()
    for team_id in team_ids:
        members = TeamRepository.get_team_members(client, team_id)
        user_ids_set.update([m.user_id for m in members])

    return list(user_ids_set)


class AuditTimeSeriesService:
    """Service for time-series audit data"""

    @staticmethod
    async def get_adoption_curve(
        client: Client,
        organization_id: str,
        start_date: str | None,
        end_date: str | None,
        days: int,
        team_ids: List[str] | None,
        granularity: str
    ) -> AdoptionCurveResponseDTO:
        """Get adoption curve (usage over time) with team breakdown"""
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)
        user_ids = _get_user_ids_for_teams(client, organization_id, team_ids)

        if not user_ids:
            return AdoptionCurveResponseDTO(
                organization_id=organization_id,
                date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
                granularity=granularity,
                team_filter=team_ids,
                data=AdoptionCurveDataDTO(
                    overall=[],
                    by_team={},
                    total_prompts=0,
                    total_chats=0,
                    average_daily_prompts=0.0
                ),
                generated_at=datetime.now()
            )

        # Fetch all enriched_chats for the organization within date range
        overall_result = client.table("enriched_chats") \
            .select("created_at, chat_id, user_id") \
            .in_("user_id", user_ids) \
            .gte("created_at", start_dt.isoformat()) \
            .lte("created_at", end_dt.isoformat()) \
            .execute()

        # Group by date based on granularity
        date_counts = defaultdict(int)
        for row in (overall_result.data or []):
            created_at = datetime.fromisoformat(row["created_at"].replace('Z', '+00:00'))

            # Truncate date based on granularity
            if granularity == "week":
                # Get start of week (Monday)
                date_key = (created_at - timedelta(days=created_at.weekday())).date()
            elif granularity == "month":
                date_key = created_at.replace(day=1).date()
            else:  # day
                date_key = created_at.date()

            date_counts[date_key] += 1

        # Convert to sorted timeline
        overall_timeline = [
            TimeSeriesDataPointDTO(
                date=str(date),
                value=float(count)
            )
            for date, count in sorted(date_counts.items())
        ]

        # Get by-team breakdown if teams specified
        by_team = {}
        if team_ids and len(team_ids) > 0:
            teams = TeamRepository.get_organization_teams(client, organization_id)
            for team_id in team_ids:
                team = next((t for t in teams if t.id == team_id), None)
                if not team:
                    continue

                team_members = TeamRepository.get_team_members(client, team_id)
                team_user_ids = [m.user_id for m in team_members]

                if not team_user_ids:
                    continue

                # Filter data for this team
                team_date_counts = defaultdict(int)
                for row in (overall_result.data or []):
                    if row["user_id"] not in team_user_ids:
                        continue

                    created_at = datetime.fromisoformat(row["created_at"].replace('Z', '+00:00'))

                    # Truncate date based on granularity
                    if granularity == "week":
                        date_key = (created_at - timedelta(days=created_at.weekday())).date()
                    elif granularity == "month":
                        date_key = created_at.replace(day=1).date()
                    else:  # day
                        date_key = created_at.date()

                    team_date_counts[date_key] += 1

                by_team[team.name] = [
                    TimeSeriesDataPointDTO(
                        date=str(date),
                        value=float(count)
                    )
                    for date, count in sorted(team_date_counts.items())
                ]

        # Calculate totals
        total_prompts = sum(point.value for point in overall_timeline)

        # Get total chats
        chats_result = client.table("enriched_chats") \
            .select("chat_id", count="exact") \
            .in_("user_id", user_ids) \
            .gte("created_at", start_dt.isoformat()) \
            .lte("created_at", end_dt.isoformat()) \
            .execute()

        total_chats = chats_result.count or 0

        days_in_period = (end_dt - start_dt).days + 1
        average_daily_prompts = total_prompts / days_in_period if days_in_period > 0 else 0.0

        return AdoptionCurveResponseDTO(
            organization_id=organization_id,
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            granularity=granularity,
            team_filter=team_ids,
            data=AdoptionCurveDataDTO(
                overall=overall_timeline,
                by_team=by_team,
                total_prompts=int(total_prompts),
                total_chats=total_chats,
                average_daily_prompts=average_daily_prompts
            ),
            generated_at=datetime.now()
        )

    @staticmethod
    async def get_risk_timeline(
        client: Client,
        organization_id: str,
        start_date: str | None,
        end_date: str | None,
        days: int,
        team_ids: List[str] | None,
        granularity: str
    ) -> RiskTimelineResponseDTO:
        """Get risk timeline with breakdown by risk level and type"""
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)
        user_ids = _get_user_ids_for_teams(client, organization_id, team_ids)

        if not user_ids:
            return RiskTimelineResponseDTO(
                organization_id=organization_id,
                date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
                granularity=granularity,
                team_filter=team_ids,
                data=RiskTimelineDataDTO(
                    timeline=[],
                    total_risky_messages=0,
                    risk_level_totals={},
                    risk_type_totals={}
                ),
                generated_at=datetime.now()
            )

        date_trunc = _get_date_trunc_sql(granularity)

        # Get enriched messages with risk data grouped by date
        response = client.table("enriched_messages") \
            .select("created_at, overall_risk_level, risk_categories") \
            .in_("user_id", user_ids) \
            .gte("created_at", start_dt.isoformat()) \
            .lte("created_at", end_dt.isoformat()) \
            .neq("overall_risk_level", "none") \
            .execute()

        # Group by date
        timeline_data = defaultdict(lambda: {
            "total": 0,
            "by_risk_level": defaultdict(int),
            "by_risk_type": defaultdict(int)
        })

        risk_level_totals = defaultdict(int)
        risk_type_totals = defaultdict(int)
        total_risky = 0

        for row in (response.data or []):
            date = row["created_at"].split("T")[0]
            risk_level = row.get("overall_risk_level", "none")
            risk_categories = row.get("risk_categories", {})

            timeline_data[date]["total"] += 1
            timeline_data[date]["by_risk_level"][risk_level] += 1
            risk_level_totals[risk_level] += 1
            total_risky += 1

            # Parse risk categories
            if isinstance(risk_categories, dict):
                for category, details in risk_categories.items():
                    if isinstance(details, dict) and details.get("detected"):
                        timeline_data[date]["by_risk_type"][category] += 1
                        risk_type_totals[category] += 1

        # Build timeline
        timeline = [
            RiskTimelineDataPointDTO(
                date=date,
                total_risky_messages=data["total"],
                by_risk_level=dict(data["by_risk_level"]),
                by_risk_type=dict(data["by_risk_type"])
            )
            for date, data in sorted(timeline_data.items())
        ]

        return RiskTimelineResponseDTO(
            organization_id=organization_id,
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            granularity=granularity,
            team_filter=team_ids,
            data=RiskTimelineDataDTO(
                timeline=timeline,
                total_risky_messages=total_risky,
                risk_level_totals=dict(risk_level_totals),
                risk_type_totals=dict(risk_type_totals)
            ),
            generated_at=datetime.now()
        )

    @staticmethod
    async def get_quality_timeline(
        client: Client,
        organization_id: str,
        start_date: str | None,
        end_date: str | None,
        days: int,
        team_ids: List[str] | None,
        granularity: str
    ) -> QualityTimelineResponseDTO:
        """Get quality score evolution over time"""
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)
        user_ids = _get_user_ids_for_teams(client, organization_id, team_ids)

        if not user_ids:
            return QualityTimelineResponseDTO(
                organization_id=organization_id,
                date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
                granularity=granularity,
                team_filter=team_ids,
                data=QualityTimelineDataDTO(
                    overall=[],
                    by_team={},
                    overall_average=0.0,
                    total_rated=0
                ),
                generated_at=datetime.now()
            )

        # Get overall quality timeline
        response = client.table("enriched_chats") \
            .select("created_at, quality_score") \
            .in_("user_id", user_ids) \
            .gte("created_at", start_dt.isoformat()) \
            .lte("created_at", end_dt.isoformat()) \
            .not_.is_("quality_score", "null") \
            .execute()

        # Group by date
        date_scores = defaultdict(list)
        all_scores = []

        for row in (response.data or []):
            date = row["created_at"].split("T")[0]
            score = row.get("quality_score")
            if score is not None:
                date_scores[date].append(score)
                all_scores.append(score)

        # Build overall timeline
        overall_timeline = [
            QualityTimelineDataPointDTO(
                date=date,
                average_score=sum(scores) / len(scores),
                median_score=sorted(scores)[len(scores) // 2] if scores else None,
                total_rated=len(scores)
            )
            for date, scores in sorted(date_scores.items())
        ]

        # Get by-team breakdown if teams specified
        by_team = {}
        if team_ids and len(team_ids) > 0:
            teams = TeamRepository.get_organization_teams(client, organization_id)
            for team_id in team_ids:
                team = next((t for t in teams if t.id == team_id), None)
                if not team:
                    continue

                team_members = TeamRepository.get_team_members(client, team_id)
                team_user_ids = [m.user_id for m in team_members]

                if not team_user_ids:
                    continue

                team_response = client.table("enriched_chats") \
                    .select("created_at, quality_score") \
                    .in_("user_id", team_user_ids) \
                    .gte("created_at", start_dt.isoformat()) \
                    .lte("created_at", end_dt.isoformat()) \
                    .not_.is_("quality_score", "null") \
                    .execute()

                team_date_scores = defaultdict(list)
                for row in (team_response.data or []):
                    date = row["created_at"].split("T")[0]
                    score = row.get("quality_score")
                    if score is not None:
                        team_date_scores[date].append(score)

                by_team[team.name] = [
                    QualityTimelineDataPointDTO(
                        date=date,
                        average_score=sum(scores) / len(scores),
                        median_score=sorted(scores)[len(scores) // 2] if scores else None,
                        total_rated=len(scores)
                    )
                    for date, scores in sorted(team_date_scores.items())
                ]

        overall_average = sum(all_scores) / len(all_scores) if all_scores else 0.0

        return QualityTimelineResponseDTO(
            organization_id=organization_id,
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            granularity=granularity,
            team_filter=team_ids,
            data=QualityTimelineDataDTO(
                overall=overall_timeline,
                by_team=by_team,
                overall_average=overall_average,
                total_rated=len(all_scores)
            ),
            generated_at=datetime.now()
        )

    @staticmethod
    async def get_theme_distribution(
        client: Client,
        organization_id: str,
        start_date: str | None,
        end_date: str | None,
        days: int,
        team_ids: List[str] | None,
        top_n: int
    ) -> ThemeTimelineResponseDTO:
        """Get theme distribution for the period"""
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)
        user_ids = _get_user_ids_for_teams(client, organization_id, team_ids)

        if not user_ids:
            return ThemeTimelineResponseDTO(
                organization_id=organization_id,
                date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
                team_filter=team_ids,
                top_themes=[],
                current_distribution=ThemeDistributionDTO(themes={}, total=0),
                generated_at=datetime.now()
            )

        response = client.table("enriched_chats") \
            .select("theme") \
            .in_("user_id", user_ids) \
            .gte("created_at", start_dt.isoformat()) \
            .lte("created_at", end_dt.isoformat()) \
            .not_.is_("theme", "null") \
            .execute()

        # Count themes
        theme_counts = defaultdict(int)
        for row in (response.data or []):
            theme = row.get("theme")
            if theme:
                theme_counts[theme] += 1

        # Get top N themes
        top_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
        top_theme_names = [theme for theme, _ in top_themes]

        total = sum(theme_counts.values())

        return ThemeTimelineResponseDTO(
            organization_id=organization_id,
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            team_filter=team_ids,
            top_themes=top_theme_names,
            current_distribution=ThemeDistributionDTO(
                themes=dict(theme_counts),
                total=total
            ),
            generated_at=datetime.now()
        )

    @staticmethod
    async def get_intent_distribution(
        client: Client,
        organization_id: str,
        start_date: str | None,
        end_date: str | None,
        days: int,
        team_ids: List[str] | None,
        top_n: int
    ) -> IntentTimelineResponseDTO:
        """Get intent distribution for the period"""
        start_dt, end_dt = _calculate_date_range(start_date, end_date, days)
        user_ids = _get_user_ids_for_teams(client, organization_id, team_ids)

        if not user_ids:
            return IntentTimelineResponseDTO(
                organization_id=organization_id,
                date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
                team_filter=team_ids,
                top_intents=[],
                current_distribution=IntentDistributionDTO(intents={}, total=0),
                generated_at=datetime.now()
            )

        response = client.table("enriched_chats") \
            .select("intent") \
            .in_("user_id", user_ids) \
            .gte("created_at", start_dt.isoformat()) \
            .lte("created_at", end_dt.isoformat()) \
            .not_.is_("intent", "null") \
            .execute()

        # Count intents
        intent_counts = defaultdict(int)
        for row in (response.data or []):
            intent = row.get("intent")
            if intent:
                intent_counts[intent] += 1

        # Get top N intents
        top_intents = sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
        top_intent_names = [intent for intent, _ in top_intents]

        total = sum(intent_counts.values())

        return IntentTimelineResponseDTO(
            organization_id=organization_id,
            date_range={"start_date": start_dt.isoformat(), "end_date": end_dt.isoformat()},
            team_filter=team_ids,
            top_intents=top_intent_names,
            current_distribution=IntentDistributionDTO(
                intents=dict(intent_counts),
                total=total
            ),
            generated_at=datetime.now()
        )
