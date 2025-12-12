"""
FATS Comment Model - Maps to legacy 'fcomments' table
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.session import Base

class FATSComment(Base):
    """
    Comments on FATS entries
    Maps to legacy 'fcomments' table
    """
    __tablename__ = "fcomments"
    
    # Legacy table structure
    idno = Column(Integer, primary_key=True, autoincrement=True)
    faultidno = Column(Integer)  # References fault.idno (but as int in legacy)
    todo = Column(String(80))
    solution = Column(String(80))
    operator = Column(String(20))  # Commenter/operator name
    datein = Column(DateTime, default=datetime.utcnow)
    sdescribe = Column(Text)  # Comment text/description
    
    # Relationships disabled to avoid circular import issues in current setup
    # fats_entry = relationship("FATSEntry", back_populates="comments")
    
    def __repr__(self):
        return f"<FATSComment(idno={self.idno}, faultidno={self.faultidno}, operator='{self.operator}')>"
