"""
DTO Mapping Utilities
Transforms between domain entities and DTOs for cleaner code
"""
from domains.entities.enrichment_entities import (
    EnrichedChat, EnrichedMessage, QualityMetrics,
    FeedbackDetail, RiskCategory, RiskIssue
)
from domains.entities.audit_entities import (
    QualityStats, RiskStats, UsageStats, ThemeStats, IntentStats,
    TopUser, TopPrompt, RiskyPrompt
)
from dtos.enrichment_dto import (
    ChatEnrichmentRequestDTO, ChatEnrichmentResponseDTO,
    QualityMetricsDTO, FeedbackDTO,
    RiskCategoryDetailDTO, RiskIssueDTO
)
from dtos.audit_dto import (
    QualityStatsDTO, RiskStatsDTO, UsageStatsDTO,
    ThemeStatsDTO, IntentStatsDTO,
    TopUserDTO, TopPromptDTO, RiskyPromptDTO
)


# ==================== ENRICHMENT MAPPERS ====================

def classification_to_enriched_chat(classification_result: dict, request: ChatEnrichmentRequestDTO) -> EnrichedChat:
    """Transform classification result to EnrichedChat entity"""
    quality_metrics = _extract_quality_metrics(classification_result)
    feedback = _extract_feedback(classification_result)

    return EnrichedChat(
        chat_id=request.chat_id,
        chat_provider_id=request.chat_provider_id,
        message_provider_id=request.message_provider_id,
        is_work_related=classification_result.get("is_work_related", False),
        theme=classification_result.get("theme"),
        intent=classification_result.get("intent"),
        quality_metrics=quality_metrics,
        feedback=feedback,
        raw_response=classification_result,
        processing_time_ms=classification_result.get("processing_time_ms"),
        model_used=classification_result.get("model_used")
    )


def classification_to_response_dto(classification_result: dict) -> ChatEnrichmentResponseDTO:
    """Transform classification result to response DTO"""
    quality_dto = _quality_metrics_to_dto(classification_result.get("quality"))
    feedback_dto = _feedback_to_dto(classification_result.get("feedback"))

    return ChatEnrichmentResponseDTO(
        is_work_related=classification_result.get("is_work_related", False),
        theme=classification_result.get("theme", "unknown"),
        intent=classification_result.get("intent", "unknown"),
        quality=quality_dto,
        feedback=feedback_dto,
        raw=classification_result,
        processing_time_ms=classification_result.get("processing_time_ms")
    )


def risk_assessment_to_enriched_message(risk_result: dict, request) -> EnrichedMessage:
    """Transform risk result to EnrichedMessage entity"""
    risk_categories = _extract_risk_categories(risk_result)
    detected_issues = _extract_detected_issues(risk_result)

    return EnrichedMessage(
        message_provider_id=request.message_provider_id,
        message_id=request.message_id,
        overall_risk_level=risk_result.get("overall_risk_level", "none"),
        overall_risk_score=risk_result.get("overall_risk_score", 0.0),
        risk_categories=risk_categories,
        risk_summary=risk_result.get("risk_summary", []),
        detected_issues=detected_issues,
        processing_time_ms=risk_result.get("processing_time_ms"),
        model_used=risk_result.get("model_used")
    )


def risk_assessment_to_response_dto(risk_result: dict):
    """Transform risk result to response DTO"""
    risk_categories_dto = {}
    for category_name in ["pii", "security", "confidential", "misinformation", "data_leakage", "compliance"]:
        if category_name in risk_result:
            cat_data = risk_result[category_name]
            risk_categories_dto[category_name] = RiskCategoryDetailDTO(
                level=cat_data.get("risk_level", "none"),
                score=cat_data.get("risk_score", 0.0),
                detected=cat_data.get("risk_level") not in ["none", None],
                details=cat_data.get("description")
            )

    detected_issues_dto = []
    for category_name, cat_data in risk_result.items():
        if isinstance(cat_data, dict) and cat_data.get("detected_items"):
            for item in cat_data["detected_items"]:
                detected_issues_dto.append(RiskIssueDTO(
                    category=category_name,
                    severity=cat_data.get("risk_level", "low"),
                    description=f"{item} detected",
                    details=cat_data.get("description")
                ))

    from dtos.enrichment_dto import EnrichMessageResponseDTO
    return EnrichMessageResponseDTO(
        overall_risk_level=risk_result.get("overall_risk_level", "none"),
        overall_risk_score=risk_result.get("overall_risk_score", 0.0),
        risk_categories=risk_categories_dto,
        risk_summary=risk_result.get("risk_summary", []),
        detected_issues=detected_issues_dto,
        processing_time_ms=risk_result.get("processing_time_ms")
    )


