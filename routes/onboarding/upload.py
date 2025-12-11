"""
POST /onboarding/upload endpoints

Handles file uploads for company logos and profile pictures during onboarding.
"""

import logging

from fastapi import File, HTTPException, Request, UploadFile

from services.file_upload_service import file_upload_service

from . import router

logger = logging.getLogger(__name__)


@router.post("/upload-company-logo")
async def upload_company_logo(request: Request, file: UploadFile = File(...)):
    """
    Upload a company logo image.

    Accepts image files (JPEG, PNG, GIF, WebP, SVG) up to 5MB.
    Returns the public URL of the uploaded file.
    """
    try:
        user_id = request.state.user_id
    except AttributeError:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if not file.content_type:
        raise HTTPException(status_code=400, detail="Missing content type")

    try:
        # Read file content
        file_content = await file.read()

        # Upload to storage
        client = request.state.supabase_client
        public_url = file_upload_service.upload_company_logo(
            client=client,
            user_id=user_id,
            file_content=file_content,
            content_type=file.content_type,
            original_filename=file.filename,
        )

        logger.info(f"[ONBOARDING] Uploaded company logo for user {user_id}")

        return {"logo_url": public_url}

    except ValueError as e:
        logger.warning(f"[ONBOARDING] Invalid file upload: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"[ONBOARDING] Error uploading company logo: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to upload file")


@router.post("/upload-profile-picture")
async def upload_profile_picture(request: Request, file: UploadFile = File(...)):
    """
    Upload a profile picture image.

    Accepts image files (JPEG, PNG, GIF, WebP, SVG) up to 5MB.
    Returns the public URL of the uploaded file.
    """
    try:
        user_id = request.state.user_id
    except AttributeError:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if not file.content_type:
        raise HTTPException(status_code=400, detail="Missing content type")

    try:
        # Read file content
        file_content = await file.read()

        # Upload to storage
        client = request.state.supabase_client
        public_url = file_upload_service.upload_profile_picture(
            client=client,
            user_id=user_id,
            file_content=file_content,
            content_type=file.content_type,
            original_filename=file.filename,
        )

        logger.info(f"[ONBOARDING] Uploaded profile picture for user {user_id}")

        return {"profile_picture_url": public_url}

    except ValueError as e:
        logger.warning(f"[ONBOARDING] Invalid file upload: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"[ONBOARDING] Error uploading profile picture: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to upload file")
