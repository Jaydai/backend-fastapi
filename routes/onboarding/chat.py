"""
POST /onboarding/chat endpoints

AI-powered onboarding endpoints for generating company descriptions,
job descriptions, AI use cases, and completing the onboarding flow.
"""

import logging

from fastapi import HTTPException, Request

from dtos.onboarding_dto import (
    GenerateCompanyDescriptionRequestDTO,
    GenerateCompanyDescriptionResponseDTO,
    GenerateJobDescriptionRequestDTO,
    GenerateJobDescriptionResponseDTO,
    GenerateUseCasesRequestDTO,
    GenerateUseCasesResponseDTO,
    AIUseCaseDTO,
    CompleteOnboardingChatRequestDTO,
    CompleteOnboardingChatResponseDTO,
)
from repositories.onboarding_repository import OnboardingRepository
from services.onboarding_chat_service import onboarding_chat_service

from . import router

logger = logging.getLogger(__name__)


@router.post("/chat/generate-company", response_model=GenerateCompanyDescriptionResponseDTO)
async def generate_company_description(request: Request, data: GenerateCompanyDescriptionRequestDTO):
    """
    Generate a company description based on company name and URLs.

    Takes company name and optional website/LinkedIn URLs and returns
    a generated company description and industry.
    """
    try:
        user_id = request.state.user_id
    except AttributeError:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        result = onboarding_chat_service.generate_company_description(
            company_name=data.company_name,
            website_url=data.website_url,
            linkedin_url=data.linkedin_url,
            language=data.language,
        )

        logger.info(f"[ONBOARDING] Generated company description for user {user_id}: {data.company_name}")

        return GenerateCompanyDescriptionResponseDTO(
            company_description=result["company_description"],
            industry=result["industry"],
        )

    except Exception as e:
        logger.error(f"[ONBOARDING] Error generating company description: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate company description")


@router.post("/chat/generate-job", response_model=GenerateJobDescriptionResponseDTO)
async def generate_job_description(request: Request, data: GenerateJobDescriptionRequestDTO):
    """
    Generate a job description from LinkedIn URL or manual input.

    Takes LinkedIn URL or manual description and returns a structured
    job profile with title, description, and seniority level.
    """
    try:
        user_id = request.state.user_id
    except AttributeError:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        result = onboarding_chat_service.generate_job_description(
            linkedin_url=data.linkedin_url,
            manual_description=data.manual_description,
            company_description=data.company_description,
            language=data.language,
        )

        logger.info(f"[ONBOARDING] Generated job description for user {user_id}")

        return GenerateJobDescriptionResponseDTO(
            job_title=result["job_title"],
            job_description=result["job_description"],
            seniority_level=result["seniority_level"],
        )

    except Exception as e:
        logger.error(f"[ONBOARDING] Error generating job description: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate job description")


@router.post("/chat/generate-use-cases", response_model=GenerateUseCasesResponseDTO)
async def generate_use_cases(request: Request, data: GenerateUseCasesRequestDTO):
    """
    Generate AI use cases tailored to the user's job.

    Takes job title, description, and company context and returns 8-10 specific
    AI use cases relevant to that role.
    """
    try:
        user_id = request.state.user_id
    except AttributeError:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        use_cases = onboarding_chat_service.generate_ai_use_cases(
            job_title=data.job_title,
            job_description=data.job_description,
            company_description=data.company_description,
            industry=data.industry,
            language=data.language,
        )

        logger.info(f"[ONBOARDING] Generated AI use cases for user {user_id}: {data.job_title}")

        return GenerateUseCasesResponseDTO(
            use_cases=[AIUseCaseDTO(**uc) for uc in use_cases]
        )

    except Exception as e:
        logger.error(f"[ONBOARDING] Error generating use cases: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate use cases")


@router.post("/chat/complete", response_model=CompleteOnboardingChatResponseDTO)
async def complete_onboarding_chat(request: Request, data: CompleteOnboardingChatRequestDTO):
    """
    Complete the onboarding chat and save all data.

    Generates a summary and saves all collected data to the database.
    """
    try:
        user_id = request.state.user_id
    except AttributeError:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        # Generate summary
        result = onboarding_chat_service.generate_onboarding_summary(
            company_name=data.company_name,
            company_description=data.company_description,
            industry=data.industry,
            job_title=data.job_title,
            job_description=data.job_description,
            selected_use_cases=data.selected_use_cases,
            ai_dreams=data.ai_dreams,
            user_message=data.user_message,
            signup_source=data.signup_source,
        )

        # Save to database
        client = request.state.supabase_client
        extracted_data = result["extracted_data"]

        # Build chat history as a record of what was collected
        chat_history = [
            {"step": "company_info", "company_name": data.company_name, "company_description": data.company_description, "industry": data.industry},
            {"step": "job_info", "job_title": data.job_title, "job_description": data.job_description},
            {"step": "use_cases", "selected": data.selected_use_cases},
            {"step": "ai_dreams", "value": data.ai_dreams},
            {"step": "user_message", "value": data.user_message},
            {"step": "source", "value": data.signup_source},
        ]

        OnboardingRepository.save_chat_data(
            client=client,
            user_id=user_id,
            chat_history=chat_history,
            chat_summary=result["summary"],
            extracted_data=extracted_data,
        )

        logger.info(f"[ONBOARDING] Completed onboarding chat for user {user_id}")

        return CompleteOnboardingChatResponseDTO(
            summary=result["summary"],
            extracted_data=extracted_data,
        )

    except Exception as e:
        logger.error(f"[ONBOARDING] Error completing onboarding chat: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to complete onboarding")
