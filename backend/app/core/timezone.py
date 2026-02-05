"""
Timezone utilities for OPAL system
Handles HST (Hawaii Standard Time) conversion
"""
from datetime import datetime, timedelta

# HST is UTC-10 (no daylight saving time in Hawaii)
HST_OFFSET = timedelta(hours=-10)

def get_hst_now() -> datetime:
    """
    Get current time in HST (Hawaii Standard Time)
    HST is UTC-10
    """
    return datetime.utcnow() + HST_OFFSET

def utc_to_hst(utc_time: datetime) -> datetime:
    """
    Convert UTC datetime to HST
    """
    if utc_time is None:
        return None
    return utc_time + HST_OFFSET

def hst_to_utc(hst_time: datetime) -> datetime:
    """
    Convert HST datetime to UTC
    """
    if hst_time is None:
        return None
    return hst_time - HST_OFFSET
