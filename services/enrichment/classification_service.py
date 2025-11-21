"""
Improved Classification Service with better error handling and validation
"""
import json
import logging
import time
from openai import OpenAI
from typing import Optional
from config.enrichment_config import enrichment_config

logger = logging.getLogger(__name__)


class ClassificationService:
    """
    Improved service for classifying and evaluating chat quality
    """

    def __init__(self):
        self.client = OpenAI()
        self.prompt_template = self._load_prompt_template()

    @staticmethod
    def _load_prompt_template() -> str:
        """Load classification prompt from file"""
        try:
            with open("prompts/chat_classification_quality.txt", "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.error("Classification prompt file not found")
            raise

    def classify_chat(
        self,
        user_message: str,
        assistant_response: Optional[str] = None
    ) -> dict:
        """
        Classify a chat and evaluate its quality

        Returns dict with classification and quality assessment
        Raises exception on failure after retries
        """
        start_time = time.time()

        # Truncate messages if needed
        user_message_truncated = user_message[:enrichment_config.MAX_TRUNCATED_MESSAGE_LENGTH]
        assistant_response_truncated = (
            assistant_response[:enrichment_config.MAX_TRUNCATED_MESSAGE_LENGTH]
            if assistant_response
            else "N/A"
        )

        # Build prompt
        prompt = self.prompt_template.format(
            user_message=user_message_truncated,
            assistant_response=assistant_response_truncated
        )

        # Call LLM with retry logic
        raw_response = self._call_llm_with_retry(prompt)

        # Validate and parse response
        parsed_result = self._validate_classification_response(raw_response)

        # Add processing metadata
        processing_time_ms = int((time.time() - start_time) * 1000)
        parsed_result["processing_time_ms"] = processing_time_ms
        parsed_result["model_used"] = enrichment_config.DEFAULT_CLASSIFICATION_MODEL

        return parsed_result

    def _call_llm_with_retry(self, prompt: str) -> dict:
        """
        Call LLM with retry logic on failure
        """
        last_error = None

        for attempt in range(enrichment_config.MAX_LLM_RETRIES + 1):
            try:
                response = self.client.chat.completions.create(
                    model=enrichment_config.DEFAULT_CLASSIFICATION_MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a prompt classification and quality evaluation expert. Respond only with valid JSON."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=enrichment_config.CLASSIFICATION_TEMPERATURE,
                    max_tokens=enrichment_config.CLASSIFICATION_MAX_TOKENS,
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
        logger.error(f"Classification failed after {enrichment_config.MAX_LLM_RETRIES + 1} attempts: {last_error}")
        raise Exception(f"Classification service failed: {last_error}")

    def _validate_classification_response(self, raw_response: dict) -> dict:
        """
        Validate LLM response structure and provide defaults if needed
        """
        from utils.enrichment import sanitize_classification_result
        return sanitize_classification_result(raw_response)


# Singleton instance
classification_service = ClassificationService()
