from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from db.engine import engine

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False, autoflush=False
)
