"""
Onboarding Chat Service

Handles AI-powered onboarding conversations using OpenAI Responses API.
Generates company descriptions, job descriptions, AI use cases, and personalizes the onboarding experience.
Supports multiple languages (en, fr).
"""

import json
import logging
import os
from typing import Any

from openai import OpenAI

logger = logging.getLogger(__name__)

# Configuration
ONBOARDING_MODEL = "gpt-4.1-nano"
GENERATION_TEMPERATURE = 0.7
MOCK_MODE = False  # Set to True for testing without OpenAI


class OnboardingChatService:
    """
    Service for AI-powered onboarding flow.

    Features:
    - Generate company descriptions from name/URL
    - Generate job descriptions from LinkedIn URL or manual input
    - Generate AI use cases tailored to the role
    - Multi-language support (en, fr)
    - Mock mode for testing without API key
    """

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and not MOCK_MODE:
            self.client = OpenAI()
            self.mock_mode = False
        else:
            self.client = None
            self.mock_mode = True
            logger.warning("OpenAI API key not set or mock mode enabled - using mock responses")

    def generate_company_description(
        self,
        company_name: str,
        website_url: str | None = None,
        linkedin_url: str | None = None,
        language: str = "en",
    ) -> dict[str, str]:
        """
        Generate a company description based on name and URLs.

        Args:
            company_name: Name of the company
            website_url: Company website URL (optional)
            linkedin_url: Company LinkedIn URL (optional)
            language: Language code ('en' or 'fr')

        Returns:
            Dict with company_description and industry
        """
        if self.mock_mode:
            return self._mock_company_description(company_name, language)

        lang_instruction = "Respond in French." if language == "fr" else "Respond in English."

        context_parts = [f"Company name: {company_name}"]
        if website_url:
            context_parts.append(f"Website: {website_url}")
        if linkedin_url:
            context_parts.append(f"LinkedIn: {linkedin_url}")

        context = "\n".join(context_parts)

        prompt = f"""Based on this company information:
{context}

Generate a brief, professional description of this company. If you recognize the company, provide accurate information. If not, create a plausible description based on the name.

{lang_instruction}

Respond in this exact JSON format:
{{
    "company_description": "A 2-3 sentence description of what the company does, its industry, and its focus.",
    "industry": "The primary industry (e.g., Technology, Finance, Healthcare, Retail, etc.)"
}}"""

        try:
            response = self.client.responses.create(
                model=ONBOARDING_MODEL,
                input=[{"role": "user", "content": prompt}],
                temperature=GENERATION_TEMPERATURE,
            )

            response_text = response.output_text.strip()

            # Handle markdown code blocks
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]

            parsed = json.loads(response_text)

            logger.info(f"[ONBOARDING] Generated company description for: {company_name}")
            return parsed

        except Exception as e:
            logger.error(f"[ONBOARDING] Error generating company description: {e}")
            return self._mock_company_description(company_name, language)

    def generate_job_description(
        self,
        linkedin_url: str | None = None,
        manual_description: str | None = None,
        company_description: str | None = None,
        language: str = "en",
    ) -> dict[str, Any]:
        """
        Generate a job description from LinkedIn URL or manual input.

        Args:
            linkedin_url: User's LinkedIn profile URL (optional)
            manual_description: Manual job description (optional)
            company_description: Company description for context (optional)
            language: Language code ('en' or 'fr')

        Returns:
            Dict with job_title, job_description, and seniority_level
        """
        if self.mock_mode:
            return self._mock_job_description(manual_description, language)

        lang_instruction = "Respond in French." if language == "fr" else "Respond in English."

        context_parts = []
        if linkedin_url:
            context_parts.append(f"LinkedIn profile: {linkedin_url}")
        if manual_description:
            context_parts.append(f"User description: {manual_description}")
        if company_description:
            context_parts.append(f"Company context: {company_description}")

        context = "\n".join(context_parts) if context_parts else "No specific information provided"

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
                model=ONBOARDING_MODEL,
                input=[{"role": "user", "content": prompt}],
                temperature=GENERATION_TEMPERATURE,
            )

            response_text = response.output_text.strip()

            # Handle markdown code blocks
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]

            parsed = json.loads(response_text)

            logger.info(f"[ONBOARDING] Generated job description")
            return parsed

        except Exception as e:
            logger.error(f"[ONBOARDING] Error generating job description: {e}")
            return self._mock_job_description(manual_description, language)

    def generate_ai_use_cases(
        self,
        job_title: str,
        job_description: str,
        company_description: str | None = None,
        industry: str | None = None,
        language: str = "en",
    ) -> list[dict[str, str]]:
        """
        Generate AI use cases tailored to the user's role and company.

        Args:
            job_title: The user's job title
            job_description: Description of the job
            company_description: Company description for context (optional)
            industry: Industry for context (optional)
            language: Language code ('en' or 'fr')

        Returns:
            List of 8-10 AI use cases with title, description, and category
        """
        if self.mock_mode:
            return self._mock_ai_use_cases(job_title, language)

        lang_instruction = "Respond in French." if language == "fr" else "Respond in English."
        categories_note = (
            "One of: Rédaction, Recherche, Analyse, Communication, Planification, Automatisation, Apprentissage, Créatif"
            if language == "fr"
            else "One of: Writing, Research, Analysis, Communication, Planning, Automation, Learning, Creative"
        )

        context_parts = [
            f"Job title: {job_title}",
            f"Role description: {job_description}",
        ]
        if company_description:
            context_parts.append(f"Company: {company_description}")
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
                model=ONBOARDING_MODEL,
                input=[{"role": "user", "content": prompt}],
                temperature=GENERATION_TEMPERATURE,
            )

            response_text = response.output_text.strip()

            # Handle markdown code blocks
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]

            parsed = json.loads(response_text)
            use_cases = parsed.get("use_cases", [])

            logger.info(f"[ONBOARDING] Generated {len(use_cases)} AI use cases for: {job_title}")
            return use_cases[:10]  # Ensure max 10

        except Exception as e:
            logger.error(f"[ONBOARDING] Error generating AI use cases: {e}")
            return self._mock_ai_use_cases(job_title, language)

    def generate_onboarding_summary(
        self,
        company_name: str | None,
        company_description: str | None,
        industry: str | None,
        job_title: str,
        job_description: str,
        selected_use_cases: list[str],
        ai_dreams: str | None,
        user_message: str | None,
        signup_source: str,
    ) -> dict[str, Any]:
        """
        Generate a summary of the onboarding data.

        Returns structured data to store in the database.
        """
        summary_parts = [f"A {job_title}"]
        if company_name:
            summary_parts.append(f"at {company_name}")
        if industry:
            summary_parts.append(f"in {industry}")

        summary = " ".join(summary_parts)
        summary += " interested in using AI for: "

        if selected_use_cases:
            summary += ", ".join(selected_use_cases[:4])
            if len(selected_use_cases) > 4:
                summary += f" and {len(selected_use_cases) - 4} more areas"
        else:
            summary += "exploring AI productivity tools"

        if ai_dreams:
            summary += f". Dreams of: {ai_dreams[:100]}"

        return {
            "summary": summary,
            "extracted_data": {
                "company_name": company_name,
                "company_description": company_description,
                "job_type": job_title,
                "job_description": job_description,
                "job_industry": industry,
                "interests": selected_use_cases,
                "ai_dreams": ai_dreams,
                "user_message": user_message,
                "signup_source": signup_source,
            }
        }

    def _mock_company_description(self, company_name: str, language: str = "en") -> dict[str, str]:
        """Generate mock company description for testing."""
        if language == "fr":
            return {
                "company_description": f"{company_name} est une entreprise innovante qui se concentre sur la création de valeur pour ses clients grâce à des solutions modernes et efficaces.",
                "industry": "Technologie"
            }
        return {
            "company_description": f"{company_name} is an innovative company focused on creating value for its customers through modern and effective solutions.",
            "industry": "Technology"
        }

    def _mock_job_description(self, manual_description: str | None, language: str = "en") -> dict[str, Any]:
        """Generate mock job description for testing."""
        if manual_description:
            title = manual_description.split()[0].title() if manual_description else "Professional"
        else:
            title = "Professional"

        if language == "fr":
            return {
                "job_title": title,
                "job_description": f"Responsable de la gestion de projets et de la coordination des équipes pour atteindre les objectifs de l'entreprise.",
                "seniority_level": "mid"
            }
        return {
            "job_title": title,
            "job_description": f"Responsible for managing projects and coordinating teams to achieve company objectives.",
            "seniority_level": "mid"
        }

    def _mock_ai_use_cases(self, job_title: str, language: str = "en") -> list[dict[str, str]]:
        """Generate mock AI use cases for testing."""
        job_lower = job_title.lower()

        if language == "fr":
            if "engineer" in job_lower or "developer" in job_lower or "ingénieur" in job_lower or "développeur" in job_lower:
                return [
                    {"title": "Rédiger la documentation technique", "description": "Générer automatiquement une documentation claire et complète pour les fonctions, APIs et modules. L'IA peut créer des docstrings, des fichiers README et de la documentation utilisateur.", "category": "Rédaction"},
                    {"title": "Débugger les erreurs complexes", "description": "Analyser rapidement les messages d'erreur et stack traces pour identifier la cause racine. L'IA peut suggérer des corrections et expliquer pourquoi l'erreur s'est produite.", "category": "Analyse"},
                    {"title": "Assistance code review", "description": "Obtenir des suggestions détaillées pour améliorer la qualité du code, détecter les bugs potentiels et identifier les vulnérabilités de sécurité avant la production.", "category": "Analyse"},
                    {"title": "Écrire des tests unitaires", "description": "Générer des cas de test complets couvrant les cas limites et les scénarios edge. L'IA peut créer des tests pour différents frameworks et assurer une bonne couverture.", "category": "Automatisation"},
                    {"title": "Expliquer du code legacy", "description": "Comprendre rapidement des codebases complexes et du code hérité. L'IA peut résumer la logique, identifier les patterns et documenter les comportements.", "category": "Apprentissage"},
                    {"title": "Rédiger des specs techniques", "description": "Créer des spécifications techniques détaillées et des documents de conception à partir de requirements généraux. Structurer les décisions d'architecture.", "category": "Rédaction"},
                    {"title": "Optimiser les requêtes SQL", "description": "Analyser et améliorer les performances des requêtes de base de données. L'IA peut suggérer des index et réécrire des requêtes inefficaces.", "category": "Analyse"},
                    {"title": "Générer du boilerplate code", "description": "Créer rapidement du code de base pour de nouveaux composants, services ou fonctionnalités en suivant les patterns existants du projet.", "category": "Automatisation"},
                ]
            else:
                return [
                    {"title": "Rédiger des emails professionnels", "description": "Composer rapidement des emails clairs et professionnels adaptés au contexte. L'IA ajuste le ton selon le destinataire et l'objectif du message.", "category": "Communication"},
                    {"title": "Créer des résumés de réunion", "description": "Transformer des notes de réunion brutes en résumés structurés avec les points clés, décisions prises et actions à suivre.", "category": "Rédaction"},
                    {"title": "Rechercher des informations", "description": "Rassembler et synthétiser rapidement des informations sur n'importe quel sujet. L'IA peut compiler des sources multiples en un résumé cohérent.", "category": "Recherche"},
                    {"title": "Créer des présentations", "description": "Générer des plans de présentation, rédiger le contenu des slides et suggérer des visualisations pour communiquer efficacement.", "category": "Créatif"},
                    {"title": "Analyser des données", "description": "Identifier les tendances et patterns dans vos données. L'IA peut créer des analyses préliminaires et suggérer des insights.", "category": "Analyse"},
                    {"title": "Rédiger des rapports", "description": "Créer des rapports clairs et structurés à partir de données brutes. L'IA peut formater et adapter le style selon l'audience.", "category": "Rédaction"},
                    {"title": "Planifier des projets", "description": "Décomposer des projets complexes en tâches gérables avec des estimations et dépendances. Créer des timelines réalistes.", "category": "Planification"},
                    {"title": "Traduire des documents", "description": "Traduire rapidement des documents tout en préservant le contexte professionnel et les nuances du texte original.", "category": "Communication"},
                ]
        else:
            # English responses
            if "engineer" in job_lower or "developer" in job_lower:
                return [
                    {"title": "Write technical documentation", "description": "Automatically generate clear and comprehensive documentation for functions, APIs, and modules. AI can create docstrings, README files, and user documentation.", "category": "Writing"},
                    {"title": "Debug complex errors", "description": "Quickly analyze error messages and stack traces to identify root causes. AI can suggest fixes and explain why the error occurred.", "category": "Analysis"},
                    {"title": "Code review assistance", "description": "Get detailed suggestions to improve code quality, detect potential bugs, and identify security vulnerabilities before production.", "category": "Analysis"},
                    {"title": "Write unit tests", "description": "Generate comprehensive test cases covering edge cases and boundary scenarios. AI can create tests for different frameworks and ensure good coverage.", "category": "Automation"},
                    {"title": "Explain legacy code", "description": "Quickly understand complex and inherited codebases. AI can summarize logic, identify patterns, and document behaviors.", "category": "Learning"},
                    {"title": "Draft technical specs", "description": "Create detailed technical specifications and design documents from general requirements. Structure architecture decisions.", "category": "Writing"},
                    {"title": "Optimize SQL queries", "description": "Analyze and improve database query performance. AI can suggest indexes and rewrite inefficient queries.", "category": "Analysis"},
                    {"title": "Generate boilerplate code", "description": "Quickly create base code for new components, services, or features following existing project patterns.", "category": "Automation"},
                ]
            elif "product" in job_lower or "manager" in job_lower:
                return [
                    {"title": "Write PRDs", "description": "Draft comprehensive product requirements documents that clearly communicate features, user stories, and acceptance criteria to engineering teams.", "category": "Writing"},
                    {"title": "Analyze user feedback", "description": "Synthesize patterns from user interviews, surveys, and support tickets to identify key themes and actionable insights.", "category": "Research"},
                    {"title": "Competitive research", "description": "Quickly gather and summarize competitive intelligence, feature comparisons, and market positioning analysis.", "category": "Research"},
                    {"title": "Draft release notes", "description": "Create clear, user-friendly release communications that highlight key changes and benefits for different audiences.", "category": "Writing"},
                    {"title": "Meeting summaries", "description": "Transform meeting notes into structured summaries with key decisions, action items, and owners clearly identified.", "category": "Communication"},
                    {"title": "Roadmap planning", "description": "Help prioritize features based on impact and effort, organize quarterly roadmaps, and communicate trade-offs.", "category": "Planning"},
                    {"title": "Write user stories", "description": "Generate well-structured user stories with clear acceptance criteria from high-level feature descriptions.", "category": "Writing"},
                    {"title": "Stakeholder updates", "description": "Create executive summaries and progress reports tailored to different stakeholder audiences and their concerns.", "category": "Communication"},
                ]
            elif "market" in job_lower:
                return [
                    {"title": "Write blog posts", "description": "Create engaging, SEO-optimized content for your company blog that drives traffic and establishes thought leadership.", "category": "Writing"},
                    {"title": "Social media copy", "description": "Generate compelling posts optimized for each platform with appropriate tone, length, and call-to-actions.", "category": "Creative"},
                    {"title": "Email campaigns", "description": "Draft email sequences and newsletters with personalized content, compelling subject lines, and clear CTAs.", "category": "Writing"},
                    {"title": "SEO optimization", "description": "Improve content for search engine visibility with keyword suggestions, meta descriptions, and content structure recommendations.", "category": "Analysis"},
                    {"title": "Campaign analysis", "description": "Analyze marketing metrics, identify trends, and generate insights to optimize campaign performance and ROI.", "category": "Analysis"},
                    {"title": "Ad copy variations", "description": "Create multiple A/B test variations for advertisements with different angles, hooks, and value propositions.", "category": "Creative"},
                    {"title": "Customer personas", "description": "Develop detailed customer personas based on data and research to guide targeting and messaging decisions.", "category": "Research"},
                    {"title": "Competitive positioning", "description": "Analyze competitor messaging and positioning to identify differentiation opportunities and messaging gaps.", "category": "Research"},
                ]
            else:
                return [
                    {"title": "Draft professional emails", "description": "Compose clear, professional emails quickly with the right tone for each recipient. AI adjusts formality and structure based on context.", "category": "Communication"},
                    {"title": "Create meeting summaries", "description": "Transform raw meeting notes into structured summaries with key points, decisions made, and action items to follow.", "category": "Writing"},
                    {"title": "Research topics quickly", "description": "Gather and synthesize information on any subject rapidly. AI can compile multiple sources into a coherent summary.", "category": "Research"},
                    {"title": "Build presentations", "description": "Generate presentation outlines, write slide content, and suggest visualizations to communicate effectively.", "category": "Creative"},
                    {"title": "Analyze data patterns", "description": "Identify trends and patterns in your data. AI can create preliminary analyses and suggest insights.", "category": "Analysis"},
                    {"title": "Write structured reports", "description": "Create clear, structured reports from raw data. AI can format and adapt style based on audience.", "category": "Writing"},
                    {"title": "Plan complex projects", "description": "Break down complex projects into manageable tasks with estimates and dependencies. Create realistic timelines.", "category": "Planning"},
                    {"title": "Translate documents", "description": "Quickly translate documents while preserving professional context and nuances of the original text.", "category": "Communication"},
                ]


# Singleton instance
onboarding_chat_service = OnboardingChatService()
