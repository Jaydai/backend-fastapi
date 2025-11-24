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
        self.use_assistant = enrichment_config.MESSAGE_ENRICHMENT_ASSISTANT_ID is not None

        if self.use_assistant:
            logger.info(f"Using OpenAI Assistant API with ID: {enrichment_config.MESSAGE_ENRICHMENT_ASSISTANT_ID}")
        else:
            logger.info("Using legacy chat completions (no assistant ID configured)")
            self.prompt_template = self._load_prompt_template()

    @staticmethod
    def _load_prompt_template() -> str:
        """Load risk assessment prompt from file (legacy mode)"""
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
        logger.info(f"[RISK DEBUG] assess_message_risk called with content length: {len(content)}")
        start_time = time.time()

        # Truncate content if needed
        from utils.enrichment import truncate_message
        content_truncated = truncate_message(content)
        logger.info(f"[RISK DEBUG] Content truncated to: {len(content_truncated)} chars")

        # Format context
        context_str = json.dumps(context) if context else "N/A"

        if self.use_assistant:
            # Use Assistants API
            user_prompt = f"""**MESSAGE TO ANALYZE:**
{content_truncated}

**CONTEXT:** {context_str}

**ROLE:** {role}"""
            raw_response = self._call_assistant_with_retry(user_prompt)
        else:
            # Legacy: Use chat completions with template
            prompt = self.prompt_template.format(
                message_content=content_truncated,
                context=context_str,
                role=role
            )
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
                logger.info(f"[RISK DEBUG] Raw LLM response (first 200 chars): {repr(content[:200])}")

                # Remove markdown code blocks if present
                if content.strip().startswith("```"):
                    # Extract JSON from markdown code block
                    lines = content.strip().split("\n")
                    # Remove first line (```json or ```)
                    lines = lines[1:]
                    # Remove last line (```)
                    if lines and lines[-1].strip() == "```":
                        lines = lines[:-1]
                    content = "\n".join(lines)
                    logger.info(f"[RISK DEBUG] After markdown strip (first 200 chars): {repr(content[:200])}")

                # Handle case where LLM returns JSON content without opening/closing braces
                content_stripped = content.strip()
                if content_stripped and not content_stripped.startswith("{"):
                    # LLM returned JSON fields without wrapping braces - wrap it
                    logger.info(f"[RISK DEBUG] Adding opening brace to JSON")
                    content = "{" + content_stripped + "}"
                elif content_stripped and not content_stripped.endswith("}"):
                    # Missing closing brace
                    logger.info(f"[RISK DEBUG] Adding closing brace to JSON")
                    content = content_stripped + "}"
                else:
                    # Use stripped version
                    content = content_stripped

                logger.info(f"[RISK DEBUG] Final content before JSON parse (first 200 chars): {repr(content[:200])}")
                return json.loads(content)

            except json.JSONDecodeError as e:
                last_error = f"Invalid JSON response: {str(e)}"
                logger.warning(f"Attempt {attempt + 1} failed: {last_error}")
                logger.warning(f"Raw content (first 500 chars): {content[:500] if content else 'None'}")

            except Exception as e:
                last_error = f"LLM API error: {str(e)}"
                logger.warning(f"Attempt {attempt + 1} failed: {last_error}")

            # Wait before retry
            if attempt < enrichment_config.MAX_LLM_RETRIES:
                time.sleep(enrichment_config.LLM_RETRY_DELAY_SECONDS)

        # All retries failed
        logger.error(f"Risk assessment failed after {enrichment_config.MAX_LLM_RETRIES + 1} attempts: {last_error}")
        raise Exception(f"Risk assessment service failed: {last_error}")

    def _call_assistant_with_retry(self, user_prompt: str) -> dict:
        """
        Call OpenAI Assistant with retry logic on failure
        """
        last_error = None

        for attempt in range(enrichment_config.MAX_LLM_RETRIES + 1):
            try:
                # Create a thread
                thread = self.client.beta.threads.create()

                # Add message to thread
                self.client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content=user_prompt
                )

                # Run the assistant
                run = self.client.beta.threads.runs.create(
                    thread_id=thread.id,
                    assistant_id=enrichment_config.MESSAGE_ENRICHMENT_ASSISTANT_ID
                )

                # Wait for completion
                while run.status in ["queued", "in_progress"]:
                    time.sleep(0.5)
                    run = self.client.beta.threads.runs.retrieve(
                        thread_id=thread.id,
                        run_id=run.id
                    )

                if run.status == "completed":
                    # Get messages
                    messages = self.client.beta.threads.messages.list(thread_id=thread.id)
                    assistant_message = next(
                        (msg for msg in messages.data if msg.role == "assistant"),
                        None
                    )

                    if assistant_message:
                        content = assistant_message.content[0].text.value
                        logger.info(f"[RISK DEBUG] Raw assistant response (first 200 chars): {repr(content[:200])}")

                        # Parse JSON
                        content_stripped = content.strip()

                        # Remove markdown code blocks if present
                        if content_stripped.startswith("```"):
                            lines = content_stripped.split("\n")
                            lines = lines[1:]
                            if lines and lines[-1].strip() == "```":
                                lines = lines[:-1]
                            content_stripped = "\n".join(lines).strip()

                        return json.loads(content_stripped)
                    else:
                        raise Exception("No assistant response found")
                else:
                    raise Exception(f"Assistant run failed with status: {run.status}")

            except json.JSONDecodeError as e:
                last_error = f"Invalid JSON response: {str(e)}"
                logger.warning(f"Attempt {attempt + 1} failed: {last_error}")

            except Exception as e:
                last_error = f"Assistant API error: {str(e)}"
                logger.warning(f"Attempt {attempt + 1} failed: {last_error}")

            # Wait before retry
            if attempt < enrichment_config.MAX_LLM_RETRIES:
                time.sleep(enrichment_config.LLM_RETRY_DELAY_SECONDS)

        # All retries failed
        logger.error(f"Assistant risk assessment failed after {enrichment_config.MAX_LLM_RETRIES + 1} attempts: {last_error}")
        raise Exception(f"Assistant risk assessment service failed: {last_error}")

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

