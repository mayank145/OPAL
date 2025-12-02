"""
Pydantic schemas for FATS images
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FATSImageBase(BaseModel):
    """Base image schema"""
    fats_id: int = Field(..., description="FATS entry ID")
    filename: str = Field(..., description="Original filename")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    mime_type: Optional[str] = Field(None, description="MIME type")

class FATSImageCreate(BaseModel):
    """Schema for creating image (used in upload)"""
    pass  # File comes from multipart form

class FATSImageResponse(BaseModel):
    """Schema for image response"""
    id: int
    fats_id: int
    filename: str
    stored_filename: str
    file_path: str
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    uploaded_by: Optional[str] = None
    uploaded_at: datetime
    url: Optional[str] = Field(None, description="URL to access the image")

    class Config:
        from_attributes = True

