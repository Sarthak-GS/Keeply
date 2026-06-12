import logging
from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from config.settings import settings
from database.session import engine, get_db
from database.base import Base

# Import all models so SQLAlchemy registers them before create_all
from models import user, vault_entry, folder  # noqa: F401
from routers import auth, vault, folders, profile

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


# ── Lifespan for Async DB Initialization ─────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        def check_and_create(sync_conn):
            from sqlalchemy import inspect
            inspector = inspect(sync_conn)
            if "users" in inspector.get_table_names():
                columns = [col["name"] for col in inspector.get_columns("users")]
                if "encrypted_dek" not in columns:
                    Base.metadata.drop_all(bind=sync_conn)
            Base.metadata.create_all(bind=sync_conn)
            
        await conn.run_sync(check_and_create)
    yield


# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="Vaultify", version="1.0.0", docs_url="/docs", lifespan=lifespan)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(vault.router)
app.include_router(folders.router)
app.include_router(profile.router)


# ── Health Endpoint ──────────────────────────────────────────────────────────
@app.get("/health")
async def health(db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        # Check database connectivity
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Database connection is down",
        )


# ── Error handlers ─────────────────────────────────────────────────────────────
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return templates.TemplateResponse(
        request, "errors/404.html", {}, status_code=404
    )


@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    return templates.TemplateResponse(
        request, "errors/500.html", {}, status_code=500
    )


# ── Auth redirect for 307 (dependency redirects) ──────────────────────────────
@app.exception_handler(307)
async def redirect_handler(request: Request, exc):
    from fastapi.responses import RedirectResponse
    location = exc.headers.get("Location", "/login") if exc.headers else "/login"
    return RedirectResponse(url=location, status_code=302)