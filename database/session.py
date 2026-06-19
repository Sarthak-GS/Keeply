from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config.settings import settings

# Supabase async engine with pooler compatibility
engine = create_async_engine(
    settings.async_database_url,
    pool_pre_ping=False,
    pool_size=5,
    max_overflow=10,
    pool_recycle=300,
    pool_timeout=10,
    connect_args={
        "ssl": "require",
        "statement_cache_size": 0,
        "command_timeout": 10,
    },
)

SessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with SessionLocal() as db:
        yield db
