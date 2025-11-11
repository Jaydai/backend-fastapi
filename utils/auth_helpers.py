from fastapi import Response
from domains.entities import Session


COOKIE_MAX_AGE = 7 * 24 * 60 * 60  # 7 days
SESSION_COOKIE_KEY = "session_token"
REFRESH_COOKIE_KEY = "refresh_token"


def set_auth_cookies(response: Response, session: Session) -> None:
    response.set_cookie(
        key=SESSION_COOKIE_KEY,
        value=session.access_token,
        httponly=True,
        secure=True,  # HTTPS only
        samesite="lax",
        max_age=COOKIE_MAX_AGE,
        path="/"
    )

    response.set_cookie(
        key=REFRESH_COOKIE_KEY,
        value=session.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=COOKIE_MAX_AGE,
        path="/"
    )


def clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(
        key=SESSION_COOKIE_KEY,
        path="/"
    )
    response.delete_cookie(
        key=REFRESH_COOKIE_KEY,
        path="/"
    )
