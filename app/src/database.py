from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from fastapi import HTTPException
from sqlalchemy.future import select
from src.models import Base
import os

engine = create_async_engine(os.getenv("POSTGRES_URL"))

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def init():
    await create_tables()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def db_get():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def query(session: AsyncSession, model, filter: list = [], noexception: bool = False, user: bool = False):
    query = select(model).filter(*filter)
    get_result = await session.execute(query)
    result = get_result.scalars().first()
        
    if not result and not noexception:
        if not user:
            raise HTTPException(status_code=204)  
        else:
            raise HTTPException(status_code=401)
    
    return result

async def query_bulk(session: AsyncSession, model, filter = [], order = None, offset: int = None, limit: int = None, noexception: bool = False):
    query = select(model).filter(*filter).order_by(order).limit(limit).offset(offset)
    get_result = await session.execute(query)
    result = get_result.scalars().all()       
    
    if not result and not noexception:
        return []
    
    return result