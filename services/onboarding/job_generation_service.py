"""
Job Generation Service

Handles AI-powered job description and user blocks generation.
Uses OpenAI to generate job profiles and personalized blocks.
"""

import json
import logging
import os
import uuid
from typing import Any

from openai import OpenAI

logger = logging.getLogger(__name__)

# Configuration
GENERATION_MODEL = "gpt-4.1-nano"
GENERATION_TEMPERATURE = 0.7


class JobGenerationService:
    """
    Service for generating job descriptions and user blocks using AI.

    Features:
    - Generate job descriptions from LinkedIn URL or manual input
    - Generate personalized context, role, and goal blocks
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

    def generate_job_description(
        self,
        linkedin_url: str | None = None,
        manual_description: str | None = None,
        organization_description: str | None = None,
        language: str = "en",
    ) -> dict[str, Any]:
        """
        Generate a job description from LinkedIn URL or manual input.

        Args:
            linkedin_url: User's LinkedIn profile URL (optional)
            manual_description: Manual job description (optional)
            organization_description: Organization description for context (optional)
            language: Language code ('en' or 'fr')

        Returns:
            Dict with job_title, job_description, and seniority_level
        """
        if self.mock_mode:
            return self._mock_job_description(manual_description, language)

        lang_instruction = (
            "Respond in French." if language == "fr" else "Respond in English."
        )

        context_parts = []
        if linkedin_url:
            context_parts.append(f"LinkedIn profile: {linkedin_url}")
        if manual_description:
            context_parts.append(f"User description: {manual_description}")
        if organization_description:
            context_parts.append(f"Organization context: {organization_description}")

        context = (
            "\n".join(context_parts)
            if context_parts
            else "No specific information provided"
        )

        prompt = f"""Based on this information about a professional:
{context}

Generate a structured job profile. If a LinkedIn URL is provided, infer details from the URL structure. If manual description is provided, structure it professionally.

{lang_instruction}

Respond in this exact JSON format:
{{
    "job_title": "Professional job title",
    "job_description": "A 2-3 sentence description of their role and responsibilities",
    "seniority_level": "junior/mid/senior/lead/executive"
}}"""

        try:
            response = self.client.responses.create(
                model=GENERATION_MODEL,
                input=[{"role": "user", "content": prompt}],
                temperature=GENERATION_TEMPERATURE,
            )

            response_text = response.output_text.strip()
            parsed = self._parse_json_response(response_text)

            logger.info("[ONBOARDING] Generated job description")
            return parsed

        except Exception as e:
            logger.error(f"[ONBOARDING] Error generating job description: {e}")
            return self._mock_job_description(manual_description, language)

    def generate_user_blocks(
        self,
        job_title: str,
        linkedin_url: str | None = None,
        manual_description: str | None = None,
        organization_name: str | None = None,
        organization_description: str | None = None,
        industry: str | None = None,
        language: str = "en",
    ) -> dict[str, Any]:
        """
        Generate user blocks: context block, role blocks, and goal blocks.

        Args:
            job_title: The user's job title
            linkedin_url: User's LinkedIn profile URL (optional)
            manual_description: Manual job description (optional)
            organization_name: Organization name for context (optional)
            organization_description: Organization description for context (optional)
            industry: Industry for context (optional)
            language: Language code ('en' or 'fr')

        Returns:
            Dict with context_block, role_blocks, goal_blocks, job_title, job_description, seniority_level
        """
        if self.mock_mode:
            return self._mock_user_blocks(job_title, organization_name, language)

        lang_instruction = (
            "Respond in French." if language == "fr" else "Respond in English."
        )

        context_parts = [f"Job title: {job_title}"]
        if linkedin_url:
            context_parts.append(f"LinkedIn: {linkedin_url}")
        if manual_description:
            context_parts.append(f"Job details: {manual_description}")
        if organization_name:
            context_parts.append(f"Organization: {organization_name}")
        if organization_description:
            context_parts.append(f"Organization description: {organization_description}")
        if industry:
            context_parts.append(f"Industry: {industry}")

        context = "\n".join(context_parts)

        prompt = f"""Based on this professional profile:
{context}

Generate personalized blocks for this user. These blocks will help them use AI more effectively.

{lang_instruction}

