from fastapi import Response
from domains.entities import Session
from config.settings import settings, Environment

from domains.entities import Session

COOKIE_MAX_AGE = 7 * 24 * 60 * 60  # 7 days
ACCESS_COOKIE_KEY = "access_token"
REFRESH_COOKIE_KEY = "refresh_token"


def get_cookie_domain() -> str | None:
    """
    Get cookie domain based on environment.
    - Local: None (localhost doesn't need domain)
    - Dev: .dev.jayd.ai (shared across subdomains)
    - Prod: .jayd.ai (shared across subdomains)
    """
    env = settings.ENVIRONMENT
    if env == Environment.LOCAL:
        return None
    elif env == Environment.DEV:
        return ".dev.jayd.ai"
    else:  # Production
        return ".jayd.ai"


def is_secure_cookie() -> bool:
    """
    Determine if cookies should be secure (HTTPS only).
    - Local: False (HTTP)
    - Dev/Prod: True (HTTPS)
    """
    return settings.ENVIRONMENT != Environment.LOCAL


def set_auth_cookies(response: Response, session: Session) -> None:
    """
    Set authentication cookies for both access and refresh tokens.
    Cookies are configured based on environment for cross-subdomain auth.
    """
    cookie_domain = get_cookie_domain()
    secure = is_secure_cookie()

    # Common cookie parameters
    cookie_params = {
        "httponly": True,
        "secure": secure,
        "samesite": "lax",
        "max_age": COOKIE_MAX_AGE,
        "path": "/"
    }

    # Add domain if applicable (not for localhost)
    if cookie_domain:
        cookie_params["domain"] = cookie_domain

    # Set access token cookie
    response.set_cookie(
        key=ACCESS_COOKIE_KEY,
        value=session.access_token,
        **cookie_params
    )

    # Set refresh token cookie
    response.set_cookie(
        key=REFRESH_COOKIE_KEY,
        value=session.refresh_token,
        **cookie_params
    )


def clear_auth_cookies(response: Response) -> None:
    """
    Clear authentication cookies.
    Must match the domain used when setting cookies for proper deletion.
    """
    cookie_domain = get_cookie_domain()

    # Common parameters for deletion
    delete_params = {"path": "/"}
    if cookie_domain:
        delete_params["domain"] = cookie_domain

    response.delete_cookie(
        key=ACCESS_COOKIE_KEY,
        **delete_params
    )
    response.delete_cookie(
        key=REFRESH_COOKIE_KEY,
        **delete_params
    )
