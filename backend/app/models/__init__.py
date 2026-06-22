# Database models - All mapping to legacy tables
from .fats_entry import FATSEntry  # Maps to 'fault' table
from .fats_comment import FATSComment  # Maps to 'fcomments' table
# Removed FATSImage - using filesystem-only approach for images
from .reference import FSection, FStaff  # Maps to 'fsection' and 'fstaff' tables
from .summit_legacy import Day, Item, Prog, ItemReq

__all__ = [
    "FATSEntry",
    "FATSComment",
    "FSection",
    "FStaff",
    "Day",
    "Item",
    "Prog",
    "ItemReq",
]
