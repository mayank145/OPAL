#!/usr/bin/env python3
"""
Migration script to convert all existing UTC timestamps to HST
This is a ONE-TIME migration that subtracts 10 hours from all datetime fields

IMPORTANT: This should only be run ONCE!
"""
import asyncio
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from datetime import timedelta

# Import settings
sys.path.insert(0, '/Users/mayankchoudhary/Desktop/Subaru_Telescope/OPAL/backend')
from app.core.config import settings

# HST offset
HST_OFFSET = timedelta(hours=-10)

async def migrate_timestamps():
    """
    Convert all UTC timestamps to HST by subtracting 10 hours
    """
    print("="*60)
    print("TIMEZONE MIGRATION: UTC → HST")
    print("="*60)
    print("\nThis will subtract 10 hours from ALL datetime fields")
    print("in the database to convert from UTC to HST.\n")
    
    # Create engine
    engine = create_async_engine(
        settings.async_database_url,
        echo=True
    )
    
    async_session = sessionmaker(
        engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
    
    async with async_session() as session:
        try:
            print("\n📊 Checking current data...")
            
            # Check sample data before migration
            result = await session.execute(text("""
                SELECT idno, datein, updated_at 
                FROM fault 
                WHERE datein IS NOT NULL 
                LIMIT 5
            """))
            sample_before = result.fetchall()
            
            print("\n📋 Sample BEFORE migration (first 5 entries):")
            for row in sample_before:
                print(f"  FATS {row[0]}: datein={row[1]}, updated_at={row[2]}")
            
            # Get counts
            result = await session.execute(text("SELECT COUNT(*) FROM fault WHERE datein IS NOT NULL"))
            fault_count = result.scalar()
            
            result = await session.execute(text("SELECT COUNT(*) FROM fcomments WHERE datein IS NOT NULL"))
            comment_count = result.scalar()
            
            print(f"\n📈 Records to update:")
            print(f"  - FATS entries: {fault_count}")
            print(f"  - Comments: {comment_count}")
            
            # Confirm before proceeding
            print("\n⚠️  WARNING: This operation will modify the database!")
            response = input("\nProceed with migration? (yes/no): ")
            
            if response.lower() != 'yes':
                print("\n❌ Migration cancelled.")
                return
            
            print("\n🔄 Starting migration...")
            
            # Update fault table - datein (skip invalid '0000-00-00 00:00:00' dates)
            print("\n1️⃣ Updating fault.datein...")
            result = await session.execute(text("""
                UPDATE fault 
                SET datein = DATE_SUB(datein, INTERVAL 10 HOUR)
                WHERE datein IS NOT NULL 
                AND datein != '0000-00-00 00:00:00'
                AND datein > '1970-01-01 00:00:00'
            """))
            await session.commit()
            print(f"   ✓ Updated {result.rowcount} records")
            
            # Update fault table - updated_at (skip invalid dates)
            print("\n2️⃣ Updating fault.updated_at...")
            result = await session.execute(text("""
                UPDATE fault 
                SET updated_at = DATE_SUB(updated_at, INTERVAL 10 HOUR)
                WHERE updated_at IS NOT NULL 
                AND updated_at != '0000-00-00 00:00:00'
                AND updated_at > '1970-01-01 00:00:00'
            """))
            await session.commit()
            print(f"   ✓ Updated {result.rowcount} records")
            
            # Update fault table - resolved_at (skip invalid dates)
            print("\n3️⃣ Updating fault.resolved_at...")
            result = await session.execute(text("""
                UPDATE fault 
                SET resolved_at = DATE_SUB(resolved_at, INTERVAL 10 HOUR)
                WHERE resolved_at IS NOT NULL 
                AND resolved_at != '0000-00-00 00:00:00'
                AND resolved_at > '1970-01-01 00:00:00'
            """))
            await session.commit()
            print(f"   ✓ Updated {result.rowcount} records")
            
            # Update fcomments table (skip invalid dates)
            print("\n4️⃣ Updating fcomments.datein...")
            result = await session.execute(text("""
                UPDATE fcomments 
                SET datein = DATE_SUB(datein, INTERVAL 10 HOUR)
                WHERE datein IS NOT NULL 
                AND datein != '0000-00-00 00:00:00'
                AND datein > '1970-01-01 00:00:00'
            """))
            await session.commit()
            print(f"   ✓ Updated {result.rowcount} records")
            
            # Check if fats_images table exists and update if it does
            print("\n5️⃣ Checking for fats_images table...")
            result = await session.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = DATABASE() 
                AND table_name = 'fats_images'
            """))
            table_exists = result.scalar()
            
            if table_exists:
                print("   Table exists, updating uploaded_at...")
                result = await session.execute(text("""
                    UPDATE fats_images 
                    SET uploaded_at = DATE_SUB(uploaded_at, INTERVAL 10 HOUR)
                    WHERE uploaded_at IS NOT NULL 
                    AND uploaded_at != '0000-00-00 00:00:00'
                    AND uploaded_at > '1970-01-01 00:00:00'
                """))
                await session.commit()
                print(f"   ✓ Updated {result.rowcount} records")
            else:
                print("   ⊘ Table does not exist, skipping")
            
            # Verify migration
            print("\n✅ Verifying migration...")
            result = await session.execute(text("""
                SELECT idno, datein, updated_at 
                FROM fault 
                WHERE datein IS NOT NULL 
                LIMIT 5
            """))
            sample_after = result.fetchall()
            
            print("\n📋 Sample AFTER migration (first 5 entries):")
            for row in sample_after:
                print(f"  FATS {row[0]}: datein={row[1]}, updated_at={row[2]}")
            
            print("\n" + "="*60)
            print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
            print("="*60)
            print("\nAll timestamps have been converted from UTC to HST.")
            print("The difference should be approximately 10 hours earlier.\n")
            
        except Exception as e:
            print(f"\n❌ ERROR during migration: {e}")
            await session.rollback()
            raise
        finally:
            await engine.dispose()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("UTC to HST Timezone Migration Script")
    print("="*60)
    asyncio.run(migrate_timestamps())
