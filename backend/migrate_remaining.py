#!/usr/bin/env python3
"""
Continue HST migration - Update remaining fields
(fault.datein was already updated successfully)
"""
import asyncio
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

sys.path.insert(0, '/Users/mayankchoudhary/Desktop/Subaru_Telescope/OPAL/backend')
from app.core.config import settings

async def migrate_remaining():
    print("="*60)
    print("Continuing HST Migration - Remaining Fields")
    print("="*60)
    
    engine = create_async_engine(settings.async_database_url, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        try:
            # Update fault table - updated_at
            print("\n1️⃣ Updating fault.updated_at...")
            result = await session.execute(text("""
                UPDATE fault 
                SET updated_at = DATE_SUB(updated_at, INTERVAL 10 HOUR)
                WHERE updated_at IS NOT NULL 
                AND updated_at > '1970-01-01 00:00:00'
            """))
            await session.commit()
            print(f"   ✓ Updated {result.rowcount} records")
            
            # Update fault table - resolved_at
            print("\n2️⃣ Updating fault.resolved_at...")
            result = await session.execute(text("""
                UPDATE fault 
                SET resolved_at = DATE_SUB(resolved_at, INTERVAL 10 HOUR)
                WHERE resolved_at IS NOT NULL 
                AND resolved_at > '1970-01-01 00:00:00'
            """))
            await session.commit()
            print(f"   ✓ Updated {result.rowcount} records")
            
            # Update fcomments table
            print("\n3️⃣ Updating fcomments.datein...")
            result = await session.execute(text("""
                UPDATE fcomments 
                SET datein = DATE_SUB(datein, INTERVAL 10 HOUR)
                WHERE datein IS NOT NULL 
                AND datein != '0000-00-00 00:00:00'
                AND datein > '1970-01-01 00:00:00'
            """))
            await session.commit()
            print(f"   ✓ Updated {result.rowcount} records")
            
            # Check if fats_images table exists
            print("\n4️⃣ Checking for fats_images table...")
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
                    AND uploaded_at > '1970-01-01 00:00:00'
                """))
                await session.commit()
                print(f"   ✓ Updated {result.rowcount} records")
            else:
                print("   ⊘ Table does not exist, skipping")
            
            print("\n" + "="*60)
            print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
            print("="*60)
            print("\nAll timestamps have been converted to HST.\n")
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            await session.rollback()
            raise
        finally:
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(migrate_remaining())
