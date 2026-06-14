import logging
from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from config.settings import settings
from database.session import engine, get_db
from database.base import Base

# Import all models so SQLAlchemy registers them before create_all
from models import user, vault_entry, folder, password_reset  # noqa: F401
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
            tables = inspector.get_table_names()

            if "users" in tables:
                columns = [col["name"] for col in inspector.get_columns("users")]
                # If deprecated columns exist, recreate database for a clean start
                if "encrypted_dek" in columns or "server_encrypted_dek" in columns:
                    Base.metadata.drop_all(bind=sync_conn)

            Base.metadata.create_all(bind=sync_conn)

        await conn.run_sync(check_and_create)
    yield


# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="Vaultify", version="1.0.0", docs_url="/docs", lifespan=lifespan)

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
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Database connection is down")
# ── Helper: detect if request expects JSON or HTML ────────────────────────────
def _wants_json(request: Request) -> bool:
    accept = request.headers.get("accept", "")
    if "application/json" in accept:
        return True
    if request.url.path.startswith("/api/") or request.url.path == "/token":
        return True
    if "authorization" in request.headers:
        return True
    return False


# ── Error Handlers ────────────────────────────────────────────────────────────

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle all HTTPExceptions — return JSON for API, HTML for browser."""
    # For 401 on browser requests → redirect to login
    if exc.status_code == 401 and not _wants_json(request):
        return RedirectResponse(url="/login", status_code=302)

    # For API/fetch requests → return JSON
    if _wants_json(request):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    # For browser requests → render a styled error page
    error_info = {
        400: ("⚠️", "Bad Request", exc.detail or "The request was invalid."),
        403: ("🚫", "Forbidden", exc.detail or "You don't have permission to access this."),
        404: ("🔍", "Not Found", exc.detail or "This page doesn't exist or has been moved."),
        422: ("📝", "Validation Error", exc.detail or "The submitted data is invalid."),
        500: ("💥", "Server Error", exc.detail or "Something went wrong on our end."),
        503: ("🔧", "Service Unavailable", exc.detail or "The service is temporarily unavailable."),
    }
    icon, title, message = error_info.get(
        exc.status_code,
        ("❌", "Error", exc.detail or "An unexpected error occurred."),
    )
    return templates.TemplateResponse(
        request,
        "errors/generic.html",
        {
            "status_code": exc.status_code,
            "icon": icon,
            "title": title,
            "message": message,
        },
        status_code=exc.status_code,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle pydantic/FastAPI validation errors gracefully."""
    errors = exc.errors()
    # Build a human-readable summary
    messages = []
    for err in errors:
        field = " → ".join(str(loc) for loc in err.get("loc", []))
        messages.append(f"{field}: {err.get('msg', 'invalid')}")
    detail = "; ".join(messages)

    if _wants_json(request):
        return JSONResponse(
            status_code=422,
            content={"detail": detail, "errors": errors},
        )

    return templates.TemplateResponse(
        request,
        "errors/generic.html",
        {
            "status_code": 422,
            "icon": "📝",
            "title": "Validation Error",
            "message": detail,
        },
        status_code=422,
    )


@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    return templates.TemplateResponse(
        request, "errors/500.html", {}, status_code=500
    )