Respond in this exact JSON format:
{{
    "job_title": "The formatted job title",
    "job_description": "A 2-3 sentence description of what this professional does, their key responsibilities, and their typical tasks",
    "seniority_level": "junior/mid/senior/lead/executive",
    "context_block": {{
        "title": "I work as...",
        "description": "A first-person narrative (2-3 sentences) describing who they are professionally, what they do, and their context. Start with 'I am a...' or 'Je suis...' depending on language."
    }},
    "role_blocks": [
        {{
            "title": "Short role name (e.g., 'SEO Specialist')",
            "description": "What this expert does and how they can help (1-2 sentences)",
            "icon": "A single relevant emoji",
            "category": "A category like Marketing, Engineering, Design, Finance, Operations, Strategy, Analytics, Communication"
        }}
    ],
    "goal_blocks": [
        {{
            "title": "Short goal name (e.g., 'Improve Conversion Rate')",
            "description": "What achieving this goal means and why it matters (1-2 sentences)",
            "icon": "A single relevant emoji",
            "category": "A category like Growth, Efficiency, Quality, Innovation, Cost, Revenue, Team, Customer"
        }}
    ]
}}

Important:
- Generate exactly 3 role_blocks (expert personas the user might want AI to act as)
- Generate exactly 3 goal_blocks (professional objectives relevant to this role)
- Make roles and goals highly specific to this job title and industry
- Each block should be actionable and useful for AI interactions"""

        try:
            response = self.client.responses.create(
                model=GENERATION_MODEL,
                input=[{"role": "user", "content": prompt}],
                temperature=GENERATION_TEMPERATURE,
            )

            response_text = response.output_text.strip()
            parsed = self._parse_json_response(response_text)

            # Add IDs and types to blocks
            result = self._format_blocks_response(parsed, job_title)

            logger.info(f"[ONBOARDING] Generated user blocks for: {job_title}")
            return result

        except Exception as e:
            logger.error(f"[ONBOARDING] Error generating user blocks: {e}")
            return self._mock_user_blocks(job_title, organization_name, language)

    def _format_blocks_response(
        self, parsed: dict[str, Any], job_title: str
    ) -> dict[str, Any]:
        """Format the parsed AI response into the expected structure with IDs."""
        context_block = {
            "id": str(uuid.uuid4()),
            "type": "context",
            "title": parsed["context_block"]["title"],
            "description": parsed["context_block"]["description"],
            "icon": "briefcase",
        }

        role_blocks = []
        for rb in parsed.get("role_blocks", [])[:3]:
            role_blocks.append(
                {
                    "id": str(uuid.uuid4()),
                    "type": "role",
                    "title": rb["title"],
                    "description": rb["description"],
                    "icon": rb.get("icon", "user"),
                    "category": rb.get("category", "General"),
                }
            )

        goal_blocks = []
        for gb in parsed.get("goal_blocks", [])[:3]:
            goal_blocks.append(
                {
                    "id": str(uuid.uuid4()),
                    "type": "goal",
                    "title": gb["title"],
                    "description": gb["description"],
                    "icon": gb.get("icon", "target"),
                    "category": gb.get("category", "General"),
                }
            )

        return {
            "context_block": context_block,
            "role_blocks": role_blocks,
            "goal_blocks": goal_blocks,
            "job_title": parsed.get("job_title", job_title),
            "job_description": parsed.get("job_description", ""),
            "seniority_level": parsed.get("seniority_level", "mid"),
        }

    def _parse_json_response(self, response_text: str) -> dict[str, Any]:
        """Parse JSON from AI response, handling markdown code blocks."""
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]

        return json.loads(response_text.strip())

    def _mock_job_description(
        self, manual_description: str | None, language: str = "en"
    ) -> dict[str, Any]:
        """Generate mock job description for testing."""
        if manual_description:
            title = (
                manual_description.split()[0].title()
                if manual_description
                else "Professional"
            )
        else:
            title = "Professional"

        if language == "fr":
            return {
                "job_title": title,
                "job_description": "Responsable de la gestion de projets et de la coordination des équipes pour atteindre les objectifs de l'entreprise.",
                "seniority_level": "mid",
            }
        return {
            "job_title": title,
            "job_description": "Responsible for managing projects and coordinating teams to achieve company objectives.",
            "seniority_level": "mid",
        }

    def _mock_user_blocks(
        self,
        job_title: str,
        organization_name: str | None,
        language: str = "en",
    ) -> dict[str, Any]:
        """Generate mock user blocks for testing."""
        job_lower = job_title.lower()

        if language == "fr":
            org_part = f" chez {organization_name}" if organization_name else ""
            context_desc = f"Je suis {job_title}{org_part}. Je suis responsable de la stratégie et de l'exécution des initiatives clés de mon domaine. Mon travail implique la coordination d'équipes et la livraison de résultats mesurables."
            role_blocks, goal_blocks = self._get_mock_blocks_fr(job_lower)
            context_title = "Je travaille comme..."
            job_desc = f"Responsable des initiatives clés et de la coordination d'équipe en tant que {job_title}."
        else:
            org_part = f" at {organization_name}" if organization_name else ""
            context_desc = f"I am a {job_title}{org_part}. I am responsible for strategy and execution of key initiatives in my domain. My work involves coordinating teams and delivering measurable results."
            role_blocks, goal_blocks = self._get_mock_blocks_en(job_lower)
            context_title = "I work as..."
            job_desc = f"Responsible for key initiatives and team coordination as a {job_title}."

        context_block = {
            "id": str(uuid.uuid4()),
            "type": "context",
            "title": context_title,
            "description": context_desc,
            "icon": "briefcase",
        }

        return {
            "context_block": context_block,
            "role_blocks": role_blocks,
            "goal_blocks": goal_blocks,
            "job_title": job_title,
            "job_description": job_desc,
            "seniority_level": "mid",
        }

    def _get_mock_blocks_en(
        self, job_lower: str
    ) -> tuple[list[dict], list[dict]]:
        """Get mock blocks for English language."""
        if "engineer" in job_lower or "developer" in job_lower:
            role_blocks = [
                {
                    "id": str(uuid.uuid4()),
                    "type": "role",
                    "title": "Code Reviewer",
                    "description": "Reviews code for quality, security, and best practices.",
                    "icon": "🔍",
                    "category": "Engineering",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "role",
                    "title": "Tech Writer",
                    "description": "Creates clear technical documentation and guides.",
                    "icon": "📝",
                    "category": "Documentation",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "role",
                    "title": "DevOps Expert",
                    "description": "Optimizes deployment and infrastructure processes.",
                    "icon": "🚀",
                    "category": "Operations",
                },
            ]
            goal_blocks = [
                {
                    "id": str(uuid.uuid4()),
                    "type": "goal",
                    "title": "Code Quality",
                    "description": "Improve codebase quality and reduce technical debt.",
                    "icon": "✅",
                    "category": "Quality",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "goal",
                    "title": "Ship Faster",
                    "description": "Reduce time-to-production for new features.",
                    "icon": "⚡",
                    "category": "Efficiency",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "goal",
                    "title": "System Reliability",
                    "description": "Improve uptime and reduce incident response time.",
                    "icon": "🛡️",
                    "category": "Quality",
                },
            ]
        elif "market" in job_lower or "marketing" in job_lower:
            role_blocks = [
                {
                    "id": str(uuid.uuid4()),
                    "type": "role",
                    "title": "SEO Specialist",
                    "description": "Expert in search engine optimization and keyword strategies.",
                    "icon": "🔍",
                    "category": "Marketing",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "role",
                    "title": "Copywriter",
                    "description": "Crafts compelling and persuasive marketing copy.",
                    "icon": "✍️",
                    "category": "Content",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "role",
                    "title": "Data Analyst",
                    "description": "Analyzes marketing data and identifies trends.",
                    "icon": "📊",
                    "category": "Analytics",
                },
            ]
            goal_blocks = [
                {
                    "id": str(uuid.uuid4()),
                    "type": "goal",
                    "title": "Improve Conversion Rate",
                    "description": "Increase conversions by optimizing the user journey.",
                    "icon": "📈",
                    "category": "Growth",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "goal",
                    "title": "Content Strategy",
                    "description": "Develop a comprehensive editorial calendar.",
                    "icon": "📋",
                    "category": "Strategy",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "goal",
                    "title": "Campaign ROI",
                    "description": "Maximize return on investment from marketing campaigns.",
                    "icon": "💰",
                    "category": "Revenue",
                },
            ]
        else:
            role_blocks = [
                {
                    "id": str(uuid.uuid4()),
                    "type": "role",
                    "title": "Strategic Consultant",
                    "description": "Advises on strategic decisions and process optimization.",
                    "icon": "🎯",
                    "category": "Strategy",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "role",
                    "title": "Professional Writer",
                    "description": "Writes clear and impactful professional documents.",
                    "icon": "✍️",
                    "category": "Communication",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "role",
                    "title": "Analyst",
                    "description": "Analyzes data and generates actionable insights.",
                    "icon": "📊",
                    "category": "Analytics",
                },
            ]
            goal_blocks = [
                {
                    "id": str(uuid.uuid4()),
                    "type": "goal",
                    "title": "Team Productivity",
                    "description": "Improve team efficiency and collaboration.",
                    "icon": "⚡",
                    "category": "Efficiency",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "goal",
                    "title": "Deliverable Quality",
                    "description": "Ensure quality and consistency of deliverables.",
                    "icon": "✅",
                    "category": "Quality",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "goal",
                    "title": "Innovation",
                    "description": "Identify and implement innovative solutions.",
                    "icon": "💡",
                    "category": "Innovation",
                },
            ]

        return role_blocks, goal_blocks

    def _get_mock_blocks_fr(
        self, job_lower: str
    ) -> tuple[list[dict], list[dict]]:
        """Get mock blocks for French language."""
        if "market" in job_lower or "marketing" in job_lower:
            role_blocks = [
                {
                    "id": str(uuid.uuid4()),
                    "type": "role",
                    "title": "Spécialiste SEO",
                    "description": "Expert en optimisation pour les moteurs de recherche.",
                    "icon": "🔍",
                    "category": "Marketing",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "role",
                    "title": "Copywriter",
                    "description": "Rédige des textes marketing percutants et persuasifs.",
                    "icon": "✍️",
                    "category": "Contenu",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "role",
                    "title": "Analyste Data",
                    "description": "Analyse les données marketing et identifie les tendances.",
                    "icon": "📊",
                    "category": "Analytics",
                },
            ]
            goal_blocks = [
                {
                    "id": str(uuid.uuid4()),
                    "type": "goal",
                    "title": "Améliorer le taux de conversion",
                    "description": "Augmenter les conversions en optimisant le parcours utilisateur.",
                    "icon": "📈",
                    "category": "Croissance",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "goal",
                    "title": "Stratégie de contenu",
                    "description": "Développer un calendrier éditorial complet.",
                    "icon": "📋",
                    "category": "Stratégie",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "goal",
                    "title": "ROI des campagnes",
                    "description": "Maximiser le retour sur investissement des campagnes.",
                    "icon": "💰",
                    "category": "Revenue",
                },
            ]
        else:
            role_blocks = [
                {
                    "id": str(uuid.uuid4()),
                    "type": "role",
                    "title": "Consultant Stratégique",
                    "description": "Conseille sur les décisions stratégiques.",
                    "icon": "🎯",
                    "category": "Stratégie",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "role",
                    "title": "Rédacteur Pro",
                    "description": "Rédige des documents professionnels clairs.",
                    "icon": "✍️",
                    "category": "Communication",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "role",
                    "title": "Analyste",
                    "description": "Analyse les données et génère des insights.",
                    "icon": "📊",
                    "category": "Analytics",
                },
            ]
            goal_blocks = [
                {
                    "id": str(uuid.uuid4()),
                    "type": "goal",
                    "title": "Productivité équipe",
                    "description": "Améliorer l'efficacité et la collaboration.",
                    "icon": "⚡",
                    "category": "Efficacité",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "goal",
                    "title": "Qualité livrables",
                    "description": "Assurer la qualité des livrables.",
                    "icon": "✅",
                    "category": "Qualité",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "goal",
                    "title": "Innovation",
                    "description": "Identifier et implémenter des solutions innovantes.",
                    "icon": "💡",
                    "category": "Innovation",
                },
            ]

        return role_blocks, goal_blocks


# Singleton instance
job_generation_service = JobGenerationService()
