#!/usr/bin/env python3
"""
List legacy MariaDB `items` / `progs` rows that the ETL skips (no matching `days.idno`).

Uses SUMLOGS_DATABASE_URL from backend/.env.
"""
from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import urlparse, unquote

import pymysql
from pymysql.cursors import DictCursor

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import settings  # noqa: E402


def connect():
    raw = (settings.sumlogs_database_url or "").strip().replace("mysql+pymysql://", "mysql://", 1)
    p = urlparse(raw)
    db = (p.path or "/").lstrip("/").split("/")[0] or "sumlogs"
    return pymysql.connect(
        host=p.hostname or "localhost",
        port=p.port or 3306,
        user=unquote(p.username or ""),
        password=unquote(p.password or ""),
        database=db,
        charset="utf8mb4",
        cursorclass=DictCursor,
    )


def main() -> None:
    conn = connect()
    cur = conn.cursor()

    print("=== items: dayidno NULL or not in days ===\n")
    cur.execute(
        """
        SELECT i.idno, i.dayidno, i.date, i.logcrew, LEFT(i.itemtitle, 80) AS title_preview
        FROM items i
        LEFT JOIN days d ON d.idno = i.dayidno
        WHERE i.dayidno IS NULL OR d.idno IS NULL
        ORDER BY i.idno
        """
    )
    rows = cur.fetchall()
    print(f"count: {len(rows)}\n")
    for r in rows:
        print(
            f"idno={r['idno']}\tdayidno={r['dayidno']}\tdate={r['date']}\t"
            f"logcrew={r['logcrew']!r}\ttitle={r['title_preview']!r}"
        )

    print("\n=== progs: dayidno NULL or not in days ===\n")
    cur.execute(
        """
        SELECT p.idno, p.dayidno, p.date, p.seq, LEFT(p.instr, 40) AS instr_preview
        FROM progs p
        LEFT JOIN days d ON d.idno = p.dayidno
        WHERE p.dayidno IS NULL OR d.idno IS NULL
        ORDER BY p.idno
        """
    )
    prows = cur.fetchall()
    print(f"count: {len(prows)}\n")
    for r in prows:
        print(
            f"idno={r['idno']}\tdayidno={r['dayidno']}\tdate={r['date']}\tseq={r['seq']}\t"
            f"instr={r['instr_preview']!r}"
        )

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
