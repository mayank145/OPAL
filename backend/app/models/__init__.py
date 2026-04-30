# Database models - All mapping to legacy tables
from .fats_entry import FATSEntry  # Maps to 'fault' table
from .fats_comment import FATSComment  # Maps to 'fcomments' table
# Removed FATSImage - using filesystem-only approach for images
from .reference import FSection, FStaff  # Maps to 'fsection' and 'fstaff' tables
from .summit import (
    SummitDay,
    CrewAssignment,
    WeatherSnapshot,
    ObservationProgram,
    WorkPlan,
    LogItem,
    WorkPlanItemLink,
    EmailDelivery,
)

__all__ = [
    "FATSEntry",
    "FATSComment",
    "FSection",
    "FStaff",
    "SummitDay",
    "CrewAssignment",
    "WeatherSnapshot",
    "ObservationProgram",
    "WorkPlan",
    "LogItem",
    "WorkPlanItemLink",
    "EmailDelivery",
]
