"""
Database configuration and connection management
"""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from loguru import logger

from utils.config import settings
from utils.portable_paths import get_database_path


# Create async engine
engine = create_async_engine(
    f"sqlite+aiosqlite:///{get_database_path()}",
    echo=settings.DEBUG,
    future=True,
)

# Create async session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for all models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session
    
    Usage in FastAPI routes:
    @app.get("/items")
    async def get_items(db: AsyncSession = Depends(get_db)):
        ...
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Initialize database - create all tables
    """
    logger.info("Initializing database...")
    
    # Import all models to register them with Base
    from database import models  # noqa
    
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created")
    
    # Create indexes
    await _create_indexes()
    logger.info("Database initialization complete")


async def _create_indexes() -> None:
    """
    Create database indexes for performance
    """
    async with engine.begin() as conn:
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_chat_id ON messages(chat_id);
        """)
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);
        """)
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_chats_updated_at ON chats(updated_at);
        """)
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_chats_folder_id ON chats(folder_id);
        """)
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_chats_pinned ON chats(pinned);
        """)
    logger.info("Database indexes created")


async def close_db() -> None:
    """
    Close database connections
    """
    await engine.dispose()
    logger.info("Database connections closed")
