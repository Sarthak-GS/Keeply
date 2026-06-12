from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config.settings import settings

url = settings.DATABASE_URL
if url.startswith("sqlite://"):
    url = url.replace("sqlite://", "sqlite+aiosqlite://")

connect_args = {}
if "sqlite" in url:
    connect_args = {"check_same_thread": False}

engine = create_async_engine(url, connect_args=connect_args)
SessionLocal = async_sessionmaker(bind=engine, autoflush=False, autocommit=False)


async def get_db():
    """FastAPI async dependency that yields a DB session per request."""
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
