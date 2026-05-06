"""
Authentication core — LDAP validation, group lookup, JWT utilities, and
the FastAPI dependency used to guard protected routes.

Mirrors the logic from the legacy login2.php:
  - ldap_validate()       → PHP ldap_validate($user, $pw)
  - is_o_account()        → PHP $oFail check
  - get_ldap_groups()     → PHP ldap_search() + group loop → logcrew / privy
  - create_access_token() → PHP $_SESSION['login'] / killsession
  - require_auth()        → PHP door.php / door()
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Cookie, HTTPException, Request, status
from jose import JWTError, jwt
from ldap3 import ALL_ATTRIBUTES, Connection, Server, SUBTREE
from ldap3.core.exceptions import LDAPException

from app.core.config import settings

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# o-account blocker (port of PHP $oFail logic)
# ---------------------------------------------------------------------------

def is_o_account(username: str) -> bool:
    """
    Block observer-type accounts (e.g. o12345).
    Matches PHP: strlen==6, first char 'o', second char is a digit.
    """
    if len(username) == 6 and username[0] == "o" and username[1].isdigit():
        return True
    return False


# ---------------------------------------------------------------------------
# LDAP credential validation (port of PHP ldap_validate($user, $pw))
# ---------------------------------------------------------------------------

def _check_dev_local_user(username: str, password: str) -> bool:
    """
    In DEBUG mode, allow login via DEV_LOCAL_USERS env var.
    Format: "user1:pass1,user2:pass2"
    """
    if not settings.debug or not settings.dev_local_users:
        return False
    for entry in settings.dev_local_users.split(","):
        entry = entry.strip()
        if ":" not in entry:
            continue
        u, p = entry.split(":", 1)
        if u.strip() == username and p.strip() == password:
            logger.info("Dev local user bypass for: %s", username)
            return True
    return False


def ldap_validate(username: str, password: str) -> bool:
    """
    Attempt a simple-bind against the Subaru LDAP server.
    In DEBUG mode, DEV_LOCAL_USERS entries bypass LDAP entirely.
    Returns True on success, False on any failure.
    """
    if not password:
        return False

    # Dev bypass — skip LDAP when running locally
    if _check_dev_local_user(username, password):
        return True

    user_dn = f"uid={username},{settings.ldap_people_dn}"
    try:
        server = Server(settings.ldap_host, port=settings.ldap_port)
        conn = Connection(server, user=user_dn, password=password, auto_bind=True)
        conn.unbind()
        logger.info("LDAP bind succeeded for user: %s", username)
        return True
    except LDAPException as exc:
        logger.warning("LDAP bind failed for user %s: %s", username, exc)
        return False
    except Exception as exc:
        logger.error("Unexpected LDAP error for user %s: %s", username, exc)
        return False


# ---------------------------------------------------------------------------
# LDAP group lookup (port of PHP ldap_search + group loop)
# ---------------------------------------------------------------------------

# Map of LDAP cn → (logcrew, privy).  Later entries in the list can
# override earlier ones, matching the PHP loop behaviour.
_GROUP_RULES: list[tuple[str, Optional[str], Optional[str]]] = [
    # (group cn,  logcrew override,  privy override)
    ("ssgroup",   "TO",             "subaru"),
    ("operators", "TO",             "subaru"),
    ("opecenter", None,             "admin"),
    ("daycrew",   "DC",             None),
]


def get_ldap_groups(username: str) -> tuple[str, str]:
    """
    Search LDAP for all groups that contain the user and derive
    logcrew + privy exactly as login2.php did.

    In DEBUG mode, dev-bypass users get admin/TO privileges without LDAP.
    Returns (logcrew, privy).  Defaults: ('WP', 'none').
    """
    # Dev bypass — grant TO + admin to any local dev user
    if settings.debug and settings.dev_local_users:
        for entry in settings.dev_local_users.split(","):
            if ":" in entry and entry.strip().split(":", 1)[0].strip() == username:
                logger.info("Dev local user group bypass for: %s → TO/admin", username)
                return "TO", "admin"

    logcrew = "WP"
    privy = "none"

    try:
        server = Server(settings.ldap_host, port=settings.ldap_port)
        # Anonymous bind for group search (same as PHP — no bind credentials used)
        conn = Connection(server, auto_bind=True)
        conn.search(
            search_base=settings.ldap_group_dn,
            search_filter=f"(memberuid={username})",
            search_scope=SUBTREE,
            attributes=["cn"],
        )
        entries = conn.entries
        conn.unbind()

        for entry in entries:
            group_cn = str(entry.cn).strip()
            for rule_cn, lc_override, privy_override in _GROUP_RULES:
                if group_cn == rule_cn:
                    if lc_override:
                        logcrew = lc_override
                    if privy_override:
                        privy = privy_override

        logger.info("LDAP groups for %s → logcrew=%s privy=%s", username, logcrew, privy)
    except LDAPException as exc:
        logger.warning("LDAP group lookup failed for %s: %s", username, exc)
    except Exception as exc:
        logger.error("Unexpected error in LDAP group lookup for %s: %s", username, exc)

    return logcrew, privy


# ---------------------------------------------------------------------------
# JWT helpers
# ---------------------------------------------------------------------------

def create_access_token(data: dict) -> str:
    """
    Create a signed JWT.  Token payload = data + 'exp' claim.
    """
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.access_token_expire_hours)
    payload["exp"] = expire
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT.  Raises HTTP 401 on any error.
    """
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError as exc:
        logger.warning("JWT decode failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid. Please log in again.",
        )


# ---------------------------------------------------------------------------
# FastAPI dependency — guards protected routes (replaces PHP door.php)
# ---------------------------------------------------------------------------

async def require_auth(request: Request) -> dict:
    """
    FastAPI dependency.  Reads the httpOnly session cookie, validates the JWT,
    and returns the decoded payload dict.

    Usage:
        @router.post("/some-protected-endpoint")
        async def handler(current_user: dict = Depends(require_auth)):
            ...
    """
    token: Optional[str] = request.cookies.get(settings.cookie_name)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Please log in.",
        )
    return decode_access_token(token)
