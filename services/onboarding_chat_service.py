"""
Onboarding Chat Service

Handles AI-powered onboarding conversations using OpenAI Responses API.
Generates company descriptions, job descriptions, AI use cases, and personalizes the onboarding experience.
Supports multiple languages (en, fr).
"""

import json
import logging
import os
import re
import uuid
from typing import Any
from urllib.parse import urlparse

import httpx
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

    def fetch_company_logo(
        self,
        website_url: str | None = None,
        linkedin_url: str | None = None,
    ) -> str | None:
        """
        Fetch company logo from website or LinkedIn.

        Args:
            website_url: Company website URL
            linkedin_url: Company LinkedIn URL

        Returns:
            Logo URL if found, None otherwise
        """
        logo_url = None

        # Try website first
        if website_url:
            logo_url = self._fetch_logo_from_website(website_url)

        # Try LinkedIn if no logo found
        if not logo_url and linkedin_url:
            logo_url = self._fetch_logo_from_linkedin(linkedin_url)

        return logo_url

    def _fetch_logo_from_website(self, website_url: str) -> str | None:
        """
        Fetch favicon/logo from website.

        Priority order:
        1. High-resolution favicon (icon with sizes attribute, prefer largest)
        2. Apple touch icon (usually high quality square icon)
        3. Standard favicon link
        4. /favicon.ico fallback
        5. og:image as last resort (often not a logo)
        """
        try:
            # Ensure URL has scheme
            if not website_url.startswith(("http://", "https://")):
                website_url = f"https://{website_url}"

            parsed = urlparse(website_url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"

            with httpx.Client(timeout=10.0, follow_redirects=True) as client:
                response = client.get(website_url)
                response.raise_for_status()
                html = response.text

                def resolve_url(url: str) -> str:
                    """Resolve relative URLs to absolute."""
                    if url.startswith("//"):
                        return f"https:{url}"
                    elif url.startswith("/"):
                        return base_url + url
                    elif not url.startswith(("http://", "https://")):
                        return f"{base_url}/{url}"
                    return url

                # 1. Look for high-res icons with sizes (prefer 192x192, 180x180, 152x152, etc.)
                # Match: <link rel="icon" sizes="192x192" href="...">
                icon_with_sizes = re.findall(
                    r'<link[^>]*rel=["\'](?:icon|shortcut icon)["\'][^>]*(?:sizes=["\'](\d+)x\d+["\'][^>]*)?href=["\']([^"\']+)["\']',
                    html,
                    re.IGNORECASE
                )
                # Also match reversed attribute order
                icon_with_sizes += re.findall(
                    r'<link[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\'](?:icon|shortcut icon)["\'][^>]*(?:sizes=["\'](\d+)x\d+["\'])?',
                    html,
                    re.IGNORECASE
                )

                # Parse and sort by size (largest first)
                sized_icons = []
                for match in icon_with_sizes:
                    if isinstance(match, tuple) and len(match) == 2:
                        size_str, href = match
                        if href and not size_str:
                            # Reversed order match
                            href, size_str = match
                        size = int(size_str) if size_str and size_str.isdigit() else 0
                        if href:
                            sized_icons.append((size, href))

                # Sort by size descending, filter for reasonable sizes
                sized_icons.sort(key=lambda x: x[0], reverse=True)
                for size, href in sized_icons:
                    if size >= 32:  # Prefer icons 32px or larger
                        logo = resolve_url(href)
                        logger.info(f"[ONBOARDING] Found icon with size {size}x{size}: {logo}")
                        return logo

                # 2. Look for apple-touch-icon (usually 180x180 or larger, good quality)
                apple_patterns = [
                    r'<link[^>]*rel=["\']apple-touch-icon(?:-precomposed)?["\'][^>]*href=["\']([^"\']+)["\']',
                    r'<link[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\']apple-touch-icon(?:-precomposed)?["\']',
                ]
                for pattern in apple_patterns:
                    apple_match = re.search(pattern, html, re.IGNORECASE)
                    if apple_match:
                        logo = resolve_url(apple_match.group(1))
                        logger.info(f"[ONBOARDING] Found apple-touch-icon: {logo}")
                        return logo

                # 3. Look for any favicon link (without size requirement)
                favicon_patterns = [
                    r'<link[^>]*rel=["\'](?:shortcut )?icon["\'][^>]*href=["\']([^"\']+)["\']',
                    r'<link[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\'](?:shortcut )?icon["\']',
                ]
                for pattern in favicon_patterns:
                    favicon_match = re.search(pattern, html, re.IGNORECASE)
                    if favicon_match:
                        logo = resolve_url(favicon_match.group(1))
                        logger.info(f"[ONBOARDING] Found favicon link: {logo}")
                        return logo

                # 4. Try common favicon paths
                common_paths = [
                    "/favicon.ico",
                    "/favicon.png",
                    "/favicon-32x32.png",
                    "/favicon-16x16.png",
                    "/apple-touch-icon.png",
                ]
                for path in common_paths:
                    favicon_url = f"{base_url}{path}"
                    try:
                        favicon_response = client.head(favicon_url)
                        if favicon_response.status_code == 200:
                            content_type = favicon_response.headers.get("content-type", "")
                            if "image" in content_type or path.endswith((".ico", ".png", ".svg")):
                                logger.info(f"[ONBOARDING] Found favicon at common path: {favicon_url}")
                                return favicon_url
                    except Exception:
                        pass

                # 5. og:image as last resort (often a banner, not ideal but better than nothing)
                og_patterns = [
                    r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']',
                    r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*property=["\']og:image["\']',
                ]
                for pattern in og_patterns:
                    og_match = re.search(pattern, html, re.IGNORECASE)
                    if og_match:
                        logo = resolve_url(og_match.group(1))
                        logger.info(f"[ONBOARDING] Found og:image (fallback): {logo}")
                        return logo

        except Exception as e:
            logger.warning(f"[ONBOARDING] Error fetching logo from website: {e}")

        return None

    def _fetch_logo_from_linkedin(self, linkedin_url: str) -> str | None:
        """Fetch logo from LinkedIn company page."""
        # LinkedIn requires authentication for scraping, so we can't easily fetch logos
        # For now, return None - in production, you'd use LinkedIn API
        logger.info(f"[ONBOARDING] LinkedIn logo fetching not implemented: {linkedin_url}")
        return None

    def fetch_profile_picture(self, linkedin_url: str | None = None) -> str | None:
        """
        Fetch profile picture from LinkedIn profile URL.

        Args:
            linkedin_url: User's LinkedIn profile URL

        Returns:
            URL of the profile picture or None if not found
        """
        if not linkedin_url:
            return None

        picture_url = self._fetch_picture_from_linkedin(linkedin_url)
        return picture_url

    def _fetch_picture_from_linkedin(self, linkedin_url: str) -> str | None:
        """
        Fetch profile picture from LinkedIn profile page.

        LinkedIn blocks most scraping, but we can try to get the og:image
        which sometimes contains the profile picture.
        """
        try:
            # Ensure URL has scheme
            if not linkedin_url.startswith(("http://", "https://")):
                linkedin_url = f"https://{linkedin_url}"

            # Normalize LinkedIn URL
            if "linkedin.com/in/" not in linkedin_url.lower():
                logger.warning(f"[ONBOARDING] Invalid LinkedIn profile URL: {linkedin_url}")
                return None

            with httpx.Client(
                timeout=10.0,
                follow_redirects=True,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                },
            ) as client:
                response = client.get(linkedin_url)
                response.raise_for_status()
                html = response.text

                # Look for og:image which often contains profile picture
                og_patterns = [
                    r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']',
                    r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*property=["\']og:image["\']',
                ]

                for pattern in og_patterns:
                    og_match = re.search(pattern, html, re.IGNORECASE)
                    if og_match:
                        image_url = og_match.group(1)
                        # LinkedIn profile pictures usually contain "profile-displayphoto" or similar
                        # Filter out generic LinkedIn images
                        if "profile" in image_url.lower() or "media" in image_url.lower():
                            logger.info(f"[ONBOARDING] Found LinkedIn profile picture: {image_url[:100]}...")
                            return image_url

                # Try to find profile image in the HTML directly
                # LinkedIn uses various patterns for profile images
                img_patterns = [
                    r'<img[^>]*class=["\'][^"\']*profile-photo[^"\']*["\'][^>]*src=["\']([^"\']+)["\']',
                    r'<img[^>]*src=["\']([^"\']+)["\'][^>]*class=["\'][^"\']*profile-photo[^"\']*["\']',
                    r'<img[^>]*class=["\'][^"\']*pv-top-card[^"\']*["\'][^>]*src=["\']([^"\']+)["\']',
                ]

                for pattern in img_patterns:
                    img_match = re.search(pattern, html, re.IGNORECASE)
                    if img_match:
                        image_url = img_match.group(1)
                        logger.info(f"[ONBOARDING] Found LinkedIn profile image: {image_url[:100]}...")
                        return image_url

        except httpx.HTTPStatusError as e:
            logger.warning(f"[ONBOARDING] LinkedIn returned {e.response.status_code} for {linkedin_url}")
        except Exception as e:
            logger.warning(f"[ONBOARDING] Error fetching profile picture from LinkedIn: {e}")

        return None

    def generate_user_blocks(
        self,
        job_title: str,
        linkedin_url: str | None = None,
        manual_description: str | None = None,
        company_name: str | None = None,
        company_description: str | None = None,
        industry: str | None = None,
        language: str = "en",
    ) -> dict[str, Any]:
        """
        Generate user blocks: context block, role blocks, and goal blocks.

        Args:
            job_title: The user's job title
            linkedin_url: User's LinkedIn profile URL (optional)
            manual_description: Manual job description (optional)
            company_name: Company name for context (optional)
            company_description: Company description for context (optional)
            industry: Industry for context (optional)
            language: Language code ('en' or 'fr')

        Returns:
            Dict with context_block, role_blocks, goal_blocks, job_title, job_description, seniority_level
        """
        if self.mock_mode:
            return self._mock_user_blocks(job_title, company_name, language)

        lang_instruction = "Respond in French." if language == "fr" else "Respond in English."

        context_parts = [f"Job title: {job_title}"]
        if linkedin_url:
            context_parts.append(f"LinkedIn: {linkedin_url}")
        if manual_description:
            context_parts.append(f"Job details: {manual_description}")
        if company_name:
            context_parts.append(f"Company: {company_name}")
        if company_description:
            context_parts.append(f"Company description: {company_description}")
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

            # Add IDs and types to blocks
            context_block = {
                "id": str(uuid.uuid4()),
                "type": "context",
                "title": parsed["context_block"]["title"],
                "description": parsed["context_block"]["description"],
                "icon": "briefcase",
            }

            role_blocks = []
            for rb in parsed.get("role_blocks", [])[:3]:
                role_blocks.append({
                    "id": str(uuid.uuid4()),
                    "type": "role",
                    "title": rb["title"],
                    "description": rb["description"],
                    "icon": rb.get("icon", "user"),
                    "category": rb.get("category", "General"),
                })

            goal_blocks = []
            for gb in parsed.get("goal_blocks", [])[:3]:
                goal_blocks.append({
                    "id": str(uuid.uuid4()),
                    "type": "goal",
                    "title": gb["title"],
                    "description": gb["description"],
                    "icon": gb.get("icon", "target"),
                    "category": gb.get("category", "General"),
                })

            logger.info(f"[ONBOARDING] Generated user blocks for: {job_title}")

            return {
                "context_block": context_block,
                "role_blocks": role_blocks,
                "goal_blocks": goal_blocks,
                "job_title": parsed.get("job_title", job_title),
                "job_description": parsed.get("job_description", ""),
                "seniority_level": parsed.get("seniority_level", "mid"),
            }

        except Exception as e:
            logger.error(f"[ONBOARDING] Error generating user blocks: {e}")
            return self._mock_user_blocks(job_title, company_name, language)

    def _mock_user_blocks(self, job_title: str, company_name: str | None, language: str = "en") -> dict[str, Any]:
        """Generate mock user blocks for testing."""
        job_lower = job_title.lower()

        if language == "fr":
            company_part = f" chez {company_name}" if company_name else ""
            context_desc = f"Je suis {job_title}{company_part}. Je suis responsable de la stratégie et de l'exécution des initiatives clés de mon domaine. Mon travail implique la coordination d'équipes et la livraison de résultats mesurables."

            if "market" in job_lower or "marketing" in job_lower:
                role_blocks = [
                    {"id": str(uuid.uuid4()), "type": "role", "title": "Spécialiste SEO", "description": "Expert en optimisation pour les moteurs de recherche et stratégies de mots-clés.", "icon": "🔍", "category": "Marketing"},
                    {"id": str(uuid.uuid4()), "type": "role", "title": "Copywriter", "description": "Rédige des textes marketing percutants et persuasifs.", "icon": "✍️", "category": "Contenu"},
                    {"id": str(uuid.uuid4()), "type": "role", "title": "Analyste Data", "description": "Analyse les données marketing et identifie les tendances.", "icon": "📊", "category": "Analytics"},
                ]
                goal_blocks = [
                    {"id": str(uuid.uuid4()), "type": "goal", "title": "Améliorer le taux de conversion", "description": "Augmenter les conversions en optimisant le parcours utilisateur.", "icon": "📈", "category": "Croissance"},
                    {"id": str(uuid.uuid4()), "type": "goal", "title": "Stratégie de contenu", "description": "Développer un calendrier éditorial complet pour accroître la notoriété.", "icon": "📋", "category": "Stratégie"},
                    {"id": str(uuid.uuid4()), "type": "goal", "title": "ROI des campagnes", "description": "Maximiser le retour sur investissement des campagnes marketing.", "icon": "💰", "category": "Revenue"},
                ]
            else:
                role_blocks = [
                    {"id": str(uuid.uuid4()), "type": "role", "title": "Consultant Stratégique", "description": "Conseille sur les décisions stratégiques et l'optimisation des processus.", "icon": "🎯", "category": "Stratégie"},
                    {"id": str(uuid.uuid4()), "type": "role", "title": "Rédacteur Pro", "description": "Rédige des documents professionnels clairs et impactants.", "icon": "✍️", "category": "Communication"},
                    {"id": str(uuid.uuid4()), "type": "role", "title": "Analyste", "description": "Analyse les données et génère des insights actionnables.", "icon": "📊", "category": "Analytics"},
                ]
                goal_blocks = [
                    {"id": str(uuid.uuid4()), "type": "goal", "title": "Productivité équipe", "description": "Améliorer l'efficacité et la collaboration de l'équipe.", "icon": "⚡", "category": "Efficacité"},
                    {"id": str(uuid.uuid4()), "type": "goal", "title": "Qualité livrables", "description": "Assurer la qualité et la cohérence des livrables.", "icon": "✅", "category": "Qualité"},
                    {"id": str(uuid.uuid4()), "type": "goal", "title": "Innovation", "description": "Identifier et implémenter des solutions innovantes.", "icon": "💡", "category": "Innovation"},
                ]
        else:
            company_part = f" at {company_name}" if company_name else ""
            context_desc = f"I am a {job_title}{company_part}. I am responsible for strategy and execution of key initiatives in my domain. My work involves coordinating teams and delivering measurable results."

            if "market" in job_lower or "marketing" in job_lower:
                role_blocks = [
                    {"id": str(uuid.uuid4()), "type": "role", "title": "SEO Specialist", "description": "Expert in search engine optimization and keyword strategies.", "icon": "🔍", "category": "Marketing"},
                    {"id": str(uuid.uuid4()), "type": "role", "title": "Copywriter", "description": "Crafts compelling and persuasive marketing copy.", "icon": "✍️", "category": "Content"},
                    {"id": str(uuid.uuid4()), "type": "role", "title": "Data Analyst", "description": "Analyzes marketing data and identifies trends.", "icon": "📊", "category": "Analytics"},
                ]
                goal_blocks = [
                    {"id": str(uuid.uuid4()), "type": "goal", "title": "Improve Conversion Rate", "description": "Increase conversions by optimizing the user journey.", "icon": "📈", "category": "Growth"},
                    {"id": str(uuid.uuid4()), "type": "goal", "title": "Content Strategy", "description": "Develop a comprehensive editorial calendar to increase brand awareness.", "icon": "📋", "category": "Strategy"},
                    {"id": str(uuid.uuid4()), "type": "goal", "title": "Campaign ROI", "description": "Maximize return on investment from marketing campaigns.", "icon": "💰", "category": "Revenue"},
                ]
            elif "engineer" in job_lower or "developer" in job_lower:
                role_blocks = [
                    {"id": str(uuid.uuid4()), "type": "role", "title": "Code Reviewer", "description": "Reviews code for quality, security, and best practices.", "icon": "🔍", "category": "Engineering"},
                    {"id": str(uuid.uuid4()), "type": "role", "title": "Tech Writer", "description": "Creates clear technical documentation and guides.", "icon": "📝", "category": "Documentation"},
                    {"id": str(uuid.uuid4()), "type": "role", "title": "DevOps Expert", "description": "Optimizes deployment and infrastructure processes.", "icon": "🚀", "category": "Operations"},
                ]
                goal_blocks = [
                    {"id": str(uuid.uuid4()), "type": "goal", "title": "Code Quality", "description": "Improve codebase quality and reduce technical debt.", "icon": "✅", "category": "Quality"},
                    {"id": str(uuid.uuid4()), "type": "goal", "title": "Ship Faster", "description": "Reduce time-to-production for new features.", "icon": "⚡", "category": "Efficiency"},
                    {"id": str(uuid.uuid4()), "type": "goal", "title": "System Reliability", "description": "Improve uptime and reduce incident response time.", "icon": "🛡️", "category": "Quality"},
                ]
            else:
                role_blocks = [
                    {"id": str(uuid.uuid4()), "type": "role", "title": "Strategic Consultant", "description": "Advises on strategic decisions and process optimization.", "icon": "🎯", "category": "Strategy"},
                    {"id": str(uuid.uuid4()), "type": "role", "title": "Professional Writer", "description": "Writes clear and impactful professional documents.", "icon": "✍️", "category": "Communication"},
                    {"id": str(uuid.uuid4()), "type": "role", "title": "Analyst", "description": "Analyzes data and generates actionable insights.", "icon": "📊", "category": "Analytics"},
                ]
                goal_blocks = [
                    {"id": str(uuid.uuid4()), "type": "goal", "title": "Team Productivity", "description": "Improve team efficiency and collaboration.", "icon": "⚡", "category": "Efficiency"},
                    {"id": str(uuid.uuid4()), "type": "goal", "title": "Deliverable Quality", "description": "Ensure quality and consistency of deliverables.", "icon": "✅", "category": "Quality"},
                    {"id": str(uuid.uuid4()), "type": "goal", "title": "Innovation", "description": "Identify and implement innovative solutions.", "icon": "💡", "category": "Innovation"},
                ]

        context_block = {
            "id": str(uuid.uuid4()),
            "type": "context",
            "title": "I work as..." if language == "en" else "Je travaille comme...",
            "description": context_desc,
            "icon": "briefcase",
        }

        return {
            "context_block": context_block,
            "role_blocks": role_blocks,
            "goal_blocks": goal_blocks,
            "job_title": job_title,
            "job_description": f"Responsible for key initiatives and team coordination as a {job_title}." if language == "en" else f"Responsable des initiatives clés et de la coordination d'équipe en tant que {job_title}.",
            "seniority_level": "mid",
        }


# Singleton instance
onboarding_chat_service = OnboardingChatService()
