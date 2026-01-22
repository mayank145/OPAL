"""
FATS Service - Business logic for FATS operations
Implements all requirements:
1. Delete blank FATS
2. Confirmation popup for FATS creation
3. Add comments to FATS
4. Search by IDNo shows result first
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_, or_, func, case
from sqlalchemy.orm import selectinload
from typing import List, Optional, Tuple
from datetime import datetime

from app.models import FATSEntry, FATSComment
from app.schemas.fats_entry import FATSEntryCreate, FATSEntryUpdate, FATSCommentCreate
# from app.models.fats_entry import FATSStatus, FATSPriority

class FATSService:
    """Service for FATS operations"""
    
    async def delete_blank_fats(self, db: AsyncSession) -> int:
        """
        Requirement #1: Delete blank FATS entries
        Delete all entries where issue, description (idescribe), and solution are all N/A (or empty/null)
        """
        # Imports already available at module level
        
        # Helper function to check if a field is N/A, empty, or null
        # Handles: NULL, empty string, whitespace-only, or "N/A" (case-insensitive)
        # Also handles HTML-wrapped N/A like "<p>N/A</p>"
        def is_na_or_empty(column):
            # Use COALESCE to handle NULL values
            # Remove HTML tags: replace <p> and </p> with empty string
            cleaned = func.replace(
                func.replace(
                    func.coalesce(column, ""), 
                    "<p>", 
                    ""
                ), 
                "</p>", 
                ""
            )
            trimmed = func.trim(cleaned)
            upper_trimmed = func.upper(trimmed)
            
            return or_(
                column == None,
                column == "",
                trimmed == "",
                upper_trimmed == "N/A"
            )
        
        # Check for entries where issue, idescribe, and solution are all N/A/empty/null
        blank_query = select(FATSEntry).where(
            and_(
                is_na_or_empty(FATSEntry.issue),
                is_na_or_empty(FATSEntry.idescribe),
                is_na_or_empty(FATSEntry.solution)
            )
        )
        
        result = await db.execute(blank_query)
        blank_entries = result.scalars().all()
        
        # Delete blank entries
        for entry in blank_entries:
            await db.delete(entry)
        
        await db.commit()
        return len(blank_entries)
    
    async def get_fats_by_id(self, db: AsyncSession, fats_id: str) -> Optional[FATSEntry]:
        """Get FATS entry by ID - handles string to int conversion for legacy table"""
        # Convert string ID to int for legacy fault.idno (which is int)
        try:
            idno_int = int(fats_id)
        except (ValueError, TypeError):
            return None
        
        result = await db.execute(
            select(FATSEntry)
            .where(FATSEntry.idno == idno_int)
        )
        return result.scalar_one_or_none()
    
    async def get_all_fats(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,
        section: Optional[str] = None,
        section2: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[FATSEntry]:
        """Get all FATS entries with filtering - optimized with database indexes"""
        # Reasonable limits for pagination
        limit = min(limit, 1000)  # Allow up to 1000 results
        skip = min(skip, 5000)  # Cap skip to prevent deep pagination
        
        try:
            # Start with base query
            query = select(FATSEntry)
            
            # Variable to track if we need custom ordering for ID search
            is_id_search = False
            fault_id_to_prioritize = None
            
            # Apply search filter if provided
            if search and search.strip() and len(search.strip()) >= 1:
                search_trimmed = search.strip()
                
                # Check if search term is a number (fault ID search)
                if search_trimmed.isdigit():
                    # If searching by fault ID: show exact match first, then related faults
                    try:
                        fault_id = int(search_trimmed)
                        search_pattern = f"%{search_trimmed}%"
                        
                        # Search for exact ID match OR mentions in text fields
                        query = query.where(
                            or_(
                                FATSEntry.idno == fault_id,  # Exact ID match
                                FATSEntry.issue.ilike(search_pattern),  # ID mentioned in issue
                                FATSEntry.solution.ilike(search_pattern),  # ID mentioned in solution
                                FATSEntry.idescribe.ilike(search_pattern),  # ID mentioned in description
                                FATSEntry.sdescribe.ilike(search_pattern)  # ID mentioned in solution description
                            )
                        )
                        
                        # Mark that we need to prioritize the exact ID match
                        is_id_search = True
                        fault_id_to_prioritize = fault_id
                    except ValueError:
                        # If conversion fails, treat as text search
                        pass
                else:
                    # For keyword/phrase search, search across all fields
                    # Use exact word matching for more precise results
                    search_pattern = f"%{search_trimmed}%"
                    
                    # Search across all fields - now fast with database indexes!
                    query = query.where(
                        or_(
                            FATSEntry.issue.ilike(search_pattern),
                            FATSEntry.solution.ilike(search_pattern),
                            FATSEntry.operator.ilike(search_pattern),
                            FATSEntry.idescribe.ilike(search_pattern),
                            FATSEntry.sdescribe.ilike(search_pattern)
                        )
                    )
            
            # Apply section filter - searches BOTH section and section2 columns
            # This matches old system behavior: select one section, search both columns
            if section and section.strip():
                section_value = section.strip()
                query = query.where(
                    or_(
                        FATSEntry.section == section_value,
                        FATSEntry.section2 == section_value
                    )
                )
            # Note: section2 parameter is kept for backwards compatibility but not used
            # The single section filter now searches both columns
            
            # Apply status filter (uses idx_fault_status index)
            if status and status.strip():
                query = query.where(FATSEntry.status == status.strip())
            
            # Order by: exact ID match first (for ID searches), then by idno descending
            if is_id_search and fault_id_to_prioritize:
                # Prioritize exact ID match, then show other related faults
                query = query.order_by(
                    case(
                        (FATSEntry.idno == fault_id_to_prioritize, 0),  # Exact match: priority 0 (first)
                        else_=1  # Other matches: priority 1 (after)
                    ),
                    FATSEntry.idno.desc()  # Within each priority, order by ID descending
                )
            else:
                # Default: order by idno descending (uses PRIMARY KEY index - very fast)
                query = query.order_by(FATSEntry.idno.desc())
            
            # Apply pagination
            query = query.limit(limit).offset(skip)
            
            # Execute query
            result = await db.execute(query)
            fats_list = list(result.scalars().all())
            
            return fats_list
        except Exception as e:
            # Log error using proper logging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in get_all_fats: {e}", exc_info=True)
            return []
    
    async def search_by_idno(self, db: AsyncSession, idno: str) -> List[FATSEntry]:
        """
        Requirement #4: Search by IDNo, return as first result
        Results are ordered by date descending (newest first)
        """
        # Get exact match first
        exact_match = await self.get_fats_by_id(db, idno)
        
        # Get all other entries (already ordered by date descending)
        other_entries = await self.get_all_fats(db, skip=0, limit=1000)
        
        # Remove exact match from other entries if it exists
        if exact_match:
            other_entries = [entry for entry in other_entries if entry.idno != int(idno)]
            # Return exact match first, then others (already sorted by date descending)
            return [exact_match] + other_entries
        
        return other_entries
    
    async def create_fats_entry(
        self, 
        db: AsyncSession, 
        fats_data: FATSEntryCreate,
        confirmed: bool = False
    ) -> Optional[FATSEntry]:
        """
        Requirement #2: Create FATS with confirmation
        idno is optional - if not provided, database will auto-generate it
        """
        if not confirmed:
            # Return None to trigger confirmation dialog
            return None
        
        # If idno is provided, check if it already exists
        if fats_data.idno is not None:
            existing_fats = await self.get_fats_by_id(db, str(fats_data.idno))
            if existing_fats:
                raise ValueError(f"FATS entry with ID {fats_data.idno} already exists")
        
        # Create new FATS entry
        # If idno is None, database will auto-generate it (auto_increment)
        create_data = {
            "issue": fats_data.issue,
            "idescribe": fats_data.idescribe,
            "solution": fats_data.solution,
            "sdescribe": fats_data.sdescribe,
            "section": fats_data.section,
            "status": fats_data.status,
            "assigned_to": fats_data.assigned_to,
            "created_by": fats_data.created_by,
            "datein": datetime.utcnow(),
            "todo": fats_data.todo,
            "operator": fats_data.operator,
            "section2": fats_data.section2
        }
        
        # Only include idno if it's provided
        if fats_data.idno is not None:
            create_data["idno"] = fats_data.idno
        
        fats_entry = FATSEntry(**create_data)
        
        db.add(fats_entry)
        await db.commit()
        await db.refresh(fats_entry)
        
        return fats_entry
    
    async def update_fats_entry(
        self, 
        db: AsyncSession, 
        fats_id: str, 
        update_data: FATSEntryUpdate
    ) -> Optional[FATSEntry]:
        """Update FATS entry"""
        fats_entry = await self.get_fats_by_id(db, fats_id)
        if not fats_entry:
            return None
        
        # Update only provided fields
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(fats_entry, field, value)
        
        fats_entry.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(fats_entry)
        
        return fats_entry
    
    async def delete_fats_entry(self, db: AsyncSession, fats_id: str) -> bool:
        """Delete FATS entry"""
        fats_entry = await self.get_fats_by_id(db, fats_id)
        if not fats_entry:
            return False
        
        await db.delete(fats_entry)
        await db.commit()
        return True
    
    async def add_comment(
        self,
        db: AsyncSession,
        fats_id: str,
        comment_text: str,
        commenter: str,
        todo: Optional[str] = None,
        solution: Optional[str] = None
    ) -> Optional[FATSComment]:
        """
        Add comment to FATS entry
        Maps to legacy fcomments table
        """
        # Verify FATS entry exists
        fats_entry = await self.get_fats_by_id(db, fats_id)
        if not fats_entry:
            return None
        
        # Convert fats_id (string) to int for legacy faultidno field
        try:
            faultidno = int(fats_id)
        except ValueError:
            return None
        
        # Create comment using legacy field names
        comment = FATSComment(
            faultidno=faultidno,  # Legacy field name
            sdescribe=comment_text,  # Legacy field for comment text
            operator=commenter,  # Legacy field for operator/commenter
            todo=todo,  # Legacy field for todo
            solution=solution,  # Legacy field for solution
            datein=datetime.utcnow()
        )
        
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        
        return comment
    
    async def get_fats_comments(self, db: AsyncSession, fats_id: str) -> List[FATSComment]:
        """Get all comments for a FATS entry - returns legacy model objects"""
        # Convert fats_id (string) to int for legacy faultidno field
        try:
            faultidno = int(fats_id)
        except ValueError:
            return []
        
        try:
            result = await db.execute(
                select(FATSComment)
                .where(FATSComment.faultidno == faultidno)
                .order_by(FATSComment.datein.desc())
                .limit(100)  # Limit comments to prevent timeout
            )
            return list(result.scalars().all())
        except Exception as e:
            # If there's an error (e.g., table doesn't exist), return empty list
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error querying comments: {e}", exc_info=True)
            return []
    
    async def update_comment(
        self,
        db: AsyncSession,
        comment_id: int,
        comment_text: Optional[str] = None,
        commenter: Optional[str] = None,
        todo: Optional[str] = None,
        solution: Optional[str] = None
    ) -> Optional[FATSComment]:
        """
        Update a comment
        Only updates fields that are provided (not None)
        """
        try:
            # Fetch the existing comment
            result = await db.execute(
                select(FATSComment).where(FATSComment.idno == comment_id)
            )
            comment = result.scalar_one_or_none()
            
            if not comment:
                return None
            
            # Update fields if provided
            if comment_text is not None:
                comment.sdescribe = comment_text
            if commenter is not None:
                comment.operator = commenter
            if todo is not None:
                comment.todo = todo
            if solution is not None:
                comment.solution = solution
            
            await db.commit()
            await db.refresh(comment)
            
            return comment
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error updating comment {comment_id}: {e}")
            await db.rollback()
            return None
    
    async def get_fats_statistics(self, db: AsyncSession) -> dict:
        """Get FATS statistics - optimized with single query"""
        # Use a single query to count total FATS entries
        stats_query = select(
            func.count(FATSEntry.idno).label('total')
        )
        
        result = await db.execute(stats_query)
        row = result.first()
        
        total = row.total or 0 if row else 0
        
        return {
            "total_fats": total
        }
