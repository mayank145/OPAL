"""
Image Service - Handles image upload, storage, and retrieval for FATS entries
Filesystem-only approach (no database table)
"""
import os
import uuid
import glob
from pathlib import Path
from typing import List, Optional, Dict
from fastapi import UploadFile, HTTPException, status
from datetime import datetime

from app.core.config import settings

class ImageService:
    """Service for handling FATS images - filesystem only"""
    
    def __init__(self):
        # Ensure upload directories exist
        self.upload_base = Path(settings.upload_dir)
        self.fats_images_dir = Path(settings.fats_images_dir)
        self.fats_images_dir.mkdir(parents=True, exist_ok=True)
    
    def _generate_filename(self, fats_id: int, original_filename: str) -> str:
        """
        Generate filename following legacy pattern: {idno}_{uuid}.{ext}
        """
        # Get file extension
        ext = Path(original_filename).suffix.lower()
        # Generate unique filename: {idno}_{uuid}{ext}
        unique_id = str(uuid.uuid4())[:8]
        return f"{fats_id}_{unique_id}{ext}"
    
    def _get_file_path(self, filename: str) -> Path:
        """Get full path to stored file"""
        return self.fats_images_dir / filename
    
    def _validate_image_file(self, file: UploadFile, content: bytes) -> None:
        """
        Validate image file type and size
        """
        # Validate file type
        if file.content_type not in settings.allowed_image_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file.content_type} not allowed. Allowed types: {', '.join(settings.allowed_image_types)}"
            )
        
        # Validate file size
        file_size = len(content)
        if file_size > settings.max_upload_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size {file_size} bytes ({file_size / 1024 / 1024:.2f} MB) exceeds maximum allowed size of {settings.max_upload_size} bytes ({settings.max_upload_size / 1024 / 1024:.2f} MB)"
            )
        
        # Validate minimum file size (prevent empty/corrupted files)
        if file_size < 100:  # At least 100 bytes
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File appears to be empty or corrupted"
            )
    
    def _parse_fats_id_from_filename(self, filename: str) -> Optional[int]:
        """
        Parse FATS ID from filename pattern: {fats_id}_{uuid}.{ext}
        Returns None if pattern doesn't match
        """
        try:
            # Extract FATS ID from filename (everything before first underscore after numbers)
            parts = filename.split('_')
            if parts:
                # First part should be the FATS ID
                fats_id_str = parts[0]
                return int(fats_id_str)
        except (ValueError, IndexError):
            pass
        return None
    
    def _get_image_info(self, file_path: Path) -> Dict:
        """
        Get image metadata from file system
        """
        stat = file_path.stat()
        return {
            'filename': file_path.name,
            'stored_filename': file_path.name,
            'file_path': str(file_path.relative_to(self.upload_base)),
            'file_size': stat.st_size,
            'mime_type': self._guess_mime_type(file_path),
            'uploaded_at': datetime.fromtimestamp(stat.st_mtime),
        }
    
    def _guess_mime_type(self, file_path: Path) -> str:
        """Guess MIME type from file extension"""
        ext = file_path.suffix.lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
        }
        return mime_types.get(ext, 'image/jpeg')
    
    async def upload_image(
        self,
        fats_id: int,
        file: UploadFile,
        uploaded_by: str = "system"
    ) -> Dict:
        """
        Upload an image for a FATS entry - filesystem only
        Returns dict with image info
        """
        # Read file content
        content = await file.read()
        
        # Validate file
        self._validate_image_file(file, content)
        
        # Generate filename
        stored_filename = self._generate_filename(fats_id, file.filename or "image")
        file_path = self._get_file_path(stored_filename)
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save file to disk
        try:
            with open(file_path, "wb") as f:
                f.write(content)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save image file: {str(e)}"
            )
        
        # Return image info (no database record)
        image_info = self._get_image_info(file_path)
        image_info['fats_id'] = fats_id
        image_info['uploaded_by'] = uploaded_by
        image_info['original_filename'] = file.filename or "image"
        
        return image_info
    
    async def upload_multiple_images(
        self,
        fats_id: int,
        files: List[UploadFile],
        uploaded_by: str = "system"
    ) -> List[Dict]:
        """
        Upload multiple images for a FATS entry
        Returns list of successfully uploaded image info dicts
        """
        uploaded_images = []
        errors = []
        
        for file in files:
            try:
                image_info = await self.upload_image(fats_id, file, uploaded_by)
                uploaded_images.append(image_info)
            except HTTPException as e:
                errors.append(f"{file.filename}: {e.detail}")
            except Exception as e:
                errors.append(f"{file.filename}: {str(e)}")
        
        if errors and not uploaded_images:
            # All uploads failed
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"All image uploads failed: {'; '.join(errors)}"
            )
        
        if errors:
            # Some uploads failed, but some succeeded
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Some images failed to upload: {'; '.join(errors)}")
        
        return uploaded_images
    
    def get_images_for_fats(self, fats_id: int) -> List[Dict]:
        """
        Get all images for a FATS entry by scanning filesystem
        Uses glob pattern to find all files starting with {fats_id}_
        """
        try:
            # Use glob to find all images for this FATS ID
            pattern = str(self.fats_images_dir / f"{fats_id}_*")
            image_files = glob.glob(pattern)
            
            images = []
            for file_path_str in image_files:
                file_path = Path(file_path_str)
                # Verify it's a file and has valid extension
                if file_path.is_file() and file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                    # Verify FATS ID matches (double-check)
                    parsed_id = self._parse_fats_id_from_filename(file_path.name)
                    if parsed_id == fats_id:
                        image_info = self._get_image_info(file_path)
                        image_info['fats_id'] = fats_id
                        image_info['id'] = hash(file_path.name) % (10**9)  # Generate pseudo-ID from filename hash
                        images.append(image_info)
            
            # Sort by filename (which includes timestamp from UUID, so roughly chronological)
            images.sort(key=lambda x: x['filename'], reverse=True)
            
            return images
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error scanning images for FATS {fats_id}: {e}", exc_info=True)
            return []
    
    def get_image_file_path(self, filename: str) -> Path:
        """Get file system path for an image by filename"""
        return self._get_file_path(filename)
    
    def get_image_url(self, filename: str) -> str:
        """Get URL path for an image by filename"""
        return f"/api/v1/fats/images/{filename}/file"
    
    def delete_image(self, filename: str) -> bool:
        """
        Delete an image by filename
        Returns True if deleted, False if not found
        """
        file_path = self._get_file_path(filename)
        try:
            if file_path.exists():
                file_path.unlink()
                return True
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Could not delete image file {file_path}: {e}")
        return False
