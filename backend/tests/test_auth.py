"""
Auth test suite — covers every login scenario from the legacy PHP system.

Tests are organised in 4 groups:

  Group 1 — Unit tests for app/core/auth.py (no network, no DB)
  Group 2 — Integration tests for POST /api/v1/auth/login
  Group 3 — Integration tests for GET /me and POST /logout
  Group 4 — Protected route guard tests

All LDAP calls and DB calls are mocked — tests run fully offline.
"""

from __future__ import annotations

import time
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from jose import jwt

from app.core.config import settings
from app.db.session import get_clients_db
from app.main import app


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_token(username: str = "testuser", privy: str = "none",
                logcrew: str = "WP", uid: int = 42,
                expire_hours: int = 24) -> str:
    payload = {
        "sub": username, "privy": privy, "logcrew": logcrew, "uid": uid,
        "exp": datetime.now(timezone.utc) + timedelta(hours=expire_hours),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def _expired_token(username: str = "testuser") -> str:
    payload = {
        "sub": username, "privy": "none", "logcrew": "WP", "uid": 1,
        "exp": datetime.now(timezone.utc) - timedelta(hours=1),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def _tampered_token() -> str:
    payload = {
        "sub": "hacker", "privy": "admin", "logcrew": "WP", "uid": 0,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }
    return jwt.encode(payload, "wrong-secret", algorithm=settings.algorithm)


def _mock_db(privy=None, idno=None):
    """
    Mock async DB session.
    privy/idno set → simulates user found in clients.users.
    Both None → fetchone returns None (user not in DB).
    """
    db = AsyncMock()
    result = MagicMock()
    result.fetchone.return_value = (privy, idno) if privy is not None else None
    db.execute = AsyncMock(return_value=result)
    db.commit = AsyncMock()
    return db


def _override_db(privy=None, idno=None):
    """
    FastAPI dependency override for get_clients_db.
    Must be an async generator to match the real dependency signature.
    """
    async def _dep():
        yield _mock_db(privy, idno)
    return _dep


def _fresh_client() -> TestClient:
    """New TestClient with no carried-over cookies."""
    return TestClient(app, raise_server_exceptions=False)


# ===========================================================================
# GROUP 1 — Unit tests: app/core/auth.py (pure Python, no HTTP)
# ===========================================================================

class TestIsOAccount:
    """is_o_account() mirrors the PHP $oFail check in login2.php."""

    def test_classic_o_account(self):
        from app.core.auth import is_o_account
        assert is_o_account("o12345") is True

    def test_o_account_all_numeric(self):
        from app.core.auth import is_o_account
        assert is_o_account("o98765") is True

    def test_normal_username_not_blocked(self):
        from app.core.auth import is_o_account
        assert is_o_account("winegar") is False

    def test_too_short_not_blocked(self):
        from app.core.auth import is_o_account
        assert is_o_account("o123") is False   # only 5 chars

    def test_second_char_letter_not_blocked(self):
        from app.core.auth import is_o_account
        assert is_o_account("optics") is False  # 'p' not a digit

    def test_wrong_prefix_not_blocked(self):
        from app.core.auth import is_o_account
        assert is_o_account("a12345") is False

    def test_subaru_account_not_blocked(self):
        from app.core.auth import is_o_account
        assert is_o_account("subaru") is False

    def test_empty_string_not_blocked(self):
        from app.core.auth import is_o_account
        assert is_o_account("") is False


class TestJWT:
    """JWT creation and validation."""

    def test_roundtrip(self):
        from app.core.auth import create_access_token, decode_access_token
        token = create_access_token({"sub": "winegar", "privy": "admin",
                                     "logcrew": "TO", "uid": 99})
        payload = decode_access_token(token)
        assert payload["sub"] == "winegar"
        assert payload["privy"] == "admin"
        assert payload["logcrew"] == "TO"
        assert payload["uid"] == 99

    def test_expired_raises_401(self):
        from fastapi import HTTPException
        from app.core.auth import decode_access_token
        with pytest.raises(HTTPException) as exc:
            decode_access_token(_expired_token())
        assert exc.value.status_code == 401

    def test_tampered_raises_401(self):
        from fastapi import HTTPException
        from app.core.auth import decode_access_token
        with pytest.raises(HTTPException) as exc:
            decode_access_token(_tampered_token())
        assert exc.value.status_code == 401

    def test_garbage_raises_401(self):
        from fastapi import HTTPException
        from app.core.auth import decode_access_token
        with pytest.raises(HTTPException) as exc:
            decode_access_token("this.is.garbage")
        assert exc.value.status_code == 401

    def test_token_has_future_expiry(self):
        from app.core.auth import create_access_token
        token = create_access_token({"sub": "test"})
        payload = jwt.decode(token, settings.secret_key,
                             algorithms=[settings.algorithm])
        assert payload["exp"] > time.time()


# ===========================================================================
# GROUP 2 — Integration tests: POST /api/v1/auth/login
# ===========================================================================

class TestLogin:
    """
    Each test gets a fresh client + clean dependency overrides
    so no cookies or DB state leaks between tests.
    """

    def setup_method(self):
        app.dependency_overrides = {}
        self.client = _fresh_client()

    def teardown_method(self):
        app.dependency_overrides = {}

    # ── Successful logins ────────────────────────────────────────────────────

    def test_success_returns_user_data_and_cookie(self):
        """Valid LDAP credentials → 200, correct JSON, httpOnly cookie set."""
        app.dependency_overrides[get_clients_db] = _override_db("none", 42)
        with patch("app.api.v1.auth.ldap_validate", return_value=True), \
             patch("app.api.v1.auth.get_ldap_groups", return_value=("WP", "none")):
            r = self.client.post("/api/v1/auth/login",
                                 json={"username": "winegar", "password": "secret"})

        assert r.status_code == 200
        d = r.json()
        assert d["username"] == "winegar"
        assert d["privy"] == "none"
        assert d["logcrew"] == "WP"
        assert d["uid"] == 42
        assert settings.cookie_name in r.cookies

    def test_username_is_lowercased(self):
        """Input 'WINEGAR' must be normalised to 'winegar' (mirrors PHP strtolower)."""
        app.dependency_overrides[get_clients_db] = _override_db()
        with patch("app.api.v1.auth.ldap_validate", return_value=True), \
             patch("app.api.v1.auth.get_ldap_groups", return_value=("WP", "none")):
            r = self.client.post("/api/v1/auth/login",
                                 json={"username": "WINEGAR", "password": "secret"})

        assert r.status_code == 200
        assert r.json()["username"] == "winegar"

    def test_user_not_in_db_defaults_privy_none_uid_zero(self):
        """LDAP passes but user absent from clients.users → privy='none', uid=0."""
        app.dependency_overrides[get_clients_db] = _override_db()  # fetchone → None
        with patch("app.api.v1.auth.ldap_validate", return_value=True), \
             patch("app.api.v1.auth.get_ldap_groups", return_value=("WP", "none")):
            r = self.client.post("/api/v1/auth/login",
                                 json={"username": "newperson", "password": "secret"})

        assert r.status_code == 200
        assert r.json()["privy"] == "none"
        assert r.json()["uid"] == 0

    # ── LDAP group → role mapping ────────────────────────────────────────────

    def test_ssgroup_member_gets_TO_and_subaru(self):
        """ssgroup/operators → logcrew='TO', privy='subaru' (telescope operator)."""
        app.dependency_overrides[get_clients_db] = _override_db("none", 10)
        with patch("app.api.v1.auth.ldap_validate", return_value=True), \
             patch("app.api.v1.auth.get_ldap_groups", return_value=("TO", "subaru")):
            r = self.client.post("/api/v1/auth/login",
                                 json={"username": "operator1", "password": "secret"})

        assert r.status_code == 200
        assert r.json()["logcrew"] == "TO"
        assert r.json()["privy"] == "subaru"

    def test_opecenter_member_gets_admin(self):
        """opecenter group → privy='admin'."""
        app.dependency_overrides[get_clients_db] = _override_db("none", 5)
        with patch("app.api.v1.auth.ldap_validate", return_value=True), \
             patch("app.api.v1.auth.get_ldap_groups", return_value=("WP", "admin")):
            r = self.client.post("/api/v1/auth/login",
                                 json={"username": "mgr", "password": "secret"})

        assert r.status_code == 200
        assert r.json()["privy"] == "admin"

    def test_daycrew_member_gets_DC(self):
        """daycrew group → logcrew='DC'."""
        app.dependency_overrides[get_clients_db] = _override_db("none", 7)
        with patch("app.api.v1.auth.ldap_validate", return_value=True), \
             patch("app.api.v1.auth.get_ldap_groups", return_value=("DC", "none")):
            r = self.client.post("/api/v1/auth/login",
                                 json={"username": "daycrew1", "password": "secret"})

        assert r.status_code == 200
        assert r.json()["logcrew"] == "DC"

    def test_no_ldap_group_defaults_WP(self):
        """No LDAP group → logcrew='WP' (Work Plan — the default)."""
        app.dependency_overrides[get_clients_db] = _override_db("none", 3)
        with patch("app.api.v1.auth.ldap_validate", return_value=True), \
             patch("app.api.v1.auth.get_ldap_groups", return_value=("WP", "none")):
            r = self.client.post("/api/v1/auth/login",
                                 json={"username": "observer", "password": "secret"})

        assert r.status_code == 200
        assert r.json()["logcrew"] == "WP"

    # ── Special 'subaru' shared account ─────────────────────────────────────

    def test_subaru_account_always_gets_top_privy(self):
        """'subaru' is always forced to privy='subaru', uid=0 regardless of DB/LDAP."""
        app.dependency_overrides[get_clients_db] = _override_db("none", 999)
        with patch("app.api.v1.auth.ldap_validate", return_value=True), \
             patch("app.api.v1.auth.get_ldap_groups", return_value=("WP", "none")):
            r = self.client.post("/api/v1/auth/login",
                                 json={"username": "subaru", "password": "secret"})

        assert r.status_code == 200
        assert r.json()["privy"] == "subaru"
        assert r.json()["uid"] == 0

    # ── Failure cases ────────────────────────────────────────────────────────

    def test_wrong_password_returns_401(self):
        """LDAP bind fails → 401 Unauthorized."""
        app.dependency_overrides[get_clients_db] = _override_db()
        with patch("app.api.v1.auth.ldap_validate", return_value=False):
            r = self.client.post("/api/v1/auth/login",
                                 json={"username": "winegar", "password": "wrong"})

        assert r.status_code == 401
        assert "invalid" in r.json()["detail"].lower()

    def test_o_account_returns_403(self):
        """o-accounts blocked before LDAP is attempted → 403 Forbidden."""
        app.dependency_overrides[get_clients_db] = _override_db()
        r = self.client.post("/api/v1/auth/login",
                             json={"username": "o12345", "password": "anything"})

        assert r.status_code == 403
        assert "not permitted" in r.json()["detail"].lower()

    def test_missing_username_returns_422(self):
        r = self.client.post("/api/v1/auth/login", json={"password": "secret"})
        assert r.status_code == 422

    def test_missing_password_returns_422(self):
        r = self.client.post("/api/v1/auth/login", json={"username": "winegar"})
        assert r.status_code == 422

    def test_empty_body_returns_422(self):
        r = self.client.post("/api/v1/auth/login", json={})
        assert r.status_code == 422

    # ── Cookie security ──────────────────────────────────────────────────────

    def test_cookie_is_httponly(self):
        """httpOnly prevents JS from reading the session token."""
        app.dependency_overrides[get_clients_db] = _override_db()
        with patch("app.api.v1.auth.ldap_validate", return_value=True), \
             patch("app.api.v1.auth.get_ldap_groups", return_value=("WP", "none")):
            r = self.client.post("/api/v1/auth/login",
                                 json={"username": "winegar", "password": "secret"})

        assert r.status_code == 200
        assert "httponly" in r.headers.get("set-cookie", "").lower()

    def test_cookie_has_max_age(self):
        """Cookie carries a max-age so the browser enforces the 24-hr expiry."""
        app.dependency_overrides[get_clients_db] = _override_db()
        with patch("app.api.v1.auth.ldap_validate", return_value=True), \
             patch("app.api.v1.auth.get_ldap_groups", return_value=("WP", "none")):
            r = self.client.post("/api/v1/auth/login",
                                 json={"username": "winegar", "password": "secret"})

        assert "max-age" in r.headers.get("set-cookie", "").lower()


# ===========================================================================
# GROUP 3 — GET /me  and  POST /logout
# ===========================================================================

class TestMe:
    """Each test uses a fresh client to avoid cookie pollution from other tests."""

    def setup_method(self):
        app.dependency_overrides = {}

    def teardown_method(self):
        app.dependency_overrides = {}

    def test_me_with_valid_cookie_returns_user(self):
        token = _make_token("winegar", "admin", "TO", 99)
        client = _fresh_client()
        client.cookies.set(settings.cookie_name, token)
        r = client.get("/api/v1/auth/me")

        assert r.status_code == 200
        d = r.json()
        assert d["username"] == "winegar"
        assert d["privy"] == "admin"
        assert d["logcrew"] == "TO"
        assert d["uid"] == 99

    def test_me_returns_all_required_fields(self):
        token = _make_token("noriko", "subaru", "DC", 7)
        client = _fresh_client()
        client.cookies.set(settings.cookie_name, token)
        r = client.get("/api/v1/auth/me")

        assert r.status_code == 200
        assert {"username", "privy", "logcrew", "uid"}.issubset(r.json().keys())

    def test_me_without_cookie_returns_401(self):
        r = _fresh_client().get("/api/v1/auth/me")
        assert r.status_code == 401

    def test_me_with_expired_token_returns_401(self):
        client = _fresh_client()
        client.cookies.set(settings.cookie_name, _expired_token())
        r = client.get("/api/v1/auth/me")
        assert r.status_code == 401

    def test_me_with_tampered_token_returns_401(self):
        client = _fresh_client()
        client.cookies.set(settings.cookie_name, _tampered_token())
        r = client.get("/api/v1/auth/me")
        assert r.status_code == 401


class TestLogout:

    def setup_method(self):
        app.dependency_overrides = {}

    def teardown_method(self):
        app.dependency_overrides = {}

    def test_logout_with_valid_cookie_succeeds(self):
        app.dependency_overrides[get_clients_db] = _override_db()
        client = _fresh_client()
        client.cookies.set(settings.cookie_name, _make_token("winegar"))
        r = client.post("/api/v1/auth/logout")

        assert r.status_code == 200
        assert "logged out" in r.json()["message"].lower()

    def test_logout_clears_cookie(self):
        """After logout the cookie max-age must be 0 (deleted)."""
        app.dependency_overrides[get_clients_db] = _override_db()
        client = _fresh_client()
        client.cookies.set(settings.cookie_name, _make_token("winegar"))
        r = client.post("/api/v1/auth/logout")

        set_cookie = r.headers.get("set-cookie", "").lower()
        assert "max-age=0" in set_cookie

    def test_logout_without_cookie_returns_401(self):
        r = _fresh_client().post("/api/v1/auth/logout")
        assert r.status_code == 401

    def test_logout_with_expired_token_returns_401(self):
        client = _fresh_client()
        client.cookies.set(settings.cookie_name, _expired_token())
        r = client.post("/api/v1/auth/logout")
        assert r.status_code == 401


# ===========================================================================
# GROUP 4 — Protected route guard
# ===========================================================================

class TestProtectedRoutes:
    """Write endpoints require auth; read endpoints remain public."""

    def test_create_fats_without_auth_returns_401(self):
        r = _fresh_client().post("/api/v1/fats/",
                                 json={"title": "Test", "date": "2026-01-01"})
        assert r.status_code == 401

    def test_update_fats_without_auth_returns_401(self):
        r = _fresh_client().put("/api/v1/fats/9999", json={})
        assert r.status_code == 401

    def test_delete_fats_without_auth_returns_401(self):
        r = _fresh_client().delete("/api/v1/fats/9999")
        assert r.status_code == 401

    def test_add_comment_without_auth_returns_401(self):
        r = _fresh_client().post("/api/v1/fats/9999/comments",
                                 json={"comment_text": "test"})
        assert r.status_code == 401

    def test_upload_image_without_auth_returns_401(self):
        r = _fresh_client().post("/api/v1/fats/9999/images",
                                 files={"file": ("f.jpg", b"data", "image/jpeg")})
        assert r.status_code == 401

    def test_create_summit_day_without_auth_returns_401(self):
        r = _fresh_client().post("/api/v1/summit/days",
                                 json={"log_date": "2026-01-01"})
        assert r.status_code == 401

    def test_patch_summit_day_without_auth_returns_401(self):
        r = _fresh_client().patch("/api/v1/summit/day/2026-01-01", json={})
        assert r.status_code == 401

    def test_create_log_item_without_auth_returns_401(self):
        r = _fresh_client().post("/api/v1/summit/day/2026-01-01/items", json={})
        assert r.status_code == 401

    def test_get_fats_list_is_public(self):
        """GET (read) endpoints should not require auth."""
        r = _fresh_client().get("/api/v1/fats/")
        assert r.status_code != 401

    def test_get_reference_sections_is_public(self):
        r = _fresh_client().get("/api/v1/reference/sections")
        assert r.status_code != 401

    def test_health_endpoint_is_public(self):
        r = _fresh_client().get("/health")
        assert r.status_code == 200
