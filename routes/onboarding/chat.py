"""
POST /onboarding/chat endpoints

AI-powered onboarding endpoints for generating organization descriptions,
job descriptions, AI use cases, and completing the onboarding flow.

Refactored to use:
- Auth dependencies for cleaner route handlers
- Split services for better separation of concerns
- Organization terminology (not company)
"""

import logging

from fastapi import HTTPException, Request

from dtos.onboarding_dto import (
    AIUseCaseDTO,
    BlockDTO,
    CompleteOnboardingChatRequestDTO,
    CompleteOnboardingChatRequestDTOV2,
    CompleteOnboardingChatResponseDTO,
    FetchOrganizationLogoRequestDTO,
    FetchOrganizationLogoResponseDTO,
    FetchProfilePictureRequestDTO,
    FetchProfilePictureResponseDTO,
    GenerateJobDescriptionRequestDTO,
    GenerateJobDescriptionResponseDTO,
    GenerateOrganizationDescriptionRequestDTO,
    GenerateOrganizationDescriptionResponseDTO,
    GenerateUseCasesRequestDTO,
    GenerateUseCasesResponseDTO,
    GenerateUserBlocksRequestDTO,
    GenerateUserBlocksResponseDTO,
)
from repositories.onboarding_repository import OnboardingRepository
from services.onboarding import (
    asset_fetcher_service,
    job_generation_service,
    organization_generation_service,
    use_case_generation_service,
)
from utils.dependencies import AuthenticatedUser, SupabaseClient

from . import router

logger = logging.getLogger(__name__)


# =============================================================================
# Organization Generation Endpoints
# =============================================================================


@router.post(
    "/chat/generate-organization",
    response_model=GenerateOrganizationDescriptionResponseDTO,
)
async def generate_organization_description(
    user_id: AuthenticatedUser,
    data: GenerateOrganizationDescriptionRequestDTO,
) -> GenerateOrganizationDescriptionResponseDTO:
    """
    Generate an organization description based on name and URLs.

    Takes organization name and optional website/LinkedIn URLs and returns
    a generated organization description and industry.
    """
    try:
        result = organization_generation_service.generate_description(
            organization_name=data.organization_name,
            website_url=data.website_url,
            linkedin_url=data.linkedin_url,
            language=data.language,
        )

        logger.info(
            f"[ONBOARDING] Generated organization description for user {user_id}: {data.organization_name}"
        )

        return GenerateOrganizationDescriptionResponseDTO(
            organization_description=result["organization_description"],
            industry=result["industry"],
        )

    except Exception as e:
        logger.error(
            f"[ONBOARDING] Error generating organization description: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=500, detail="Failed to generate organization description"
        )


# Legacy endpoint alias for backward compatibility
@router.post(
    "/chat/generate-company",
    response_model=GenerateOrganizationDescriptionResponseDTO,
    deprecated=True,
)
async def generate_company_description(
    user_id: AuthenticatedUser,
    data: GenerateOrganizationDescriptionRequestDTO,
) -> GenerateOrganizationDescriptionResponseDTO:
    """
    DEPRECATED: Use /chat/generate-organization instead.

    Generate an organization description based on name and URLs.
    """
    return await generate_organization_description(user_id, data)


# =============================================================================
# Job Generation Endpoints
# =============================================================================


@router.post("/chat/generate-job", response_model=GenerateJobDescriptionResponseDTO)
async def generate_job_description(
    user_id: AuthenticatedUser,
    data: GenerateJobDescriptionRequestDTO,
) -> GenerateJobDescriptionResponseDTO:
    """
    Generate a job description from LinkedIn URL or manual input.

    Takes LinkedIn URL or manual description and returns a structured
    job profile with title, description, and seniority level.
    """
    try:
        result = job_generation_service.generate_job_description(
            linkedin_url=data.linkedin_url,
            manual_description=data.manual_description,
            organization_description=data.organization_description,
            language=data.language,
        )

        logger.info(f"[ONBOARDING] Generated job description for user {user_id}")

        return GenerateJobDescriptionResponseDTO(
            job_title=result["job_title"],
            job_description=result["job_description"],
            seniority_level=result["seniority_level"],
        )

    except Exception as e:
        logger.error(
            f"[ONBOARDING] Error generating job description: {e}", exc_info=True
        )
        raise HTTPException(status_code=500, detail="Failed to generate job description")


