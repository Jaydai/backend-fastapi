"""
File Upload Service

Handles file uploads to Supabase Storage for organization logos and profile pictures.
"""

import logging
import uuid

from supabase import Client

logger = logging.getLogger(__name__)

# Configuration
STORAGE_BUCKET = "uploads"
ORGANIZATION_LOGOS_FOLDER = "organization-logos"
PROFILE_PICTURES_FOLDER = "profile-pictures"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml"]


class FileUploadService:
    """
    Service for uploading files to Supabase Storage.

    Features:
    - Upload organization logos
    - Upload profile pictures
    - File type validation
    - File size validation
    - Generate public URLs
    """

    @staticmethod
    def validate_image(content_type: str, file_size: int) -> None:
        """
        Validate image file type and size.

        Args:
            content_type: MIME type of the file
            file_size: Size of the file in bytes

        Raises:
            ValueError: If validation fails
        """
        if content_type not in ALLOWED_IMAGE_TYPES:
            raise ValueError(f"Invalid file type: {content_type}. Allowed: {', '.join(ALLOWED_IMAGE_TYPES)}")

        if file_size > MAX_FILE_SIZE:
            raise ValueError(f"File too large: {file_size} bytes. Maximum: {MAX_FILE_SIZE} bytes")

    @staticmethod
    def upload_organization_logo(
        client: Client,
        user_id: str,
        file_content: bytes,
        content_type: str,
        original_filename: str | None = None,
    ) -> str:
        """
        Upload an organization logo to Supabase Storage.

        Args:
            client: Supabase client
            user_id: User ID for organizing files
            file_content: Binary content of the file
            content_type: MIME type of the file
            original_filename: Original filename (optional, for extension)

        Returns:
            Public URL of the uploaded file
        """
        FileUploadService.validate_image(content_type, len(file_content))

        extension = FileUploadService._get_extension(content_type, original_filename)
        filename = f"{uuid.uuid4()}{extension}"
        file_path = f"{ORGANIZATION_LOGOS_FOLDER}/{user_id}/{filename}"

        try:
            client.storage.from_(STORAGE_BUCKET).upload(
                path=file_path,
                file=file_content,
                file_options={"content-type": content_type},
            )

            public_url = client.storage.from_(STORAGE_BUCKET).get_public_url(file_path)

            logger.info(f"Uploaded organization logo for user {user_id}: {file_path}")
            return public_url

        except Exception as e:
            logger.error(f"Error uploading organization logo: {e}", exc_info=True)
            raise ValueError(f"Failed to upload file: {str(e)}")

    # Legacy alias for backward compatibility
    upload_company_logo = upload_organization_logo

    @staticmethod
    def upload_profile_picture(
        client: Client,
        user_id: str,
        file_content: bytes,
        content_type: str,
        original_filename: str | None = None,
    ) -> str:
        """
        Upload a profile picture to Supabase Storage.

        Args:
            client: Supabase client
            user_id: User ID for organizing files
            file_content: Binary content of the file
            content_type: MIME type of the file
            original_filename: Original filename (optional, for extension)

        Returns:
            Public URL of the uploaded file
        """
        FileUploadService.validate_image(content_type, len(file_content))

        extension = FileUploadService._get_extension(content_type, original_filename)
        filename = f"{uuid.uuid4()}{extension}"
        file_path = f"{PROFILE_PICTURES_FOLDER}/{user_id}/{filename}"

        try:
            client.storage.from_(STORAGE_BUCKET).upload(
                path=file_path,
                file=file_content,
                file_options={"content-type": content_type},
            )

            public_url = client.storage.from_(STORAGE_BUCKET).get_public_url(file_path)

            logger.info(f"Uploaded profile picture for user {user_id}: {file_path}")
            return public_url

        except Exception as e:
            logger.error(f"Error uploading profile picture: {e}", exc_info=True)
            raise ValueError(f"Failed to upload file: {str(e)}")

    @staticmethod
    def _get_extension(content_type: str, original_filename: str | None) -> str:
        """Get file extension from content type or original filename."""
        # Try to get from original filename first
        if original_filename and "." in original_filename:
            return "." + original_filename.rsplit(".", 1)[1].lower()

        # Fall back to content type mapping
        type_to_ext = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/gif": ".gif",
            "image/webp": ".webp",
            "image/svg+xml": ".svg",
        }
        return type_to_ext.get(content_type, ".png")


# Singleton instance
file_upload_service = FileUploadService()
