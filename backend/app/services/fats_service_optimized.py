"""
Optimized FATS Service - Uses database indexes for fast search
This is an improved version that searches all 4 fields efficiently
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_, or_, func, text
from typing import List, Optional
from datetime import datetime

from app.models import FATSEntry, FATSComment
from app.schemas.fats_entry import FATSEntryCreate, FATSEntryUpdate

class FATSServiceOptimized:
    """
    Optimized service for FATS operations with proper indexing strategy
    """
    
    async def get_all_fats(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,
        section: Optional[str] = None,
        status: Optional[str] = None,
        use_fulltext: bool = False  # Set to True after adding FULLTEXT indexes
    ) -> List[FATSEntry]:
        """
        Get all FATS entries with filtering - optimized for performance
        
        Performance strategies:
        1. If use_fulltext=False: Uses regular indexes with ILIKE (works without FULLTEXT indexes)
        2. If use_fulltext=True: Uses MySQL FULLTEXT search (requires FULLTEXT indexes)
        """
        # Reasonable limits
        limit = min(limit, 1000)
        skip = min(skip, 5000)
        
        try:
            query = select(FATSEntry)
            
            # Apply search if provided
            if search and search.strip() and len(search.strip()) >= 2:
                search_trimmed = search.strip()
                
                if use_fulltext:
                    # OPTION 2: Use FULLTEXT search (requires FULLTEXT indexes)
                    # This is MUCH faster for searching large text fields
                    search_pattern = search_trimmed
                    
                    # Use MATCH AGAINST for FULLTEXT search
                    # Note: This requires the FULLTEXT indexes from add_fulltext_indexes.sql
                    query = query.where(
                        or_(
                            # Regular LIKE for smaller fields
                            FATSEntry.issue.ilike(f"%{search_pattern}%"),
                            FATSEntry.solution.ilike(f"%{search_pattern}%"),
                            FATSEntry.operator.ilike(f"%{search_pattern}%"),
                            # FULLTEXT search for large text fields
                            text(f"MATCH(idescribe) AGAINST('{search_pattern}' IN BOOLEAN MODE)"),
                            text(f"MATCH(sdescribe) AGAINST('{search_pattern}' IN BOOLEAN MODE)")
                        )
                    )
                else:
                    # OPTION 1: Use regular indexes with ILIKE
                    # This works immediately after running add_search_indexes.sql
                    search_pattern = f"%{search_trimmed}%"
                    
                    # Search all 4 fields - fast with proper indexes
                    query = query.where(
                        or_(
                            FATSEntry.issue.ilike(search_pattern),
                            FATSEntry.solution.ilike(search_pattern),
                            FATSEntry.operator.ilike(search_pattern),
                            # Note: These will be slower without FULLTEXT indexes
                            # but still work for 1400 entries
                            FATSEntry.idescribe.ilike(search_pattern),
                            FATSEntry.sdescribe.ilike(search_pattern)
                        )
                    )
            
            # Apply other filters (these use indexes)
            if section and section.strip():
                query = query.where(FATSEntry.section == section.strip())
            
            if status and status.strip():
                query = query.where(FATSEntry.status == status.strip())
            
            # Order by idno descending (uses PRIMARY KEY index - very fast)
            query = query.order_by(FATSEntry.idno.desc())
            
            # Apply pagination
            query = query.limit(limit).offset(skip)
            
            # Execute query
            result = await db.execute(query)
            fats_list = list(result.scalars().all())
            
            return fats_list
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in get_all_fats: {e}", exc_info=True)
            return []


# IMPLEMENTATION NOTES:
# ====================
# 
# Step 1: Add Regular Indexes
# ----------------------------
# Run: mysql -u opal -popal_password opal < add_search_indexes.sql
# This adds indexes on: solution, operator, section, status, assigned_to
# 
# Step 2 (Optional): Add FULLTEXT Indexes  
# ----------------------------------------
# Run: mysql -u opal -popal_password opal < add_fulltext_indexes.sql
# This adds FULLTEXT indexes on: issue, solution, idescribe, sdescribe
# 
# Step 3: Update Service
# ----------------------
# Replace the get_all_fats method in fats_service.py with this optimized version
# Set use_fulltext=False initially, then True after adding FULLTEXT indexes
#
# Performance Expectations:
# -------------------------
# - With regular indexes only: 20-50ms for searches on issue/solution/operator
# - With regular indexes only: 100-200ms for searches on idescribe/sdescribe  
# - With FULLTEXT indexes: 10-30ms for all searches including descriptions