@router.post("/chat/generate-user-blocks", response_model=GenerateUserBlocksResponseDTO)
async def generate_user_blocks(
    user_id: AuthenticatedUser,
    data: GenerateUserBlocksRequestDTO,
) -> GenerateUserBlocksResponseDTO:
    """
    Generate user blocks: context block, role blocks, and goal blocks.

    Takes job information and generates personalized blocks that the user
    can use with AI interactions.
    """
    try:
        result = job_generation_service.generate_user_blocks(
            job_title=data.job_title,
            linkedin_url=data.linkedin_url,
            manual_description=data.manual_description,
            organization_name=data.organization_name,
            organization_description=data.organization_description,
            industry=data.industry,
            language=data.language,
        )

        logger.info(
            f"[ONBOARDING] Generated user blocks for user {user_id}: {data.job_title}"
        )

        return GenerateUserBlocksResponseDTO(
            context_block=BlockDTO(**result["context_block"]),
            role_blocks=[BlockDTO(**rb) for rb in result["role_blocks"]],
            goal_blocks=[BlockDTO(**gb) for gb in result["goal_blocks"]],
            job_title=result["job_title"],
            job_description=result["job_description"],
            seniority_level=result["seniority_level"],
        )

    except Exception as e:
        logger.error(
            f"[ONBOARDING] Error generating user blocks: {e}", exc_info=True
        )
        raise HTTPException(status_code=500, detail="Failed to generate user blocks")


# =============================================================================
# Use Case Generation Endpoints
# =============================================================================


@router.post("/chat/generate-use-cases", response_model=GenerateUseCasesResponseDTO)
async def generate_use_cases(
    user_id: AuthenticatedUser,
    data: GenerateUseCasesRequestDTO,
) -> GenerateUseCasesResponseDTO:
    """
    Generate AI use cases tailored to the user's job.

    Takes job title, description, and organization context and returns 8-10
    specific AI use cases relevant to that role.
    """
    try:
        use_cases = use_case_generation_service.generate_use_cases(
            job_title=data.job_title,
            job_description=data.job_description,
            organization_description=data.organization_description,
            industry=data.industry,
            language=data.language,
        )

        logger.info(
            f"[ONBOARDING] Generated AI use cases for user {user_id}: {data.job_title}"
        )

        return GenerateUseCasesResponseDTO(
            use_cases=[AIUseCaseDTO(**uc) for uc in use_cases]
        )

    except Exception as e:
        logger.error(f"[ONBOARDING] Error generating use cases: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate use cases")


# =============================================================================
# Asset Fetching Endpoints
# =============================================================================


@router.post(
    "/chat/fetch-organization-logo",
    response_model=FetchOrganizationLogoResponseDTO,
)
async def fetch_organization_logo(
    user_id: AuthenticatedUser,
    data: FetchOrganizationLogoRequestDTO,
) -> FetchOrganizationLogoResponseDTO:
    """
    Fetch organization logo from website URL or LinkedIn.

    Attempts to find the organization logo by scraping og:image, apple-touch-icon,
    or favicon from the provided URLs.
    """
    if not data.website_url and not data.linkedin_url:
        raise HTTPException(status_code=400, detail="At least one URL is required")

    try:
        logo_url = asset_fetcher_service.fetch_organization_logo(
            website_url=data.website_url,
            linkedin_url=data.linkedin_url,
        )

        logger.info(
            f"[ONBOARDING] Fetched organization logo for user {user_id}: {logo_url}"
        )

        return FetchOrganizationLogoResponseDTO(logo_url=logo_url)

    except Exception as e:
        logger.error(
            f"[ONBOARDING] Error fetching organization logo: {e}", exc_info=True
        )
        # Return None instead of error - logo fetching is not critical
        return FetchOrganizationLogoResponseDTO(logo_url=None)


