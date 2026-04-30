#!/usr/bin/env python3
"""
One-time ETL: legacy MariaDB `sumlogs` → Postgres `opal_summit` (Summit schema).

Requires:
  SUMLOGS_DATABASE_URL=mysql+pymysql://user:pass@host:3306/sumlogs
  SUMMIT_SYNC_DATABASE_URL or SUMMIT_ASYNC_DATABASE_URL (async URL is converted for psycopg2)

Usage:
  cd backend && python scripts/migrate_sumlogs_to_postgres.py --dry-run
  python scripts/migrate_sumlogs_to_postgres.py --truncate --yes
  python scripts/migrate_sumlogs_to_postgres.py --from-date 2020-01-01 --to-date 2020-12-31
"""
from __future__ import annotations

import argparse
import sys
import uuid
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple
from urllib.parse import unquote, urlparse
from zoneinfo import ZoneInfo

import pymysql
from pymysql.cursors import DictCursor

BACKEND = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND))

from app.core.config import settings  # noqa: E402

try:
    import psycopg2
    from psycopg2.extras import execute_values
except ImportError as e:
    raise SystemExit("Install psycopg2-binary: pip install psycopg2-binary") from e

HST = ZoneInfo("Pacific/Honolulu")


def _summit_sync_dsn() -> str:
    explicit = (settings.summit_sync_database_url or "").strip()
    if explicit:
        return explicit
    u = settings.summit_async_database_url
    return u.replace("postgresql+asyncpg://", "postgresql://", 1)


def _mysql_connect() -> pymysql.connections.Connection:
    raw = (settings.sumlogs_database_url or "").strip()
    if not raw:
        raise SystemExit("Set SUMLOGS_DATABASE_URL in backend/.env")
    url = raw.replace("mysql+pymysql://", "mysql://", 1)
    p = urlparse(url)
    dbname = (p.path or "/").lstrip("/").split("/")[0] or "sumlogs"
    return pymysql.connect(
        host=p.hostname or "localhost",
        port=p.port or 3306,
        user=unquote(p.username or ""),
        password=unquote(p.password or ""),
        database=dbname,
        charset="utf8mb4",
        cursorclass=DictCursor,
    )


def _aware(dt: Optional[Any]) -> Optional[datetime]:
    if dt is None:
        return None
    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            return dt.replace(tzinfo=HST)
        return dt.astimezone(HST)
    return None


def _parse_float(s: Any) -> Optional[float]:
    if s is None or s == "":
        return None
    try:
        return float(str(s).strip())
    except ValueError:
        return None


def _parse_int(s: Any) -> Optional[int]:
    if s is None or s == "":
        return None
    try:
        return int(str(s).strip())
    except ValueError:
        return None


def _txt(v: Any) -> Optional[str]:
    """PostgreSQL rejects NUL (0x00) in text; legacy MySQL rows may contain them."""
    if v is None:
        return None
    if isinstance(v, (bytes, bytearray)):
        s = bytes(v).decode("utf-8", errors="replace")
    else:
        s = str(v)
    return s.replace("\x00", "") if "\x00" in s else s


def _map_crew_tab(raw: Any) -> str:
    if raw is None:
        return "ALL"
    v = str(raw).strip().upper()
    if v in ("", "ALL", "AL", "A"):
        return "ALL"
    if v in ("TO", "IO", "DC", "WP"):
        return v
    if v in ("TO-IO", "TI", "T-I"):
        return "TO-IO"
    return "ALL"


def mysql_table_columns(cur, table: str) -> Set[str]:
    cur.execute(
        """
        SELECT COLUMN_NAME AS c FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s
        """,
        (table,),
    )
    return {r["c"] for r in cur.fetchall()}


def fetch_days_filtered(
    cur,
    cols: Set[str],
    from_d: Optional[date],
    to_d: Optional[date],
) -> List[Dict[str, Any]]:
    need = {
        "idno",
        "date",
        "day",
        "to1",
        "to1loc",
        "to2",
        "to2loc",
        "io1",
        "io1loc",
        "io2",
        "io2loc",
        "dc1",
        "dc2",
        "toin",
        "toout",
        "ioin",
        "ioout",
        "dcin",
        "dcout",
        "sky",
        "seeing",
        "temp",
        "wind",
        "humid",
        "comment",
    }
    email_extra = {"mailed", "mailtime", "mailsmoka", "smokatime", "mailday", "maildtime"}
    sel = sorted(cols & (need | email_extra))
    if "idno" not in cols or "date" not in cols:
        raise SystemExit("days table must have idno and date columns")
    q = f"SELECT {', '.join('`' + c + '`' for c in sel)} FROM days WHERE 1=1"
    args: List[Any] = []
    if from_d:
        q += " AND `date` >= %s"
        args.append(from_d)
    if to_d:
        q += " AND `date` <= %s"
        args.append(to_d)
    q += " ORDER BY `date`"
    cur.execute(q, args)
    return list(cur.fetchall())


