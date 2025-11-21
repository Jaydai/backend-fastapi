"""
Improved Risk Assessment Service with better error handling and validation
"""
import json
import logging
import time
from openai import OpenAI
from typing import Optional
from config.enrichment_config import enrichment_config

logger = logging.getLogger(__name__)


class RiskAssessmentService:
    """
    Improved service for assessing message risks
    """

    def __init__(self):
        self.client = OpenAI()
        self.prompt_template = self._load_prompt_template()

    @staticmethod
    def _load_prompt_template() -> str:
        """Load risk assessment prompt from file"""
        try:
            with open("prompts/risk_assessment.txt", "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.error("Risk assessment prompt file not found")
            raise

    def assess_message_risk(
        self,
        content: str,
        role: str = "user",
        context: Optional[dict] = None
    ) -> dict:
        """
        Assess risks in a message

        Returns dict with risk assessment across all categories
        Raises exception on failure after retries
        """
        start_time = time.time()

        # Truncate content if needed
        from utils.enrichment import truncate_message
        content_truncated = truncate_message(content)

        # Format context
        context_str = json.dumps(context) if context else "N/A"

        # Build prompt
        prompt = self.prompt_template.format(
            message_content=content_truncated,
            context=context_str,
            role=role
        )

        # Call LLM with retry logic
        raw_response = self._call_llm_with_retry(prompt)

        # Validate and enhance response
        enhanced_result = self._validate_and_enhance_risk_response(raw_response)

        # Add processing metadata
        processing_time_ms = int((time.time() - start_time) * 1000)
        enhanced_result["processing_time_ms"] = processing_time_ms
        enhanced_result["model_used"] = enrichment_config.DEFAULT_RISK_ASSESSMENT_MODEL

        return enhanced_result

    def _call_llm_with_retry(self, prompt: str) -> dict:
        """
        Call LLM with retry logic on failure
        """
        last_error = None

        for attempt in range(enrichment_config.MAX_LLM_RETRIES + 1):
            try:
                response = self.client.chat.completions.create(
                    model=enrichment_config.DEFAULT_RISK_ASSESSMENT_MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a security risk assessment expert. Respond only with valid JSON."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=enrichment_config.RISK_ASSESSMENT_TEMPERATURE,
                    max_tokens=enrichment_config.RISK_ASSESSMENT_MAX_TOKENS,
                    response_format={"type": "json_object"}
                )

                content = response.choices[0].message.content
                return json.loads(content)

            except json.JSONDecodeError as e:
                last_error = f"Invalid JSON response: {str(e)}"
                logger.warning(f"Attempt {attempt + 1} failed: {last_error}")

            except Exception as e:
                last_error = f"LLM API error: {str(e)}"
                logger.warning(f"Attempt {attempt + 1} failed: {last_error}")

            # Wait before retry
            if attempt < enrichment_config.MAX_LLM_RETRIES:
                time.sleep(enrichment_config.LLM_RETRY_DELAY_SECONDS)

        # All retries failed
        logger.error(f"Risk assessment failed after {enrichment_config.MAX_LLM_RETRIES + 1} attempts: {last_error}")
        raise Exception(f"Risk assessment service failed: {last_error}")

    def _validate_and_enhance_risk_response(self, raw_response: dict) -> dict:
        """
        Validate LLM response structure and recalculate overall risk with proper weighting
        """
        from utils.enrichment import sanitize_risk_assessment_result

        # Sanitize the basic structure
        sanitized = sanitize_risk_assessment_result(raw_response)

        # Recalculate overall risk with proper weighting
        overall_data = self._calculate_overall_risk(sanitized)
        sanitized["overall_risk_level"] = overall_data["level"]
        sanitized["overall_risk_score"] = overall_data["score"]

        return sanitized

    def _calculate_overall_risk(self, risk_data: dict) -> dict:
        """
        Calculate overall risk using weighted scoring
        Returns: {"level": str, "score": float}
        """
        category_scores = {
            "pii": risk_data.get("pii", {}).get("risk_score", 0),
            "security": risk_data.get("security", {}).get("risk_score", 0),
            "confidential": risk_data.get("confidential", {}).get("risk_score", 0),
            "misinformation": risk_data.get("misinformation", {}).get("risk_score", 0),
            "data_leakage": risk_data.get("data_leakage", {}).get("risk_score", 0),
            "compliance": risk_data.get("compliance", {}).get("risk_score", 0)
        }

        # Apply weights
        weighted_scores = []
        total_weight = 0

        for category, score in category_scores.items():
            weight = enrichment_config.RISK_CATEGORY_WEIGHTS.get(category, 1.0)
            weighted_scores.append(score * weight)
            total_weight += weight

        # Calculate weighted average
        overall_score = sum(weighted_scores) / total_weight if total_weight > 0 else 0

        # Determine level from score
        overall_level = enrichment_config.get_risk_level_from_score(overall_score)

        return {
            "score": round(overall_score, 2),
            "level": overall_level
        }


# Singleton instance
risk_assessment_service = RiskAssessmentService()