# Legacy endpoint alias
@router.post(
    "/chat/fetch-company-logo",
    response_model=FetchOrganizationLogoResponseDTO,
    deprecated=True,
)
async def fetch_company_logo(
    user_id: AuthenticatedUser,
    data: FetchOrganizationLogoRequestDTO,
) -> FetchOrganizationLogoResponseDTO:
    """DEPRECATED: Use /chat/fetch-organization-logo instead."""
    return await fetch_organization_logo(user_id, data)


@router.post(
    "/chat/fetch-profile-picture",
    response_model=FetchProfilePictureResponseDTO,
)
async def fetch_profile_picture(
    user_id: AuthenticatedUser,
    data: FetchProfilePictureRequestDTO,
) -> FetchProfilePictureResponseDTO:
    """
    Fetch profile picture from LinkedIn profile URL.

    Attempts to find the user's profile picture by scraping the LinkedIn profile page.
    """
    if not data.linkedin_url:
        raise HTTPException(status_code=400, detail="LinkedIn URL is required")

    try:
        picture_url = asset_fetcher_service.fetch_profile_picture(
            linkedin_url=data.linkedin_url,
        )

        logger.info(
            f"[ONBOARDING] Fetched profile picture for user {user_id}: {picture_url is not None}"
        )

        return FetchProfilePictureResponseDTO(profile_picture_url=picture_url)

    except Exception as e:
        logger.error(
            f"[ONBOARDING] Error fetching profile picture: {e}", exc_info=True
        )
        # Return None instead of error - profile picture fetching is not critical
        return FetchProfilePictureResponseDTO(profile_picture_url=None)


# =============================================================================
# Chat Completion Endpoints
# =============================================================================


def _generate_summary(
    organization_name: str | None,
    organization_description: str | None,
    industry: str | None,
    job_title: str,
    job_description: str,
    selected_use_cases: list[str],
    ai_dreams: str | None,
    signup_source: str,
) -> dict:
    """Generate onboarding summary from collected data."""
    summary_parts = [f"A {job_title}"]
    if organization_name:
        summary_parts.append(f"at {organization_name}")
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
            "organization_name": organization_name,
            "organization_description": organization_description,
            "job_type": job_title,
            "job_description": job_description,
            "job_industry": industry,
            "interests": selected_use_cases,
            "ai_dreams": ai_dreams,
            "signup_source": signup_source,
        },
    }


@router.post("/chat/complete", response_model=CompleteOnboardingChatResponseDTO)
async def complete_onboarding_chat(
    user_id: AuthenticatedUser,
    client: SupabaseClient,
    data: CompleteOnboardingChatRequestDTO,
) -> CompleteOnboardingChatResponseDTO:
    """
    Complete the onboarding chat and save all data (legacy v1).

    Generates a summary and saves all collected data to the database.
    """
    try:
        # Generate summary
        result = _generate_summary(
            organization_name=data.company_name,
            organization_description=data.company_description,
            industry=data.industry,
            job_title=data.job_title,
            job_description=data.job_description,
            selected_use_cases=data.selected_use_cases,
            ai_dreams=data.ai_dreams,
            signup_source=data.signup_source,
        )

        # Build chat history as a record of what was collected
        chat_history = [
            {
                "step": "organization_info",
                "organization_name": data.company_name,
                "organization_description": data.company_description,
                "industry": data.industry,
            },
            {
                "step": "job_info",
                "job_title": data.job_title,
                "job_description": data.job_description,
            },
            {"step": "use_cases", "selected": data.selected_use_cases},
            {"step": "ai_dreams", "value": data.ai_dreams},
            {"step": "user_message", "value": data.user_message},
            {"step": "source", "value": data.signup_source},
        ]

        # Save to new table
        OnboardingRepository.save_chat_completion(
            client=client,
            user_id=user_id,
            data={
                "organization_name": data.company_name,
                "organization_description": data.company_description,
                "industry": data.industry,
                "job_title": data.job_title,
                "job_description": data.job_description,
                "selected_use_cases": data.selected_use_cases,
                "ai_dreams": data.ai_dreams,
                "signup_source": data.signup_source,
                "chat_history": chat_history,
                "chat_summary": result["summary"],
            },
        )

        logger.info(f"[ONBOARDING] Completed onboarding chat for user {user_id}")

        return CompleteOnboardingChatResponseDTO(
            summary=result["summary"],
            extracted_data=result["extracted_data"],
        )

    except Exception as e:
        logger.error(
            f"[ONBOARDING] Error completing onboarding chat: {e}", exc_info=True
        )
        raise HTTPException(status_code=500, detail="Failed to complete onboarding")