def map_wp_item_to_work_plan(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "window_start": _aware(row.get("realstart")),
        "window_end": _aware(row.get("realend")),
        "nite_effect": _txt(row.get("niteeffect")),
        "day_effect": _txt(row.get("dayeffect")),
        "location": _txt(row.get("location")),
        "location2": _txt(row.get("location2")),
        "location3": _txt(row.get("location3")),
        "assigned1": _txt(row.get("assigned1")),
        "assigned2": _txt(row.get("assigned2")),
        "dcassist": _txt(row.get("dcassist")),
        "notify": _txt(row.get("notify")),
        "contact1": _txt(row.get("contact1")),
        "contact2": _txt(row.get("contact2")),
        "others": _txt(row.get("others")),
        "otherreq": _txt(row.get("otherreq")),
        "comptitle": _txt(row.get("comptitle")),
        "comptext": _txt(row.get("comptext")),
        "master": _parse_int(row.get("master")),
        "intervene": _txt(row.get("intervene")),
        "melco": _txt(row.get("melco")),
        "fai": _txt(row.get("fai")),
        "seats": _parse_int(row.get("seats")),
        "seats2": _parse_int(row.get("seats2")),
        "pseats": _parse_int(row.get("pseats")),
        "pass_text": _txt(row.get("pass")),
        "rpass_text": _txt(row.get("rpass")),
        "requirements": _txt(row.get("requirements")),
        "notes": _txt(row.get("itemtext")),
    }


def truncate_summit(pg) -> None:
    cur = pg.cursor()
    for tbl in (
        "work_plan_item_links",
        "log_items",
        "email_deliveries",
        "observation_programs",
        "weather_snapshots",
        "crew_assignments",
        "work_plans",
        "summit_days",
    ):
        cur.execute(f"DELETE FROM {tbl}")
    cur.close()
    pg.commit()


