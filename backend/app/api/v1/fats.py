"""
FATS API Endpoints - Implements all 4 requirements
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from typing import List as ListType
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.session import get_db
from app.schemas.fats_entry import (
    FATSEntryCreate, FATSEntryUpdate, FATSEntryResponse, 
    FATSEntryWithComments, FATSCommentCreate, FATSCommentUpdate, FATSCommentResponse
)
# Removed FATSImageResponse import - using dict responses for filesystem-only approach
from app.services.fats_service import FATSService
from app.services.image_service import ImageService
# from app.models.fats_entry import FATSStatus

router = APIRouter()

# Initialize services
fats_service = FATSService()
image_service = ImageService()

@router.get("/", response_model=List[FATSEntryResponse])
async def list_fats(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=10000, description="Max number of records to return"),
    search: Optional[str] = Query(None, description="Search term"),
    section: Optional[str] = Query(None, description="Filter by section"),
    section2: Optional[str] = Query(None, description="Filter by section2"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: AsyncSession = Depends(get_db)
):
    """
    List all FATS entries with filtering and pagination
    """
    try:
        fats_entries = await fats_service.get_all_fats(
            db=db,
            skip=skip,
            limit=limit,
            search=search,
            section=section,
            section2=section2,
            status=status
        )
        return fats_entries
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in list_fats: {e}", exc_info=True)
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching FATS entries: {str(e)}"
        )

@router.get("/search/{idno}", response_model=List[FATSEntryResponse])
async def search_by_idno(
    idno: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Requirement #4: Search by IDNo, return as first result
    """
    fats_entries = await fats_service.search_by_idno(db, idno)
    return fats_entries

@router.get("/{fats_id}", response_model=FATSEntryWithComments)
async def get_fats(
    fats_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific FATS entry with comments
    """
    from app.schemas.fats_entry import FATSCommentResponse
    try:
        fats_entry = await fats_service.get_fats_by_id(db, fats_id)
        if not fats_entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"FATS entry with ID {fats_id} not found"
            )
        
        # Load comments with error handling (don't fail if comments can't be loaded)
        comments_response = []
        try:
            comments = await fats_service.get_fats_comments(db, fats_id)
            comments_response = [FATSCommentResponse.from_legacy_model(c) for c in comments]
        except Exception as e:
            # Log error but don't fail the whole request
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Could not load comments for FATS {fats_id}: {e}")
            comments_response = []
        
        # Create response with comments (Pydantic v2 uses model_validate)
        response = FATSEntryWithComments.model_validate(fats_entry)
        response.comments = comments_response
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching FATS entry: {str(e)}"
        )

@router.post("/", response_model=FATSEntryResponse, status_code=status.HTTP_201_CREATED)
async def create_fats(
    fats_data: FATSEntryCreate,
    confirmed: bool = Query(False, description="Confirmation for FATS creation"),
    db: AsyncSession = Depends(get_db)
):
    """
    Requirement #2: Create FATS with confirmation
    idno is optional - if not provided, database will auto-generate it
    """
    # Create FATS entry (with confirmation)
    # ID conflict check is handled in the service layer
    try:
        fats_entry = await fats_service.create_fats_entry(db, fats_data, confirmed)
    except ValueError as e:
        # Handle ID conflict error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    if not fats_entry:
        # Return confirmation required response
        return {
            "message": "Confirmation required to create FATS entry",
            "requires_confirmation": True,
            "fats_data": fats_data.dict()
        }
    
    return fats_entry

@router.put("/{fats_id}", response_model=FATSEntryResponse)
async def update_fats(
    fats_id: str,
    update_data: FATSEntryUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update FATS entry
    """
    fats_entry = await fats_service.update_fats_entry(db, fats_id, update_data)
    if not fats_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"FATS entry with ID {fats_id} not found"
        )
    return fats_entry

@router.delete("/{fats_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fats(
    fats_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete FATS entry
    """
    deleted = await fats_service.delete_fats_entry(db, fats_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"FATS entry with ID {fats_id} not found"
        )
    return None

@router.delete("/cleanup/blank", response_model=dict)
async def delete_blank_fats(
    db: AsyncSession = Depends(get_db)
):
    """
    Requirement #1: Delete blank FATS entries
    """
    deleted_count = await fats_service.delete_blank_fats(db)
    return {
        "message": f"Deleted {deleted_count} blank FATS entries",
        "deleted_count": deleted_count
    }

@router.post("/{fats_id}/comments", response_model=FATSCommentResponse, status_code=status.HTTP_201_CREATED)
async def add_comment(
    fats_id: str,
    comment_data: FATSCommentCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Add comment to FATS entry
    Maps legacy fcomments table fields to API response
    """
    from app.schemas.fats_entry import FATSCommentResponse
    comment = await fats_service.add_comment(
        db=db,
        fats_id=fats_id,
        comment_text=comment_data.comment_text,
        commenter=comment_data.commenter,
        todo=comment_data.todo,
        solution=comment_data.solution
    )
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"FATS entry with ID {fats_id} not found"
        )
    
    # Convert legacy model to response schema
    return FATSCommentResponse.from_legacy_model(comment)