@router.post("/chat/complete-v2", response_model=CompleteOnboardingChatResponseDTO)
async def complete_onboarding_chat_v2(
    user_id: AuthenticatedUser,
    client: SupabaseClient,
    data: CompleteOnboardingChatRequestDTOV2,
) -> CompleteOnboardingChatResponseDTO:
    """
    Complete the onboarding chat and save all data (v2 with blocks).

    Enhanced version that includes organization logo, profile picture, and user blocks.
    """
    try:
        # Generate summary
        result = _generate_summary(
            organization_name=data.organization_name,
            organization_description=data.organization_description,
            industry=data.industry,
            job_title=data.job_title,
            job_description=data.job_description,
            selected_use_cases=data.selected_use_cases,
            ai_dreams=data.ai_dreams,
            signup_source=data.signup_source,
        )

        # Add new fields to extracted data
        extracted_data = result["extracted_data"]
        extracted_data["organization_logo_url"] = data.organization_logo_url
        extracted_data["profile_picture_url"] = data.profile_picture_url
        extracted_data["job_seniority"] = data.seniority_level

        # Build enhanced chat history
        chat_history = [
            {
                "step": "organization_info",
                "organization_name": data.organization_name,
                "organization_logo_url": data.organization_logo_url,
                "organization_description": data.organization_description,
                "industry": data.industry,
            },
            {
                "step": "user_info",
                "profile_picture_url": data.profile_picture_url,
                "job_title": data.job_title,
                "job_description": data.job_description,
                "seniority_level": data.seniority_level,
            },
            {
                "step": "blocks",
                "context_block": data.context_block.model_dump()
                if data.context_block
                else None,
                "role_blocks": [rb.model_dump() for rb in data.role_blocks],
                "goal_blocks": [gb.model_dump() for gb in data.goal_blocks],
                "selected_role_block_ids": data.selected_role_block_ids,
                "selected_goal_block_ids": data.selected_goal_block_ids,
            },
            {"step": "use_cases", "selected": data.selected_use_cases},
            {"step": "invite", "emails": data.invited_emails},
            {"step": "ai_dreams", "value": data.ai_dreams},
            {"step": "user_message", "value": data.user_message},
            {"step": "source", "value": data.signup_source},
        ]

        # Save to new table with all data
        OnboardingRepository.save_chat_completion(
            client=client,
            user_id=user_id,
            data={
                "organization_name": data.organization_name,
                "organization_description": data.organization_description,
                "organization_logo_url": data.organization_logo_url,
                "industry": data.industry,
                "job_title": data.job_title,
                "job_description": data.job_description,
                "job_seniority": data.seniority_level,
                "context_block": data.context_block.model_dump()
                if data.context_block
                else None,
                "role_blocks": [rb.model_dump() for rb in data.role_blocks],
                "goal_blocks": [gb.model_dump() for gb in data.goal_blocks],
                "selected_role_block_ids": data.selected_role_block_ids,
                "selected_goal_block_ids": data.selected_goal_block_ids,
                "selected_use_cases": data.selected_use_cases,
                "ai_dreams": data.ai_dreams,
                "signup_source": data.signup_source,
                "chat_history": chat_history,
                "chat_summary": result["summary"],
            },
        )

        logger.info(f"[ONBOARDING] Completed onboarding chat v2 for user {user_id}")

        return CompleteOnboardingChatResponseDTO(
            summary=result["summary"],
            extracted_data=extracted_data,
        )

    except Exception as e:
        logger.error(
            f"[ONBOARDING] Error completing onboarding chat v2: {e}", exc_info=True
        )
        raise HTTPException(status_code=500, detail="Failed to complete onboarding")
