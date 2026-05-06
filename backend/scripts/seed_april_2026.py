"""
Seed realistic Subaru Telescope summit log data for April 2026.

Run from backend/:
    source venv/bin/activate
    python scripts/seed_april_2026.py

Idempotent-ish: re-running adds more data; to truly reset, delete the day first.
"""

from __future__ import annotations

import random
import sys
from datetime import datetime, timedelta, timezone

import httpx
from jose import jwt

BASE = "http://127.0.0.1:8000/api/v1/summit"

# ── Auth ─────────────────────────────────────────────────────────────────────
def _token() -> str:
    from app.core.config import settings
    payload = {
        "sub": "mayank", "privy": "subaru", "logcrew": "TO", "uid": 1,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def _make_client() -> httpx.Client:
    from app.core.config import settings
    return httpx.Client(
        base_url="http://127.0.0.1:8000",
        headers={"Cookie": f"{settings.cookie_name}={_token()}"},
        timeout=20, follow_redirects=True,
    )

# ── Subaru-specific lookup tables ─────────────────────────────────────────────

INSTRUMENTS = ["HSC", "HDS", "IRCS", "SCExAO", "FOCAS", "MOIRCS", "COMICS", "SWIMS", "IRD", "VAMPIRES"]

TO_CREW = ["Winegar", "Basri", "Hattori K.", "Takami M.", "Usuda T.", "Kudo T.",
           "Kashikawa N.", "Hayano Y.", "Minowa Y.", "Ozaki S."]
IO_CREW = ["Ikeda Y.", "Narita N.", "Tanaka I.", "Yamada T.", "Furusawa Y.",
           "Shimizu Y.", "Nishimoto A.", "Sako S.", "Sugai H.", "Ohyama Y."]
DC_CREW = ["Choudhary M.", "Letawsky S.", "Guyon O.", "Tamura M.", "Oya S.",
           "Suzuki R.", "Takato N.", "Terada H.", "Watanabe M.", "Yoshida M."]

PROPOSERS = [
    ("Miyazaki S.", "HSC"), ("Baba J.", "HDS"), ("Nishiyama S.", "IRCS"),
    ("Currie T.", "SCExAO"), ("Ono Y.", "FOCAS"), ("Konishi M.", "MOIRCS"),
    ("Fujiwara H.", "COMICS"), ("Goto T.", "SWIMS"), ("Kotani T.", "IRD"),
    ("Lozi J.", "VAMPIRES"), ("Hayashi M.", "IRCS"), ("Doi M.", "HSC"),
    ("Ouchi M.", "HSC"), ("Imanishi M.", "IRCS"), ("Minami Y.", "HDS"),
    ("Kinoshita D.", "FOCAS"), ("Abe L.", "SCExAO"), ("Kuzuhara M.", "IRD"),
]

SKY_CONDITIONS = ["Photometric", "Thin cirrus", "Partly cloudy", "Variable clouds",
                  "Clear", "Excellent seeing", "Photometric, windy"]
SEEINGS = ["0.3\"", "0.4\"", "0.5\"", "0.6\"", "0.7\"", "0.8\"", "1.0\"", "1.2\"", "1.5\""]
WINDS = ["3 kn NE", "8 kn N", "12 kn NW", "5 kn E", "20 kn NE", "15 kn S", "2 kn variable"]
TEMPS = ["-2°C", "0°C", "2°C", "4°C", "6°C", "8°C", "1°C", "-1°C"]
HUMIDS = ["25%", "30%", "40%", "50%", "60%", "75%", "85%"]

SUBSYSTEMS = ["Telescope", "Dome", "Instrument", "AO", "Electronics", "Software", "Other"]
LOCATIONS = ["Summit", "IR3", "CS", "Nasmyth", "Hilo Base", "Remote"]

TROUBLE_TEMPLATES = [
    ("AO188 DM actuator stuck", "AO188 deformable mirror actuator #{n} showing no response. "
     "Manual reset attempted. System restarted with 1 actuator masked. Correction quality reduced "
     "~2% but science accepted. Reported to AO group for next maintenance window."),
    ("M2 hexapod communication loss", "M2 secondary mirror hexapod lost communication during "
     "focus sequence. TCS showed timeout. Power cycle of hexapod controller restored comms. "
     "Re-homed all 6 axes. Focus check confirmed. Downtime ~{dt} min."),
    ("IRTC detector warm-up", "IR tip-tilt sensor temperature drifted above nominal (+2K). "
     "Cryocooler power adjusted. Stabilised after 20 min. No data loss."),
    ("Dome shutter hesitation", "Dome shutter E paused during opening at 60% position. "
     "Limit switch check OK. Manual jog completed opening. Logged for engineering follow-up."),
    ("HSC dewar vacuum warning", "HSC dewar pressure gauge tripped warning threshold. "
     "Secondary ion pump boosted. Pressure returned nominal within 10 min. Continued observing."),
    ("Guider CCD readout noise spike", "Guide camera readout showing elevated noise on col 512. "
     "Reset CCD controller. Noise cleared. No science impact."),
    ("TCS time server drift", "Telescope control system NTP sync dropped for 3 min. "
     "Time correction applied. Logged {dt} min downtime; pointing model unaffected."),
    ("FOCAS long-slit mask jam", "FOCAS slit mask changer did not seat properly for 0.3\" slit. "
     "Exchange retried 2x. Manual intervention via engineering GUI succeeded."),
    ("Wind shake above limit at {wind} kn", "Wind speed exceeded operation limit. "
     "Dome partially closed to azimuth shield. Resumed observing in protected direction."),
    ("IRCS cold stage warming trend", "IRCS cold stage temperature trending 0.1 K/hr above set point. "
     "Compressor status checked — OK. Adjusted cooling setpoint. Trend reversed after 30 min."),
]

COMMENT_TEMPLATES = [
    "Opened dome at {t} HST. Conditions nominal. Evening sky clear.",
    "Handover from night crew completed at {t} HST. Daytime work plan reviewed.",
    "Twilight flats completed for {instr}. 12 frames taken.",
    "Pointing check run using HD {n} — offset corrected, dAZ={az}\" dEL={el}\".",
    "Autoguider acquired on GSC {n}. Guide star FWHM {seeing}.",
    "Instrument change from {i1} to {i2} completed. Realignment verified.",
    "Operator break {t}–{t2} HST. Telescope tracking in safe mode.",
    "Focus sequence run. Best focus at {foc} mm (delta {df} µm from previous).",
    "Slew to engineering target for M2 active optics check. Wavefront measurement OK.",
    "Summit power monitoring: stable. UPS load {load}%.",
    "Closed dome at {t} HST. Morning twilight. Instrument warming procedure started.",
    "Software restart: TCS rebooted following connectivity alert. Recovery 8 min.",
    "Weather hold {dur} min due to humidity > 90%. Reopened at {t} HST.",
    "Background sky measurement: {sky} ADU/arcsec² in {band}.",
    "Calibration arc lamps taken for {instr}. Spectra quality good.",
    "All-sky camera shows {sky_cond}. Proceeding with program.",
    "Filter change: {f1} → {f2}. Wheel confirmed at target position.",
    "Maintenance complete on {sys}. System returned to operations.",
    "End of engineering block. Science operations resumed at {t} HST.",
    "Pressure/humidity alert cleared. Conditions improving.",
]

WP_TEMPLATES = [
    {
        "prefix": "AO188 routine maintenance",
        "texts": [
            "Replace WFS lenslet array and inspect DM actuator connectors.",
            "Check all 188 actuator responses. Mask stuck actuators.",
            "Calibrate WFS camera dark frames and flat fields.",
        ],
        "intervene": "Yes", "location": "Nasmyth",
    },
    {
        "prefix": "HSC focal-plane maintenance",
        "texts": [
            "Clean HSC corrector lens element C5 (dust spotted last run).",
            "Check cryo-cooler compressor oil level. Inspect cold-head vibration isolators.",
        ],
        "intervene": "Yes", "location": "CS",
    },
    {
        "prefix": "TCS software update",
        "texts": [
            "Apply TCS patch v4.3.2 — NTP sync improvement and AG communication fix.",
            "Update pointing model lookup table. Run regression tests.",
        ],
        "intervene": "No", "location": "Hilo Base",
    },
    {
        "prefix": "Telescope lubrication & inspection",
        "texts": [
            "Lubricate azimuth drive rack and pinion. Check encoder read-head alignment.",
            "Inspect primary mirror lateral supports. Re-torque bolts to spec.",
        ],
        "intervene": "Yes", "location": "Summit",
    },
    {
        "prefix": "IRCS detector controller check",
        "texts": [
            "Test IRCS H2RG readout modes. Verify dark current and read noise.",
            "Inspect cryo-cooler cold head. Check vacuum seal integrity.",
        ],
        "intervene": "Yes", "location": "IR3",
    },
    {
        "prefix": "Summit facility electrical inspection",
        "texts": [
            "Inspect PDU bus-bars in main electrical room. Test UPS bypass.",
            "Test emergency lighting and generator load transfer.",
        ],
        "intervene": "No", "location": "Summit",
    },
    {
        "prefix": "FOCAS instrument servicing",
        "texts": [
            "Replace mask exchange mechanism drive belt. Lubricate linear rails.",
            "Calibrate VPH grating tilt encoder. Run mask wheel homing test.",
        ],
        "intervene": "Yes", "location": "Nasmyth",
    },
    {
        "prefix": "HDS fiber injection alignment",
        "texts": [
            "Re-align fiber injection module after last instrument rotation.",
            "Check iodine cell temperature stability. Run wavelength stability test.",
        ],
        "intervene": "Yes", "location": "Nasmyth",
    },
]

TRANSPORT_POOL = [
    ("Aihara H.", "Jing Y.", "Chen Y."),
    ("Sugahara Y.", "Ono Y.", "—"),
    ("Ouchi M.", "Shibuya T.", "Inoue A."),
    ("Egami E.", "—", "—"),
    ("Tamura M.", "Kotani T.", "Kudo T."),
]

def _iso(date_str: str, hour: int, minute: int) -> str:
    return f"{date_str}T{hour:02d}:{minute:02d}:00+00:00"

def _rng(seed: int) -> random.Random:
    return random.Random(seed)

# ── Seed one day ─────────────────────────────────────────────────────────────

def seed_day(c: httpx.Client, date_str: str, day_n: int) -> None:
    r = _rng(day_n * 37 + 1337)
    print(f"\n─── {date_str} ───")

    # Day-of-week for context
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    is_weekend = dt.weekday() >= 5
    is_engineering = r.random() < 0.2 or is_weekend  # ~20% + weekends

    # ── Day label + zoom
    label_choices = [
        "Night ops", "Eng run", "Shared-risk", "ToO", "Classical", "Service", "Half-night",
    ] if not is_engineering else ["Day eng", "Maint", "Engineering", "Subsys test"]
    label = r.choice(label_choices)
    zoom_id = str(r.randint(80000000, 89999999)) if r.random() < 0.6 else ""
    zoom_pw = f"Sub{r.randint(100,999)}" if zoom_id else ""
    zoom_url = f"https://zoom.us/j/{zoom_id}" if zoom_id else ""

    resp = c.patch(f"{BASE}/day/{date_str}", json={
        "day_label": label,
        "zoom_meeting_id": zoom_id,
        "zoom_password": zoom_pw,
        "zoom_join_url": zoom_url,
    })
    if resp.status_code not in (200, 201):
        print(f"  WARN patch day: {resp.status_code} {resp.text[:200]}")

    # ── Weather
    sky = r.choice(SKY_CONDITIONS)
    seeing = r.choice(SEEINGS)
    wind = r.choice(WINDS)
    temp = r.choice(TEMPS)
    hum = r.choice(HUMIDS)
    resp = c.put(f"{BASE}/day/{date_str}/weather", json={
        "sky": sky, "seeing": seeing, "wind": wind,
        "temp_raw": temp, "humidity_raw": hum,
        "comment_text": f"Station-{r.randint(1,3)} data. Tropopause at {r.randint(14,18)} km.",
    })
    if resp.status_code == 200:
        print(f"  weather OK  sky={sky}  seeing={seeing}")
    else:
        print(f"  WARN weather: {resp.status_code}")

    # ── Crew
    n_to = r.randint(1, 2)
    n_io = r.randint(1, 2)
    n_dc = r.randint(1, 2)
    crew_added = 0
    for i in range(n_to):
        name = r.choice(TO_CREW)
        loc = "Summit" if i == 0 else r.choice(["Summit", "Remote"])
        resp = c.post(f"{BASE}/day/{date_str}/crew", json={
            "role": "TO", "member_name": name, "location": loc,
            "time_in": _iso(date_str, 8, 0), "time_out": _iso(date_str, 20, 0),
        })
        if resp.status_code == 201:
            crew_added += 1
    for i in range(n_io):
        name = r.choice(IO_CREW)
        loc = r.choice(["Summit", "Remote", "Hilo Base"])
        resp = c.post(f"{BASE}/day/{date_str}/crew", json={
            "role": "IO", "member_name": name, "location": loc,
            "time_in": _iso(date_str, 18, 30), "time_out": _iso(date_str + "T06:00:00+00:00", 6, 0),
        })
        if resp.status_code == 201:
            crew_added += 1
    for _ in range(n_dc):
        name = r.choice(DC_CREW)
        resp = c.post(f"{BASE}/day/{date_str}/crew", json={
            "role": "DC", "member_name": name, "location": "Hilo Base",
            "time_in": _iso(date_str, 18, 0), "time_out": _iso(date_str, 22, 0),
        })
        if resp.status_code == 201:
            crew_added += 1
    print(f"  crew added: {crew_added}")

    # ── Observation programs
    n_prog = r.randint(1, 3) if not is_engineering else 0
    progs_added = 0
    for sort_i in range(n_prog):
        pi, instr = r.choice(PROPOSERS)
        prop_num = r.randint(1, 50)
        semester = "S26A" if r.random() < 0.7 else "S25B"
        time_start = _iso(date_str, 18 + sort_i * 3, 0)
        time_end = _iso(date_str, 21 + sort_i * 3, 0)
        resp = c.post(f"{BASE}/day/{date_str}/programs", json={
            "propid": f"{semester}-{prop_num:03d}",
            "instr": instr,
            "pi": pi,
            "alloc": str(r.randint(2, 6)),
            "sort_order": sort_i + 1,
            "slot_start": time_start,
            "slot_end": time_end,
            "gid": r.choice(["A", "B", "C", "S", "T"]),
            "obs1": r.choice(IO_CREW),
            "obs1loc": r.choice(["Summit", "Remote", "Hilo"]),
            "notes": f"{r.randint(1,5)} hr block. {r.choice(['PI connected remotely.','PI on-site.','ToO priority A.','Service mode.'])}",
        })
        if resp.status_code == 201:
            progs_added += 1
    print(f"  programs added: {progs_added}")

    # ── Work plan (engineering) – add 1–2 on engineering days, 0–1 on normal
    n_wp = r.randint(1, 2) if is_engineering else r.randint(0, 1)
    wp_tmpl = r.sample(WP_TEMPLATES, min(n_wp, len(WP_TEMPLATES)))
    wp_ids = []
    for tmpl in wp_tmpl:
        text = r.choice(tmpl["texts"])
        transport = r.choice(TRANSPORT_POOL)
        master = r.randint(2, 5)
        seats = master + r.randint(1, 4)
        resp = c.post(f"{BASE}/day/{date_str}/work-plans", json={
            "comptitle": tmpl["prefix"],
            "comptext": text,
            "intervene": tmpl["intervene"],
            "location": tmpl["location"],
            "assigned1": r.choice(DC_CREW),
            "assigned2": r.choice(DC_CREW),
            "melco": f"MC-{r.randint(1,9):02d}",
            "fai": f"FAI-{r.randint(1,9):02d}",
            "master": master,
            "seats": seats,
            "pass_text": ", ".join(filter(lambda x: x != "—", transport)),
            "nite_effect": r.choice(["None", "Minor delay possible", "No effect"]),
            "requirements": f"Hard hat, safety shoes required. Min {r.randint(2,4)} personnel.",
        })
        if resp.status_code == 201:
            wp_ids.append(resp.json()["id"])
    print(f"  work plans added: {len(wp_ids)}")

    # ── Log items
    # Determine if there was a trouble event
    has_trouble = r.random() < 0.45
    trouble_dt = r.randint(10, 90) if has_trouble else 0

    hour_open = 18 if not is_engineering else 8
    items_added = 0

    # 1. Open dome / start of operations
    open_hr = hour_open
    open_body = r.choice(COMMENT_TEMPLATES[:2]).format(
        t=f"{open_hr:02d}:{r.randint(0,59):02d}", instr="", n="", az="", el="",
        seeing="", i1="", i2="", foc="", df="", load=r.randint(60, 85),
        sky_cond=sky.lower(), dur="", sky="", band="", f1="", f2="", sys="",
    ).split(".")[0] + "."
    resp = c.post(f"{BASE}/day/{date_str}/items", json={
        "crew_tab": "TO",
        "item_type": "Comment",
        "status": "Completed",
        "title": "Start of operations",
        "body": open_body,
        "item_time": _iso(date_str, open_hr, r.randint(0, 30)),
        "created_by": r.choice(TO_CREW),
    })
    if resp.status_code == 201:
        items_added += 1

    # 2. Focus check
    resp = c.post(f"{BASE}/day/{date_str}/items", json={
        "crew_tab": "TO",
        "item_type": "Comment",
        "status": "Completed",
        "title": "Focus sequence",
        "body": (f"Focus sequence run at start of night. Best focus "
                 f"{r.randint(7300,7600)}.{r.randint(0,9)} mm "
                 f"(delta {r.randint(-30,30)} µm from previous run). "
                 f"Seeing {seeing} on Hartmann test."),
        "item_time": _iso(date_str, open_hr, r.randint(15, 59)),
        "created_by": r.choice(TO_CREW),
    })
    if resp.status_code == 201:
        items_added += 1

    # 3. IO entry — program start
    if n_prog > 0:
        pi, instr = r.choice(PROPOSERS)
        resp = c.post(f"{BASE}/day/{date_str}/items", json={
            "crew_tab": "IO",
            "item_type": "Comment",
            "status": "Completed",
            "title": f"Program start: {instr}",
            "body": (f"Observer {pi} connected. {instr} target acquisition complete. "
                     f"First science frame at {open_hr+1:02d}:{r.randint(0,59):02d} HST. "
                     f"Sky background nominal ({r.randint(100,400)} ADU/px)."),
            "item_time": _iso(date_str, open_hr + 1, r.randint(0, 30)),
            "created_by": r.choice(IO_CREW),
        })
        if resp.status_code == 201:
            items_added += 1

    # 4. Trouble item (conditional)
    if has_trouble:
        tmpl = r.choice(TROUBLE_TEMPLATES)
        title_raw, body_raw = tmpl
        title = title_raw.format(n=r.randint(1,188), wind=r.choice(["22","25","28","30"]))
        body = body_raw.format(n=r.randint(1,188), dt=trouble_dt,
                               wind=r.choice(["22","25","28","30"]))
        resp = c.post(f"{BASE}/day/{date_str}/items", json={
            "crew_tab": "TO",
            "item_type": "Trouble",
            "status": "Completed" if r.random() < 0.75 else "Incompleted",
            "title": title,
            "body": body,
            "subsystem": r.choice(SUBSYSTEMS),
            "downtime_minutes": trouble_dt,
            "item_time": _iso(date_str, open_hr + r.randint(1, 4), r.randint(0, 59)),
            "created_by": r.choice(TO_CREW),
            "summit_access": "No",
        })
        if resp.status_code == 201:
            items_added += 1

    # 5. DC entry — engineering / maintenance note
    if is_engineering or r.random() < 0.6:
        eng_bodies = [
            f"Performed pre-observation check: M1 support forces within ±0.5 N of nominal. "
            f"All {r.randint(255,261)} support actuators responding.",
            f"M2 active optics: wavefront RMS after correction {r.uniform(30,90):.0f} nm. "
            f"Good seeing tonight; 6 Zernike modes corrected.",
            f"Primary mirror cell cleaned. Lateral support pads inspected — no wear observed.",
            f"Cassegrain cable wrap at {r.randint(-300,300)}°. Limit check OK.",
            f"Nasmyth rotator drive temp {r.uniform(15,30):.1f}°C. Lubrication schedule: next {r.randint(10,60)} days.",
            f"Instrument rotator position reset. ADC alignment verified with collimation star.",
        ]
        resp = c.post(f"{BASE}/day/{date_str}/items", json={
            "crew_tab": "DC",
            "item_type": "Comment",
            "status": "Completed",
            "title": "Day crew maintenance note",
            "body": r.choice(eng_bodies),
            "item_time": _iso(date_str, r.randint(9, 16), r.randint(0, 59)),
            "created_by": r.choice(DC_CREW),
        })
        if resp.status_code == 201:
            items_added += 1

    # 6. WP log entry (if work plans created)
    for wp_id in wp_ids[:1]:
        resp = c.post(f"{BASE}/day/{date_str}/items", json={
            "crew_tab": "WP",
            "item_type": "Comment",
            "status": "Completed",
            "title": "Work plan executed",
            "body": (f"Work plan carried out as scheduled. "
                     f"Duration: {r.randint(45,180)} min. "
                     f"No unplanned scope extension. "
                     f"Sign-off by {r.choice(DC_CREW)}."),
            "item_time": _iso(date_str, r.randint(10, 17), r.randint(0, 59)),
            "work_plan_id": wp_id,
            "created_by": r.choice(DC_CREW),
        })
        if resp.status_code == 201:
            items_added += 1

    # 7. Closing entry
    close_hr = 6 if not is_engineering else 17
    resp = c.post(f"{BASE}/day/{date_str}/items", json={
        "crew_tab": "TO",
        "item_type": "Summary",
        "status": "Completed",
        "title": "End of operations",
        "body": (f"Closed dome at {close_hr:02d}:{r.randint(0,59):02d} HST. "
                 f"{'Morning twilight.' if not is_engineering else 'Engineering complete.'} "
                 f"Total downtime: {trouble_dt} min. "
                 f"Effective on-sky: {r.randint(4,9)}h {r.randint(0,59):02d}m. "
                 f"Conditions overall: {sky.lower()}."),
        "item_time": _iso(date_str, close_hr, r.randint(10, 59)),
        "created_by": r.choice(TO_CREW),
    })
    if resp.status_code == 201:
        items_added += 1

    print(f"  log items added: {items_added}  (downtime={trouble_dt} min)")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    sys.path.insert(0, ".")   # so 'from app.core.config import settings' works
    c = _make_client()

    # Verify server is up
    r = c.get("http://127.0.0.1:8000/api/v1/summit/health")
    if r.status_code != 200:
        print("ERROR: server not reachable. Start uvicorn first.")
        sys.exit(1)

    print("Seeding April 2026 with Subaru Telescope operations data …")
    for day_n, day in enumerate(range(1, 31), start=1):
        date_str = f"2026-04-{day:02d}"
        try:
            seed_day(c, date_str, day_n)
        except Exception as exc:
            print(f"  ERROR on {date_str}: {exc}")

    print("\n✓ Seeding complete.")


if __name__ == "__main__":
    main()
