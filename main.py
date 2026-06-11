import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware

from config.settings import settings
from database.session import engine
from database.base import Base

# Import all models so SQLAlchemy registers them before create_all
from models import user, vault_entry, folder  # noqa: F401
from routers import auth, vault, folders, profile

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# ── Create all DB tables on startup ───────────────────────────────────────────
from sqlalchemy import inspect
inspector = inspect(engine)
if "users" in inspector.get_table_names():
    columns = [col["name"] for col in inspector.get_columns("users")]
    if "encrypted_dek" not in columns:
        logger.info("Outdated schema detected. Recreating database tables...")
        Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="Vaultify", version="1.0.0", docs_url="/docs")

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(vault.router)
app.include_router(folders.router)
app.include_router(profile.router)


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