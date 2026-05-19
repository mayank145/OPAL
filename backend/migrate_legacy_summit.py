"""
Legacy Summit Log Migration Script
===================================
Migrates data from legacy sumlogs MariaDB (on opal/amber) to new OPAL PostgreSQL.

Usage (from backend/ directory):
  # First open SSH tunnel in a separate terminal:
  #   ssh -N -L 3307:opal:3306 amber &
  python3 migrate_legacy_summit.py

Tables migrated:
  days       → summit_days + crew_assignments + weather_snapshots + email_deliveries
  items(WP)  → work_plans  (+ itemreqs → req_flags / lockout_flags)
  items(*)   → log_items
  progs      → observation_programs
"""

import sys
import uuid
import pymysql
import psycopg2
import psycopg2.extras
from datetime import datetime, timezone

# ── Connection config ────────────────────────────────────────────────────────
MYSQL_CFG = dict(
    host="127.0.0.1",
    port=3307,           # SSH-tunnel: ssh -N -L 3307:opal:3306 amber
    user="root",
    password="kulaiwi7",
    database="sumlogs",
    charset="utf8mb4",
    use_unicode=True,
)

PG_DSN = "postgresql://mayankchoudhary:summit_db@localhost:5432/opal_summit"

# ── Constants ────────────────────────────────────────────────────────────────
REQUIRED_FLAG_SET = {
    'Move-Tel','Move-EL','Move-AZ','80t-Crane','NsIR-Crane','SmallDoor-Crane',
    'BSIT','TUE-Opt-Crane','TUE-Opt-US','Gen2-Allocation','MirrorHatch',
    'CherryPicker','ForkLift','Hazardous-Materials','MainShutter','Others',
    'BSIT','NoLights-Dome',
}
LOCKOUT_FLAG_SET = {
    'No-Tel-Move','No-AZ-Move','No-EL-Move','NoLights-Dome',
    'No-TopScreen-Move','No-MirrorCover-Move','No-MainShutter','No-UnitSelector-Move',
}
VALID_CREW_TABS = {'TO','IO','DC','WP','ALL','TO-IO'}

def s(v, maxlen=None):
    """Strip and truncate a string value; return None for empty."""
    if v is None:
        return None
    v = str(v).strip()
    if not v:
        return None
    if maxlen:
        v = v[:maxlen]
    return v

def dt_utc(v):
    """Convert naive datetime to UTC-aware."""
    if v is None:
        return None
    if isinstance(v, datetime):
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v
    return None

def safe_int(v):
    if v is None:
        return None
    try:
        return int(v)
    except (ValueError, TypeError):
        return None


def progress(msg):
    print(msg, flush=True)


