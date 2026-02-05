"""
FATS Entry Model - Enhanced version of the existing fault table
"""
from sqlalchemy import Column, String, Text, Boolean, DateTime, Enum, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.session import Base
from app.core.timezone import get_hst_now

class FATSStatus(str, enum.Enum):
    ACTIVE = "Active"
    CANCELED = "Canceled"

class FATSEntry(Base):
    """
    Enhanced FATS Entry model based on existing fault table
    """
    __tablename__ = "fault"
    
    # Existing columns (keep for compatibility)
    idno = Column(Integer, primary_key=True, autoincrement=True)  # Primary key from existing table (legacy uses int)
    issue = Column(String(500))
    idescribe = Column(Text)
    solution = Column(String(500))
    sdescribe = Column(Text)
    todo = Column(String(80))  # Added to match legacy
    section = Column(String(100))
    operator = Column(String(20))  # Added to match legacy
    datein = Column(DateTime, default=get_hst_now)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    views = Column(Integer, default=0)  # Added to match legacy
    
    # New columns for enhanced functionality
    is_blank = Column(Boolean, default=False)
    status = Column(String(20), default="open")
    section2 = Column(String(30))  # Added to match legacy
    assigned_to = Column(String(100))
    created_by = Column(String(100))
    resolved_at = Column(DateTime)
    updated_at = Column(DateTime, default=get_hst_now, onupdate=get_hst_now)
    
    # Relationships will be added later to avoid circular import issues
    # comments = relationship("FATSComment", back_populates="fats_entry", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<FATSEntry(idno='{self.idno}', issue='{self.issue}', status='{self.status}')>"
