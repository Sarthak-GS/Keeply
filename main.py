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

from models import user, vault_entry, folder, password_reset 
from routers import auth, vault, folders, profile

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    import asyncio
    from sqlalchemy import text

    async def _warm_pool():
        try:
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info("Database connection verified.")
        except Exception as e:
            logger.error(f"Database connection failed on startup: {e}")

    asyncio.create_task(_warm_pool())
    yield


app = FastAPI(title="Keeply", version="1.0.0", docs_url="/docs", lifespan=lifespan)

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        return True
    if request.url.path.startswith("/api/") or request.url.path in ("/token", "/reset-password"):
        return True
    if "authorization" in request.headers:
        return True
    return False


# ── Error Handlers ────────────────────────────────────────────────────────────

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle all HTTPExceptions — return JSON for API, HTML for browser."""
    if exc.status_code == 401 and not _wants_json(request):
        return RedirectResponse(url="/login", status_code=302)

    if _wants_json(request):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    error_info = {
        400: ("", "Bad Request", exc.detail or "The request was invalid."),
        403: ("", "Forbidden", exc.detail or "You don't have permission to access this."),
        404: ("", "Not Found", exc.detail or "This page doesn't exist or has been moved."),
        422: ("", "Validation Error", exc.detail or "The submitted data is invalid."),
        500: ("", "Server Error", exc.detail or "Something went wrong on our end."),
        503: ("", "Service Unavailable", exc.detail or "The service is temporarily unavailable."),
    }
    icon, title, message = error_info.get(
        exc.status_code,
        ("", "Error", exc.detail or "An unexpected error occurred."),
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
    messages = []
    for err in errors:
        loc = err.get("loc", [])
        msg = err.get("msg", "invalid")
        # Clean up default Pydantic prefix "Value error, "
        if msg.startswith("Value error, "):
            msg = msg.replace("Value error, ", "", 1)
        
        # Clean up field location representation by filtering out technical loc keywords
        fields = [str(x) for x in loc if x not in ("body", "__root__")]
        if fields:
            field_name = " ".join(fields).replace("_", " ").title()
            messages.append(f"{field_name}: {msg}")
        else:
            messages.append(msg)
            
    detail = "; ".join(messages)

    if _wants_json(request):
        from fastapi.encoders import jsonable_encoder
        return JSONResponse(
            status_code=422,
            content={"detail": detail, "errors": jsonable_encoder(errors)},
        )

    return templates.TemplateResponse(
        request,
        "errors/generic.html",
        {
            "status_code": 422,
            "icon": "",
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