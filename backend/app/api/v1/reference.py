"""
Reference Data API Endpoints - fsection, fstaff, and summit refer codes.
Provides dropdown options for FATS and Summit Logging forms.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, List

from sqlalchemy import text

from app.db.session import get_clients_db, get_db, get_sumlogs_db
from app.models.reference import FSection, FStaff

router = APIRouter()

# ── Summit refer codes (mirrored from legacy sumlogs.refer table) ────────────
# These are the operational code groups used in the Work Plan dialog.
_REFER_CODES: Dict[str, List[str]] = {
    "PLANREQ": [
        "Move-Tel", "Move-EL", "Move-AZ", "80t-Crane", "NsIR-Crane",
        "SmallDoor-Crane", "BSIT", "TUE-Opt-Crane", "TUE-Opt-US",
        "Gen2-Allocation", "MirrorHatch", "CherryPicker", "ForkLift",
        "Hazardous-Materials", "MainShutter", "Others",
    ],
    "PLANLOCK": [
        "No-Tel-Move", "No-AZ-Move", "No-EL-Move", "NoLights-Dome",
        "No-TopScreen-Move", "No-MirrorCover-Move", "No-MainShutter",
        "No-UnitSelector-Move",
    ],
    "DCASSIST": [".none", "DC1", "DC2", "DC-Any", "DC-All"],
    "INSTR": [
        "CHARIS", "CIAO", "CISCO", "COMICS", "FMOS", "FOCAS", "HDS",
        "HSC", "IRCS", "MOIRCS", "PFS", "SCExAO", "others",
    ],
    "ALLOC": [
        "OpenUse", "InstrEng", "TelEng", "UHObs", "ServiceObs",
        "StaffObs", "ToO", "Engineering",
    ],
    "LOCATIONS": [
        ".none", "CB-1-Floor", "CB-2-Floor", "CB-3-Floor", "ESB",
        "ESB-Exterior", "ESB-Catwalk", "Elevators", "Vent-Floor",
        "Obs-Floor", "Obs-Floor-Opt", "Obs-Floor-IR", "Nas-Floor",
        "Nas-Floor-Opt", "Nas-Floor-IR", "Tertiary-Floor",
        "Tertiary-Floor-Opt", "Tertiary-Floor-IR", "TUE-Floor",
        "TUE-Floor-Opt", "TUE-Floor-IR", "High-Roof", "Low-Roof",
        "Summit-Safety", "MainShutter-IR", "MainShutter-Opt",
        "Penthouse", "Coude", "Crane Floor",
    ],
    "TIME": [
        "", "00:00", "00:30", "01:00", "01:30", "02:00", "02:30",
        "03:00", "03:30", "04:00", "04:30", "05:00", "05:30",
        "06:00", "06:30", "07:00", "07:30", "08:00", "08:30",
        "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
        "12:00", "12:30", "13:00", "13:30", "14:00", "14:30",
        "15:00", "15:30", "16:00", "16:30", "17:00", "17:30",
        "18:00", "18:30", "19:00", "19:30", "20:00", "20:30",
        "21:00", "21:30", "22:00", "22:30", "23:00", "23:30",
    ],
}


@router.get("/refer-codes")
async def get_refer_codes():
    """Return all summit Work Plan reference code groups (mirrors legacy sumlogs.refer table)."""
    return _REFER_CODES


@router.get("/refer-codes/{code_type}", response_model=List[str])
async def get_refer_codes_by_type(code_type: str):
    """Return codes for a specific refer type (e.g. PLANREQ, PLANLOCK, DCASSIST)."""
    key = code_type.upper()
    if key not in _REFER_CODES:
        raise HTTPException(
            status_code=404,
            detail=f"Refer code type '{code_type}' not found. Valid types: {list(_REFER_CODES.keys())}",
        )
    return _REFER_CODES[key]

@router.get("/sections", response_model=List[str])
async def get_sections(db: AsyncSession = Depends(get_db)):
    """
    Get all section values from fsection table
    Used for section and section2 dropdowns
    """
    try:
        # Direct execution - SQLAlchemy handles timeouts via pool_timeout
        result = await db.execute(
            select(FSection.section)
            .distinct()
            .order_by(FSection.section)
            .limit(200)  # Limit to prevent timeout
        )
        sections = [row[0] for row in result.all() if row[0]]  # Filter out None/empty values
        # Always include .none as first option
        if '.none' not in sections:
            sections.insert(0, '.none')
        elif sections[0] != '.none':
            sections.remove('.none')
            sections.insert(0, '.none')
        return sections
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error fetching sections: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        # Return default sections on error
        return ['.none', 'Telescope/Dome', 'Instruments/PFS', 'Dome/Environment']

@router.get("/sections2", response_model=List[str])
async def get_sections2(db: AsyncSession = Depends(get_db)):
    """
    Get all distinct section2 values from fault table
    Used for section2 dropdown
    """
    try:
        from app.models.fats_entry import FATSEntry
        # Get distinct section2 values from the fault table
        result = await db.execute(
            select(FATSEntry.section2)
            .distinct()
            .where(FATSEntry.section2.isnot(None))
            .where(FATSEntry.section2 != '')
            .order_by(FATSEntry.section2)
            .limit(200)  # Limit to prevent timeout
        )
        sections2 = [row[0] for row in result.all() if row[0]]  # Filter out None/empty values
        # Always include .none as first option
        if '.none' not in sections2:
            sections2.insert(0, '.none')
        elif sections2[0] != '.none':
            sections2.remove('.none')
            sections2.insert(0, '.none')
        return sections2
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error fetching sections2: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        # Return default sections2 on error
        return ['.none', 'Dome/Air Condition', 'TWS/TSC', 'Cars']

@router.get("/staff", response_model=List[str])
async def get_staff(db: AsyncSession = Depends(get_db)):
    """
    Get all staff names from fstaff table
    Used for operator dropdown
    """
    try:
        # Direct execution - SQLAlchemy handles timeouts via pool_timeout
        result = await db.execute(
            select(FStaff.name)
            .distinct()
            .order_by(FStaff.name)
            .limit(100)  # Limit to prevent timeout
        )
        staff = [row[0] for row in result.all() if row[0]]  # Filter out None/empty values
        # Always include .none as first option
        if '.none' not in staff:
            staff.insert(0, '.none')
        elif staff[0] != '.none':
            staff.remove('.none')
            staff.insert(0, '.none')
        return staff
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error fetching staff: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        # Return default staff on error
        return ['.none', 'mayank', 'letawsky', 'twin']


@router.get("/org-users")
async def get_org_users(
    sumlogs_db: AsyncSession = Depends(get_sumlogs_db),
    clients_db: AsyncSession = Depends(get_clients_db),
):
    """
    Return the Subaru Telescope staff list for Assigned1 / Notify dropdowns.

    Primary source: sumlogs.users  (SELECT user … ORDER BY user) — same query
    as the legacy planone.py.  Falls back to clients.users (privy='subaru') if
    the sumlogs DB is unreachable.

    Returns [{ username, display }] sorted alphabetically.
    """
    sentinel = [{"username": ".none", "display": "— none —"}]

    # ── Try sumlogs.users first (matches legacy planone.py exactly) ──────────
    if sumlogs_db is not None:
        try:
            result = await sumlogs_db.execute(
                text(
                    "SELECT user FROM users "
                    "WHERE status = 'Active' "
                    "  AND user IS NOT NULL AND user != '' "
                    "  AND user NOT LIKE 'newuser%' AND user != 'none' "
                    "ORDER BY user "
                    "LIMIT 300"
                )
            )
            rows = result.fetchall()
            if rows:
                users = [
                    {"username": row[0].strip(), "display": row[0].strip()}
                    for row in rows
                    if row[0] and row[0].strip()
                ]
                return sentinel + users
        except Exception as exc:
            import logging
            logging.getLogger(__name__).warning(
                f"sumlogs DB unreachable for org-users, falling back to clients DB: {exc}"
            )

    # ── Fallback: clients.users where privy='subaru' ──────────────────────────
    try:
        result = await clients_db.execute(
            text(
                "SELECT username, first, last "
                "FROM users "
                "WHERE privy = 'subaru' AND status = 'Active' "
                "  AND username IS NOT NULL AND username != '' "
                "ORDER BY last, first "
                "LIMIT 200"
            )
        )
        rows = result.fetchall()
        users = []
        for row in rows:
            username = (row[0] or "").strip()
            first    = (row[1] or "").strip()
            last     = (row[2] or "").strip()
            if not username:
                continue
            full = f"{first} {last}".strip()
            users.append({"username": username, "display": f"{full} ({username})"})
        return sentinel + users
    except Exception as exc:
        import logging
        logging.getLogger(__name__).error(f"Error fetching org users (fallback): {exc}", exc_info=True)
        return sentinel
