import asyncio
from app.db.session import get_db
from sqlalchemy import text

async def test():
    async for db in get_db():
        result = await db.execute(text('SELECT COUNT(*) as count FROM fault'))
        count = result.scalar()
        print(f'✅ Database connection successful!')
        print(f'   Total faults in database: {count}')
        return

asyncio.run(test())
