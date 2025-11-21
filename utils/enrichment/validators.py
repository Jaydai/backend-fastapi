"""
Validation Utilities
Validates and sanitizes enrichment data
"""
from config.enrichment_config import enrichment_config


def truncate_message(content: str, max_length: int | None = None) -> str:
    """
    Truncate message to maximum length for AI processing

    Args:
        content: Message content to truncate
        max_length: Maximum length (defaults to config value)

    Returns:
        Truncated content
    """
    if max_length is None:
        max_length = enrichment_config.MAX_TRUNCATED_MESSAGE_LENGTH

    return content[:max_length]


def validate_quality_scores(quality_data: dict) -> dict:
    """
    Validate and clamp quality scores to valid ranges

    Args:
        quality_data: Quality scores from AI

    Returns:
        Validated quality data with clamped values
    """
    validated = quality_data.copy()

    # Clamp overall score to 0-100
    if "overall_score" in validated:
        validated["overall_score"] = max(0, min(100, validated.get("overall_score", 0)))

    # Clamp individual scores to 1-5
    for field in ["clarity", "context", "specificity", "actionability"]:
        if field in validated:
            validated[field] = max(1, min(5, validated.get(field, 1)))

    return validated


def validate_risk_scores(risk_data: dict) -> dict:
    """
    Validate and clamp risk scores to valid ranges

    Args:
        risk_data: Risk assessment from AI

    Returns:
        Validated risk data with clamped values
    """
    validated = risk_data.copy()

    # Validate each category
    for category in ["pii", "security", "confidential", "misinformation", "data_leakage", "compliance"]:
        if category in validated and isinstance(validated[category], dict):
            cat_data = validated[category]

            # Clamp risk_score to 0-100
            if "risk_score" in cat_data:
                cat_data["risk_score"] = max(0, min(100, cat_data.get("risk_score", 0)))

            # Ensure risk_level is valid
            if "risk_level" in cat_data:
                valid_levels = ["none", "low", "medium", "high", "critical"]
                if cat_data["risk_level"] not in valid_levels:
                    cat_data["risk_level"] = "none"

    # Validate overall risk score
    if "overall_risk_score" in validated:
        validated["overall_risk_score"] = max(0.0, min(100.0, validated.get("overall_risk_score", 0.0)))

    return validated


def ensure_required_fields(data: dict, required_fields: list[str], defaults: dict | None = None) -> dict:
    """
    Ensure required fields exist in data, add defaults if missing

    Args:
        data: Data dictionary to validate
        required_fields: List of required field names
        defaults: Optional default values for missing fields

    Returns:
        Data with all required fields
    """
    defaults = defaults or {}
    validated = data.copy()

    for field in required_fields:
        if field not in validated:
            validated[field] = defaults.get(field, None)

    return validated


def sanitize_classification_result(result: dict) -> dict:
    """
    Sanitize and validate classification result from AI

    Args:
        result: Raw classification result

    Returns:
        Sanitized result with validated values
    """
    sanitized = result.copy()

    # Ensure required fields
    required_fields = ["is_work_related", "theme", "intent"]
    for field in required_fields:
        if field not in sanitized:
            sanitized[field] = False if field == "is_work_related" else "unknown"

    # Validate quality if present
    if "quality" in sanitized:
        sanitized["quality"] = validate_quality_scores(sanitized["quality"])

    # Ensure feedback structure
    if "feedback" in sanitized and isinstance(sanitized["feedback"], dict):
        feedback = sanitized["feedback"]
        if "strengths" not in feedback:
            feedback["strengths"] = []
        if "improvements" not in feedback:
            feedback["improvements"] = []
        if "summary" not in feedback:
            feedback["summary"] = "No summary provided"

    return sanitized


def sanitize_risk_assessment_result(result: dict) -> dict:
    """
    Sanitize and validate risk assessment result from AI

    Args:
        result: Raw risk assessment result

    Returns:
        Sanitized result with validated values
    """
    import logging
    logger = logging.getLogger(__name__)

    sanitized = validate_risk_scores(result)

    # Ensure all risk categories exist with valid structure
    risk_categories = ["pii", "security", "confidential", "misinformation", "data_leakage", "compliance"]
    for category in risk_categories:
        if category not in sanitized:
            logger.warning(f"Missing risk category: {category}")
            sanitized[category] = {
                "risk_level": "none",
                "risk_score": 0,
                "description": f"No {category} assessment available"
            }
        else:
            # Ensure category has all required fields
            cat_data = sanitized[category]
            if "risk_level" not in cat_data:
                cat_data["risk_level"] = "none"
            if "risk_score" not in cat_data:
                cat_data["risk_score"] = 0
            if "description" not in cat_data:
                cat_data["description"] = f"No {category} data"

    # Ensure risk_summary is a list
    if "risk_summary" not in sanitized or not isinstance(sanitized["risk_summary"], list):
        sanitized["risk_summary"] = []

    # Ensure overall risk level exists
    if "overall_risk_level" not in sanitized:
        sanitized["overall_risk_level"] = "none"

    return sanitized


def is_valid_risk_level(level: str) -> bool:
    """Check if risk level is valid"""
    return level in ["none", "low", "medium", "high", "critical"]


def get_risk_level_hierarchy(min_risk_level: str) -> list[str]:
    """
    Get list of risk levels >= min_risk_level

    Args:
        min_risk_level: Minimum risk level threshold

    Returns:
        List of risk levels to include
    """
    hierarchy = {
        "critical": ["critical"],
        "high": ["critical", "high"],
        "medium": ["critical", "high", "medium"],
        "low": ["critical", "high", "medium", "low"]
    }

    return hierarchy.get(min_risk_level, ["critical", "high", "medium"])