def main():
    progress("Connecting to legacy MySQL (sumlogs)…")
    my = pymysql.connect(**MYSQL_CFG, cursorclass=pymysql.cursors.DictCursor)
    progress("Connecting to new PostgreSQL (opal_summit)…")
    pg = psycopg2.connect(PG_DSN)
    pg.autocommit = False
    psycopg2.extras.register_uuid()

    cur_my = my.cursor()
    cur_pg = pg.cursor()

    # ── Step 1: summit_days ──────────────────────────────────────────────────
    progress("\n[1/5] Migrating summit_days…")
    cur_my.execute("SELECT * FROM days ORDER BY date")
    days_rows = cur_my.fetchall()

    # Build legacy_id → new UUID map
    day_id_map = {}  # legacy days.idno → new UUID

    # Fetch existing legacy IDs already in PG (for idempotency)
    cur_pg.execute("SELECT legacy_day_id, id FROM summit_days WHERE legacy_day_id IS NOT NULL")
    for row in cur_pg.fetchall():
        day_id_map[row[0]] = row[1]

    inserted_days = 0
    for row in days_rows:
        leg_id = row['idno']
        if leg_id in day_id_map:
            continue
        new_id = uuid.uuid4()
        cur_pg.execute("""
            INSERT INTO summit_days
              (id, legacy_day_id, log_date, day_label, history_text, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, now(), now())
            ON CONFLICT (log_date) DO UPDATE
              SET legacy_day_id = EXCLUDED.legacy_day_id,
                  day_label = COALESCE(EXCLUDED.day_label, summit_days.day_label),
                  history_text = COALESCE(EXCLUDED.history_text, summit_days.history_text),
                  updated_at = now()
            RETURNING id
        """, (new_id, leg_id, row['date'], s(row.get('day'), 80), s(row.get('history'))))
        result = cur_pg.fetchone()
        day_id_map[leg_id] = result[0]
        inserted_days += 1

    pg.commit()
    progress(f"  → {inserted_days} new summit_days inserted ({len(day_id_map)} total)")

    # ── Step 2: crew_assignments ─────────────────────────────────────────────
    progress("\n[2/5] Migrating crew_assignments…")
    # Clear existing crew for days we're about to insert (avoid duplication on re-run)
    cur_pg.execute("SELECT COUNT(*) FROM crew_assignments")
    existing_crew = cur_pg.fetchone()[0]

    if existing_crew == 0:
        crew_rows = []
        for row in days_rows:
            day_uuid = day_id_map.get(row['idno'])
            if not day_uuid:
                continue
            sort = 0
            # TO1
            if s(row.get('to1')):
                crew_rows.append((uuid.uuid4(), day_uuid, 'TO', s(row['to1'],40), s(row.get('to1loc'),30), dt_utc(row.get('toin')), dt_utc(row.get('toout')), sort)); sort+=1
            # TO2
            if s(row.get('to2')):
                crew_rows.append((uuid.uuid4(), day_uuid, 'TO', s(row['to2'],40), None, None, None, sort)); sort+=1
            # IO1
            if s(row.get('io1')):
                crew_rows.append((uuid.uuid4(), day_uuid, 'IO', s(row['io1'],40), s(row.get('io1loc'),30), dt_utc(row.get('ioin')), dt_utc(row.get('ioout')), sort)); sort+=1
            # IO2
            if s(row.get('io2')):
                crew_rows.append((uuid.uuid4(), day_uuid, 'IO', s(row['io2'],40), None, None, None, sort)); sort+=1
            # DC1
            if s(row.get('dc1')):
                crew_rows.append((uuid.uuid4(), day_uuid, 'DC', s(row['dc1'],40), None, dt_utc(row.get('dcin')), dt_utc(row.get('dcout')), sort)); sort+=1
            # DC2
            if s(row.get('dc2')):
                crew_rows.append((uuid.uuid4(), day_uuid, 'DC', s(row['dc2'],40), None, None, None, sort)); sort+=1

        psycopg2.extras.execute_values(cur_pg, """
            INSERT INTO crew_assignments
              (id, summit_day_id, role, member_name, location, time_in, time_out, sort_order)
            VALUES %s
        """, crew_rows, page_size=500)
        pg.commit()
        progress(f"  → {len(crew_rows)} crew_assignments inserted")
    else:
        progress(f"  → Skipped (already have {existing_crew} rows)")

    # ── Step 2b: weather_snapshots ───────────────────────────────────────────
    progress("\n  Migrating weather_snapshots…")
    cur_pg.execute("SELECT COUNT(*) FROM weather_snapshots")
    if cur_pg.fetchone()[0] == 0:
        wx_rows = []
        for row in days_rows:
            day_uuid = day_id_map.get(row['idno'])
            if not day_uuid:
                continue
            if any(s(row.get(f)) for f in ['sky','seeing','temp','wind','humid','comment']):
                wx_rows.append((
                    uuid.uuid4(), day_uuid,
                    s(row.get('sky')), s(row.get('seeing')),
                    s(row.get('temp')), None,
                    s(row.get('wind')),
                    s(row.get('humid')), None,
                    s(row.get('comment'), 200),
                ))
        psycopg2.extras.execute_values(cur_pg, """
            INSERT INTO weather_snapshots
              (id, summit_day_id, sky, seeing, temp_raw, temp_c, wind,
               humidity_raw, humidity_pct, comment_text)
            VALUES %s
        """, wx_rows, page_size=500)
        pg.commit()
        progress(f"  → {len(wx_rows)} weather_snapshots inserted")
    else:
        progress("  → Skipped (already have rows)")

    # ── Step 2c: email_deliveries ────────────────────────────────────────────
    progress("\n  Migrating email_deliveries…")
    cur_pg.execute("SELECT COUNT(*) FROM email_deliveries")
    if cur_pg.fetchone()[0] == 0:
        ed_rows = []
        for row in days_rows:
            day_uuid = day_id_map.get(row['idno'])
            if not day_uuid:
                continue
            if any(row.get(f) for f in ['mailed','mailsmoka','mailday']):
                ed_rows.append((
                    uuid.uuid4(), day_uuid,
                    s(row.get('mailed'),1), dt_utc(row.get('mailtime')),
                    s(row.get('mailsmoka'),1), dt_utc(row.get('smokatime')),
                    s(row.get('mailday'),1), dt_utc(row.get('maildtime')),
                ))
        psycopg2.extras.execute_values(cur_pg, """
            INSERT INTO email_deliveries
              (id, summit_day_id, mailed, mailtime, mailsmoka, smokatime, mailday, maildtime)
            VALUES %s
        """, ed_rows, page_size=500)
        pg.commit()
        progress(f"  → {len(ed_rows)} email_deliveries inserted")
    else:
        progress("  → Skipped (already have rows)")

    # ── Step 3: observation_programs ────────────────────────────────────────
    progress("\n[3/5] Migrating observation_programs…")
    cur_pg.execute("SELECT COUNT(*) FROM observation_programs")
    if cur_pg.fetchone()[0] == 0:
        cur_my.execute("SELECT * FROM progs ORDER BY date, seq, idno")
        prog_rows = cur_my.fetchall()
        op_rows = []
        for row in prog_rows:
            # find day UUID — prefer dayidno, fall back to date lookup
            day_uuid = day_id_map.get(row.get('dayidno'))
            if not day_uuid and row.get('date'):
                cur_pg.execute("SELECT id FROM summit_days WHERE log_date = %s", (row['date'],))
                r = cur_pg.fetchone()
                if r:
                    day_uuid = r[0]
            if not day_uuid:
                continue
            op_rows.append((
                uuid.uuid4(), row['idno'], day_uuid,
                safe_int(row.get('seq') and ord(row['seq'])) if row.get('seq') and len(str(row['seq']))==1 else 0,
                s(row.get('instr'),10), s(row.get('alloc'),10),
                s(row.get('pi'),50), s(row.get('ao1'),10), s(row.get('ao2'),10),
                dt_utc(row.get('intime')), dt_utc(row.get('outtime')),
                s(row.get('gid'),10), s(row.get('propid'),20),
                s(row.get('obs1'),50), s(row.get('obs1loc'),10),
                s(row.get('obs2'),50), s(row.get('obs2loc'),10),
                s(row.get('obs3'),50), s(row.get('obs3loc'),10),
                s(row.get('obs4'),50), s(row.get('obs4loc'),10),
                s(row.get('ss'),30), s(row.get('ssloc'),10),
                s(row.get('ss2'),30), s(row.get('ss2loc'),10),
                s(row.get('others1'),50), s(row.get('others1loc'),10),
                s(row.get('others2'),50), s(row.get('others2loc'),10),
                s(row.get('comment'),100),
            ))
        psycopg2.extras.execute_values(cur_pg, """
            INSERT INTO observation_programs
              (id, legacy_prog_id, summit_day_id, sort_order,
               instr, alloc, pi, ao1, ao2, slot_start, slot_end, gid, propid,
               obs1, obs1loc, obs2, obs2loc, obs3, obs3loc, obs4, obs4loc,
               ss, ssloc, ss2, ss2loc, others1, others1loc, others2, others2loc,
               comment_text)
            VALUES %s
            ON CONFLICT (legacy_prog_id) DO NOTHING
        """, op_rows, page_size=200)
        pg.commit()
        progress(f"  → {len(op_rows)} observation_programs inserted")
    else:
        progress("  → Skipped (already have rows)")

    # ── Step 4: work_plans (from items WHERE logcrew='WP') ──────────────────
    progress("\n[4/5] Migrating work_plans…")
    # Prefetch itemreqs: {planidno: (req_flags, lockout_flags)}
    cur_my.execute("SELECT planidno, code FROM itemreqs ORDER BY planidno")
    req_map = {}  # planidno → {'req': [], 'lock': []}
    for r in cur_my.fetchall():
        pid = r['planidno']
        code = s(r.get('code'))
        if not code:
            continue
        if pid not in req_map:
            req_map[pid] = {'req': [], 'lock': []}
        if code in LOCKOUT_FLAG_SET:
            req_map[pid]['lock'].append(code)
        else:
            req_map[pid]['req'].append(code)

    # Fetch already-migrated legacy IDs (idempotent)
    cur_pg.execute("SELECT legacy_item_id, id FROM work_plans WHERE legacy_item_id IS NOT NULL")
    wp_id_map = {row[0]: row[1] for row in cur_pg.fetchall()}

    cur_my.execute("SELECT * FROM items WHERE logcrew = 'WP' ORDER BY date, idno")
    wp_rows = cur_my.fetchall()
    wp_insert = []
    for row in wp_rows:
        leg_id = row['idno']
        if leg_id in wp_id_map:
            continue  # already migrated
        day_uuid = day_id_map.get(row.get('dayidno'))
        if not day_uuid and row.get('date'):
            cur_pg.execute("SELECT id FROM summit_days WHERE log_date = %s", (row['date'],))
            r2 = cur_pg.fetchone()
            if r2:
                day_uuid = r2[0]
        if not day_uuid:
            continue
        new_wp_id = uuid.uuid4()
        wp_id_map[leg_id] = new_wp_id
        codes = req_map.get(leg_id, {'req': [], 'lock': []})
        req_f = ','.join(codes['req']) or None
        lock_f = ','.join(codes['lock']) or None
        status = s(row.get('status'), 20) or 'Planned'
        wp_insert.append((
            new_wp_id, leg_id, day_uuid,
            dt_utc(row.get('itemtime')),   # window_start
            dt_utc(row.get('endtime')),    # window_end
            s(row.get('contact1'), 40),    # requestor
            status,
            s(row.get('type'), 20),        # wp_type
            s(row.get('subsystem'), 20),   # wp_subsystem
            s(row.get('itemtext')),        # plan_text
            s(row.get('comment')),         # day_warning
            None,                          # nite_warning
            s(row.get('pass'), 80),        # teampass
            dt_utc(row.get('realstart')),
            dt_utc(row.get('realend')),
            req_f, lock_f,
            s(row.get('niteeffect'), 100),
            s(row.get('dayeffect'), 100),
            s(row.get('location'), 20),
            s(row.get('location2'), 20),
            s(row.get('location3'), 20),
            s(row.get('assigned1'), 30),
            s(row.get('assigned2'), 50),
            s(row.get('dcassist'), 10),
            s(row.get('notify'), 20),
            s(row.get('contact1'), 20),    # contact1
            s(row.get('contact2'), 50),
            s(row.get('others'), 50),
            s(row.get('otherreq'), 40),
            s(row.get('itemtitle'), 200),  # comptitle
            s(row.get('comment')),         # comptext
            safe_int(row.get('master')),
            s(row.get('intervene'), 20),
            s(row.get('melco'), 20),
            s(row.get('fai'), 20),
            safe_int(row.get('seats')),
            safe_int(row.get('seats2')),
            safe_int(row.get('pseats')),
            s(row.get('pass'), 80),        # pass_text
            s(row.get('rpass'), 80),       # rpass_text
        ))

    if wp_insert:
        psycopg2.extras.execute_values(cur_pg, """
            INSERT INTO work_plans
              (id, legacy_item_id, summit_day_id,
               window_start, window_end,
               requestor, wp_status, wp_type, wp_subsystem,
               plan_text, day_warning, nite_warning, teampass,
               realstart, realend, req_flags, lockout_flags,
               nite_effect, day_effect,
               location, location2, location3,
               assigned1, assigned2, dcassist, notify,
               contact1, contact2, others, otherreq,
               comptitle, comptext,
               master, intervene, melco, fai,
               seats, seats2, pseats, pass_text, rpass_text)
            VALUES %s
        """, wp_insert, page_size=200)
        pg.commit()
        progress(f"  → {len(wp_insert)} new work_plans inserted (total now: {len(wp_id_map)})")
    else:
        progress(f"  → All {len(wp_id_map)} work_plans already migrated")

    # ── Step 5: log_items ───────────────────────────────────────────────────
    progress("\n[5/5] Migrating log_items…")
    cur_pg.execute("SELECT COUNT(*) FROM log_items")
    if cur_pg.fetchone()[0] == 0:
        cur_my.execute("""
            SELECT * FROM items
            WHERE logcrew IN ('TO','IO','DC','ALL','TO-IO','')
               OR (logcrew IS NULL)
            ORDER BY date, idno
        """)
        item_rows = cur_my.fetchall()
        li_insert = []
        skipped = 0
        for row in item_rows:
            day_uuid = day_id_map.get(row.get('dayidno'))
            if not day_uuid and row.get('date'):
                cur_pg.execute("SELECT id FROM summit_days WHERE log_date = %s", (row['date'],))
                r2 = cur_pg.fetchone()
                if r2:
                    day_uuid = r2[0]
            if not day_uuid:
                skipped += 1
                continue
            crew_tab = s(row.get('logcrew'), 10) or 'ALL'
            if crew_tab not in VALID_CREW_TABS:
                crew_tab = 'ALL'
            downtime = safe_int(row.get('downtime'))
            # Link to work plan if residno points to a WP item
            wp_uuid = None
            for res_field in ['residno','residno2','residno3','residno4','residno5','residno6']:
                r_id = safe_int(row.get(res_field))
                if r_id and r_id in wp_id_map:
                    wp_uuid = wp_id_map[r_id]
                    break
            li_insert.append((
                uuid.uuid4(), row['idno'], safe_int(row.get('oldidno')),
                day_uuid, wp_uuid,
                crew_tab,
                dt_utc(row.get('itemtime')),
                s(row.get('itemtitle'), 200),
                s(row.get('itemtext')),
                s(row.get('type'), 16),
                downtime,
                s(row.get('subsystem'), 10),
                s(row.get('status'), 15),
                s(row.get('user'), 20),
                s(row.get('history')),
                s(row.get('comment')),
                dt_utc(row.get('timestamp')),
                dt_utc(row.get('updatestamp')),
            ))

        psycopg2.extras.execute_values(cur_pg, """
            INSERT INTO log_items
              (id, legacy_item_id, legacy_old_item_id,
               summit_day_id, work_plan_id,
               crew_tab, item_time, title, body,
               item_type, downtime_minutes, subsystem, status,
               created_by, history_text, comment_text,
               created_at, updated_at)
            VALUES %s
            ON CONFLICT DO NOTHING
        """, li_insert, page_size=500)
        pg.commit()
        progress(f"  → {len(li_insert)} log_items inserted (skipped {skipped} without a day)")
    else:
        progress("  → Skipped (already have rows)")

    # ── Summary ──────────────────────────────────────────────────────────────
    progress("\n✅ Migration complete! Summary:")
    for table in ['summit_days','crew_assignments','weather_snapshots','email_deliveries',
                  'observation_programs','work_plans','log_items']:
        cur_pg.execute(f"SELECT COUNT(*) FROM {table}")
        progress(f"   {table}: {cur_pg.fetchone()[0]:,} rows")

    cur_my.close(); my.close()
    cur_pg.close(); pg.close()


if __name__ == "__main__":
    main()
