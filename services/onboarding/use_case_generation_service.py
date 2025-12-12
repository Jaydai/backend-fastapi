"""
Use Case Generation Service

Handles AI-powered generation of AI use cases tailored to the user's role.
Uses OpenAI to generate specific, actionable use cases.
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


class UseCaseGenerationService:
    """
    Service for generating AI use cases tailored to user roles.

    Features:
    - Generate role-specific AI use cases
    - Multi-language support (en, fr)
    - Category-based organization
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

    def generate_use_cases(
        self,
        job_title: str,
        job_description: str,
        organization_description: str | None = None,
        industry: str | None = None,
        language: str = "en",
    ) -> list[dict[str, str]]:
        """
        Generate AI use cases tailored to the user's role and organization.

        Args:
            job_title: The user's job title
            job_description: Description of the job
            organization_description: Organization description for context (optional)
            industry: Industry for context (optional)
            language: Language code ('en' or 'fr')

        Returns:
            List of 8-10 AI use cases with title, description, and category
        """
        if self.mock_mode:
            return self._mock_use_cases(job_title, language)

        lang_instruction = (
            "Respond in French." if language == "fr" else "Respond in English."
        )
        categories_note = (
            "One of: Rédaction, Recherche, Analyse, Communication, Planification, Automatisation, Apprentissage, Créatif"
            if language == "fr"
            else "One of: Writing, Research, Analysis, Communication, Planning, Automation, Learning, Creative"
        )

        context_parts = [
            f"Job title: {job_title}",
            f"Role description: {job_description}",
        ]
        if organization_description:
            context_parts.append(f"Organization: {organization_description}")
        if industry:
            context_parts.append(f"Industry: {industry}")

        context = "\n".join(context_parts)

        prompt = f"""For a professional with this profile:
{context}

Generate 8-10 specific, practical ways they could use AI to be more productive. Focus on real daily tasks and workflows relevant to their specific role and industry.

{lang_instruction}

Respond in this exact JSON format:
{{
    "use_cases": [
        {{
            "title": "Short action title (e.g., 'Draft client proposals')",
            "description": "A detailed explanation (2-3 sentences) of how AI helps with this specific task and the benefits",
            "category": "{categories_note}"
        }}
    ]
}}

Make each use case highly specific and actionable for a {job_title}. Consider their industry context. Avoid generic suggestions."""

        try:
            response = self.client.responses.create(
                model=GENERATION_MODEL,
                input=[{"role": "user", "content": prompt}],
                temperature=GENERATION_TEMPERATURE,
            )

            response_text = response.output_text.strip()
            parsed = self._parse_json_response(response_text)
            use_cases = parsed.get("use_cases", [])

            logger.info(
                f"[ONBOARDING] Generated {len(use_cases)} AI use cases for: {job_title}"
            )
            return use_cases[:10]  # Ensure max 10

        except Exception as e:
            logger.error(f"[ONBOARDING] Error generating AI use cases: {e}")
            return self._mock_use_cases(job_title, language)

    def _parse_json_response(self, response_text: str) -> dict[str, Any]:
        """Parse JSON from AI response, handling markdown code blocks."""
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]

        return json.loads(response_text.strip())

    def _mock_use_cases(
        self, job_title: str, language: str = "en"
    ) -> list[dict[str, str]]:
        """Generate mock AI use cases for testing."""
        job_lower = job_title.lower()

        if language == "fr":
            return self._mock_use_cases_fr(job_lower)
        return self._mock_use_cases_en(job_lower)

    def _mock_use_cases_en(self, job_lower: str) -> list[dict[str, str]]:
        """Generate English mock use cases."""
        if "engineer" in job_lower or "developer" in job_lower:
            return [
                {
                    "title": "Write technical documentation",
                    "description": "Automatically generate clear documentation for functions, APIs, and modules. AI can create docstrings, README files, and user documentation.",
                    "category": "Writing",
                },
                {
                    "title": "Debug complex errors",
                    "description": "Quickly analyze error messages and stack traces to identify root causes. AI can suggest fixes and explain why the error occurred.",
                    "category": "Analysis",
                },
                {
                    "title": "Code review assistance",
                    "description": "Get detailed suggestions to improve code quality, detect potential bugs, and identify security vulnerabilities before production.",
                    "category": "Analysis",
                },
                {
                    "title": "Write unit tests",
                    "description": "Generate comprehensive test cases covering edge cases. AI can create tests for different frameworks and ensure good coverage.",
                    "category": "Automation",
                },
                {
                    "title": "Explain legacy code",
                    "description": "Quickly understand complex and inherited codebases. AI can summarize logic, identify patterns, and document behaviors.",
                    "category": "Learning",
                },
                {
                    "title": "Draft technical specs",
                    "description": "Create detailed technical specifications and design documents from general requirements.",
                    "category": "Writing",
                },
                {
                    "title": "Optimize SQL queries",
                    "description": "Analyze and improve database query performance. AI can suggest indexes and rewrite inefficient queries.",
                    "category": "Analysis",
                },
                {
                    "title": "Generate boilerplate code",
                    "description": "Quickly create base code for new components following existing project patterns.",
                    "category": "Automation",
                },
            ]
        elif "product" in job_lower or "manager" in job_lower:
            return [
                {
                    "title": "Write PRDs",
                    "description": "Draft comprehensive product requirements documents that clearly communicate features and user stories to engineering teams.",
                    "category": "Writing",
                },
                {
                    "title": "Analyze user feedback",
                    "description": "Synthesize patterns from user interviews, surveys, and support tickets to identify key themes and insights.",
                    "category": "Research",
                },
                {
                    "title": "Competitive research",
                    "description": "Quickly gather and summarize competitive intelligence, feature comparisons, and market positioning analysis.",
                    "category": "Research",
                },
                {
                    "title": "Draft release notes",
                    "description": "Create clear, user-friendly release communications that highlight key changes for different audiences.",
                    "category": "Writing",
                },
                {
                    "title": "Meeting summaries",
                    "description": "Transform meeting notes into structured summaries with key decisions and action items clearly identified.",
                    "category": "Communication",
                },
                {
                    "title": "Roadmap planning",
                    "description": "Help prioritize features based on impact and effort, organize quarterly roadmaps.",
                    "category": "Planning",
                },
                {
                    "title": "Write user stories",
                    "description": "Generate well-structured user stories with clear acceptance criteria from high-level descriptions.",
                    "category": "Writing",
                },
                {
                    "title": "Stakeholder updates",
                    "description": "Create executive summaries and progress reports tailored to different stakeholder audiences.",
                    "category": "Communication",
                },
            ]
        elif "market" in job_lower:
            return [
                {
                    "title": "Write blog posts",
                    "description": "Create engaging, SEO-optimized content for your company blog that drives traffic.",
                    "category": "Writing",
                },
                {
                    "title": "Social media copy",
                    "description": "Generate compelling posts optimized for each platform with appropriate tone and CTAs.",
                    "category": "Creative",
                },
                {
                    "title": "Email campaigns",
                    "description": "Draft email sequences with personalized content, compelling subject lines, and clear CTAs.",
                    "category": "Writing",
                },
                {
                    "title": "SEO optimization",
                    "description": "Improve content for search engine visibility with keyword suggestions and meta descriptions.",
                    "category": "Analysis",
                },
                {
                    "title": "Campaign analysis",
                    "description": "Analyze marketing metrics, identify trends, and generate insights to optimize performance.",
                    "category": "Analysis",
                },
                {
                    "title": "Ad copy variations",
                    "description": "Create multiple A/B test variations for advertisements with different angles.",
                    "category": "Creative",
                },
                {
                    "title": "Customer personas",
                    "description": "Develop detailed customer personas based on data to guide targeting decisions.",
                    "category": "Research",
                },
                {
                    "title": "Competitive positioning",
                    "description": "Analyze competitor messaging to identify differentiation opportunities.",
                    "category": "Research",
                },
            ]
        else:
            return [
                {
                    "title": "Draft professional emails",
                    "description": "Compose clear, professional emails quickly with the right tone for each recipient.",
                    "category": "Communication",
                },
                {
                    "title": "Create meeting summaries",
                    "description": "Transform raw meeting notes into structured summaries with key points and action items.",
                    "category": "Writing",
                },
                {
                    "title": "Research topics quickly",
                    "description": "Gather and synthesize information on any subject rapidly from multiple sources.",
                    "category": "Research",
                },
                {
                    "title": "Build presentations",
                    "description": "Generate presentation outlines, write slide content, and suggest visualizations.",
                    "category": "Creative",
                },
                {
                    "title": "Analyze data patterns",
                    "description": "Identify trends and patterns in your data. AI can create preliminary analyses.",
                    "category": "Analysis",
                },
                {
                    "title": "Write structured reports",
                    "description": "Create clear, structured reports from raw data adapted to your audience.",
                    "category": "Writing",
                },
                {
                    "title": "Plan complex projects",
                    "description": "Break down complex projects into manageable tasks with estimates and dependencies.",
                    "category": "Planning",
                },
                {
                    "title": "Translate documents",
                    "description": "Quickly translate documents while preserving professional context and nuances.",
                    "category": "Communication",
                },
            ]

    def _mock_use_cases_fr(self, job_lower: str) -> list[dict[str, str]]:
        """Generate French mock use cases."""
        if "engineer" in job_lower or "developer" in job_lower or "ingénieur" in job_lower or "développeur" in job_lower:
            return [
                {
                    "title": "Rédiger la documentation technique",
                    "description": "Générer automatiquement une documentation claire pour les fonctions, APIs et modules.",
                    "category": "Rédaction",
                },
                {
                    "title": "Débugger les erreurs complexes",
                    "description": "Analyser rapidement les messages d'erreur pour identifier la cause racine.",
                    "category": "Analyse",
                },
                {
                    "title": "Assistance code review",
                    "description": "Obtenir des suggestions pour améliorer la qualité du code et détecter les bugs potentiels.",
                    "category": "Analyse",
                },
                {
                    "title": "Écrire des tests unitaires",
                    "description": "Générer des cas de test complets couvrant les cas limites.",
                    "category": "Automatisation",
                },
                {
                    "title": "Expliquer du code legacy",
                    "description": "Comprendre rapidement des codebases complexes et du code hérité.",
                    "category": "Apprentissage",
                },
                {
                    "title": "Rédiger des specs techniques",
                    "description": "Créer des spécifications techniques détaillées à partir de requirements généraux.",
                    "category": "Rédaction",
                },
                {
                    "title": "Optimiser les requêtes SQL",
                    "description": "Analyser et améliorer les performances des requêtes de base de données.",
                    "category": "Analyse",
                },
                {
                    "title": "Générer du boilerplate code",
                    "description": "Créer rapidement du code de base pour de nouveaux composants.",
                    "category": "Automatisation",
                },
            ]
        else:
            return [
                {
                    "title": "Rédiger des emails professionnels",
                    "description": "Composer rapidement des emails clairs et professionnels adaptés au contexte.",
                    "category": "Communication",
                },
                {
                    "title": "Créer des résumés de réunion",
                    "description": "Transformer des notes de réunion en résumés structurés avec actions à suivre.",
                    "category": "Rédaction",
                },
                {
                    "title": "Rechercher des informations",
                    "description": "Rassembler et synthétiser rapidement des informations sur n'importe quel sujet.",
                    "category": "Recherche",
                },
                {
                    "title": "Créer des présentations",
                    "description": "Générer des plans de présentation et rédiger le contenu des slides.",
                    "category": "Créatif",
                },
                {
                    "title": "Analyser des données",
                    "description": "Identifier les tendances et patterns dans vos données.",
                    "category": "Analyse",
                },
                {
                    "title": "Rédiger des rapports",
                    "description": "Créer des rapports clairs et structurés à partir de données brutes.",
                    "category": "Rédaction",
                },
                {
                    "title": "Planifier des projets",
                    "description": "Décomposer des projets complexes en tâches gérables avec estimations.",
                    "category": "Planification",
                },
                {
                    "title": "Traduire des documents",
                    "description": "Traduire rapidement des documents tout en préservant le contexte professionnel.",
                    "category": "Communication",
                },
            ]


# Singleton instance
use_case_generation_service = UseCaseGenerationService()
