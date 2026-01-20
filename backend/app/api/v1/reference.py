"""
Reference Data API Endpoints - fsection and fstaff
Provides dropdown options for FATS forms
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.models.reference import FSection, FStaff

router = APIRouter()

@router.get("/sections", response_model=List[str])
async def get_sections(db: AsyncSession = Depends(get_db)):
    """
    Get all section values from fsection table
    Used for section and section2 dropdowns
    """
    try:
        # Direct execution - SQLAlchemy handles timeouts via pool_timeout
        result = await db.execute(
            select(FSection.section)
            .distinct()
            .order_by(FSection.section)
            .limit(200)  # Limit to prevent timeout
        )
        sections = [row[0] for row in result.all() if row[0]]  # Filter out None/empty values
        # Always include .none as first option
        if '.none' not in sections:
            sections.insert(0, '.none')
        elif sections[0] != '.none':
            sections.remove('.none')
            sections.insert(0, '.none')
        return sections
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error fetching sections: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        # Return default sections on error
        return ['.none', 'Telescope/Dome', 'Instruments/PFS', 'Dome/Environment']

@router.get("/sections2", response_model=List[str])
async def get_sections2(db: AsyncSession = Depends(get_db)):
    """
    Get all distinct section2 values from fault table
    Used for section2 dropdown
    """
    try:
        from app.models.fats_entry import FATSEntry
        # Get distinct section2 values from the fault table
        result = await db.execute(
            select(FATSEntry.section2)
            .distinct()
            .where(FATSEntry.section2.isnot(None))
            .where(FATSEntry.section2 != '')
            .order_by(FATSEntry.section2)
            .limit(200)  # Limit to prevent timeout
        )
        sections2 = [row[0] for row in result.all() if row[0]]  # Filter out None/empty values
        # Always include .none as first option
        if '.none' not in sections2:
            sections2.insert(0, '.none')
        elif sections2[0] != '.none':
            sections2.remove('.none')
            sections2.insert(0, '.none')
        return sections2
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error fetching sections2: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        # Return default sections2 on error
        return ['.none', 'Dome/Air Condition', 'TWS/TSC', 'Cars']

@router.get("/staff", response_model=List[str])
async def get_staff(db: AsyncSession = Depends(get_db)):
    """
    Get all staff names from fstaff table
    Used for operator dropdown
    """
    try:
        # Direct execution - SQLAlchemy handles timeouts via pool_timeout
        result = await db.execute(
            select(FStaff.name)
            .distinct()
            .order_by(FStaff.name)
            .limit(100)  # Limit to prevent timeout
        )
        staff = [row[0] for row in result.all() if row[0]]  # Filter out None/empty values
        # Always include .none as first option
        if '.none' not in staff:
            staff.insert(0, '.none')
        elif staff[0] != '.none':
            staff.remove('.none')
            staff.insert(0, '.none')
        return staff
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error fetching staff: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        # Return default staff on error
        return ['.none', 'mayank', 'letawsky', 'twin']

