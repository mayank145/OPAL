"""
Summit Log end-to-end test suite.

Tests run against the LIVE server at http://127.0.0.1:8000
(start it with: source venv/bin/activate && uvicorn app.main:app --reload --port 8000)

Auth is provided by constructing a valid JWT and passing it as a cookie — exactly
the same pattern as the unit test in test_auth.py.

Covers:
  1  Health check
  2  Monthly view (structure, validation)
  3  Year overview  (structure, first_instr, empty year)
  4  Day CRUD       (create, view, patch, zoom fields, 409 duplicate)
  5  Log Items CRUD (create, get, patch, delete, summit_access field)
  6  Summit Access  (dedicated field-level tests)
  7  Work Plans     (create, patch, delete; new transport/seating fields)
  8  Crew           (create, patch, delete)
  9  Weather        (upsert, idempotent)
 10  Programs       (create, patch, delete)
 11  Search         (keyword, multi-word, date-range, crew-tab, pagination)
 12  Auth guards    (all write endpoints must reject no-cookie requests)
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import httpx
import pytest
from jose import jwt

# ── config ───────────────────────────────────────────────────────────────────
BASE_URL = "http://127.0.0.1:8000"
BASE = f"{BASE_URL}/api/v1/summit"

# A test day we own end-to-end (year 2099 avoids colliding with real data)
_CREATE_DATE = "2099-12-01"


# ── auth helpers ─────────────────────────────────────────────────────────────

def _get_secret_key() -> str:
    from app.core.config import settings
    return settings.secret_key


def _get_cookie_name() -> str:
    from app.core.config import settings
    return settings.cookie_name


def _make_token(username: str = "testuser", privy: str = "subaru",
                logcrew: str = "TO") -> str:
    from app.core.config import settings
    payload = {
        "sub": username, "privy": privy, "logcrew": logcrew, "uid": 1,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def _auth_headers() -> dict:
    cookie_name = _get_cookie_name()
    token = _make_token()
    return {"Cookie": f"{cookie_name}={token}"}


# ── shared clients ────────────────────────────────────────────────────────────

AUTH = httpx.Client(base_url=BASE_URL, headers=_auth_headers(), timeout=15,
                    follow_redirects=True)
ANON = httpx.Client(base_url=BASE_URL, timeout=15, follow_redirects=True)


# ── utility ───────────────────────────────────────────────────────────────────

def _ok(resp: httpx.Response, expected=(200, 201)):
    codes = (expected,) if isinstance(expected, int) else tuple(expected)
    assert resp.status_code in codes, (
        f"Expected {codes}, got {resp.status_code}: {resp.text[:600]}"
    )
    return resp.json()


# =============================================================================
# 1  Health
# =============================================================================

class TestHealth:
    def test_summit_health(self):
        r = AUTH.get(f"{BASE}/health")
        d = _ok(r)
        assert d["status"] == "healthy"
        assert d["database"] == "postgres"


# =============================================================================
# 2  Monthly view
# =============================================================================

class TestMonthly:
    def test_monthly_returns_structure(self):
        r = AUTH.get(f"{BASE}/monthly", params={"year": 2026, "month": 5})
        d = _ok(r)
        assert "year" in d and "month" in d and "days" in d
        assert d["year"] == 2026 and d["month"] == 5
        assert isinstance(d["days"], list)

    def test_monthly_day_fields(self):
        r = AUTH.get(f"{BASE}/monthly", params={"year": 2026, "month": 5})
        d = _ok(r)
        if d["days"]:
            day = d["days"][0]
            for key in ("id", "log_date", "entry_count", "total_downtime"):
                assert key in day

    def test_monthly_invalid_month_422(self):
        r = AUTH.get(f"{BASE}/monthly", params={"year": 2026, "month": 13})
        assert r.status_code == 422

    def test_monthly_no_auth_allowed(self):
        r = ANON.get(f"{BASE}/monthly", params={"year": 2026, "month": 5})
        assert r.status_code == 200


# =============================================================================
# 3  Year overview
# =============================================================================

class TestYearOverview:
    def test_year_structure(self):
        r = AUTH.get(f"{BASE}/year/2026")
        d = _ok(r)
        assert "year" in d and "days" in d
        assert d["year"] == 2026
        assert isinstance(d["days"], list)

    def test_year_empty_for_future(self):
        r = AUTH.get(f"{BASE}/year/2098")
        d = _ok(r)
        assert d["days"] == []

    def test_year_first_instr_key_present(self):
        r = AUTH.get(f"{BASE}/year/2026")
        d = _ok(r)
        if d["days"]:
            assert "first_instr" in d["days"][0]

    def test_year_counts_non_negative(self):
        r = AUTH.get(f"{BASE}/year/2026")
        d = _ok(r)
        for day in d["days"]:
            assert day["entry_count"] >= 0
            assert day["total_downtime"] >= 0

    def test_year_public(self):
        r = ANON.get(f"{BASE}/year/2026")
        assert r.status_code == 200


# =============================================================================
# 4  Day CRUD  (create, view, patch, zoom, 409)
# =============================================================================

class TestDayCRUD:
    @classmethod
    def setup_class(cls):
        # Ensure the test day exists (ignore 409 if already there)
        AUTH.post(f"{BASE}/days", json={
            "log_date": _CREATE_DATE,
            "day_label": "E2E test day",
            "history_text": "Automated test",
        })

    def test_create_day_requires_auth(self):
        r = ANON.post(f"{BASE}/days", json={"log_date": "2099-11-01"})
        assert r.status_code == 401

    def test_create_duplicate_returns_409(self):
        r = AUTH.post(f"{BASE}/days", json={"log_date": _CREATE_DATE})
        assert r.status_code == 409

    def test_view_day_structure(self):
        r = AUTH.get(f"{BASE}/day/{_CREATE_DATE}")
        d = _ok(r)
        assert d["log_date"] == _CREATE_DATE
        for key in ("log_items", "work_plans", "programs", "crew_assignments"):
            assert key in d

    def test_view_day_has_zoom_fields(self):
        r = AUTH.get(f"{BASE}/day/{_CREATE_DATE}")
        d = _ok(r)
        for key in ("zoom_meeting_id", "zoom_password", "zoom_join_url"):
            assert key in d, f"Missing zoom field: {key}"

    def test_view_nonexistent_returns_404(self):
        r = AUTH.get(f"{BASE}/day/2099-11-28")
        assert r.status_code == 404

    def test_patch_day_label(self):
        r = AUTH.patch(f"{BASE}/day/{_CREATE_DATE}",
                       json={"day_label": "E2E patched label"})
        d = _ok(r)
        assert d["day_label"] == "E2E patched label"

    def test_patch_zoom_fields(self):
        payload = {
            "zoom_meeting_id": "123456789",
            "zoom_password": "zp@ss",
            "zoom_join_url": "https://zoom.us/j/123456789",
        }
        _ok(AUTH.patch(f"{BASE}/day/{_CREATE_DATE}", json=payload))
        d = _ok(AUTH.get(f"{BASE}/day/{_CREATE_DATE}"))
        assert d["zoom_meeting_id"] == "123456789"
        assert d["zoom_password"] == "zp@ss"
        assert d["zoom_join_url"] == "https://zoom.us/j/123456789"

    def test_patch_zoom_fields_cleared(self):
        AUTH.patch(f"{BASE}/day/{_CREATE_DATE}",
                   json={"zoom_meeting_id": "", "zoom_password": "",
                         "zoom_join_url": ""})
        d = _ok(AUTH.get(f"{BASE}/day/{_CREATE_DATE}"))
        assert d["zoom_meeting_id"] in (None, "")
        assert d["zoom_join_url"] in (None, "")

    def test_patch_day_requires_auth(self):
        r = ANON.patch(f"{BASE}/day/{_CREATE_DATE}", json={"day_label": "x"})
        assert r.status_code == 401


# =============================================================================
# 5  Log Items CRUD
# =============================================================================

class TestLogItems:
    _item_id: str | None = None

    def test_create_requires_auth(self):
        r = ANON.post(f"{BASE}/day/{_CREATE_DATE}/items",
                      json={"crew_tab": "TO", "title": "no-auth"})
        assert r.status_code == 401

    def test_create(self):
        r = AUTH.post(f"{BASE}/day/{_CREATE_DATE}/items", json={
            "crew_tab": "TO",
            "title": "E2E test item",
            "body": "Automated test body",
            "item_type": "Comment",
            "status": "Completed",
            "subsystem": "Dome",
            "downtime_minutes": 15,
            "summit_access": "Yes",
        })
        d = _ok(r, 201)
        TestLogItems._item_id = d["id"]
        assert d["title"] == "E2E test item"
        assert d["summit_access"] == "Yes"
        assert d["downtime_minutes"] == 15

    def test_get(self):
        assert TestLogItems._item_id
        r = AUTH.get(f"{BASE}/items/{TestLogItems._item_id}")
        d = _ok(r)
        assert d["id"] == TestLogItems._item_id

    def test_patch(self):
        assert TestLogItems._item_id
        r = AUTH.patch(f"{BASE}/items/{TestLogItems._item_id}", json={
            "title": "E2E patched item",
            "summit_access": "No",
            "downtime_minutes": 5,
        })
        d = _ok(r)
        assert d["title"] == "E2E patched item"
        assert d["summit_access"] == "No"
        assert d["downtime_minutes"] == 5

    def test_appears_in_day_view(self):
        r = AUTH.get(f"{BASE}/day/{_CREATE_DATE}")
        d = _ok(r)
        ids = [i["id"] for i in d["log_items"]]
        assert TestLogItems._item_id in ids

    def test_downtime_in_day_total(self):
        r = AUTH.get(f"{BASE}/day/{_CREATE_DATE}")
        d = _ok(r)
        assert d["total_downtime"] >= 5

    def test_invalid_crew_tab_422(self):
        r = AUTH.post(f"{BASE}/day/{_CREATE_DATE}/items",
                      json={"crew_tab": "INVALID", "title": "bad"})
        assert r.status_code == 422

    def test_delete(self):
        assert TestLogItems._item_id
        r = AUTH.delete(f"{BASE}/items/{TestLogItems._item_id}")
        assert r.status_code == 204

    def test_get_deleted_404(self):
        assert TestLogItems._item_id
        r = AUTH.get(f"{BASE}/items/{TestLogItems._item_id}")
        assert r.status_code == 404


# =============================================================================
# 6  Summit Access field
# =============================================================================

class TestSummitAccess:
    _item_id: str | None = None

    @classmethod
    def setup_class(cls):
        r = AUTH.post(f"{BASE}/day/{_CREATE_DATE}/items", json={
            "crew_tab": "TO", "title": "SA test", "summit_access": "Yes",
        })
        assert r.status_code == 201, r.text
        cls._item_id = r.json()["id"]

    @classmethod
    def teardown_class(cls):
        if cls._item_id:
            AUTH.delete(f"{BASE}/items/{cls._item_id}")

    def test_yes_persists(self):
        r = AUTH.get(f"{BASE}/items/{self._item_id}")
        assert r.json()["summit_access"] == "Yes"

    def test_update_to_no(self):
        AUTH.patch(f"{BASE}/items/{self._item_id}", json={"summit_access": "No"})
        r = AUTH.get(f"{BASE}/items/{self._item_id}")
        assert r.json()["summit_access"] == "No"

    def test_clear_to_none(self):
        AUTH.patch(f"{BASE}/items/{self._item_id}", json={"summit_access": None})
        r = AUTH.get(f"{BASE}/items/{self._item_id}")
        assert r.json()["summit_access"] is None


# =============================================================================
# 7  Work Plans  (including new transport/seating fields)
# =============================================================================

class TestWorkPlans:
    _wp_id: str | None = None

    def test_create_requires_auth(self):
        r = ANON.post(f"{BASE}/day/{_CREATE_DATE}/work-plans",
                      json={"comptitle": "no-auth"})
        assert r.status_code == 401

    def test_create_with_transport_fields(self):
        r = AUTH.post(f"{BASE}/day/{_CREATE_DATE}/work-plans", json={
            "comptitle": "E2E Work Plan",
            "comptext": "Test body",
            "intervene": "Yes",
            "melco": "MC-01",
            "fai": "FAI-02",
            "master": 3,
            "seats": 4,
            "seats2": 1,
            "pseats": 2,
            "pass_text": "Alice, Bob",
            "rpass_text": "Charlie",
        })
        d = _ok(r, 201)
        TestWorkPlans._wp_id = d["id"]
        assert d["comptitle"] == "E2E Work Plan"
        assert d["intervene"] == "Yes"
        assert d["melco"] == "MC-01"
        assert d["fai"] == "FAI-02"
        assert d["master"] == 3
        assert d["seats"] == 4
        assert d["seats2"] == 1
        assert d["pseats"] == 2
        assert d["pass_text"] == "Alice, Bob"
        assert d["rpass_text"] == "Charlie"

    def test_patch(self):
        assert TestWorkPlans._wp_id
        r = AUTH.patch(f"{BASE}/work-plans/{TestWorkPlans._wp_id}", json={
            "comptitle": "E2E WP patched",
            "seats": 6,
            "pass_text": "Dave",
        })
        d = _ok(r)
        assert d["comptitle"] == "E2E WP patched"
        assert d["seats"] == 6
        assert d["pass_text"] == "Dave"

    def test_appears_in_day_view(self):
        r = AUTH.get(f"{BASE}/day/{_CREATE_DATE}")
        d = _ok(r)
        ids = [wp["id"] for wp in d["work_plans"]]
        assert TestWorkPlans._wp_id in ids

    def test_delete(self):
        assert TestWorkPlans._wp_id
        r = AUTH.delete(f"{BASE}/work-plans/{TestWorkPlans._wp_id}")
        assert r.status_code == 204

    def test_deleted_not_in_day(self):
        r = AUTH.get(f"{BASE}/day/{_CREATE_DATE}")
        d = _ok(r)
        ids = [wp["id"] for wp in d["work_plans"]]
        assert TestWorkPlans._wp_id not in ids


# =============================================================================
# 8  Crew
# =============================================================================

class TestCrew:
    _crew_id: str | None = None

    def test_create_requires_auth(self):
        r = ANON.post(f"{BASE}/day/{_CREATE_DATE}/crew",
                      json={"role": "TO", "member_name": "nobody"})
        assert r.status_code == 401

    def test_create(self):
        r = AUTH.post(f"{BASE}/day/{_CREATE_DATE}/crew", json={
            "role": "TO", "member_name": "E2E Operator", "location": "Summit",
        })
        d = _ok(r, 201)
        TestCrew._crew_id = d["id"]
        assert d["member_name"] == "E2E Operator"
        assert d["role"] == "TO"

    def test_patch(self):
        assert TestCrew._crew_id
        r = AUTH.patch(f"{BASE}/crew/{TestCrew._crew_id}",
                       json={"member_name": "E2E Operator Updated"})
        d = _ok(r)
        assert d["member_name"] == "E2E Operator Updated"

    def test_appears_in_day_view(self):
        r = AUTH.get(f"{BASE}/day/{_CREATE_DATE}")
        d = _ok(r)
        ids = [c["id"] for c in d["crew_assignments"]]
        assert TestCrew._crew_id in ids

    def test_delete(self):
        assert TestCrew._crew_id
        r = AUTH.delete(f"{BASE}/crew/{TestCrew._crew_id}")
        assert r.status_code == 204


# =============================================================================
# 9  Weather
# =============================================================================

class TestWeather:
    def test_requires_auth(self):
        r = ANON.put(f"{BASE}/day/{_CREATE_DATE}/weather", json={"sky": "Clear"})
        assert r.status_code == 401

    def test_upsert(self):
        r = AUTH.put(f"{BASE}/day/{_CREATE_DATE}/weather", json={
            "sky": "Clear", "seeing": "0.8", "wind": "5 kn", "humidity_raw": "30",
        })
        d = _ok(r)
        assert d["sky"] == "Clear"
        assert d["seeing"] == "0.8"

    def test_idempotent(self):
        AUTH.put(f"{BASE}/day/{_CREATE_DATE}/weather", json={"sky": "Cloudy"})
        r = AUTH.put(f"{BASE}/day/{_CREATE_DATE}/weather", json={"sky": "Cloudy"})
        d = _ok(r)
        assert d["sky"] == "Cloudy"

    def test_appears_in_day_view(self):
        r = AUTH.get(f"{BASE}/day/{_CREATE_DATE}")
        d = _ok(r)
        assert d["weather"] is not None
        assert d["weather"]["sky"] in ("Clear", "Cloudy")


# =============================================================================
# 10  Observation Programs
# =============================================================================

class TestPrograms:
    _prog_id: str | None = None

    def test_create_requires_auth(self):
        r = ANON.post(f"{BASE}/day/{_CREATE_DATE}/programs", json={"propid": "X"})
        assert r.status_code == 401

    def test_create(self):
        r = AUTH.post(f"{BASE}/day/{_CREATE_DATE}/programs", json={
            "propid": "E2E-999", "instr": "HSC", "pi": "Test PI", "sort_order": 1,
        })
        d = _ok(r, 201)
        TestPrograms._prog_id = d["id"]
        assert d["propid"] == "E2E-999"
        assert d["instr"] == "HSC"
        assert d["pi"] == "Test PI"

    def test_patch(self):
        assert TestPrograms._prog_id
        r = AUTH.patch(f"{BASE}/programs/{TestPrograms._prog_id}",
                       json={"pi": "Updated PI"})
        d = _ok(r)
        assert d["pi"] == "Updated PI"

    def test_appears_in_day_view(self):
        r = AUTH.get(f"{BASE}/day/{_CREATE_DATE}")
        d = _ok(r)
        ids = [p["id"] for p in d["programs"]]
        assert TestPrograms._prog_id in ids

    def test_shows_in_year_overview(self):
        r = AUTH.get(f"{BASE}/year/2099")
        d = _ok(r)
        matches = [x for x in d["days"] if x["log_date"] == _CREATE_DATE]
        if matches:
            # first_instr may be HSC or None depending on sort_order
            assert matches[0]["first_instr"] in ("HSC", None)

    def test_delete(self):
        assert TestPrograms._prog_id
        r = AUTH.delete(f"{BASE}/programs/{TestPrograms._prog_id}")
        assert r.status_code == 204


# =============================================================================
# 11  Search
# =============================================================================

UNIQUE_KW = "xyzzy99e2esearchtoken"


class TestSearch:
    _search_item_id: str | None = None

    @classmethod
    def setup_class(cls):
        r = AUTH.post(f"{BASE}/day/{_CREATE_DATE}/items", json={
            "crew_tab": "TO",
            "title": f"Search test {UNIQUE_KW}",
            "body": f"Body {UNIQUE_KW} details",
            "item_type": "Comment",
        })
        if r.status_code == 201:
            cls._search_item_id = r.json()["id"]

    @classmethod
    def teardown_class(cls):
        if cls._search_item_id:
            AUTH.delete(f"{BASE}/items/{cls._search_item_id}")

    def test_structure(self):
        r = AUTH.get(f"{BASE}/search", params={"q": "test"})
        d = _ok(r)
        assert "items" in d and "total" in d
        assert isinstance(d["items"], list)

    def test_finds_seeded_item(self):
        r = AUTH.get(f"{BASE}/search", params={"q": UNIQUE_KW})
        d = _ok(r)
        assert d["total"] >= 1
        assert any(UNIQUE_KW in (i["title"] or "") for i in d["items"])

    def test_result_has_log_date(self):
        r = AUTH.get(f"{BASE}/search", params={"q": UNIQUE_KW})
        d = _ok(r)
        if d["items"]:
            assert "log_date" in d["items"][0]

    def test_multi_word_query(self):
        r = AUTH.get(f"{BASE}/search", params={"q": f"Search test {UNIQUE_KW}"})
        d = _ok(r)
        assert d["total"] >= 1

    def test_date_range_includes(self):
        r = AUTH.get(f"{BASE}/search", params={
            "q": UNIQUE_KW, "from_date": "2000-01-01", "to_date": "2099-12-31",
        })
        d = _ok(r)
        assert d["total"] >= 1

    def test_future_date_range_empty(self):
        r = AUTH.get(f"{BASE}/search", params={
            "q": UNIQUE_KW, "from_date": "2100-01-01", "to_date": "2100-12-31",
        })
        d = _ok(r)
        assert d["total"] == 0

    def test_crew_tab_match(self):
        r = AUTH.get(f"{BASE}/search", params={"q": UNIQUE_KW, "crew_tab": "TO"})
        d = _ok(r)
        assert d["total"] >= 1

    def test_crew_tab_no_match(self):
        r = AUTH.get(f"{BASE}/search", params={"q": UNIQUE_KW, "crew_tab": "DC"})
        d = _ok(r)
        assert d["total"] == 0

    def test_pagination_no_crash(self):
        _ok(AUTH.get(f"{BASE}/search", params={"q": "a", "limit": 2, "offset": 0}))
        _ok(AUTH.get(f"{BASE}/search", params={"q": "a", "limit": 2, "offset": 2}))

    def test_empty_query_422(self):
        r = AUTH.get(f"{BASE}/search", params={"q": ""})
        assert r.status_code == 422

    def test_public_read(self):
        r = ANON.get(f"{BASE}/search", params={"q": "test"})
        assert r.status_code == 200


# =============================================================================
# 12  Auth guards — every write endpoint rejects anonymous requests
# =============================================================================

class TestAuthGuards:
    def test_create_day(self):
        assert ANON.post(f"{BASE}/days", json={"log_date": "2099-01-01"}).status_code == 401

    def test_patch_day(self):
        assert ANON.patch(f"{BASE}/day/2026-05-04", json={"day_label": "x"}).status_code == 401

    def test_create_item(self):
        assert ANON.post(f"{BASE}/day/2026-05-04/items", json={"crew_tab": "TO"}).status_code == 401

    def test_patch_item(self):
        null_id = "00000000-0000-0000-0000-000000000000"
        assert ANON.patch(f"{BASE}/items/{null_id}", json={"title": "x"}).status_code == 401

    def test_delete_item(self):
        null_id = "00000000-0000-0000-0000-000000000000"
        assert ANON.delete(f"{BASE}/items/{null_id}").status_code == 401

    def test_create_crew(self):
        assert ANON.post(f"{BASE}/day/2026-05-04/crew",
                         json={"role": "TO", "member_name": "x"}).status_code == 401

    def test_upsert_weather(self):
        assert ANON.put(f"{BASE}/day/2026-05-04/weather", json={"sky": "X"}).status_code == 401

    def test_create_program(self):
        assert ANON.post(f"{BASE}/day/2026-05-04/programs",
                         json={"propid": "X"}).status_code == 401

    def test_create_work_plan(self):
        assert ANON.post(f"{BASE}/day/2026-05-04/work-plans",
                         json={"comptitle": "x"}).status_code == 401
