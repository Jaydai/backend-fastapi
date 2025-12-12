"""
Organization Generation Service

Handles AI-powered organization description generation.
Uses OpenAI to generate descriptions based on organization name and URLs.
"""

import json
import logging
import os
from typing import Any

from openai import OpenAI

logger = logging.getLogger(__name__)

# Configuration
GENERATION_MODEL = "gpt-4.1-nano"
GENERATION_TEMPERATURE = 0.7


class OrganizationGenerationService:
    """
    Service for generating organization descriptions using AI.

    Features:
    - Generate organization descriptions from name/URL
    - Multi-language support (en, fr)
    - Mock mode for testing without API key
    """

    def __init__(self):
        """Initialize the service with OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        mock_mode = os.getenv("ONBOARDING_MOCK_MODE", "false").lower() == "true"

        if api_key and not mock_mode:
            self.client = OpenAI()
            self.mock_mode = False
        else:
            self.client = None
            self.mock_mode = True
            logger.warning(
                "OpenAI API key not set or mock mode enabled - using mock responses"
            )

    def generate_description(
        self,
        organization_name: str,
        website_url: str | None = None,
        linkedin_url: str | None = None,
        language: str = "en",
    ) -> dict[str, str]:
        """
        Generate an organization description based on name and URLs.

        Args:
            organization_name: Name of the organization
            website_url: Organization website URL (optional)
            linkedin_url: Organization LinkedIn URL (optional)
            language: Language code ('en' or 'fr')

        Returns:
            Dict with organization_description and industry
        """
        if self.mock_mode:
            return self._mock_description(organization_name, language)

        lang_instruction = (
            "Respond in French." if language == "fr" else "Respond in English."
        )

        context_parts = [f"Organization name: {organization_name}"]
        if website_url:
            context_parts.append(f"Website: {website_url}")
        if linkedin_url:
            context_parts.append(f"LinkedIn: {linkedin_url}")

        context = "\n".join(context_parts)

        prompt = f"""Based on this organization information:
{context}

Generate a brief, professional description of this organization. If you recognize the organization, provide accurate information. If not, create a plausible description based on the name.

{lang_instruction}

Respond in this exact JSON format:
{{
    "organization_description": "A 2-3 sentence description of what the organization does, its industry, and its focus.",
    "industry": "The primary industry (e.g., Technology, Finance, Healthcare, Retail, etc.)"
}}"""

        try:
            response = self.client.responses.create(
                model=GENERATION_MODEL,
                input=[{"role": "user", "content": prompt}],
                temperature=GENERATION_TEMPERATURE,
            )

            response_text = response.output_text.strip()
            parsed = self._parse_json_response(response_text)

            logger.info(
                f"[ONBOARDING] Generated organization description for: {organization_name}"
            )
            return {
                "organization_description": parsed.get(
                    "organization_description",
                    parsed.get("company_description", ""),
                ),
                "industry": parsed.get("industry", ""),
            }

        except Exception as e:
            logger.error(f"[ONBOARDING] Error generating organization description: {e}")
            return self._mock_description(organization_name, language)

    def _parse_json_response(self, response_text: str) -> dict[str, Any]:
        """Parse JSON from AI response, handling markdown code blocks."""
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]

        return json.loads(response_text.strip())

    def _mock_description(
        self, organization_name: str, language: str = "en"
    ) -> dict[str, str]:
        """Generate mock organization description for testing."""
        if language == "fr":
            return {
                "organization_description": f"{organization_name} est une entreprise innovante qui se concentre sur la création de valeur pour ses clients grâce à des solutions modernes et efficaces.",
                "industry": "Technologie",
            }
        return {
            "organization_description": f"{organization_name} is an innovative organization focused on creating value for its customers through modern and effective solutions.",
            "industry": "Technology",
        }


# Singleton instance
organization_generation_service = OrganizationGenerationService()
