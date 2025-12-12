"""
POST /onboarding/upload endpoints

Handles file uploads for organization logos and profile pictures during onboarding.
"""

import logging

from fastapi import File, HTTPException, UploadFile, status

from services.file_upload_service import file_upload_service
from utils.dependencies import AuthenticatedUser, SupabaseClient

from . import router

logger = logging.getLogger(__name__)


@router.post("/upload-organization-logo")
async def upload_organization_logo(
    user_id: AuthenticatedUser,
    client: SupabaseClient,
    file: UploadFile = File(...),
) -> dict:
    """
    Upload an organization logo image.

    Accepts image files (JPEG, PNG, GIF, WebP, SVG) up to 5MB.
    Returns the public URL of the uploaded file.
    """
    if not file.content_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing content type",
        )

    try:
        file_content = await file.read()

        public_url = file_upload_service.upload_organization_logo(
            client=client,
            user_id=user_id,
            file_content=file_content,
            content_type=file.content_type,
            original_filename=file.filename,
        )

        logger.info(f"Uploaded organization logo for user {user_id}")

        return {"logo_url": public_url}

    except ValueError as e:
        logger.warning(f"Invalid file upload: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error uploading organization logo: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload file",
        )


# Legacy endpoint for backward compatibility
@router.post("/upload-company-logo", deprecated=True)
async def upload_company_logo(
    user_id: AuthenticatedUser,
    client: SupabaseClient,
    file: UploadFile = File(...),
) -> dict:
    """
    Upload a company logo image.

    DEPRECATED: Use /upload-organization-logo instead.
    """
    return await upload_organization_logo(user_id, client, file)


@router.post("/upload-profile-picture")
async def upload_profile_picture(
    user_id: AuthenticatedUser,
    client: SupabaseClient,
    file: UploadFile = File(...),
) -> dict:
    """
    Upload a profile picture image.

    Accepts image files (JPEG, PNG, GIF, WebP, SVG) up to 5MB.
    Returns the public URL of the uploaded file.
    """
    if not file.content_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing content type",
        )

    try:
        file_content = await file.read()

        public_url = file_upload_service.upload_profile_picture(
            client=client,
            user_id=user_id,
            file_content=file_content,
            content_type=file.content_type,
            original_filename=file.filename,
        )

        logger.info(f"Uploaded profile picture for user {user_id}")

        return {"profile_picture_url": public_url}

    except ValueError as e:
        logger.warning(f"Invalid file upload: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error uploading profile picture: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload file",
        )