@router.get("/{fats_id}/comments", response_model=List[FATSCommentResponse])
async def get_fats_comments(
    fats_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all comments for a FATS entry
    Maps legacy fcomments table fields to API response
    """
    from app.schemas.fats_entry import FATSCommentResponse
    comments = await fats_service.get_fats_comments(db, fats_id)
    # Convert legacy model to response schema
    return [FATSCommentResponse.from_legacy_model(comment) for comment in comments]

@router.patch("/comments/{comment_id}", response_model=FATSCommentResponse)
async def update_comment(
    comment_id: int,
    comment_data: FATSCommentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a comment
    Only provided fields will be updated
    """
    from app.schemas.fats_entry import FATSCommentResponse, FATSCommentUpdate
    
    comment = await fats_service.update_comment(
        db=db,
        comment_id=comment_id,
        comment_text=comment_data.comment_text,
        commenter=comment_data.commenter,
        todo=comment_data.todo,
        solution=comment_data.solution
    )
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with ID {comment_id} not found"
        )
    
    # Convert legacy model to response schema
    return FATSCommentResponse.from_legacy_model(comment)

@router.get("/stats/summary", response_model=dict)
async def get_fats_statistics(
    db: AsyncSession = Depends(get_db)
):
    """
    Get FATS statistics
    """
    stats = await fats_service.get_fats_statistics(db)
    return stats

# Image endpoints
@router.post("/{fats_id}/images", status_code=status.HTTP_201_CREATED)
async def upload_fats_image(
    fats_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload an image for a FATS entry
    """
    # Verify FATS entry exists
    fats_entry = await fats_service.get_fats_by_id(db, fats_id)
    if not fats_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"FATS entry with ID {fats_id} not found"
        )
    
    # Upload image (no database)
    try:
        image_info = await image_service.upload_image(
            fats_id=int(fats_id),
            file=file,
            uploaded_by="system"  # TODO: Get from authentication
        )
        
        # Add URL to response
        image_info['url'] = image_service.get_image_url(image_info['filename'])
        return image_info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading image: {str(e)}"
        )

@router.post("/{fats_id}/images/bulk", status_code=status.HTTP_201_CREATED)
async def upload_multiple_fats_images(
    fats_id: str,
    files: ListType[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload multiple images for a FATS entry
    """
    # Verify FATS entry exists
    fats_entry = await fats_service.get_fats_by_id(db, fats_id)
    if not fats_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"FATS entry with ID {fats_id} not found"
        )
    
    if not files or len(files) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files provided"
        )
    
    # Upload images (no database)
    try:
        images = await image_service.upload_multiple_images(
            fats_id=int(fats_id),
            files=files,
            uploaded_by="system"  # TODO: Get from authentication
        )
        
        # Add URLs to responses
        for image in images:
            image['url'] = image_service.get_image_url(image['filename'])
        
        return images
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading images: {str(e)}"
        )

@router.get("/{fats_id}/images")
async def get_fats_images(
    fats_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all images for a FATS entry - filesystem scan
    """
    try:
        images = image_service.get_images_for_fats(int(fats_id))
        
        # Add URLs to responses
        for image in images:
            image['url'] = image_service.get_image_url(image['filename'])
        
        return images
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error loading images for FATS {fats_id}: {e}", exc_info=True)
        return []

@router.get("/images/{filename}/file")
async def get_image_file(
    filename: str
):
    """
    Serve image file by filename - filesystem only
    """
    file_path = image_service.get_image_file_path(filename)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image file {filename} not found"
        )
    
    # Guess MIME type from extension (use public method)
    ext = file_path.suffix.lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
    }
    mime_type = mime_types.get(ext, 'image/jpeg')
    
    return FileResponse(
        path=str(file_path),
        media_type=mime_type,
        filename=filename
    )

@router.delete("/images/{filename}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fats_image(
    filename: str
):
    """
    Delete an image by filename - filesystem only
    """
    deleted = image_service.delete_image(filename)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image file {filename} not found"
        )
    return None
