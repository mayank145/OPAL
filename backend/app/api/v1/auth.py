"""
Auth router — /api/v1/auth

Endpoints:
  POST /login   — LDAP authenticate, issue JWT cookie, audit log
  POST /logout  — Clear JWT cookie, audit log
  GET  /me      — Return current user info from JWT

Replicates the full flow of legacy login2.php + logout.php.
"""

from __future__ import annotations

import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import (
    create_access_token,
    get_ldap_groups,
    is_o_account,
    ldap_validate,
    require_auth,
)
from app.core.config import settings
from app.db.session import get_clients_db

logger = logging.getLogger(__name__)

router = APIRouter()


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------

class LoginRequest(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str
    privy: str
    logcrew: str
    uid: int


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _set_auth_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=settings.cookie_name,
        value=token,
        max_age=settings.access_token_expire_hours * 3600,
        httponly=settings.cookie_httponly,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
    )


def _clear_auth_cookie(response: Response) -> None:
    response.delete_cookie(
        key=settings.cookie_name,
        httponly=settings.cookie_httponly,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
    )


async def _audit_log(
    db: AsyncSession,
    session_id: str,
    username: str,
    remote_ip: str,
    page: str,
    method: str,
    comment: str = "",
) -> None:
    """
    Insert a row into the sessions table — mirrors PHP sessions INSERT.
    Silently ignores errors so a missing table never breaks login.
    """
    now = datetime.now()
    now_str = now.strftime("%m/%d/%Y %H:%M:%S")
    now2_str = now.strftime("%Y-%m-%d")
    try:
        await db.execute(
            text(
                "INSERT INTO sessions "
                "(session, user, intime, intime2, page, remoteip, query, method, comment) "
                "VALUES (:sess, :user, :intime, :intime2, :page, :remoteip, :query, :method, :comment)"
            ),
            {
                "sess": session_id,
                "user": username,
                "intime": now_str,
                "intime2": now2_str,
                "page": page,
                "remoteip": remote_ip,
                "query": "",
                "method": method,
                "comment": comment,
            },
        )
        await db.commit()
    except Exception as exc:
        logger.warning("Audit log insert failed (non-fatal): %s", exc)


# ---------------------------------------------------------------------------
# POST /login
# ---------------------------------------------------------------------------

@router.post("/login", response_model=UserResponse)
async def login(
    body: LoginRequest,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_clients_db),
) -> UserResponse:
    """
    Authenticate via Subaru LDAP and issue a session cookie.

    Flow (mirrors login2.php):
      1. Normalise username
      2. Block o-accounts
      3. LDAP bind validation
      4. Fetch uid + privy from MariaDB users table
      5. LDAP group lookup → logcrew / privy override
      6. Special 'subaru' account override
      7. Issue JWT cookie (24 h)
      8. Audit log → sessions table
    """
    username = body.username.strip().lower()
    password = body.password
    remote_ip = request.client.host if request.client else "unknown"

    # Step 2 — block o-accounts
    if is_o_account(username):
        logger.warning("o-account login attempt blocked: %s from %s", username, remote_ip)
        await _audit_log(db, "LoginFailed", username, remote_ip, "/api/v1/auth/login", "POST", "o-account blocked")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account type is not permitted to log in.",
        )

    # Step 3 — LDAP credential check
    if not ldap_validate(username, password):
        logger.warning("Failed login for %s from %s", username, remote_ip)
        await _audit_log(db, "LoginFailed", username, remote_ip, "/api/v1/auth/login", "POST")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username/Password is invalid!",
        )

    # Step 4 — fetch uid + privy from clients.users table
    # `username` is the STN login column (confirmed from live schema: describe users)
    uid = 0
    privy = "none"
    try:
        result = await db.execute(
            text("SELECT privy, idno FROM users WHERE username = :user LIMIT 1"),
            {"user": username},
        )
        row = result.fetchone()
        if row:
            privy = (row[0] or "none").strip()
            uid = int(row[1] or 0)
    except Exception as exc:
        logger.warning("users table lookup failed for %s (non-fatal): %s", username, exc)

    # Step 5 — LDAP group lookup (may override privy / set logcrew)
    logcrew, group_privy = get_ldap_groups(username)
    if group_privy != "none":
        privy = group_privy

    # Step 6 — shared 'subaru' account always gets top privilege
    if username == "subaru":
        privy = "subaru"
        uid = 0

    # Step 7 — create JWT and set cookie
    token_data = {
        "sub": username,
        "privy": privy,
        "logcrew": logcrew,
        "uid": uid,
    }
    token = create_access_token(token_data)
    _set_auth_cookie(response, token)

    # Step 8 — audit log
    await _audit_log(
        db,
        session_id=token[:32],  # use first 32 chars of token as session id
        username=username,
        remote_ip=remote_ip,
        page="/api/v1/auth/login",
        method="POST",
        comment=f"{username} | privy={privy} | logcrew={logcrew}",
    )

    logger.info("Login success: %s privy=%s logcrew=%s from %s", username, privy, logcrew, remote_ip)
    return UserResponse(username=username, privy=privy, logcrew=logcrew, uid=uid)


# ---------------------------------------------------------------------------
# POST /logout
# ---------------------------------------------------------------------------

@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    current_user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_clients_db),
) -> dict:
    """
    Clear the session cookie and record the logout in the audit log.
    Mirrors logout.php: session_unset() + session_destroy().
    """
    username = current_user.get("sub", "unknown")
    remote_ip = request.client.host if request.client else "unknown"

    _clear_auth_cookie(response)

    await _audit_log(
        db,
        session_id="LoggedOut",
        username=username,
        remote_ip=remote_ip,
        page="/api/v1/auth/logout",
        method="POST",
    )

    logger.info("Logout: %s from %s", username, remote_ip)
    return {"message": "Logged out successfully."}


# ---------------------------------------------------------------------------
# GET /me
# ---------------------------------------------------------------------------

@router.get("/me", response_model=UserResponse)
async def me(current_user: dict = Depends(require_auth)) -> UserResponse:
    """
    Return the current authenticated user's info from the JWT.
    Used by the frontend on page load to restore session state.
    """
    return UserResponse(
        username=current_user.get("sub", ""),
        privy=current_user.get("privy", "none"),
        logcrew=current_user.get("logcrew", "WP"),
        uid=current_user.get("uid", 0),
    )