def run_etl(
    dry_run: bool,
    from_d: Optional[date],
    to_d: Optional[date],
    do_truncate: bool,
) -> None:
    dsn = _summit_sync_dsn()
    mconn = _mysql_connect()
    mcur = mconn.cursor()
    day_cols = mysql_table_columns(mcur, "days")
    item_cols = mysql_table_columns(mcur, "items")
    progs_cols = mysql_table_columns(mcur, "progs")

    days_rows = fetch_days_filtered(mcur, day_cols, from_d, to_d)
    print(f"days rows: {len(days_rows)}")

    item_sel = sorted(item_cols)
    iq = f"SELECT {', '.join('`' + c + '`' for c in item_sel)} FROM items WHERE 1=1"
    iargs: List[Any] = []
    if from_d:
        iq += " AND `date` >= %s"
        iargs.append(from_d)
    if to_d:
        iq += " AND `date` <= %s"
        iargs.append(to_d)
    mcur.execute(iq, iargs)
    items_rows = list(mcur.fetchall())
    print(f"items rows: {len(items_rows)}")

    pq = f"SELECT {', '.join('`' + c + '`' for c in sorted(progs_cols))} FROM progs WHERE 1=1"
    pargs: List[Any] = []
    if from_d:
        pq += " AND `date` >= %s"
        pargs.append(from_d)
    if to_d:
        pq += " AND `date` <= %s"
        pargs.append(to_d)
    mcur.execute(pq, pargs)
    progs_rows = list(mcur.fetchall())
    print(f"progs rows: {len(progs_rows)}")

    mcur.close()
    mconn.close()

    if dry_run:
        print("Dry run: no Postgres writes.")
        return

    pg = psycopg2.connect(dsn)
    pg.autocommit = False
    cur = pg.cursor()

    try:
        if do_truncate:
            truncate_summit(pg)

        day_uuid: Dict[int, uuid.UUID] = {}
        wp_for_day: Dict[int, uuid.UUID] = {}

        for d in days_rows:
            lid = int(d["idno"])
            log_date = d["date"]
            if not log_date:
                continue
            sid = uuid.uuid4()
            day_uuid[lid] = sid
            cur.execute(
                """
                INSERT INTO summit_days (id, legacy_day_id, log_date, day_label, history_text)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (str(sid), lid, log_date, _txt(d.get("day")), None),
            )

        # First WP item per legacy day → work_plans
        wp_first: Dict[int, Dict[str, Any]] = {}
        for row in items_rows:
            if str(row.get("logcrew", "")).strip().upper() != "WP":
                continue
            did = row.get("dayidno")
            if did is None:
                continue
            did = int(did)
            if did not in day_uuid:
                continue
            if did not in wp_first:
                wp_first[did] = row

        for did, row in wp_first.items():
            wpid = uuid.uuid4()
            wp_for_day[did] = wpid
            wp = map_wp_item_to_work_plan(row)
            cur.execute(
                """
                INSERT INTO work_plans (
                  id, summit_day_id, copied_from_id, window_start, window_end,
                  nite_effect, day_effect, location, location2, location3,
                  assigned1, assigned2, dcassist, notify, contact1, contact2,
                  others, otherreq, comptitle, comptext, master, intervene, melco, fai,
                  seats, seats2, pseats, pass_text, rpass_text, requirements, notes
                ) VALUES (
                  %s, %s, NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    str(wpid),
                    str(day_uuid[did]),
                    wp["window_start"],
                    wp["window_end"],
                    wp["nite_effect"],
                    wp["day_effect"],
                    wp["location"],
                    wp["location2"],
                    wp["location3"],
                    wp["assigned1"],
                    wp["assigned2"],
                    wp["dcassist"],
                    wp["notify"],
                    wp["contact1"],
                    wp["contact2"],
                    wp["others"],
                    wp["otherreq"],
                    wp["comptitle"],
                    wp["comptext"],
                    wp["master"],
                    wp["intervene"],
                    wp["melco"],
                    wp["fai"],
                    wp["seats"],
                    wp["seats2"],
                    wp["pseats"],
                    wp["pass_text"],
                    wp["rpass_text"],
                    wp["requirements"],
                    wp["notes"],
                ),
            )

        # Crew rows
        crew_rows: List[Tuple] = []
        for d in days_rows:
            lid = int(d["idno"])
            if lid not in day_uuid:
                continue
            sid = day_uuid[lid]
            so = 0
            pairs = [
                ("TO", d.get("to1"), d.get("to1loc"), d.get("toin"), d.get("toout")),
                ("TO", d.get("to2"), d.get("to2loc"), d.get("toin"), d.get("toout")),
                ("IO", d.get("io1"), d.get("io1loc"), d.get("ioin"), d.get("ioout")),
                ("IO", d.get("io2"), d.get("io2loc"), d.get("ioin"), d.get("ioout")),
                ("DC", d.get("dc1"), None, d.get("dcin"), d.get("dcout")),
                ("DC", d.get("dc2"), None, d.get("dcin"), d.get("dcout")),
            ]
            for role, name, loc, tin, tout in pairs:
                nm = _txt(name)
                if not nm or nm.strip() == "":
                    continue
                lc = _txt(loc)
                crew_rows.append(
                    (
                        str(uuid.uuid4()),
                        str(sid),
                        role,
                        nm.strip()[:40],
                        (lc.strip()[:30] if lc else None),
                        _aware(tin),
                        _aware(tout),
                        so,
                    )
                )
                so += 1

        if crew_rows:
            execute_values(
                cur,
                """
                INSERT INTO crew_assignments (id, summit_day_id, role, member_name, location, time_in, time_out, sort_order)
                VALUES %s
                """,
                crew_rows,
            )

        # Weather
        for d in days_rows:
            lid = int(d["idno"])
            if lid not in day_uuid:
                continue
            sid = day_uuid[lid]
            cur.execute(
                """
                INSERT INTO weather_snapshots (
                  id, summit_day_id, sky, seeing, temp_raw, temp_c, wind, humidity_raw, humidity_pct, comment_text, captured_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)
                """,
                (
                    str(uuid.uuid4()),
                    str(sid),
                    _txt(d.get("sky")),
                    _txt(d.get("seeing")),
                    _txt(d.get("temp")),
                    _parse_float(d.get("temp")),
                    _txt(d.get("wind")),
                    _txt(d.get("humid")),
                    _parse_float(d.get("humid")),
                    _txt(d.get("comment")),
                ),
            )

        # Email (only columns present on `days`)
        mail_fields = ["mailed", "mailtime", "mailsmoka", "smokatime", "mailday", "maildtime"]
        for d in days_rows:
            lid = int(d["idno"])
            if lid not in day_uuid:
                continue
            sid = day_uuid[lid]
            payload = {k: d.get(k) for k in mail_fields if k in d}
            cur.execute(
                """
                INSERT INTO email_deliveries (
                  id, summit_day_id, mailed, mailtime, mailsmoka, smokatime, mailday, maildtime,
                  am_sent_at, pm_sent_at, day_digest_sent_at, last_error
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NULL, NULL, NULL, NULL)
                """,
                (
                    str(uuid.uuid4()),
                    str(sid),
                    _txt(payload.get("mailed")),
                    _aware(payload.get("mailtime")),
                    _txt(payload.get("mailsmoka")),
                    _aware(payload.get("smokatime")),
                    _txt(payload.get("mailday")),
                    _aware(payload.get("maildtime")),
                ),
            )

        # Observation programs
        for pr in progs_rows:
            legacy_id = int(pr["idno"])
            dayid = pr.get("dayidno")
            if dayid is None:
                continue
            dayid = int(dayid)
            if dayid not in day_uuid:
                continue
            sid = day_uuid[dayid]
            code = pr.get("gid") or pr.get("propid") or None
            pc = _txt(code)
            cur.execute(
                """
                INSERT INTO observation_programs (
                  id, legacy_prog_id, summit_day_id, sort_order,
                  program_code, instr, alloc, pi, ao1, ao2,
                  slot_start, slot_end, gid, propid,
                  obs1, obs1loc, obs2, obs2loc, obs3, obs3loc, obs4, obs4loc,
                  ss, ssloc, ss2, ss2loc, others1, others1loc, others2, others2loc,
                  notes, comment_text
                ) VALUES (
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    str(uuid.uuid4()),
                    legacy_id,
                    str(sid),
                    _parse_int(pr.get("seq")) or 0,
                    (pc[:20] if pc else None),
                    _txt(pr.get("instr")),
                    _txt(pr.get("alloc")),
                    _txt(pr.get("pi")),
                    _txt(pr.get("ao1")),
                    _txt(pr.get("ao2")),
                    _aware(pr.get("intime")),
                    _aware(pr.get("outtime")),
                    _txt(pr.get("gid")),
                    _txt(pr.get("propid")),
                    _txt(pr.get("obs1")),
                    _txt(pr.get("obs1loc")),
                    _txt(pr.get("obs2")),
                    _txt(pr.get("obs2loc")),
                    _txt(pr.get("obs3")),
                    _txt(pr.get("obs3loc")),
                    _txt(pr.get("obs4")),
                    _txt(pr.get("obs4loc")),
                    _txt(pr.get("ss")),
                    _txt(pr.get("ssloc")),
                    _txt(pr.get("ss2")),
                    _txt(pr.get("ss2loc")),
                    _txt(pr.get("others1")),
                    _txt(pr.get("others1loc")),
                    _txt(pr.get("others2")),
                    _txt(pr.get("others2loc")),
                    _txt(pr.get("notes")),
                    _txt(pr.get("comment")),
                ),
            )

        # Log items
        for row in items_rows:
            did = row.get("dayidno")
            if did is None:
                continue
            did = int(did)
            if did not in day_uuid:
                continue
            sid = day_uuid[did]
            legacy_item_id = int(row["idno"])
            crew = _map_crew_tab(row.get("logcrew"))
            wpid = wp_for_day.get(did) if crew == "WP" else None
            downtime = _parse_int(row.get("downtime"))

            cur.execute(
                """
                INSERT INTO log_items (
                  id, legacy_item_id, legacy_old_item_id, summit_day_id, work_plan_id, crew_tab,
                  item_time, title, body, item_type, downtime_minutes, subsystem, status,
                  created_by, history_text, comment_text, created_at, updated_at
                ) VALUES (
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    str(uuid.uuid4()),
                    legacy_item_id,
                    _parse_int(row.get("oldidno")),
                    str(sid),
                    str(wpid) if wpid else None,
                    _txt(crew) or "ALL",
                    _aware(row.get("itemtime")),
                    _txt(row.get("itemtitle")),
                    _txt(row.get("itemtext")),
                    _txt(row.get("type")),
                    downtime,
                    _txt(row.get("subsystem")),
                    _txt(row.get("status")),
                    _txt(row.get("user")),
                    _txt(row.get("history")),
                    _txt(row.get("comment")),
                    _aware(row.get("timestamp")),
                    _aware(row.get("timestamp")),
                ),
            )

        pg.commit()
        print("Migration committed.")
    except Exception as exc:
        pg.rollback()
        raise exc
    finally:
        cur.close()
        pg.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate sumlogs → Postgres Summit schema")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--truncate", action="store_true", help="Delete all Summit rows before load")
    parser.add_argument("--yes", action="store_true", help="Required with --truncate")
    parser.add_argument("--from-date", type=lambda s: date.fromisoformat(s), default=None)
    parser.add_argument("--to-date", type=lambda s: date.fromisoformat(s), default=None)
    args = parser.parse_args()

    if args.truncate and not args.yes:
        raise SystemExit("--truncate requires --yes")

    run_etl(
        dry_run=args.dry_run,
        from_d=args.from_date,
        to_d=args.to_date,
        do_truncate=args.truncate,
    )