# ==================== AUDIT MAPPERS ====================

def quality_stats_to_dto(stats: QualityStats) -> QualityStatsDTO:
    """Convert QualityStats entity to DTO"""
    return QualityStatsDTO(**stats.__dict__)


def risk_stats_to_dto(stats: RiskStats) -> RiskStatsDTO:
    """Convert RiskStats entity to DTO"""
    return RiskStatsDTO(**stats.__dict__)


def usage_stats_to_dto(stats: UsageStats) -> UsageStatsDTO:
    """Convert UsageStats entity to DTO"""
    return UsageStatsDTO(**stats.__dict__)


def theme_stats_to_dto(stats: ThemeStats) -> ThemeStatsDTO:
    """Convert ThemeStats entity to DTO"""
    return ThemeStatsDTO(**stats.__dict__)


def intent_stats_to_dto(stats: IntentStats) -> IntentStatsDTO:
    """Convert IntentStats entity to DTO"""
    return IntentStatsDTO(**stats.__dict__)


def top_user_to_dto(user: TopUser) -> TopUserDTO:
    """Convert TopUser entity to DTO"""
    return TopUserDTO(**user.__dict__)


def top_prompt_to_dto(prompt: TopPrompt) -> TopPromptDTO:
    """Convert TopPrompt entity to DTO"""
    return TopPromptDTO(**prompt.__dict__)


def risky_prompt_to_dto(prompt: RiskyPrompt) -> RiskyPromptDTO:
    """Convert RiskyPrompt entity to DTO"""
    return RiskyPromptDTO(**prompt.__dict__)


# ==================== PRIVATE HELPER FUNCTIONS ====================

def _extract_quality_metrics(classification_result: dict) -> QualityMetrics | None:
    """Extract quality metrics from classification result"""
    if "quality" not in classification_result:
        return None

    q = classification_result["quality"]
    return QualityMetrics(
        quality_score=q.get("overall_score", 0),
        clarity_score=q.get("clarity", 0),
        context_score=q.get("context", 0),
        specificity_score=q.get("specificity", 0),
        actionability_score=q.get("actionability", 0)
    )


def _extract_feedback(classification_result: dict) -> FeedbackDetail | None:
    """Extract feedback from classification result"""
    if "feedback" not in classification_result:
        return None

    f = classification_result["feedback"]
    return FeedbackDetail(
        summary=f.get("summary", ""),
        strengths=f.get("strengths", []),
        improvements=f.get("improvements", []),
        improved_prompt_example=f.get("improved_prompt_example")
    )


def _quality_metrics_to_dto(quality_data: dict | None) -> QualityMetricsDTO | None:
    """Convert quality data to DTO"""
    if not quality_data:
        return None

    return QualityMetricsDTO(
        quality_score=quality_data.get("overall_score", 0),
        clarity_score=quality_data.get("clarity", 0),
        context_score=quality_data.get("context", 0),
        specificity_score=quality_data.get("specificity", 0),
        actionability_score=quality_data.get("actionability", 0)
    )


def _feedback_to_dto(feedback_data: dict | None) -> FeedbackDTO | None:
    """Convert feedback data to DTO"""
    if not feedback_data:
        return None

    return FeedbackDTO(
        summary=feedback_data.get("summary", ""),
        strengths=feedback_data.get("strengths", []),
        improvements=feedback_data.get("improvements", []),
        improved_prompt_example=feedback_data.get("improved_prompt_example")
    )


def _extract_risk_categories(risk_result: dict) -> dict[str, RiskCategory]:
    """Extract risk categories from risk assessment result"""
    risk_categories = {}
    for category_name in ["pii", "security", "confidential", "misinformation", "data_leakage", "compliance"]:
        if category_name in risk_result:
            cat_data = risk_result[category_name]
            risk_categories[category_name] = RiskCategory(
                level=cat_data.get("risk_level", "none"),
                score=cat_data.get("risk_score", 0.0),
                detected=cat_data.get("risk_level") not in ["none", None],
                details=cat_data.get("description")
            )
    return risk_categories


def _extract_detected_issues(risk_result: dict) -> list[RiskIssue]:
    """Extract detected issues from risk assessment result"""
    detected_issues = []
    for category_name, cat_data in risk_result.items():
        if isinstance(cat_data, dict) and cat_data.get("detected_items"):
            for item in cat_data["detected_items"]:
                detected_issues.append(RiskIssue(
                    category=category_name,
                    severity=cat_data.get("risk_level", "low"),
                    description=f"{item} detected",
                    details=cat_data.get("description")
                ))
    return detected_issues
