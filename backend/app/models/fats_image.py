"""
FATS Image Model - Tracks images associated with FATS entries
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from app.db.session import Base
from app.core.timezone import get_hst_now

class FATSImage(Base):
    """
    Images associated with FATS entries
    Maps to legacy file system storage in ../pix/ directory
    """
    __tablename__ = "fats_images"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fats_id = Column(Integer, nullable=False, index=True)  # References fault.idno
    filename = Column(String(255), nullable=False)  # Original filename
    stored_filename = Column(String(255), nullable=False)  # Actual filename on disk
    file_path = Column(String(500), nullable=False)  # Relative path from uploads directory
    file_size = Column(Integer)  # File size in bytes
    mime_type = Column(String(100))  # MIME type (e.g., image/jpeg, image/png)
    uploaded_by = Column(String(100))  # Username who uploaded
    uploaded_at = Column(DateTime, default=get_hst_now)
    
    def __repr__(self):
        return f"<FATSImage(id={self.id}, fats_id={self.fats_id}, filename='{self.filename}')>"

