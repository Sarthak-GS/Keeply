# 🔐 Vaultify — Password Manager: Complete Learning Guide
### A Beginner-Friendly, Implementation-Oriented Roadmap for FastAPI + PostgreSQL + Jinja2

> **Project Name:** Vaultify  
> **Stack:** FastAPI · Jinja2 · TailwindCSS · PostgreSQL · SQLAlchemy · JWT  
> **Goal:** Build a real, secure password manager while learning full-stack web development properly  
> **Audience:** First-time serious backend/full-stack developer  

---

## 📋 Table of Contents

1. [Project Goal](#1-project-goal)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Project Structure](#3-project-structure)
4. [Implementation Roadmap](#4-implementation-roadmap)
5. [Core Features](#5-core-features)
6. [Database Design](#6-database-design)
7. [API Design](#7-api-design)
8. [JWT Authentication](#8-jwt-authentication)
9. [Password Storage](#9-password-storage)
10. [Frontend Design](#10-frontend-design)
11. [Docker & Deployment](#11-docker--deployment)
12. [Testing & Debugging](#12-testing--debugging)
13. [Future Improvements](#13-future-improvements)
14. [Learning Guidance](#14-learning-guidance)
15. [Final Deliverable](#15-final-deliverable)

---

## 1. Project Goal

### 🎯 What Is a Password Manager?

A password manager is a secure application that stores and organizes your passwords (and other sensitive credentials) in one place, protected by a single "master password". Think of it like a locked safe where you store all your keys.

### 🏗️ Core Components of Any Password Manager

| Component | What It Does |
|---|---|
| **Authentication System** | Lets users register, log in, and log out securely |
| **Vault** | The secure container where passwords/entries live |
| **Encryption Layer** | Protects stored passwords so even the server can't read them in plain text |
| **CRUD Interface** | Create, Read, Update, Delete vault entries |
| **Password Generator** | Generates strong, random passwords |
| **Organization System** | Folders, tags, or categories to organize entries |
| **Search** | Quickly find entries |
| **UI/UX** | A clean, usable interface |

### ✅ Minimum Features (Must-Have for v1.0)

These are the features that make it a functional password manager:

1. **User Registration & Login** — Without this, nothing works
2. **JWT-based Session Management** — Keep users logged in securely
3. **Create/Read/Update/Delete Vault Entries** — The core purpose
4. **Password Hashing** — Never store master passwords in plain text
5. **Basic Vault Entry Encryption** — Protect stored site passwords
6. **Logout** — Properly invalidate sessions
7. **Simple Dashboard** — See all your stored entries
8. **Add/Edit/Delete Entry Form** — Title, username, password, URL, notes
9. **Copy Password Button** — Quick usability feature

### 🟡 Optional Features (Nice to Have in v1.5)

These add value but aren't critical for a first working version:

- Folder/category organization for vault entries
- Password strength generator
- Search and filter entries
- Favorite/starred entries
- Password visibility toggle
- Flash messages (success/error notifications)
- Profile page with password change option
- Entry notes field

### 🚫 What to Avoid Initially (Don't Overcomplicate)

As a beginner, resist the urge to add:

- **Two-Factor Authentication (2FA)** — Complex, save for later
- **Password Sharing** — Requires complex key exchange
- **Browser Extension** — Completely separate project
- **WebSockets / Real-time features** — Overkill for v1
- **Role-Based Access Control (RBAC)** — Not needed for single-user vault
- **Redis caching** — Premature optimization
- **Async database (asyncpg)** — Learn sync first, async later
- **Microservices** — Way too complex for a first project
- **Email verification** — Optional, adds complexity

> **Beginner Tip 💡:** Every feature you add before your core is working is technical debt. Finish a working core first, then expand. This is called "iterative development" and it's how real teams work.

### 📏 Realistic Scope for a First Project

**v1.0 (Your Goal):** A working web app where you can:
- Register an account
- Log in and get a JWT session
- Add, view, edit, delete passwords
- Copy a password to clipboard
- Log out

**Timeline Estimate:** 4–8 weeks (building properly, learning along the way)

---

## 2. High-Level Architecture

### 🗺️ The Big Picture (Simplified)

```
User's Browser
     │
     │  HTTP Request (GET /dashboard)
     ▼
┌─────────────────────┐
│      FastAPI         │  ← Your Python backend server
│   (main.py +         │
│    routers/)         │
└─────────┬───────────┘
          │
          │  SQLAlchemy ORM query
          ▼
┌─────────────────────┐
│    PostgreSQL DB     │  ← Your persistent data store
│  (users, passwords)  │
└─────────┬───────────┘
          │
          │  Returns data (Python objects)
          ▼
┌─────────────────────┐
│   Jinja2 Templates  │  ← HTML templating engine
│   (dashboard.html)  │
└─────────┬───────────┘
          │
          │  Rendered HTML response
          ▼
     Browser renders the page
```

### 🔧 Role of Each Technology

#### FastAPI — The Backend Brain

FastAPI is a **modern Python web framework** that handles:
- Receiving HTTP requests (GET, POST, PUT, DELETE)
- Routing requests to the right function
- Validating request data using Pydantic
- Interacting with the database via SQLAlchemy
- Returning responses (HTML via Jinja2, or JSON for API calls)

**Why FastAPI over Flask/Django?**
- Automatic API docs at `/docs` — extremely useful for learning and testing
- Built-in data validation via Pydantic
- Modern Python (type hints, async support)
- Much faster than Flask, much simpler than Django for beginners
- Great documentation

```python
# Example: A simple FastAPI route
@app.get("/dashboard")
def dashboard(request: Request, current_user: User = Depends(get_current_user)):
    entries = db.query(VaultEntry).filter(VaultEntry.user_id == current_user.id).all()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "entries": entries,
        "user": current_user
    })
```

#### Jinja2 — The HTML Templating Engine

Jinja2 lets you write **dynamic HTML**. Instead of serving static HTML files, you can inject Python variables directly into your HTML:

```html
<!-- templates/dashboard.html -->
<h1>Welcome, {{ user.username }}!</h1>
<p>You have {{ entries|length }} saved passwords.</p>

{% for entry in entries %}
  <div class="entry-card">
    <h3>{{ entry.title }}</h3>
    <p>{{ entry.username }}</p>
  </div>
{% endfor %}
```

**Why Jinja2?** It comes built-in with FastAPI's template support. It's the same templating engine used by Flask and Django, so learning it is transferable. It keeps your HTML separate from your Python logic (good practice!).

#### TailwindCSS — The Styling System

TailwindCSS is a **utility-first CSS framework**. Instead of writing custom CSS classes, you apply pre-built utility classes directly in your HTML:

```html
<!-- WITHOUT Tailwind (custom CSS needed) -->
<button class="submit-button">Login</button>

<!-- WITH Tailwind (styles applied directly) -->
<button class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition">
  Login
</button>
```

**Why Tailwind?** Rapid development, consistent design, no need to switch between HTML and CSS files constantly. The class names are self-documenting.

**Setup for Jinja2 Projects:** Use the CDN link (simple) or Tailwind CLI (proper). We'll use CLI for proper setup.

#### PostgreSQL — The Database

PostgreSQL is a powerful, open-source relational database. It stores your data in **tables** (like spreadsheets) with **relationships** between them.

- `users` table — stores user accounts
- `vault_entries` table — stores saved passwords, linked to users
- `folders` table — organizes entries into categories

**Why PostgreSQL over SQLite?**
- Production-ready (used by major companies)
- Handles concurrent users properly
- Works great with Docker for deployment
- SQLite is fine for learning but not for production

#### SQLAlchemy — The ORM (Object-Relational Mapper)

SQLAlchemy lets you interact with the database using Python objects instead of raw SQL:

```python
# Without ORM (raw SQL - error-prone)
cursor.execute("SELECT * FROM vault_entries WHERE user_id = %s", (user_id,))

# With SQLAlchemy ORM (Pythonic, safe)
entries = db.query(VaultEntry).filter(VaultEntry.user_id == user_id).all()
```

**Why SQLAlchemy?** It prevents SQL injection, makes code cleaner, handles database connections properly, and generates migrations.

#### JWT — JSON Web Tokens (Authentication)

JWT is a way to prove "who you are" to the server on every request, without the server needing to store session data.

```
Login → Server creates JWT token → Sends to browser (cookie)
Every request → Browser sends cookie → Server verifies token → Allows access
```

Think of JWT like a **stamped wristband at a concert**. Once stamped, you can re-enter freely without re-buying a ticket.

### 🔄 Complete Request Lifecycle

Here's exactly what happens when you go to `/dashboard`:

```
Step 1: Browser sends GET /dashboard
        (includes JWT cookie in headers)
        
Step 2: FastAPI receives request
        → Middleware checks for JWT cookie
        → Decodes and validates the token
        → Extracts user_id from token
        
Step 3: Route function runs
        → Calls get_current_user(token) → returns User object
        → Queries database: SELECT * FROM vault_entries WHERE user_id = ?
        → SQLAlchemy returns list of VaultEntry Python objects
        
Step 4: Jinja2 renders template
        → Injects user object and entries list into dashboard.html
        → Produces complete HTML string
        
Step 5: FastAPI returns HTML response
        → Browser receives and renders the page
        → User sees their dashboard
```

---

---

## 3. Project Structure

### 📁 The Final Folder Layout

```
vaultify/
│
├── main.py                    # App entry point — creates FastAPI app, includes routers
├── requirements.txt           # All Python dependencies
├── .env                       # Secret keys, DB URL (NEVER commit to git)
├── .env.example               # Template showing what .env needs (safe to commit)
├── .gitignore                 # Files git should ignore (.env, __pycache__, etc.)
│
├── config/
│   └── settings.py            # Loads .env variables using pydantic-settings
│
├── database/
│   ├── __init__.py
│   ├── base.py                # SQLAlchemy Base class (all models inherit from this)
│   └── session.py             # DB engine, SessionLocal, get_db() dependency
│
├── models/
│   ├── __init__.py
│   ├── user.py                # User SQLAlchemy model (maps to 'users' table)
│   ├── vault_entry.py         # VaultEntry model (maps to 'vault_entries' table)
│   └── folder.py              # Folder model (maps to 'folders' table)
│
├── schemas/
│   ├── __init__.py
│   ├── user.py                # Pydantic schemas for user (UserCreate, UserResponse)
│   ├── vault_entry.py         # Pydantic schemas for vault entries
│   └── folder.py              # Pydantic schemas for folders
│
├── routers/
│   ├── __init__.py
│   ├── auth.py                # /login, /signup, /logout routes
│   ├── vault.py               # /vault CRUD routes
│   ├── folders.py             # /folders CRUD routes
│   └── profile.py             # /profile routes
│
├── services/
│   ├── __init__.py
│   ├── auth_service.py        # Business logic: create_user, authenticate_user
│   ├── vault_service.py       # Business logic: create_entry, get_entries, etc.
│   └── folder_service.py      # Business logic: folder operations
│
├── auth/
│   ├── __init__.py
│   ├── jwt_handler.py         # create_token(), decode_token() functions
│   ├── hashing.py             # hash_password(), verify_password() using bcrypt
│   └── dependencies.py        # get_current_user() FastAPI dependency
│
├── utils/
│   ├── __init__.py
│   ├── encryption.py          # Fernet encrypt/decrypt for vault passwords
│   └── password_generator.py  # Random password generation logic
│
├── templates/
│   ├── base.html              # Base template with navbar, head tags (all pages extend this)
│   ├── auth/
│   │   ├── login.html
│   │   └── signup.html
│   ├── vault/
│   │   ├── dashboard.html     # Main vault view (list of entries)
│   │   ├── entry_form.html    # Add/Edit entry form
│   │   └── entry_detail.html  # View single entry detail
│   ├── folders/
│   │   └── folders.html
│   ├── profile/
│   │   └── profile.html
│   └── errors/
│       ├── 404.html
│       └── 500.html
│
└── static/
    ├── css/
    │   └── output.css         # Compiled Tailwind CSS (generated by Tailwind CLI)
    ├── js/
    │   └── main.js            # Frontend JavaScript (copy-to-clipboard, toggles, etc.)
    └── images/
        └── logo.svg           # App logo
```

### 📂 Folder-by-Folder Explanation

#### `main.py` — The Entry Point

This is where your FastAPI `app` object lives. It's kept **thin** — it just creates the app and connects the routers. All real logic goes elsewhere.

```python
# main.py — keep this minimal
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import auth, vault, folders, profile
from database.session import engine
from database.base import Base

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vaultify", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers with prefixes
app.include_router(auth.router)
app.include_router(vault.router, prefix="/vault")
app.include_router(folders.router, prefix="/folders")
app.include_router(profile.router, prefix="/profile")
```

#### `config/settings.py` — Configuration

Never hardcode secrets in your code. Use environment variables loaded from a `.env` file:

```python
# config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/vaultify"
    SECRET_KEY: str = "your-super-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENCRYPTION_KEY: str = "your-32-byte-fernet-key-here"

    class Config:
        env_file = ".env"

settings = Settings()
```

```bash
# .env file (NEVER commit this to git!)
DATABASE_URL=postgresql://vaultify_user:mypassword@localhost:5432/vaultify_db
SECRET_KEY=super-long-random-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ENCRYPTION_KEY=your-fernet-key-here
```

#### `database/` — Database Setup

Two files handle all database setup:

```python
# database/base.py — The SQLAlchemy declarative base
from sqlalchemy.orm import declarative_base
Base = declarative_base()
# All your models will inherit from this Base
```

```python
# database/session.py — DB connection and session management
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """FastAPI dependency that provides a DB session per request."""
    db = SessionLocal()
    try:
        yield db          # Give the session to the route function
    finally:
        db.close()        # Always close after request, even if error occurs
```

> **Why `yield` in `get_db()`?** This is a FastAPI "dependency with cleanup". The `yield` gives the DB session to your route, and the code after `finally` runs when the request is done — guaranteeing the connection is closed. This prevents connection leaks.

#### `models/` — Database Tables as Python Classes

Each model = one database table. SQLAlchemy handles the SQL for you.

```python
# models/user.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship — lets you do user.vault_entries to get all entries
    vault_entries = relationship("VaultEntry", back_populates="owner", cascade="all, delete-orphan")
    folders = relationship("Folder", back_populates="owner", cascade="all, delete-orphan")
```

#### `schemas/` — Request/Response Validation (Pydantic)

Schemas validate incoming data and shape outgoing data. They are **NOT** database models:

```python
# schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    """What we expect when someone registers."""
    username: str
    email: EmailStr       # Validates email format automatically!
    password: str

class UserResponse(BaseModel):
    """What we send back — note: NO password field!"""
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True  # Allows reading from SQLAlchemy objects
```

> **Key distinction:** `models/` = what's in the DATABASE. `schemas/` = what goes IN and OUT of your API. Never expose database models directly!

#### `routers/` — URL Route Handlers

Each router handles one area of functionality. A router is like a mini-app:

```python
# routers/auth.py
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database.session import get_db
from services import auth_service

router = APIRouter(tags=["Authentication"])

@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@router.post("/login")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    # ... create token and set cookie
```

#### `services/` — Business Logic Layer

Services contain the **actual logic** — your routes just coordinate, services do the work:

```python
# services/auth_service.py
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from auth.hashing import hash_password, verify_password

def create_user(db: Session, user_data: UserCreate) -> User:
    """Create a new user in the database."""
    hashed_pw = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Refresh to get the auto-generated ID
    return new_user

def authenticate_user(db: Session, email: str, password: str):
    """Verify login credentials."""
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
```

> **Why separate services from routers?** If your logic is in routes, you can't reuse it. If it's in services, both your web routes AND your API endpoints can call the same function. This is the **separation of concerns** principle.

#### `auth/` — Authentication Utilities

```python
# auth/hashing.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed: str) -> bool:
    return pwd_context.verify(plain_password, hashed)
```

```python
# auth/jwt_handler.py
from jose import JWTError, jwt
from datetime import datetime, timedelta
from config.settings import settings

def create_access_token(data: dict) -> str:
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
```

#### Common Beginner Mistakes to Avoid

| ❌ Mistake | ✅ Correct Approach |
|---|---|
| Putting all code in `main.py` | Split into routers, services, models |
| Storing passwords in plain text | Always hash with bcrypt |
| Committing `.env` to git | Add `.env` to `.gitignore` immediately |
| Using `SELECT *` everywhere | Only query what you need |
| Not closing DB connections | Always use `get_db()` dependency with yield |
| Hardcoding secret keys | Use environment variables |
| Mixing business logic in routes | Keep routes thin, logic in services |
| Not using Pydantic schemas | Always validate input with schemas |

---

## 4. Implementation Roadmap

> **Philosophy:** Build a working slice end-to-end before moving to the next phase. A fully working Phase 1 is better than 50% of Phase 3.

---

### 🟢 Phase 1: Foundation (Week 1)
**Goal:** Get a running FastAPI app that serves HTML pages with Tailwind styling.

**Concepts Learned:**
- How FastAPI starts and handles requests
- How Jinja2 template rendering works
- How to serve static files (CSS, JS, images)
- How TailwindCSS utility classes work
- Project structure and organization

**Files to Create:**
```
main.py                      (update existing)
config/settings.py
database/base.py
database/session.py
templates/base.html
templates/auth/login.html
templates/auth/signup.html
static/css/                  (output.css from Tailwind)
static/js/main.js
requirements.txt
.env + .env.example
.gitignore
```

**Step-by-Step:**
1. Set up virtual environment: `python -m venv venv && source venv/bin/activate`
2. Install dependencies: `pip install "fastapi[standard]" jinja2 python-multipart`
3. Create the folder structure
4. Set up TailwindCSS CLI: download `tailwindcss` binary, run `npx tailwindcss init`
5. Configure `tailwind.config.js` to scan your templates
6. Create `base.html` with navbar, head, and block structure
7. Create basic login and signup HTML pages
8. Create routes in `main.py` that serve these pages
9. Run: `fastapi dev main.py` and verify pages load

**Milestone:** You can visit `localhost:8000`, see a styled login page, and navigate between pages.

**Tailwind Setup Commands:**
```bash
# Install Tailwind CLI (no Node required for standalone binary)
# Or use CDN for development speed:
# In base.html <head>:
# <script src="https://cdn.tailwindcss.com"></script>

# For proper setup:
npm init -y
npm install -D tailwindcss
npx tailwindcss init

# tailwind.config.js
module.exports = {
  content: ["./templates/**/*.html", "./static/js/**/*.js"],
  theme: { extend: {} },
  plugins: [],
}

# Run Tailwind watcher (keep this running while developing)
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
```

---

### 🟡 Phase 2: User Authentication (Week 2)
**Goal:** Users can register, log in, and log out. JWT tokens are issued and verified.

**Concepts Learned:**
- bcrypt password hashing
- How JWT tokens are created and verified
- HTTP cookies for storing tokens securely
- FastAPI dependencies (`Depends()`)
- Form handling in FastAPI
- Pydantic validation
- SQLAlchemy model definition and table creation

**Files to Create:**
```
models/user.py
schemas/user.py
auth/hashing.py
auth/jwt_handler.py
auth/dependencies.py
services/auth_service.py
routers/auth.py
```

**Step-by-Step:**
1. Install auth packages: `pip install passlib[bcrypt] python-jose[cryptography] pydantic-settings`
2. Create the `User` SQLAlchemy model
3. Create Pydantic schemas for `UserCreate` and `UserResponse`
4. Implement `hash_password()` and `verify_password()`
5. Implement `create_access_token()` and `decode_token()`
6. Implement `get_current_user()` dependency that reads JWT from cookie
7. Create auth routes: `GET /login`, `POST /login`, `GET /signup`, `POST /signup`, `GET /logout`
8. Test registration: submit form → user appears in DB
9. Test login: submit form → JWT cookie set → redirect to dashboard

**Key Code Concept — Cookie-based JWT:**
```python
# After successful login, set JWT as HTTP-only cookie
response = RedirectResponse(url="/vault/dashboard", status_code=302)
response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,    # JavaScript cannot read this cookie (XSS protection)
    secure=False,     # Set True in production (requires HTTPS)
    samesite="lax",   # CSRF protection
    max_age=3600      # Cookie expires in 1 hour
)
return response
```

**Milestone:** You can register a new user, log in, and see "Welcome, username!" on a protected dashboard. Accessing `/vault/dashboard` without login redirects to `/login`.

---

### 🟠 Phase 3: Database Integration (Week 2-3)
**Goal:** Properly connect to PostgreSQL, run migrations, store and retrieve real data.

**Concepts Learned:**
- PostgreSQL setup and connection strings
- SQLAlchemy engine and session management
- `get_db()` dependency injection pattern
- How ORM queries work (filter, first, all, add, commit)
- Alembic for database migrations

**Files to Create/Update:**
```
database/session.py          (update with real DB URL)
models/vault_entry.py        (create)
models/folder.py             (create)
alembic/                     (migration directory)
alembic.ini
```

**PostgreSQL Setup:**
```bash
# Install PostgreSQL on Ubuntu/Linux
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE USER vaultify_user WITH PASSWORD 'yourpassword';
CREATE DATABASE vaultify_db OWNER vaultify_user;
GRANT ALL PRIVILEGES ON DATABASE vaultify_db TO vaultify_user;
\q

# Update .env
DATABASE_URL=postgresql://vaultify_user:yourpassword@localhost:5432/vaultify_db
```

**Alembic Setup (Database Migrations):**
```bash
pip install alembic
alembic init alembic

# Edit alembic/env.py to use your models and settings
# Then create your first migration:
alembic revision --autogenerate -m "create users table"
alembic upgrade head   # Apply migration to DB
```

**Why Alembic?** Without it, you'd manually write SQL `ALTER TABLE` statements every time you change a model. Alembic detects changes and generates migration scripts automatically.

**Milestone:** PostgreSQL is running, tables exist, and users are actually saved to the database.

---

### 🔵 Phase 4: Vault CRUD Operations (Week 3-4)
**Goal:** Core password manager functionality — create, view, edit, delete vault entries.

**Concepts Learned:**
- Full CRUD with SQLAlchemy
- Protecting routes with `get_current_user` dependency
- Fernet symmetric encryption for vault passwords
- Form handling with POST requests
- Redirect-After-Post pattern (prevents form resubmission)

**Files to Create:**
```
models/vault_entry.py
schemas/vault_entry.py
services/vault_service.py
routers/vault.py
utils/encryption.py
templates/vault/dashboard.html
templates/vault/entry_form.html
templates/vault/entry_detail.html
```

**Fernet Encryption for Vault Passwords:**
```bash
pip install cryptography

# Generate a key (run once, save to .env)
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

```python
# utils/encryption.py
from cryptography.fernet import Fernet
from config.settings import settings

fernet = Fernet(settings.ENCRYPTION_KEY.encode())

def encrypt_password(plain: str) -> str:
    return fernet.encrypt(plain.encode()).decode()

def decrypt_password(encrypted: str) -> str:
    return fernet.decrypt(encrypted.encode()).decode()
```

**Step-by-Step:**
1. Create `VaultEntry` model and migration
2. Create CRUD service functions: `create_entry()`, `get_all_entries()`, `get_entry_by_id()`, `update_entry()`, `delete_entry()`
3. Create vault routes: `GET /vault/dashboard`, `GET /vault/new`, `POST /vault/new`, `GET /vault/{id}`, `GET /vault/{id}/edit`, `POST /vault/{id}/edit`, `POST /vault/{id}/delete`
4. Create dashboard template showing all entries as cards
5. Create add/edit form template
6. Test full CRUD flow

**Milestone:** You can add a password entry, see it on the dashboard, click it to view details, edit it, and delete it. Passwords are stored encrypted in the DB.

---

### 🟣 Phase 5: UX Features (Week 4-5)
**Goal:** Add features that make the app actually pleasant to use.

**Features to Add:**
- Password generator (backend API endpoint + frontend JS)
- Copy-to-clipboard button (pure JavaScript)
- Search/filter entries (query parameter filtering)
- Favorite/star entries (boolean field on model)
- Folder/category organization
- Flash messages (success/error feedback)
- Password visibility toggle

**Files to Create:**
```
utils/password_generator.py
routers/folders.py
services/folder_service.py
templates/folders/folders.html
models/folder.py
schemas/folder.py
```

**Copy-to-Clipboard (Pure JS, No Backend Needed):**
```javascript
// static/js/main.js
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showFlash("Password copied!", "success");
    });
}

function showFlash(message, type) {
    const flash = document.getElementById("flash-message");
    flash.textContent = message;
    flash.className = `flash flash-${type} show`;
    setTimeout(() => flash.classList.remove("show"), 3000);
}
```

**Password Generator Route:**
```python
# routers/vault.py
@router.get("/generate-password")
def generate_password(length: int = 16, use_symbols: bool = True):
    """Returns a JSON response with a generated password."""
    password = generate_strong_password(length, use_symbols)
    return {"password": password}  # JavaScript fetches this
```

**Flash Messages with Jinja2 + Starlette Sessions:**
```bash
pip install itsdangerous  # Required for session middleware
```

```python
# main.py
from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# In a route:
request.session["flash"] = {"message": "Entry saved!", "type": "success"}

# In base.html:
{% if request.session.get("flash") %}
  <div class="alert alert-{{ request.session.flash.type }}">
    {{ request.session.flash.message }}
  </div>
{% endif %}
```

**Milestone:** App feels complete and polished. Users can generate passwords, copy them, search entries, organize with folders, and see success/error messages.

---

### ⚫ Phase 6: Polish, Profile, and Security Hardening (Week 5-6)
**Goal:** Make it production-ready with proper error handling and security.

**Tasks:**
- User profile page (change email/password)
- Custom 404/500 error pages
- Rate limiting on auth endpoints
- Input validation (max lengths, forbidden characters)
- HTTPS-ready cookie settings
- Security headers middleware
- Proper logging setup
- Environment-specific configs (dev vs production)

---

### 🚀 Phase 7: Docker & Deployment (Week 6-8)
**Goal:** Package and deploy the application.

**Tasks:**
- Write `Dockerfile` for the FastAPI app
- Write `docker-compose.yml` for app + PostgreSQL
- Set up environment variables properly
- Deploy to Render, Railway, or VPS

*(Full details in Section 11)*

---

## 8. JWT Authentication

### 🎫 What Is a JWT (JSON Web Token)?

A JWT is a **self-contained, signed token** that proves who you are. It looks like this:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4iLCJpYXQiOjE1MTYyMzkwMjJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

It has 3 parts separated by dots:
1. **Header** — Algorithm used (e.g., HS256)
2. **Payload** — The data (user ID, expiry time)
3. **Signature** — Proves the token wasn't tampered with

**Decode the payload:**
```python
import base64, json
payload = "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4iLCJpYXQiOjE1MTYyMzkwMjJ9"
print(json.loads(base64.b64decode(payload + "==")))
# Output: {"sub": "1234567890", "name": "John", "iat": 1516239022}
```

> **Important:** JWT payloads are BASE64-ENCODED, not encrypted. Anyone can read the payload! Never put sensitive data (passwords, credit cards) in the payload. Only put non-sensitive identifiers like `user_id`.

---

### 🔄 Access Token vs Refresh Token

| | Access Token | Refresh Token |
|---|---|---|
| **Lifetime** | Short (15-60 mins) | Long (7-30 days) |
| **Purpose** | Authenticate requests | Get new access tokens |
| **Stored** | HTTP-only cookie | HTTP-only cookie (separate) |
| **Risk if stolen** | Limited window of abuse | Higher risk |

**For your first project:** Just use access tokens. Implement refresh tokens later.

When the access token expires:
- **Without refresh tokens:** User must log in again
- **With refresh tokens:** Server silently issues a new access token using the refresh token

---

### 🔐 Complete Login Flow

```
┌────────────────────────────────────────────────────────────┐
│                    LOGIN FLOW                               │
│                                                             │
│  1. User submits email + password form                      │
│                      │                                      │
│  2. FastAPI receives form data                              │
│     → Looks up user by email in DB                         │
│     → Calls verify_password(plain, hashed)                 │
│     → Returns False → Show error                           │
│     → Returns True → Continue                              │
│                      │                                      │
│  3. Create JWT token                                        │
│     payload = {"sub": "42", "exp": "2024-01-01T02:00"}     │
│     token = jwt.encode(payload, SECRET_KEY, HS256)          │
│                      │                                      │
│  4. Set token as HTTP-only cookie                           │
│     Set-Cookie: access_token=eyJ...; HttpOnly; SameSite    │
│                      │                                      │
│  5. Redirect to /vault/dashboard                            │
│                      │                                      │
│  6. Browser automatically sends cookie on every request     │
│                      │                                      │
│  7. FastAPI middleware reads cookie → decodes token         │
│     → Extracts user_id → Loads user from DB                 │
│     → Injects user into route function                      │
└────────────────────────────────────────────────────────────┘
```

---

### 🔑 Token Creation and Decoding

```python
# auth/jwt_handler.py
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from config.settings import settings

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
```

---

### 🚫 Token Validation and Protected Routes

```python
# auth/dependencies.py
from fastapi import Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database.session import get_db
from models.user import User
from auth.jwt_handler import decode_token

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get("access_token")

    if not token:
        # Not logged in → redirect to login
        response = RedirectResponse(url="/login", status_code=302)
        raise HTTPException(status_code=302, headers={"Location": "/login"})

    payload = decode_token(token)
    if payload is None:
        # Token invalid/expired → redirect to login
        raise HTTPException(status_code=302, headers={"Location": "/login"})

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user or not user.is_active:
        raise HTTPException(status_code=302, headers={"Location": "/login"})

    return user
```

**Better approach using middleware for redirects:**
```python
# Create a custom exception handler
@app.exception_handler(401)
async def unauthorized_handler(request, exc):
    return RedirectResponse(url="/login")
```

---

### 🔒 Logout Implementation

```python
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("access_token")  # Remove the JWT cookie
    return response
```

**Important:** JWT tokens are stateless — the server doesn't store them, so you can't truly "invalidate" a token on the server side (without a token blacklist/Redis). For now, just deleting the cookie is sufficient for a learning project.

---

## 9. Password Storage

### 🔒 Hashing vs Encryption — The Critical Distinction

This is the **most important security concept** in your entire application.

| | Hashing | Encryption |
|---|---|---|
| **Reversible?** | ❌ No (one-way) | ✅ Yes (two-way) |
| **Use for** | User's master password | Stored vault passwords |
| **Algorithm** | bcrypt, Argon2 | Fernet (AES-256) |
| **Can recover original?** | No — that's the point! | Yes, with the key |
| **If DB is breached** | Attacker can't recover passwords | Attacker needs the key |

---

### 🔑 Why User Passwords Are Hashed (NOT Encrypted)

When a user sets their master password, you **must not** be able to recover it. Here's why:

1. If your database is breached, hackers can't reverse the hash to get passwords
2. Even YOU (the developer) should never know a user's password
3. When user logs in, you hash their input and compare hashes — no need to ever see the plain password

```python
# What happens at registration:
plain_password = "MySecretPassword123!"
hashed = bcrypt.hash(plain_password)
# Stored in DB: "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"

# What happens at login:
entered = "MySecretPassword123!"
bcrypt.verify(entered, stored_hash)  # True — passwords match!

entered = "wrongpassword"
bcrypt.verify(entered, stored_hash)  # False — passwords don't match!
```

**bcrypt** is slow by design. It takes ~100ms to hash a password. This is intentional — it makes brute-force attacks impractical.

---

### 🔐 Why Vault Passwords Need Encryption (NOT Hashing)

When you store a password for Gmail in the vault, you need to **retrieve and show it back** to the user. If you hashed it, you could never show it again. So you encrypt it:

```
User saves Gmail password: "gmail-password-123"
            │
            ▼
Fernet.encrypt("gmail-password-123") → "gAAAAABl..."  ← stored in DB
            │
User clicks "Reveal Password"
            ▼
Fernet.decrypt("gAAAAABl...") → "gmail-password-123"  ← shown to user
```

**Fernet Encryption Setup:**
```python
# Generate key ONCE, save to .env
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())  # Save this to ENCRYPTION_KEY in .env

# utils/encryption.py
from cryptography.fernet import Fernet
from config.settings import settings

_fernet = Fernet(settings.ENCRYPTION_KEY.encode())

def encrypt_password(plain: str) -> str:
    """Encrypts a vault password for storage."""
    return _fernet.encrypt(plain.encode()).decode()

def decrypt_password(encrypted: str) -> str:
    """Decrypts a stored vault password for display."""
    return _fernet.decrypt(encrypted.encode()).decode()
```

---

### ⚠️ Security Considerations (Beginner Level)

1. **Protect your ENCRYPTION_KEY** — If an attacker gets your DB + your key, they can decrypt everything. Store the key in environment variables, never in code.
2. **HTTPS in Production** — Always use HTTPS so cookies can't be intercepted
3. **Never log passwords** — Not even in debug logs
4. **Never return encrypted passwords in page HTML** — Only decrypt on user's explicit request

> **Future improvement (Advanced):** True end-to-end encryption where the server never sees the plain vault passwords — they're encrypted/decrypted in the browser using the master password as the key. This is how Bitwarden works. This is complex; save for later.

---

## 10. Frontend Design

### 🎨 How Jinja2 Templates Work

Jinja2 processes `.html` files on the server and replaces `{{ }}` (variables) and `{% %}` (logic) with real content before sending to the browser.

**Variable Output:**
```html
<p>Hello, {{ user.username }}!</p>
<p>You have {{ entries|length }} passwords saved.</p>
```

**Control Flow:**
```html
{% if entries %}
    <div class="entry-list">
        {% for entry in entries %}
            <div class="card">{{ entry.title }}</div>
        {% endfor %}
    </div>
{% else %}
    <p>No entries yet. <a href="/vault/new">Add your first!</a></p>
{% endif %}
```

**Filters:**
```html
{{ entry.title|upper }}              <!-- GMAIL -->
{{ entry.created_at|strftime }}      <!-- Jan 14, 2024 -->
{{ entry.notes|truncate(100) }}      <!-- First 100 chars... -->
```

---

### 🏗️ Template Inheritance (The Most Important Pattern)

Instead of repeating the navbar/head in every template, define a `base.html` and **extend** it:

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Vaultify{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', path='/css/output.css') }}">
</head>
<body class="bg-gray-950 text-gray-100 min-h-screen">

    <!-- Navbar -->
    <nav class="bg-gray-900 border-b border-gray-800 px-6 py-4">
        <div class="flex justify-between items-center max-w-7xl mx-auto">
            <a href="/vault/dashboard" class="text-xl font-bold text-indigo-400">🔐 Vaultify</a>
            {% if user %}
            <div class="flex gap-4 items-center">
                <span class="text-gray-400">{{ user.username }}</span>
                <a href="/logout" class="text-red-400 hover:text-red-300">Logout</a>
            </div>
            {% endif %}
        </div>
    </nav>

    <!-- Flash Messages -->
    {% if request.session.get("flash") %}
    <div class="flash-message bg-green-800 text-green-100 px-6 py-3 text-center">
        {{ request.session.pop("flash") }}
    </div>
    {% endif %}

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-6 py-8">
        {% block content %}{% endblock %}
    </main>

    <script src="{{ url_for('static', path='/js/main.js') }}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

```html
<!-- templates/vault/dashboard.html -->
{% extends "base.html" %}

{% block title %}Dashboard — Vaultify{% endblock %}

{% block content %}
<div class="flex justify-between items-center mb-8">
    <h1 class="text-3xl font-bold">Your Vault</h1>
    <a href="/vault/new" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg">
        + Add Entry
    </a>
</div>

<!-- Search Bar -->
<form method="GET" action="/vault/dashboard" class="mb-6">
    <input type="text" name="search" value="{{ search or '' }}"
           placeholder="Search passwords..."
           class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white
                  focus:outline-none focus:ring-2 focus:ring-indigo-500" />
</form>

<!-- Entries Grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    {% for entry in entries %}
    <div class="bg-gray-800 border border-gray-700 rounded-xl p-5 hover:border-indigo-500 transition-colors">
        <div class="flex justify-between items-start mb-3">
            <h3 class="font-semibold text-lg">{{ entry.title }}</h3>
            {% if entry.is_favorite %}
            <span class="text-yellow-400 text-xl">★</span>
            {% endif %}
        </div>
        <p class="text-gray-400 text-sm mb-4">{{ entry.username or "No username" }}</p>
        <div class="flex gap-2">
            <a href="/vault/{{ entry.id }}" class="text-indigo-400 hover:text-indigo-300 text-sm">View</a>
            <a href="/vault/{{ entry.id }}/edit" class="text-gray-400 hover:text-gray-300 text-sm">Edit</a>
            <button onclick="copyPassword({{ entry.id }})"
                    class="text-green-400 hover:text-green-300 text-sm">Copy</button>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}

{% block scripts %}
<script>
async function copyPassword(entryId) {
    const response = await fetch(`/api/entries/${entryId}/password`);
    const data = await response.json();
    await navigator.clipboard.writeText(data.password);
    showToast("Password copied to clipboard!");
}
</script>
{% endblock %}
```

---

### 📝 Handling Forms in FastAPI

HTML forms can only send GET and POST — not PUT or DELETE. For edit/delete, use POST with a hidden `_method` field pattern:

```html
<!-- Delete form -->
<form action="/vault/{{ entry.id }}/delete" method="POST">
    <button type="submit"
            onclick="return confirm('Delete this entry?')"
            class="text-red-400 hover:text-red-300">
        Delete
    </button>
</form>
```

**Reading form data in FastAPI:**
```python
from fastapi import Form

@router.post("/vault/new")
async def create_entry(
    title: str = Form(...),          # Required field
    username: str = Form(""),        # Optional, default empty string
    password: str = Form(...),
    url: str = Form(""),
    notes: str = Form(""),
    folder_id: int = Form(None),     # Optional integer
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ...
```

---

### 🎨 Dashboard Layout Ideas

```
┌─────────────────────────────────────────────────────┐
│  🔐 Vaultify          [username]  [Logout]           │  ← Navbar
├──────────────┬──────────────────────────────────────┤
│              │  🔍 Search...              [+ Add]    │
│  📁 Folders  │─────────────────────────────────────│
│  ─────────── │  [Gmail Card] [GitHub Card] [Bank]   │
│  All Items   │  [Netflix]    [Twitter]    [AWS]     │
│  ★ Favorites │                                      │
│  📁 Work     │  [entry cards in responsive grid]    │
│  📁 Personal │                                      │
│  📁 Finance  │                                      │
│              │                                      │
└──────────────┴──────────────────────────────────────┘
  Sidebar          Main Content Area
```

---

## 11. Docker & Deployment

### 🐳 Docker Basics (What and Why)

Docker packages your application and all its dependencies into a **container** — an isolated environment that runs identically everywhere. No more "it works on my machine" problems.

**Key concepts:**
- **Image:** A blueprint (like a class in programming)
- **Container:** A running instance of an image (like an object)
- **Dockerfile:** Instructions to build an image
- **docker-compose:** Tool to run multiple containers together (app + database)

---

### 📄 Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (Docker layer caching optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the application
COPY . .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the application with Uvicorn (production ASGI server)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

> **Why `--no-cache-dir`?** Saves space in the image by not caching pip downloads.
> **Why copy `requirements.txt` first?** Docker caches layers. If your code changes but requirements.txt doesn't, Docker reuses the cached pip install layer, making rebuilds faster.

---

### 📄 docker-compose.yml

```yaml
# docker-compose.yml
version: "3.8"

services:
  # PostgreSQL database container
  db:
    image: postgres:15-alpine
    container_name: vaultify_db
    environment:
      POSTGRES_DB: vaultify_db
      POSTGRES_USER: vaultify_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data  # Persist data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U vaultify_user -d vaultify_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  # FastAPI application container
  app:
    build: .
    container_name: vaultify_app
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://vaultify_user:${DB_PASSWORD}@db:5432/vaultify_db
      SECRET_KEY: ${SECRET_KEY}
      ALGORITHM: HS256
      ACCESS_TOKEN_EXPIRE_MINUTES: 60
      ENCRYPTION_KEY: ${ENCRYPTION_KEY}
    depends_on:
      db:
        condition: service_healthy  # Wait for DB to be ready
    volumes:
      - .:/app  # Mount code for development (remove for production)

volumes:
  postgres_data:  # Named volume for data persistence
```

**Running with Docker:**
```bash
# Start everything (builds image first if needed)
docker compose up --build

# Run in background
docker compose up -d

# View logs
docker compose logs -f app

# Run database migrations
docker compose exec app alembic upgrade head

# Stop everything
docker compose down

# Stop and delete data (fresh start)
docker compose down -v
```

---

### 🌍 Deployment Options

#### Option 1: Render (Easiest — Recommended for Beginners)

1. Push your code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add a PostgreSQL database from Render's dashboard
6. Set environment variables in Render's UI
7. Deploy!

**Free tier limitations:** Service sleeps after inactivity (30 second cold start)

#### Option 2: Railway (Also Very Easy)

1. Go to [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Add PostgreSQL plugin
4. Set environment variables
5. Deploy automatically on git push

**Advantage:** Free tier doesn't sleep containers

#### Option 3: VPS/EC2 (Most Educational)

Deploying to a VPS (DigitalOcean, Hetzner, AWS EC2) teaches you the most:

```bash
# On your VPS (Ubuntu):
# 1. Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 2. Clone your repo
git clone https://github.com/yourusername/vaultify.git
cd vaultify

# 3. Create .env file with production values
cp .env.example .env
nano .env  # Fill in production values

# 4. Start with Docker Compose
docker compose up -d

# 5. Set up Nginx as reverse proxy (optional but recommended)
sudo apt install nginx
# Configure nginx to proxy port 80 → 8000

# 6. Get free SSL with Certbot
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## 12. Testing & Debugging

### 🔍 Debugging FastAPI

**1. Built-in API Documentation (`/docs`):**
FastAPI auto-generates interactive docs at `http://localhost:8000/docs`. Use this to:
- Test any endpoint without Postman
- See request/response schemas
- Execute API calls in the browser

**2. ReDoc (Alternative docs at `/redoc`):**
Better for reading documentation, worse for testing.

**3. Logging Setup:**
```python
# In main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),                    # Console output
        logging.FileHandler("app.log")             # File output
    ]
)

logger = logging.getLogger(__name__)

# In your routes:
logger.info(f"User {user.id} logged in successfully")
logger.warning(f"Failed login attempt for email: {email}")
logger.error(f"Database error: {str(e)}")
```

**4. FastAPI Debug Mode:**
```bash
# Auto-reload on code changes
fastapi dev main.py        # Development mode (auto-reload)
uvicorn main:app --reload  # Same thing
```

---

### 🧪 Testing Your API

**Using curl (terminal):**
```bash
# Test signup
curl -X POST http://localhost:8000/signup \
  -d "username=testuser&email=test@test.com&password=Test123!" \
  -H "Content-Type: application/x-www-form-urlencoded"

# Test login and save cookie
curl -X POST http://localhost:8000/login \
  -d "email=test@test.com&password=Test123!" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -c cookies.txt -L

# Test protected route with cookie
curl http://localhost:8000/vault/dashboard \
  -b cookies.txt
```

**Using pytest:**
```bash
pip install pytest httpx

# tests/test_auth.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_signup():
    response = client.post("/signup", data={
        "username": "testuser",
        "email": "test@example.com",
        "password": "SecurePass123!",
        "confirm_password": "SecurePass123!"
    })
    assert response.status_code == 302  # Redirect after success

def test_login():
    response = client.post("/login", data={
        "email": "test@example.com",
        "password": "SecurePass123!"
    }, follow_redirects=False)
    assert response.status_code == 302
    assert "access_token" in response.cookies
```

**Run tests:**
```bash
pytest tests/ -v
```

---

### 🐛 Common Beginner Bugs

| Bug | Cause | Fix |
|---|---|---|
| `422 Unprocessable Entity` | Form field name mismatch | Check `Form(...)` parameter names match HTML `name=` attributes |
| `"Table doesn't exist"` | Migration not run | Run `alembic upgrade head` |
| Cookie not sent back | Missing `httponly=True` or wrong path | Double-check `set_cookie()` parameters |
| `IntegrityError: UNIQUE constraint` | Duplicate email/username | Check before inserting, return 400 error |
| Templates not found | Wrong path in `Jinja2Templates(directory=...)` | Use absolute path or run from project root |
| Static files 404 | Wrong mount path | Check `app.mount("/static", ...)` matches `url_for()` calls |
| CORS errors | Calling API from different origin | Not needed for Jinja2 apps (same origin) |
| `JWTError: Signature verification failed` | Wrong SECRET_KEY in .env | Regenerate token after fixing .env |
| Alembic `Target database is not up to date` | New migration not applied | Run `alembic upgrade head` |

---

## 13. Future Improvements

> ⚠️ **These are FUTURE features — do NOT implement until your core is working and deployed.**

### 🔮 Advanced Security

**Two-Factor Authentication (2FA):**
- Add TOTP (Time-based One-Time Password) using `pyotp`
- Show QR code to scan with Google Authenticator
- Require 6-digit code on login

**Client-Side Encryption (Zero-Knowledge Architecture):**
- Derive encryption key from master password in the browser (never sent to server)
- Encrypt/decrypt vault passwords entirely in JavaScript (Web Crypto API)
- Server stores only ciphertext — even a full DB breach reveals nothing

**Audit Logs:**
- New table: `audit_logs` — records every login, entry view, entry change
- "Last accessed from IP: 192.168.1.1 at 2024-01-15 14:32"

### 🔮 Advanced Features

<!-- **Password Sharing:** -->
- Generate a temporary encrypted share link
- Recipient can view password for a limited time
- Requires asymmetric encryption (RSA or elliptic curve)

**Browser Extension:**
- Separate project entirely (Chrome Extension APIs)
- Auto-fill passwords on websites
- Sync with your Vaultify account

**Import/Export:**
- Import from Bitwarden/LastPass CSV
- Export your vault as encrypted JSON

**Weak Password Detection:**
- Use `zxcvbn` library to score password strength
- Warn users about weak or reused passwords

**Password Breach Check:**
- Use HaveIBeenPwned API (k-anonymity model — privacy-safe)
- Check if your password appeared in known data breaches

### 🔮 Infrastructure

**Redis Caching:**
- Cache user sessions in Redis instead of re-querying DB every request
- Token blacklist for proper JWT invalidation on logout

**Async FastAPI + asyncpg:**
- Rewrite database layer to be fully async
- Better performance under high concurrency
- Requires `async def` routes, `await` database calls

**WebSocket Notifications:**
- Real-time alerts: "Your account was accessed from a new device"

**Background Tasks (Celery + Redis):**
- Send welcome emails asynchronously
- Scheduled password expiry reminders
- Periodic security reports

---

## 14. Learning Guidance

### 📚 What You'll Learn in Each Phase

| Phase | Key Concepts |
|---|---|
| Phase 1 | HTTP basics, Python web frameworks, HTML templating, CSS frameworks |
| Phase 2 | Cryptographic hashing, JWT tokens, authentication flow, HTTP cookies, form handling |
| Phase 3 | Relational databases, SQL basics, ORM patterns, database migrations |
| Phase 4 | CRUD operations, encryption vs hashing, SQL relationships, ownership checks |
| Phase 5 | JavaScript fetch API, UX patterns, search/filter queries, session management |
| Phase 6 | Error handling, logging, security hardening, testing |
| Phase 7 | Containerization, networking, environment management, cloud deployment |

---

### 🎯 Concepts to Understand Deeply (Not Just Copy)

1. **The Request/Response Cycle** — Trace every request from browser to database and back. Draw it on paper.
2. **How bcrypt works** — Why is it slow? What is a "salt"? Why can't you reverse it?
3. **JWT anatomy** — Manually decode a token at jwt.io. Understand what's in the payload.
4. **SQL JOINs** — How does `user_id` in `vault_entries` link to `users`? Write raw SQL too.
5. **FastAPI's Dependency Injection** — How does `Depends()` work? Why is it powerful?
6. **HTTP Cookies vs localStorage** — Why are `httponly` cookies safer for auth?
7. **Symmetric Encryption** — How does Fernet use one key to both encrypt and decrypt?

---

### 🚫 Shortcuts Beginners Should Avoid

| Shortcut | Why It's Harmful |
|---|---|
| Putting all code in `main.py` | Impossible to navigate or maintain as app grows |
| Copying JWT code without understanding it | You won't know how to debug auth issues |
| Using `SELECT *` everywhere | Inefficient, exposes unnecessary data |
| Storing secrets in code | Security vulnerability from day one |
| Skipping Pydantic validation | User can send malicious/malformed data |
| Not using database migrations | Manual schema changes cause production disasters |
| Skipping the `/docs` page | It's your best debugging tool — use it constantly |
| Committing `.env` to git | Can expose database passwords and secret keys publicly |

---

### 🧠 How to Avoid the Tutorial-Copy Mindset

The biggest trap for beginners: **copying code without building understanding**.

**Signs you're copying without learning:**
- You can't explain what a line of code does without looking it up
- You delete the code and can't rewrite it
- You don't know why something is in `services/` vs `routers/`

**How to actually learn:**
1. **Read first, then close the tutorial and write it from memory**
2. **Break things intentionally** — remove the `httponly=True` from the cookie, see what changes in browser DevTools
3. **Add a feature the tutorial didn't mention** — e.g., add a "last login time" field
4. **Explain it out loud** — if you can't explain the auth flow to a rubber duck, you don't understand it yet
5. **Read error messages fully** — FastAPI's errors are detailed, use them
6. **Use the database directly** — connect with `psql` or DBeaver and run raw SQL queries

---

### 🏆 Best Development Practices

1. **Commit often with meaningful messages:** `git commit -m "Add JWT login with cookie session"`
2. **Use virtual environments:** Never install packages globally
3. **Write `.env.example`:** Always show what variables are needed (without values)
4. **Test in `/docs`** before building the frontend for that endpoint
5. **One feature at a time:** Finish, commit, then start the next one
6. **Read the FastAPI docs** — they're excellent and beginner-friendly
7. **Use type hints everywhere** — they're not optional in FastAPI, they power the validation

---

## 15. Final Deliverable

### 📁 Final Recommended Folder Structure

```
vaultify/
├── .env                         # Secret config (gitignored)
├── .env.example                 # Template for .env (safe to commit)
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── requirements.txt
├── main.py
│
├── alembic/
│   ├── env.py
│   └── versions/
│       ├── 001_create_users_table.py
│       ├── 002_create_folders_table.py
│       └── 003_create_vault_entries_table.py
│
├── auth/
│   ├── __init__.py
│   ├── dependencies.py          # get_current_user()
│   ├── hashing.py               # bcrypt hash/verify
│   └── jwt_handler.py           # create/decode JWT
│
├── config/
│   └── settings.py              # Pydantic settings from .env
│
├── database/
│   ├── __init__.py
│   ├── base.py                  # SQLAlchemy Base
│   └── session.py               # engine, SessionLocal, get_db()
│
├── models/
│   ├── __init__.py
│   ├── folder.py
│   ├── user.py
│   └── vault_entry.py
│
├── routers/
│   ├── __init__.py
│   ├── auth.py
│   ├── folders.py
│   ├── profile.py
│   └── vault.py
│
├── schemas/
│   ├── __init__.py
│   ├── folder.py
│   ├── user.py
│   └── vault_entry.py
│
├── services/
│   ├── __init__.py
│   ├── auth_service.py
│   ├── folder_service.py
│   └── vault_service.py
│
├── static/
│   ├── css/
│   │   ├── input.css            # Tailwind input (your custom classes)
│   │   └── output.css           # Compiled Tailwind (gitignored if using CLI)
│   ├── js/
│   │   └── main.js
│   └── images/
│       └── logo.svg
│
├── templates/
│   ├── base.html
│   ├── auth/
│   │   ├── login.html
│   │   └── signup.html
│   ├── errors/
│   │   ├── 404.html
│   │   └── 500.html
│   ├── folders/
│   │   └── folders.html
│   ├── profile/
│   │   └── profile.html
│   └── vault/
│       ├── dashboard.html
│       ├── entry_detail.html
│       └── entry_form.html
│
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_vault.py
│
└── utils/
    ├── __init__.py
    ├── encryption.py
    └── password_generator.py
```

---

### 🗓️ Implementation Order (Step-by-Step)

Follow this exact order for the smoothest learning progression:

```
Week 1 — Foundation
━━━━━━━━━━━━━━━━━━
□ Set up Python virtual environment
□ Install FastAPI, Jinja2, python-multipart
□ Create folder structure
□ Set up TailwindCSS (CDN first, then CLI)
□ Create base.html template
□ Create login.html and signup.html (static, no logic yet)
□ Create main.py routes to serve these pages
□ Verify app runs: fastapi dev main.py
□ Set up .gitignore, .env, .env.example
□ Initialize git repository

Week 2 — Authentication
━━━━━━━━━━━━━━━━━━━━━━━
□ Install: passlib[bcrypt], python-jose[cryptography], pydantic-settings
□ Create config/settings.py
□ Create database/base.py and database/session.py
□ Create models/user.py (User SQLAlchemy model)
□ Create schemas/user.py (UserCreate, UserResponse)
□ Create auth/hashing.py
□ Create auth/jwt_handler.py
□ Create services/auth_service.py (create_user, authenticate_user)
□ Create auth/dependencies.py (get_current_user)
□ Create routers/auth.py (GET/POST /login, /signup, /logout)
□ Set up PostgreSQL locally
□ Run: Base.metadata.create_all() to create tables
□ Test signup → user appears in DB
□ Test login → cookie set → redirect to dashboard

Week 3 — Vault CRUD
━━━━━━━━━━━━━━━━━━━
□ Install: cryptography (for Fernet)
□ Generate Fernet key, add to .env
□ Create utils/encryption.py
□ Create models/vault_entry.py
□ Create models/folder.py
□ Set up Alembic, create migration for all tables
□ Create schemas/vault_entry.py and schemas/folder.py
□ Create services/vault_service.py (create, read, update, delete)
□ Create routers/vault.py (dashboard, new, edit, delete routes)
□ Create templates/vault/dashboard.html
□ Create templates/vault/entry_form.html
□ Test full CRUD: add → view → edit → delete

Week 4 — UX Features
━━━━━━━━━━━━━━━━━━━
□ Add copy-password API endpoint (/api/entries/{id}/password)
□ Add JavaScript copy-to-clipboard in main.js
□ Add search/filter to dashboard
□ Add password generator utility
□ Add password generator API endpoint
□ Add JavaScript UI for password generator in entry form
□ Create routers/folders.py and services/folder_service.py
□ Add toggle-favorite endpoint
□ Add flash messages middleware (itsdangerous)

Week 5 — Polish & Security
━━━━━━━━━━━━━━━━━━━━━━━━━
□ Create routers/profile.py (view/update profile, change password)
□ Add custom 404/500 error handlers
□ Add input length validation to all forms
□ Add IDOR protection checks (user owns the resource)
□ Set up logging
□ Write basic pytest tests for auth routes
□ Fix all bugs found during testing

Week 6 — Deployment
━━━━━━━━━━━━━━━━━━━
□ Write Dockerfile
□ Write docker-compose.yml
□ Test with Docker locally: docker compose up --build
□ Run migrations in container: docker compose exec app alembic upgrade head
□ Deploy to Render or Railway
□ Set production environment variables
□ Test live deployment
□ DONE! 🎉
```

---

### 📦 Recommended Libraries & Packages

```txt
# requirements.txt

# Core Framework
fastapi[standard]==0.111.0      # FastAPI with all extras (uvicorn, etc.)
jinja2==3.1.4                   # Templating engine
python-multipart==0.0.9         # Required for form data parsing

# Database
sqlalchemy==2.0.30              # ORM
psycopg2-binary==2.9.9          # PostgreSQL driver
alembic==1.13.1                 # Database migrations

# Authentication
passlib[bcrypt]==1.7.4          # Password hashing with bcrypt
python-jose[cryptography]==3.3.0  # JWT creation and validation
itsdangerous==2.2.0             # Secure cookie signing (for flash messages)

# Configuration
pydantic-settings==2.2.1        # Load settings from .env file

# Encryption
cryptography==42.0.7            # Fernet symmetric encryption for vault passwords

# Testing
pytest==8.2.0                   # Test framework
httpx==0.27.0                   # Async HTTP client (needed by TestClient)
```

**Install all at once:**
```bash
pip install "fastapi[standard]" jinja2 python-multipart sqlalchemy psycopg2-binary \
            alembic "passlib[bcrypt]" "python-jose[cryptography]" itsdangerous \
            pydantic-settings cryptography pytest httpx
pip freeze > requirements.txt
```

---

### 💡 Beginner-Friendly Tech Choices Explained

| Choice | Alternative | Why This Choice |
|---|---|---|
| **SQLAlchemy (sync)** | asyncpg, SQLModel | Simpler to learn, easier to debug, great docs |
| **Fernet encryption** | AES-GCM, RSA | Built-in to Python's cryptography package, beginner-friendly |
| **HTTP-only cookies** | localStorage, Authorization header | More secure for web apps, protects against XSS |
| **Alembic migrations** | Manual SQL scripts | Industry standard, safe, reversible |
| **bcrypt** | SHA-256, MD5 | Specifically designed for passwords, slow by design |
| **Jinja2 templates** | React, Vue, Angular | No build step, simpler for beginners, same server |
| **PostgreSQL** | SQLite, MySQL | Production-grade, great with Docker, standard in industry |
| **pydantic-settings** | python-dotenv | Better type validation, integrates with FastAPI naturally |

---

### ⏱️ Estimated Timeline

| Phase | Duration | Difficulty |
|---|---|---|
| Foundation (templates + static pages) | 3–5 days | ⭐⭐ Easy |
| Authentication (JWT + forms) | 5–7 days | ⭐⭐⭐ Medium |
| Database + Migrations | 3–5 days | ⭐⭐⭐ Medium |
| Vault CRUD + Encryption | 5–7 days | ⭐⭐⭐ Medium |
| UX Features (search, generator) | 4–6 days | ⭐⭐ Easy-Medium |
| Polish + Testing | 3–5 days | ⭐⭐⭐ Medium |
| Docker + Deployment | 3–5 days | ⭐⭐⭐⭐ Hard |
| **TOTAL** | **4–8 weeks** | |

> These estimates assume 1–3 hours of focused work per day. If you work more, it goes faster. Don't rush — understanding > speed.

---

### ✅ Milestone Checklist

#### Phase 1: Foundation
- [ ] Project folder structure created
- [ ] FastAPI app runs (`fastapi dev main.py`)
- [ ] Base Jinja2 template working
- [ ] Login and signup pages render with Tailwind styles
- [ ] Static files (CSS, JS) loading correctly

#### Phase 2: Authentication
- [ ] User can register (form → DB insert)
- [ ] Passwords are hashed with bcrypt (verify in DB)
- [ ] User can log in and receives JWT cookie
- [ ] Protected routes redirect to login if not authenticated
- [ ] User can log out (cookie cleared)

#### Phase 3: Database
- [ ] PostgreSQL connected and running
- [ ] All three tables created via Alembic migration
- [ ] Can query users, vault_entries, folders via psql
- [ ] Relationships between tables working

#### Phase 4: Vault CRUD
- [ ] Can create a new vault entry (password stored encrypted)
- [ ] Dashboard shows all entries for logged-in user
- [ ] Can edit an existing entry
- [ ] Can delete an entry
- [ ] IDOR protection: can't access other users' entries
- [ ] Copy password button decrypts and copies to clipboard

#### Phase 5: UX Features
- [ ] Search bar filters entries
- [ ] Password generator creates random passwords
- [ ] Folders can be created and entries assigned to them
- [ ] Favorites can be toggled
- [ ] Flash messages show on success/error

#### Phase 6: Polish
- [ ] Custom 404/500 error pages
- [ ] Profile page with password change
- [ ] At least one pytest test passing
- [ ] All obvious bugs fixed

#### Phase 7: Deployment
- [ ] App runs in Docker locally (`docker compose up`)
- [ ] Migrations run in container
- [ ] Deployed to Render/Railway and accessible via URL
- [ ] Environment variables set in production
- [ ] **🎉 Vaultify is LIVE!**

---

### 🚀 Your First Step (Right Now)

```bash
# Navigate to your project
cd /home/sarthak/Documents/IDP/python_practice/fastapi

# Activate or create virtual environment
python -m venv venv
source venv/bin/activate

# Install core dependencies
pip install "fastapi[standard]" jinja2 python-multipart

# Create the folder structure
mkdir -p config database models schemas routers services auth utils
mkdir -p templates/auth templates/vault templates/folders templates/profile templates/errors
mkdir -p static/css static/js static/images tests alembic

# Create __init__.py files
touch config/__init__.py database/__init__.py models/__init__.py
touch schemas/__init__.py routers/__init__.py services/__init__.py
touch auth/__init__.py utils/__init__.py tests/__init__.py

# Run the app
fastapi dev main.py
```

**Then visit:**
- `http://localhost:8000` — Your app
- `http://localhost:8000/docs` — Auto-generated API docs
- `http://localhost:8000/redoc` — Alternative docs

---

> **Final Note:** Building this project will teach you more than 3 months of tutorials. Real projects force you to make decisions, debug real errors, and understand tradeoffs. Every bug you fix on your own is worth 10 tutorial videos. You've got this! 💪

---

*Guide created for Vaultify — a FastAPI Password Manager learning project*
*Stack: FastAPI · Jinja2 · TailwindCSS · PostgreSQL · SQLAlchemy · JWT · Docker*

---

## 16. Product Design — Complete Feature & Route Specification

> This section provides an exhaustive product design document: every page, every route, every user interaction, and every UI element that Vaultify needs.

---

### 🗺️ Sitemap — Every Page in Vaultify

```
                         ┌─────────────────┐
                         │   Landing Page   │  (/)
                         │   (Not Logged In) │
                         └────────┬────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼                             ▼
            ┌──────────────┐              ┌──────────────┐
            │   Login Page  │              │  Signup Page  │
            │   (/login)    │              │  (/signup)    │
            └──────┬───────┘              └──────┬───────┘
                   │                              │
                   └──────────┬───────────────────┘
                              ▼
                    ┌──────────────────┐
                    │    Dashboard     │  (/vault/dashboard)
                    │   (Main Hub)     │
                    └────────┬────────┘
                             │
         ┌──────────┬────────┼────────┬──────────┐
         ▼          ▼        ▼        ▼          ▼
   ┌──────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐
   │ Add Entry│ │ View   │ │Folders │ │Profile │ │ Password │
   │ (/vault/ │ │ Entry  │ │(/fold  │ │(/prof  │ │ Generator│
   │  new)    │ │(/vault │ │  ers)  │ │  ile)  │ │ (modal)  │
   └──────────┘ │ /{id}) │ └────────┘ └────────┘ └──────────┘
                └───┬────┘
                    │
              ┌─────┼─────┐
              ▼           ▼
        ┌──────────┐ ┌──────────┐
        │Edit Entry│ │  Delete  │
        │(/vault/  │ │(confirm  │
        │{id}/edit)│ │ modal)   │
        └──────────┘ └──────────┘
```

---

### 📄 Page-by-Page Design Specification

---

#### Page 1: Landing Page (`/`)

**Purpose:** First thing visitors see. Introduces Vaultify and directs to login/signup.

**Route:**
```python
@router.get("/")
def landing(request: Request):
    # If user is already logged in, redirect to dashboard
    token = request.cookies.get("access_token")
    if token:
        try:
            payload = decode_token(token)
            if payload:
                return RedirectResponse(url="/vault/dashboard", status_code=302)
        except:
            pass
    return templates.TemplateResponse("landing.html", {"request": request})
```

**UI Elements:**
- Hero section: "Your passwords. Secured." with gradient text
- Brief feature highlights (3 cards: Secure, Organized, Fast)
- CTA buttons: "Get Started" → `/signup`, "Login" → `/login`
- Footer with basic links

**What the user sees:**
```
┌─────────────────────────────────────────────────────┐
│  🔐 Vaultify                    [Login]  [Sign Up]  │
├─────────────────────────────────────────────────────┤
│                                                      │
│           Your Passwords. Secured.                   │
│    One vault for all your credentials.               │
│                                                      │
│        [ Get Started ]    [ Login ]                  │
│                                                      │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐      │
│  │ 🔒 Secure  │ │ 📁 Organized│ │ ⚡ Fast    │      │
│  │ AES-256    │ │ Folders &   │ │ Instant    │      │
│  │ encryption │ │ categories  │ │ search     │      │
│  └────────────┘ └────────────┘ └────────────┘      │
│                                                      │
│  ─────────────────────────────────────────────────  │
│  © 2024 Vaultify · Privacy · Terms                   │
└─────────────────────────────────────────────────────┘
```

---

#### Page 2: Signup Page (`/signup`)

**Purpose:** Create a new user account.

**Routes:**
```python
@router.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse("auth/signup.html", {"request": request})

@router.post("/signup")
async def signup(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    errors = []

    # Validation rules
    if len(username) < 3 or len(username) > 50:
        errors.append("Username must be 3-50 characters")
    if len(password) < 8:
        errors.append("Password must be at least 8 characters")
    if password != confirm_password:
        errors.append("Passwords do not match")
    if not re.search(r'[A-Z]', password):
        errors.append("Password needs at least one uppercase letter")
    if not re.search(r'[0-9]', password):
        errors.append("Password needs at least one number")

    # Check existing user
    if db.query(User).filter(User.email == email).first():
        errors.append("Email already registered")
    if db.query(User).filter(User.username == username).first():
        errors.append("Username already taken")

    if errors:
        return templates.TemplateResponse("auth/signup.html", {
            "request": request,
            "errors": errors,
            "username": username,
            "email": email
        })

    auth_service.create_user(db, UserCreate(
        username=username, email=email, password=password
    ))
    request.session["flash"] = {"message": "Account created! Please log in.", "type": "success"}
    return RedirectResponse(url="/login", status_code=302)
```

**Form Fields:**
| Field | Type | Validation | Required |
|---|---|---|---|
| `username` | text | 3-50 chars, alphanumeric + underscore | ✅ |
| `email` | email | Valid email format, unique in DB | ✅ |
| `password` | password | Min 8 chars, 1 uppercase, 1 number | ✅ |
| `confirm_password` | password | Must match password | ✅ |

**UI Layout:**
```
┌─────────────────────────────────────────────────┐
│  🔐 Vaultify                                    │
├─────────────────────────────────────────────────┤
│                                                  │
│          ┌──────────────────────────┐            │
│          │     Create Account       │            │
│          │                          │            │
│          │  Username                │            │
│          │  [___________________]   │            │
│          │                          │            │
│          │  Email                   │            │
│          │  [___________________]   │            │
│          │                          │            │
│          │  Master Password         │            │
│          │  [___________________]👁  │            │
│          │  ░░░░░░░░ Weak           │  ← strength bar
│          │                          │            │
│          │  Confirm Password        │            │
│          │  [___________________]   │            │
│          │                          │            │
│          │  [    Create Account   ] │            │
│          │                          │            │
│          │  Already have account?   │            │
│          │  Login here              │            │
│          └──────────────────────────┘            │
│                                                  │
└─────────────────────────────────────────────────┘
```

**JavaScript features on this page:**
- Password strength meter (real-time as user types)
- Password visibility toggle (eye icon)
- Confirm password match indicator (green check / red x)

---

#### Page 3: Login Page (`/login`)

**Routes:**
```python
@router.get("/login")
def login_page(request: Request):
    message = request.query_params.get("message", "")
    flash = request.session.pop("flash", None)
    return templates.TemplateResponse("auth/login.html", {
        "request": request,
        "message": message,
        "flash": flash
    })

@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    remember_me: bool = Form(False),
    db: Session = Depends(get_db)
):
    user = auth_service.authenticate_user(db, email, password)
    if not user:
        return templates.TemplateResponse("auth/login.html", {
            "request": request,
            "error": "Invalid email or password",
            "email": email  # Preserve email input
        })

    # Token expiry: 7 days if "remember me", else 60 minutes
    expires = timedelta(days=7) if remember_me else timedelta(minutes=60)
    token = create_access_token({"sub": str(user.id)}, expires_delta=expires)

    response = RedirectResponse(url="/vault/dashboard", status_code=302)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=int(expires.total_seconds())
    )
    return response
```

**Form Fields:**
| Field | Type | Validation | Required |
|---|---|---|---|
| `email` | email | Valid format | ✅ |
| `password` | password | Non-empty | ✅ |
| `remember_me` | checkbox | Boolean | ❌ |

---

#### Page 4: Dashboard (`/vault/dashboard`) — THE MAIN PAGE

**Purpose:** Central hub. Shows all vault entries. Most time spent here.

**Route:**
```python
@router.get("/vault/dashboard")
def dashboard(
    request: Request,
    search: str = "",
    folder_id: int = None,
    favorites_only: bool = False,
    sort_by: str = "title",        # title, created_at, updated_at
    sort_order: str = "asc",       # asc, desc
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Base query — only this user's entries
    query = db.query(VaultEntry).filter(VaultEntry.user_id == current_user.id)

    # Filters
    if search:
        query = query.filter(
            or_(
                VaultEntry.title.ilike(f"%{search}%"),
                VaultEntry.username.ilike(f"%{search}%"),
                VaultEntry.url.ilike(f"%{search}%"),
                VaultEntry.notes.ilike(f"%{search}%")
            )
        )
    if folder_id:
        query = query.filter(VaultEntry.folder_id == folder_id)
    if favorites_only:
        query = query.filter(VaultEntry.is_favorite == True)

    # Sorting
    sort_column = getattr(VaultEntry, sort_by, VaultEntry.title)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    entries = query.all()
    folders = db.query(Folder).filter(Folder.user_id == current_user.id).all()

    # Stats for sidebar
    total_entries = db.query(VaultEntry).filter(VaultEntry.user_id == current_user.id).count()
    total_favorites = db.query(VaultEntry).filter(
        VaultEntry.user_id == current_user.id,
        VaultEntry.is_favorite == True
    ).count()

    return templates.TemplateResponse("vault/dashboard.html", {
        "request": request,
        "user": current_user,
        "entries": entries,
        "folders": folders,
        "search": search,
        "current_folder_id": folder_id,
        "favorites_only": favorites_only,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "total_entries": total_entries,
        "total_favorites": total_favorites
    })
```

**Full Dashboard UI Layout:**
```
┌─────────────────────────────────────────────────────────────────┐
│  🔐 Vaultify              🔍 [Quick Search...]    👤 sarthak ▼ │
│                                                    ├──────────┤ │
│                                                    │ Profile  │ │
│                                                    │ Settings │ │
│                                                    │ Logout   │ │
│                                                    └──────────┘ │
├──────────────┬──────────────────────────────────────────────────┤
│              │                                                  │
│  📊 Overview │  Your Vault                    [+ Add Entry]     │
│  ──────────  │  ─────────────────────────────────────────────   │
│  All Items 24│  🔍 [Search passwords...]  Sort: [Title ▼] [↑↓] │
│  ★ Faves   5 │                                                  │
│              │  ┌──────────────┐ ┌──────────────┐ ┌──────────┐ │
│  📁 Folders  │  │ 🌐 Gmail     │ │ 🐙 GitHub    │ │ 🏦 Bank  │ │
│  ──────────  │  │              │ │              │ │          │ │
│  📁 Work   8 │  │ john@gm...  │ │ johndoe      │ │ john_d   │ │
│  📁 Personal │  │ ••••••••    │ │ ••••••••     │ │ •••••••  │ │
│           12 │  │              │ │              │ │          │ │
│  📁 Finance 4│  │ [📋][👁][★] │ │ [📋][👁][☆] │ │ [📋][👁] │ │
│              │  └──────────────┘ └──────────────┘ └──────────┘ │
│              │                                                  │
│  [+ Folder]  │  ┌──────────────┐ ┌──────────────┐              │
│              │  │ 📺 Netflix   │ │ 🐦 Twitter   │              │
│              │  │              │ │              │              │
│              │  │ myemail@..   │ │ @johndoe     │              │
│              │  │ ••••••••     │ │ ••••••••     │              │
│              │  │              │ │              │              │
│              │  │ [📋][👁][★] │ │ [📋][👁][☆] │              │
│              │  └──────────────┘ └──────────────┘              │
│              │                                                  │
│              │  Showing 5 of 24 entries                         │
└──────────────┴──────────────────────────────────────────────────┘

Legend:
  📋 = Copy password     👁 = Reveal/View     ★ = Favorited     ☆ = Not favorited
```

**Entry Card Interactions:**
| Icon/Action | What Happens | Implementation |
|---|---|---|
| Click card title | Navigate to `/vault/{id}` (detail page) | `<a href>` link |
| 📋 Copy button | Calls `/api/entries/{id}/password`, copies to clipboard | JS `fetch()` + `navigator.clipboard` |
| 👁 Reveal button | Calls `/api/entries/{id}/password`, shows in tooltip/modal | JS `fetch()` + DOM update |
| ★/☆ Favorite | Calls `POST /vault/{id}/toggle-favorite`, toggles star | JS `fetch()` + icon swap |
| Right-click / ⋮ menu | Shows: Edit, Delete, Move to folder | Dropdown menu |

---

#### Page 5: Add New Entry (`/vault/new`)

**Routes:**
```python
@router.get("/vault/new")
def new_entry_page(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    folders = db.query(Folder).filter(Folder.user_id == current_user.id).all()
    return templates.TemplateResponse("vault/entry_form.html", {
        "request": request,
        "user": current_user,
        "folders": folders,
        "entry": None,          # None = creating new (not editing)
        "form_action": "/vault/new",
        "page_title": "Add New Entry"
    })

@router.post("/vault/new")
async def create_entry(
    request: Request,
    title: str = Form(...),
    username: str = Form(""),
    password: str = Form(...),
    url: str = Form(""),
    notes: str = Form(""),
    folder_id: int = Form(None),
    is_favorite: bool = Form(False),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validation
    if not title.strip():
        return templates.TemplateResponse("vault/entry_form.html", {
            "request": request, "error": "Title is required",
            "user": current_user, "entry": None,
            "form_action": "/vault/new", "page_title": "Add New Entry"
        })

    vault_service.create_entry(db, VaultEntryCreate(
        title=title, username=username, password=password,
        url=url, notes=notes, folder_id=folder_id, is_favorite=is_favorite
    ), user_id=current_user.id)

    request.session["flash"] = {"message": f"'{title}' saved to vault!", "type": "success"}
    return RedirectResponse(url="/vault/dashboard", status_code=302)
```

**Form UI:**
```
┌──────────────────────────────────────────────────┐
│  🔐 Vaultify                         👤 sarthak │
├──────────────────────────────────────────────────┤
│                                                   │
│  ← Back to Vault                                 │
│                                                   │
│  ┌────────────────────────────────────────────┐  │
│  │       Add New Entry                         │  │
│  │                                             │  │
│  │  Title *                                    │  │
│  │  [___________________________________]     │  │
│  │                                             │  │
│  │  Website URL                                │  │
│  │  [https://_________________________]       │  │
│  │                                             │  │
│  │  Username / Email                           │  │
│  │  [___________________________________]     │  │
│  │                                             │  │
│  │  Password *                                 │  │
│  │  [_________________________] 👁 [🔄 Gen]   │  │
│  │                                             │  │
│  │  ┌─ Password Generator ─────────────────┐  │  │
│  │  │  Length: [16] ──●──────── 32         │  │  │
│  │  │  ☑ Uppercase  ☑ Numbers  ☑ Symbols  │  │  │
│  │  │  [ Generate ]                        │  │  │
│  │  └──────────────────────────────────────┘  │  │
│  │                                             │  │
│  │  Folder                                     │  │
│  │  [▼ Select folder... ]                     │  │
│  │                                             │  │
│  │  Notes                                      │  │
│  │  [___________________________________]     │  │
│  │  [                                    ]     │  │
│  │  [___________________________________]     │  │
│  │                                             │  │
│  │  ☐ Add to favorites                        │  │
│  │                                             │  │
│  │  [ Cancel ]            [ Save Entry ]       │  │
│  └────────────────────────────────────────────┘  │
│                                                   │
└──────────────────────────────────────────────────┘
```

**Form Fields:**
| Field | Type | Validation | Required | Notes |
|---|---|---|---|---|
| `title` | text | 1-200 chars | ✅ | "Gmail", "GitHub" etc. |
| `url` | url | Valid URL or empty | ❌ | Auto-prepend https:// |
| `username` | text | 0-255 chars | ❌ | Login username for the site |
| `password` | password | 1-500 chars | ✅ | Encrypted before storage |
| `folder_id` | select | Must be user's folder | ❌ | Dropdown of user's folders |
| `notes` | textarea | 0-2000 chars | ❌ | Free text notes |
| `is_favorite` | checkbox | Boolean | ❌ | Star the entry |

---

#### Page 6: View Entry Detail (`/vault/{id}`)

**Route:**
```python
@router.get("/vault/{entry_id}")
def view_entry(
    entry_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    entry = db.query(VaultEntry).filter(
        VaultEntry.id == entry_id,
        VaultEntry.user_id == current_user.id  # IDOR protection
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    return templates.TemplateResponse("vault/entry_detail.html", {
        "request": request,
        "user": current_user,
        "entry": entry
    })
```

**Detail Page UI:**
```
┌──────────────────────────────────────────────────┐
│  🔐 Vaultify                         👤 sarthak │
├──────────────────────────────────────────────────┤
│                                                   │
│  ← Back to Vault                                 │
│                                                   │
│  ┌────────────────────────────────────────────┐  │
│  │  🌐 Gmail                            ★     │  │
│  │  ──────────────────────────────────────     │  │
│  │                                             │  │
│  │  Website                                    │  │
│  │  https://gmail.com          [🔗 Open]      │  │
│  │                                             │  │
│  │  Username                                   │  │
│  │  john@gmail.com             [📋 Copy]      │  │
│  │                                             │  │
│  │  Password                                   │  │
│  │  •••••••••••••              [👁] [📋 Copy] │  │
│  │                                             │  │
│  │  Folder                                     │  │
│  │  📁 Personal                                │  │
│  │                                             │  │
│  │  Notes                                      │  │
│  │  ┌──────────────────────────────────────┐  │  │
│  │  │ Recovery email: backup@outlook.com   │  │  │
│  │  │ 2FA enabled with Authenticator app   │  │  │
│  │  └──────────────────────────────────────┘  │  │
│  │                                             │  │
│  │  Created: Jan 14, 2024                      │  │
│  │  Last modified: Mar 2, 2024                 │  │
│  │                                             │  │
│  │  [ ✏️ Edit ]              [ 🗑️ Delete ]    │  │
│  └────────────────────────────────────────────┘  │
│                                                   │
└──────────────────────────────────────────────────┘
```

---

#### Page 7: Edit Entry (`/vault/{id}/edit`)

**Routes:**
```python
@router.get("/vault/{entry_id}/edit")
def edit_entry_page(
    entry_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    entry = db.query(VaultEntry).filter(
        VaultEntry.id == entry_id,
        VaultEntry.user_id == current_user.id
    ).first()
    if not entry:
        raise HTTPException(status_code=404)

    folders = db.query(Folder).filter(Folder.user_id == current_user.id).all()

    return templates.TemplateResponse("vault/entry_form.html", {
        "request": request,
        "user": current_user,
        "entry": entry,   # Pre-fill form with existing data
        "folders": folders,
        "form_action": f"/vault/{entry_id}/edit",
        "page_title": f"Edit — {entry.title}"
    })

@router.post("/vault/{entry_id}/edit")
async def update_entry(
    entry_id: int,
    request: Request,
    title: str = Form(...),
    username: str = Form(""),
    password: str = Form(""),        # Empty = keep existing password
    url: str = Form(""),
    notes: str = Form(""),
    folder_id: int = Form(None),
    is_favorite: bool = Form(False),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    entry = db.query(VaultEntry).filter(
        VaultEntry.id == entry_id,
        VaultEntry.user_id == current_user.id
    ).first()
    if not entry:
        raise HTTPException(status_code=404)

    # Update fields
    entry.title = title
    entry.username = username
    entry.url = url
    entry.notes = notes
    entry.folder_id = folder_id
    entry.is_favorite = is_favorite

    # Only update password if user provided a new one
    if password.strip():
        entry.encrypted_password = encrypt_password(password)

    db.commit()
    request.session["flash"] = {"message": f"'{title}' updated!", "type": "success"}
    return RedirectResponse(url=f"/vault/{entry_id}", status_code=302)
```

> **Design decision:** The edit form reuses the same `entry_form.html` template as the add form. The template checks `{% if entry %}` to decide whether to pre-fill fields. This is the DRY (Don't Repeat Yourself) principle.

---

#### Page 8: Delete Entry (`POST /vault/{id}/delete`)

**Route (No separate page — uses confirmation modal or POST form):**
```python
@router.post("/vault/{entry_id}/delete")
async def delete_entry(
    entry_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    entry = db.query(VaultEntry).filter(
        VaultEntry.id == entry_id,
        VaultEntry.user_id == current_user.id
    ).first()
    if not entry:
        raise HTTPException(status_code=404)

    title = entry.title
    db.delete(entry)
    db.commit()

    request.session["flash"] = {"message": f"'{title}' deleted.", "type": "warning"}
    return RedirectResponse(url="/vault/dashboard", status_code=302)
```

**Delete Confirmation (JavaScript modal, no separate page):**
```javascript
// static/js/main.js
function confirmDelete(entryId, title) {
    const modal = document.getElementById("delete-modal");
    const form = document.getElementById("delete-form");
    const titleSpan = document.getElementById("delete-title");

    titleSpan.textContent = title;
    form.action = `/vault/${entryId}/delete`;
    modal.classList.remove("hidden");
}

function closeModal() {
    document.getElementById("delete-modal").classList.add("hidden");
}
```

```html
<!-- Delete confirmation modal in base.html or dashboard.html -->
<div id="delete-modal" class="hidden fixed inset-0 bg-black/60 flex items-center justify-center z-50">
  <div class="bg-gray-800 rounded-xl p-6 max-w-md w-full mx-4">
    <h3 class="text-xl font-bold text-white mb-2">Delete Entry</h3>
    <p class="text-gray-400 mb-6">
      Are you sure you want to delete "<span id="delete-title" class="text-red-400"></span>"?
      This action cannot be undone.
    </p>
    <form id="delete-form" method="POST">
      <div class="flex gap-3 justify-end">
        <button type="button" onclick="closeModal()"
                class="px-4 py-2 bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600">
          Cancel
        </button>
        <button type="submit"
                class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">
          Delete
        </button>
      </div>
    </form>
  </div>
</div>
```

---

#### Page 9: Folders Management (`/folders`)

**Routes:**
```python
@router.get("/folders")
def folders_page(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    folders = db.query(Folder).filter(Folder.user_id == current_user.id).all()

    # Count entries per folder
    folder_data = []
    for folder in folders:
        count = db.query(VaultEntry).filter(
            VaultEntry.folder_id == folder.id
        ).count()
        folder_data.append({"folder": folder, "entry_count": count})

    # Count uncategorized entries
    uncategorized = db.query(VaultEntry).filter(
        VaultEntry.user_id == current_user.id,
        VaultEntry.folder_id == None
    ).count()

    return templates.TemplateResponse("folders/folders.html", {
        "request": request,
        "user": current_user,
        "folder_data": folder_data,
        "uncategorized_count": uncategorized
    })

@router.post("/folders/new")
async def create_folder(
    request: Request,
    name: str = Form(...),
    icon: str = Form("folder"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if len(name.strip()) < 1 or len(name) > 100:
        request.session["flash"] = {"message": "Folder name must be 1-100 characters", "type": "error"}
        return RedirectResponse(url="/folders", status_code=302)

    # Check for duplicate folder name for this user
    existing = db.query(Folder).filter(
        Folder.user_id == current_user.id,
        Folder.name == name.strip()
    ).first()
    if existing:
        request.session["flash"] = {"message": "Folder already exists", "type": "error"}
        return RedirectResponse(url="/folders", status_code=302)

    new_folder = Folder(name=name.strip(), icon=icon, user_id=current_user.id)
    db.add(new_folder)
    db.commit()

    request.session["flash"] = {"message": f"Folder '{name}' created!", "type": "success"}
    return RedirectResponse(url="/folders", status_code=302)

@router.post("/folders/{folder_id}/delete")
async def delete_folder(
    folder_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    folder = db.query(Folder).filter(
        Folder.id == folder_id,
        Folder.user_id == current_user.id
    ).first()
    if not folder:
        raise HTTPException(status_code=404)

    name = folder.name
    # Entries in this folder get folder_id = NULL (ON DELETE SET NULL)
    db.delete(folder)
    db.commit()

    request.session["flash"] = {"message": f"Folder '{name}' deleted. Entries moved to uncategorized.", "type": "warning"}
    return RedirectResponse(url="/folders", status_code=302)
```

**Folders Page UI:**
```
┌──────────────────────────────────────────────────┐
│  🔐 Vaultify                         👤 sarthak │
├──────────────────────────────────────────────────┤
│                                                   │
│  Folders                         [+ New Folder]   │
│  ─────────────────────────────────────────────── │
│                                                   │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐   │
│  │ 💼 Work    │ │ 👤 Personal│ │ 🏦 Finance │   │
│  │            │ │            │ │            │   │
│  │ 8 entries  │ │ 12 entries │ │ 4 entries  │   │
│  │            │ │            │ │            │   │
│  │ [View][🗑] │ │ [View][🗑] │ │ [View][🗑] │   │
│  └────────────┘ └────────────┘ └────────────┘   │
│                                                   │
│  ┌────────────┐                                  │
│  │ 📁 Uncateg.│                                  │
│  │            │                                  │
│  │ 3 entries  │                                  │
│  │            │                                  │
│  │ [View]     │                                  │
│  └────────────┘                                  │
│                                                   │
└──────────────────────────────────────────────────┘
```

---

#### Page 10: Profile Page (`/profile`)

**Routes:**
```python
@router.get("/profile")
def profile_page(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    total_entries = db.query(VaultEntry).filter(VaultEntry.user_id == current_user.id).count()
    total_folders = db.query(Folder).filter(Folder.user_id == current_user.id).count()

    return templates.TemplateResponse("profile/profile.html", {
        "request": request,
        "user": current_user,
        "stats": {
            "total_entries": total_entries,
            "total_folders": total_folders,
            "member_since": current_user.created_at.strftime("%B %d, %Y")
        }
    })

@router.post("/profile/update")
async def update_profile(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check uniqueness (excluding current user)
    if db.query(User).filter(User.email == email, User.id != current_user.id).first():
        return templates.TemplateResponse("profile/profile.html", {
            "request": request, "user": current_user,
            "error": "Email already in use by another account"
        })

    current_user.username = username
    current_user.email = email
    db.commit()

    request.session["flash"] = {"message": "Profile updated!", "type": "success"}
    return RedirectResponse(url="/profile", status_code=302)

@router.post("/profile/change-password")
async def change_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_new_password: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(current_password, current_user.hashed_password):
        request.session["flash"] = {"message": "Current password is incorrect", "type": "error"}
        return RedirectResponse(url="/profile", status_code=302)

    if new_password != confirm_new_password:
        request.session["flash"] = {"message": "New passwords don't match", "type": "error"}
        return RedirectResponse(url="/profile", status_code=302)

    if len(new_password) < 8:
        request.session["flash"] = {"message": "New password must be at least 8 characters", "type": "error"}
        return RedirectResponse(url="/profile", status_code=302)

    current_user.hashed_password = hash_password(new_password)
    db.commit()

    request.session["flash"] = {"message": "Password changed!", "type": "success"}
    return RedirectResponse(url="/profile", status_code=302)
```

---

### 🔌 Complete API Endpoint Reference (JSON Endpoints)

These are the AJAX/JSON endpoints called by JavaScript (not page routes):

```python
# ── Password Operations (JSON) ──────────────────────────

@router.get("/api/entries/{entry_id}/password")
def get_password(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Returns decrypted password for copy/reveal feature."""
    entry = db.query(VaultEntry).filter(
        VaultEntry.id == entry_id,
        VaultEntry.user_id == current_user.id
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return {"password": decrypt_password(entry.encrypted_password)}


# ── Toggle Favorite (JSON) ──────────────────────────────

@router.post("/api/entries/{entry_id}/toggle-favorite")
def toggle_favorite(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Toggle favorite status without page reload."""
    entry = db.query(VaultEntry).filter(
        VaultEntry.id == entry_id,
        VaultEntry.user_id == current_user.id
    ).first()
    if not entry:
        raise HTTPException(status_code=404)

    entry.is_favorite = not entry.is_favorite
    db.commit()
    return {"is_favorite": entry.is_favorite}


# ── Password Generator (JSON) ───────────────────────────

@router.get("/api/generate-password")
def generate_password_api(
    length: int = 16,
    uppercase: bool = True,
    digits: bool = True,
    symbols: bool = True,
    current_user: User = Depends(get_current_user)
):
    """Generate a random password with given options."""
    if length < 8 or length > 128:
        raise HTTPException(status_code=400, detail="Length must be 8-128")
    password = generate_strong_password(length, uppercase, digits, symbols)
    return {"password": password, "length": length}


# ── Dashboard Stats (JSON, optional) ────────────────────

@router.get("/api/stats")
def get_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Returns vault statistics for dashboard widgets."""
    return {
        "total_entries": db.query(VaultEntry).filter(VaultEntry.user_id == current_user.id).count(),
        "total_folders": db.query(Folder).filter(Folder.user_id == current_user.id).count(),
        "total_favorites": db.query(VaultEntry).filter(
            VaultEntry.user_id == current_user.id,
            VaultEntry.is_favorite == True
        ).count()
    }
```

---

### 🖱️ User Interaction Flows

#### Flow 1: First-Time User Journey

```
1. User visits https://vaultify.com
   → Sees landing page
   → Clicks "Get Started"

2. Redirected to /signup
   → Fills in username, email, password
   → Password strength meter shows "Strong" ✅
   → Clicks "Create Account"

3. POST /signup processes form
   → Validates all fields
   → Hashes password with bcrypt
   → Inserts user into database
   → Sets flash message: "Account created!"
   → Redirects to /login

4. User logs in at /login
   → Enters email + password
   → Server verifies credentials
   → JWT cookie set
   → Redirected to /vault/dashboard

5. Dashboard is empty
   → Shows: "Your vault is empty. Add your first password!"
   → Prominent "+ Add Entry" button

6. User clicks "+ Add Entry"
   → Navigated to /vault/new
   → Fills in: Title="Gmail", Username="user@gmail.com"
   → Clicks "Generate Password" → strong password appears
   → Selects folder: "Personal" (or creates one)
   → Clicks "Save Entry"

7. Redirected back to dashboard
   → Gmail card appears with masked password
   → Flash: "Gmail saved to vault!" ✅
```

#### Flow 2: Returning User — Copy Password

```
1. User visits /
   → Has valid JWT cookie → auto-redirected to /vault/dashboard

2. Sees their entries grid
   → Spots "GitHub" card
   → Clicks 📋 (copy) button on the card

3. JavaScript sends: GET /api/entries/42/password
   → Server decrypts password
   → Returns JSON: {"password": "MyGitH!ubP@ss"}

4. JavaScript calls navigator.clipboard.writeText()
   → Password copied to clipboard
   → Toast notification: "Password copied!" (disappears after 3s)

5. User pastes password into GitHub login
   → Done! Never typed the password manually.
```

#### Flow 3: Search for an Entry

```
1. User is on /vault/dashboard with 50+ entries
   → Types "bank" in search bar
   → Presses Enter (or search is live with JS debounce)

2. Browser sends: GET /vault/dashboard?search=bank
   → Server filters: WHERE title ILIKE '%bank%' OR username ILIKE '%bank%'
   → Returns only matching entries (e.g., "Bank of America", "My Bank Login")

3. User finds entry → clicks to view details
4. User clicks "Clear search" → full list returns
```

#### Flow 4: Organize with Folders

```
1. User goes to /folders
   → Sees existing folders with entry counts
   → Clicks "+ New Folder"

2. Modal/inline form appears
   → Types "Social Media"
   → Clicks Create

3. POST /folders/new → folder created
   → Flash: "Folder 'Social Media' created!"

4. User goes to /vault/42/edit (editing Twitter entry)
   → Changes folder dropdown from "None" to "Social Media"
   → Saves

5. On dashboard, clicks "Social Media" in sidebar
   → GET /vault/dashboard?folder_id=5
   → Only Social Media entries shown
```

---

### 📐 Responsive Design Breakpoints

The dashboard must work on all screen sizes:

| Breakpoint | Width | Layout Changes |
|---|---|---|
| Mobile | < 640px | Sidebar hidden (hamburger menu), 1-column grid, stacked cards |
| Tablet | 640-1024px | Sidebar collapsible, 2-column grid |
| Desktop | > 1024px | Full sidebar visible, 3-column grid |

```html
<!-- Responsive grid example with Tailwind -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
    {% for entry in entries %}
        <!-- Entry card -->
    {% endfor %}
</div>

<!-- Mobile-first sidebar toggle -->
<button id="sidebar-toggle" class="lg:hidden fixed bottom-4 right-4 bg-indigo-600 
        text-white p-3 rounded-full shadow-lg z-40">
    ☰
</button>
```

---

### 🎨 Design Tokens & Color Palette

```css
/* Recommended dark theme color system */
:root {
    /* Backgrounds */
    --bg-primary:    #0f172a;    /* Main background (slate-900) */
    --bg-secondary:  #1e293b;    /* Cards, sidebar (slate-800) */
    --bg-tertiary:   #334155;    /* Hover states (slate-700) */

    /* Text */
    --text-primary:  #f1f5f9;    /* Main text (slate-100) */
    --text-secondary:#94a3b8;    /* Muted text (slate-400) */
    --text-muted:    #64748b;    /* Very muted (slate-500) */

    /* Accent */
    --accent:        #6366f1;    /* Primary actions (indigo-500) */
    --accent-hover:  #4f46e5;    /* Hover state (indigo-600) */

    /* Semantic */
    --success:       #22c55e;    /* Green */
    --warning:       #f59e0b;    /* Amber */
    --danger:        #ef4444;    /* Red */
    --info:          #3b82f6;    /* Blue */

    /* Borders */
    --border:        #334155;    /* Card borders (slate-700) */
    --border-focus:  #6366f1;    /* Focus ring color */
}
```

---

### 🚨 Error Pages

#### 404 — Not Found

```python
# main.py — custom error handlers
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("errors/404.html", {
            "request": request
        }, status_code=404)
    if exc.status_code == 500:
        return templates.TemplateResponse("errors/500.html", {
            "request": request
        }, status_code=500)
    # For 302 (auth redirects), don't render template
    if exc.status_code == 302:
        return RedirectResponse(url=exc.headers.get("Location", "/login"))
    raise exc
```

**404 Page UI:**
```
┌──────────────────────────────────────────────────┐
│  🔐 Vaultify                                     │
├──────────────────────────────────────────────────┤
│                                                   │
│                    🔍                              │
│               404 — Not Found                     │
│                                                   │
│    The page you're looking for doesn't exist      │
│    or has been moved.                              │
│                                                   │
│         [ ← Back to Dashboard ]                   │
│                                                   │
└──────────────────────────────────────────────────┘
```

**500 Page UI:**
```
┌──────────────────────────────────────────────────┐
│  🔐 Vaultify                                     │
├──────────────────────────────────────────────────┤
│                                                   │
│                    ⚠️                              │
│           500 — Server Error                      │
│                                                   │
│    Something went wrong on our end.               │
│    Please try again later.                        │
│                                                   │
│         [ ← Back to Dashboard ]                   │
│                                                   │
└──────────────────────────────────────────────────┘
```

---

### 🔔 Toast / Flash Notification System

Every user action should give visible feedback. Here's the complete notification system:

**Types of notifications:**

| Type | Color | Icon | When Used |
|---|---|---|---|
| `success` | Green (`bg-emerald-600`) | ✅ | Entry saved, password copied, profile updated |
| `error` | Red (`bg-red-600`) | ❌ | Validation failed, wrong password, server error |
| `warning` | Amber (`bg-amber-600`) | ⚠️ | Entry deleted, folder deleted |
| `info` | Blue (`bg-blue-600`) | ℹ️ | Session expiring soon, tips |

**Server-side flash messages (Starlette sessions):**
```python
# Setting a flash message in any route:
request.session["flash"] = {
    "message": "Password entry saved!",
    "type": "success"   # success | error | warning | info
}
```

**Template rendering (base.html):**
```html
{% set flash = request.session.pop("flash", None) %}
{% if flash %}
<div id="flash-toast"
     class="fixed top-4 right-4 z-50 px-6 py-4 rounded-xl shadow-2xl text-white
            flex items-center gap-3 animate-slide-in
            {% if flash.type == 'success' %}bg-emerald-600
            {% elif flash.type == 'error' %}bg-red-600
            {% elif flash.type == 'warning' %}bg-amber-600
            {% else %}bg-blue-600{% endif %}">

    <!-- Icon -->
    {% if flash.type == 'success' %}✅
    {% elif flash.type == 'error' %}❌
    {% elif flash.type == 'warning' %}⚠️
    {% else %}ℹ️{% endif %}

    <!-- Message -->
    <span>{{ flash.message }}</span>

    <!-- Close button -->
    <button onclick="this.parentElement.remove()" class="ml-4 text-white/70 hover:text-white">✕</button>
</div>

<script>
    // Auto-dismiss after 4 seconds
    setTimeout(() => {
        const toast = document.getElementById("flash-toast");
        if (toast) {
            toast.classList.add("animate-slide-out");
            setTimeout(() => toast.remove(), 300);
        }
    }, 4000);
</script>
{% endif %}
```

**Client-side toast (for AJAX actions like copy/favorite):**
```javascript
// static/js/main.js

function showToast(message, type = "success") {
    // Remove existing toast
    const existing = document.getElementById("js-toast");
    if (existing) existing.remove();

    const colors = {
        success: "bg-emerald-600",
        error: "bg-red-600",
        warning: "bg-amber-600",
        info: "bg-blue-600"
    };
    const icons = { success: "✅", error: "❌", warning: "⚠️", info: "ℹ️" };

    const toast = document.createElement("div");
    toast.id = "js-toast";
    toast.className = `fixed top-4 right-4 z-50 px-6 py-4 rounded-xl shadow-2xl
                        text-white flex items-center gap-3 animate-slide-in ${colors[type]}`;
    toast.innerHTML = `
        <span>${icons[type]}</span>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="ml-4 text-white/70 hover:text-white">✕</button>
    `;
    document.body.appendChild(toast);

    // Auto-dismiss
    setTimeout(() => {
        toast.classList.add("opacity-0", "translate-x-4", "transition-all");
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}
```

**CSS animations (add to your Tailwind input.css or output.css):**
```css
@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
@keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
}
.animate-slide-in { animation: slideIn 0.3s ease-out; }
.animate-slide-out { animation: slideOut 0.3s ease-in; }
```

---

### 🖱️ Complete JavaScript Interaction Spec

All frontend JavaScript interactions in one place:

```javascript
// ══════════════════════════════════════════════════════
// static/js/main.js — Complete Vaultify Frontend Logic
// ══════════════════════════════════════════════════════

// ── 1. COPY PASSWORD ────────────────────────────────
async function copyPassword(entryId) {
    try {
        const response = await fetch(`/api/entries/${entryId}/password`);
        if (!response.ok) throw new Error("Failed to fetch password");
        const data = await response.json();
        await navigator.clipboard.writeText(data.password);
        showToast("Password copied to clipboard!", "success");
    } catch (err) {
        showToast("Failed to copy password", "error");
        console.error(err);
    }
}

// ── 2. COPY USERNAME ────────────────────────────────
function copyText(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast("Copied to clipboard!", "success");
    }).catch(() => {
        showToast("Failed to copy", "error");
    });
}

// ── 3. TOGGLE PASSWORD VISIBILITY ───────────────────
function togglePasswordVisibility(inputId, iconId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(iconId);
    if (input.type === "password") {
        input.type = "text";
        icon.textContent = "🙈";  // or swap SVG icon
    } else {
        input.type = "password";
        icon.textContent = "👁";
    }
}

// ── 4. REVEAL PASSWORD ON DETAIL PAGE ───────────────
async function revealPassword(entryId, spanId) {
    const span = document.getElementById(spanId);
    if (span.dataset.revealed === "true") {
        span.textContent = "••••••••••••";
        span.dataset.revealed = "false";
        return;
    }
    try {
        const response = await fetch(`/api/entries/${entryId}/password`);
        const data = await response.json();
        span.textContent = data.password;
        span.dataset.revealed = "true";
        // Auto-hide after 10 seconds for security
        setTimeout(() => {
            span.textContent = "••••••••••••";
            span.dataset.revealed = "false";
        }, 10000);
    } catch {
        showToast("Failed to reveal password", "error");
    }
}

// ── 5. TOGGLE FAVORITE ──────────────────────────────
async function toggleFavorite(entryId, iconElement) {
    try {
        const response = await fetch(`/api/entries/${entryId}/toggle-favorite`, {
            method: "POST"
        });
        const data = await response.json();
        iconElement.textContent = data.is_favorite ? "★" : "☆";
        iconElement.classList.toggle("text-yellow-400", data.is_favorite);
        iconElement.classList.toggle("text-gray-500", !data.is_favorite);
        showToast(
            data.is_favorite ? "Added to favorites!" : "Removed from favorites",
            "success"
        );
    } catch {
        showToast("Failed to update favorite", "error");
    }
}

// ── 6. PASSWORD GENERATOR ───────────────────────────
async function generatePassword() {
    const length = document.getElementById("pw-length")?.value || 16;
    const uppercase = document.getElementById("pw-uppercase")?.checked ?? true;
    const digits = document.getElementById("pw-digits")?.checked ?? true;
    const symbols = document.getElementById("pw-symbols")?.checked ?? true;

    try {
        const params = new URLSearchParams({ length, uppercase, digits, symbols });
        const response = await fetch(`/api/generate-password?${params}`);
        const data = await response.json();
        document.getElementById("password-field").value = data.password;
        showToast("Password generated!", "info");
    } catch {
        showToast("Failed to generate password", "error");
    }
}

// ── 7. PASSWORD STRENGTH METER ──────────────────────
function updatePasswordStrength(inputId, meterId, labelId) {
    const password = document.getElementById(inputId).value;
    const meter = document.getElementById(meterId);
    const label = document.getElementById(labelId);

    let score = 0;
    if (password.length >= 8) score++;
    if (password.length >= 12) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;

    const levels = [
        { width: "20%",  color: "bg-red-500",    text: "Very Weak" },
        { width: "40%",  color: "bg-orange-500",  text: "Weak" },
        { width: "60%",  color: "bg-yellow-500",  text: "Fair" },
        { width: "80%",  color: "bg-blue-500",    text: "Strong" },
        { width: "100%", color: "bg-green-500",   text: "Very Strong" }
    ];

    const level = levels[Math.min(score, 4)];
    meter.style.width = password.length === 0 ? "0%" : level.width;
    meter.className = `h-full rounded-full transition-all duration-300 ${level.color}`;
    label.textContent = password.length === 0 ? "" : level.text;
}

// ── 8. CONFIRM PASSWORD MATCH ───────────────────────
function checkPasswordMatch(passwordId, confirmId, indicatorId) {
    const password = document.getElementById(passwordId).value;
    const confirm = document.getElementById(confirmId).value;
    const indicator = document.getElementById(indicatorId);

    if (confirm.length === 0) {
        indicator.textContent = "";
    } else if (password === confirm) {
        indicator.textContent = "✅ Passwords match";
        indicator.className = "text-sm text-green-400 mt-1";
    } else {
        indicator.textContent = "❌ Passwords don't match";
        indicator.className = "text-sm text-red-400 mt-1";
    }
}

// ── 9. DELETE CONFIRMATION MODAL ────────────────────
function confirmDelete(entryId, title) {
    const modal = document.getElementById("delete-modal");
    const form = document.getElementById("delete-form");
    const titleSpan = document.getElementById("delete-title");

    titleSpan.textContent = title;
    form.action = `/vault/${entryId}/delete`;
    modal.classList.remove("hidden");
}

function closeModal() {
    document.getElementById("delete-modal").classList.add("hidden");
}

// Close modal on outside click
document.addEventListener("click", (e) => {
    const modal = document.getElementById("delete-modal");
    if (modal && e.target === modal) closeModal();
});

// Close modal on Escape key
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeModal();
});

// ── 10. MOBILE SIDEBAR TOGGLE ───────────────────────
function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("sidebar-overlay");
    sidebar.classList.toggle("-translate-x-full");
    overlay.classList.toggle("hidden");
}

// ── 11. KEYBOARD SHORTCUTS ──────────────────────────
document.addEventListener("keydown", (e) => {
    // Ctrl+K or Cmd+K → Focus search bar
    if ((e.ctrlKey || e.metaKey) && e.key === "k") {
        e.preventDefault();
        document.getElementById("search-input")?.focus();
    }
    // Ctrl+N → Go to new entry page
    if ((e.ctrlKey || e.metaKey) && e.key === "n") {
        e.preventDefault();
        window.location.href = "/vault/new";
    }
});
```

---

### ⏰ Session Timeout UX

When a user's JWT expires, they should be redirected gracefully — not shown a raw error:

```python
# auth/dependencies.py — Improved get_current_user
from jose import ExpiredSignatureError

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get("access_token")

    if not token:
        # Check if this is an API call or page request
        if request.url.path.startswith("/api/"):
            raise HTTPException(status_code=401, detail="Not authenticated")
        raise HTTPException(status_code=302, headers={"Location": "/login?message=Please+log+in"})

    try:
        payload = decode_token(token)
    except ExpiredSignatureError:
        # Token expired — clear cookie and redirect
        if request.url.path.startswith("/api/"):
            raise HTTPException(status_code=401, detail="Token expired")
        response = RedirectResponse(url="/login?message=Session+expired.+Please+log+in+again.", status_code=302)
        response.delete_cookie("access_token")
        raise HTTPException(status_code=302, headers={"Location": "/login?message=Session+expired"})
    except JWTError:
        raise HTTPException(status_code=302, headers={"Location": "/login"})

    if payload is None:
        raise HTTPException(status_code=302, headers={"Location": "/login"})

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=302, headers={"Location": "/login"})

    return user
```

**Optional: Client-side session warning (JavaScript):**
```javascript
// Warn user 5 minutes before session expires
// Requires passing token expiry time to template
const tokenExpiry = {{ token_expiry_timestamp | default(0) }};  // Unix timestamp

if (tokenExpiry > 0) {
    const warnAt = (tokenExpiry - 300) * 1000;  // 5 min before expiry
    const expireAt = tokenExpiry * 1000;

    setTimeout(() => {
        showToast("Your session will expire in 5 minutes. Save your work!", "warning");
    }, warnAt - Date.now());

    setTimeout(() => {
        window.location.href = "/login?message=Session+expired";
    }, expireAt - Date.now());
}
```

---

### 🧩 Reusable UI Component Library

These are the Tailwind component patterns you'll use repeatedly across templates:

#### Component: Input Field
```html
<!-- Reusable input component pattern -->
<div class="mb-4">
    <label for="{{ field_id }}" class="block text-sm font-medium text-gray-300 mb-1">
        {{ label }} {% if required %}<span class="text-red-400">*</span>{% endif %}
    </label>
    <input type="{{ type }}" id="{{ field_id }}" name="{{ field_name }}"
           value="{{ value or '' }}"
           placeholder="{{ placeholder }}"
           class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2.5
                  text-white placeholder-gray-500
                  focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent
                  transition-colors"
           {% if required %}required{% endif %} />
</div>
```

#### Component: Primary Button
```html
<button type="submit"
        class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold
               py-2.5 px-6 rounded-lg transition-colors duration-200
               focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2
               focus:ring-offset-gray-900 disabled:opacity-50 disabled:cursor-not-allowed">
    {{ button_text }}
</button>
```

#### Component: Entry Card
```html
<div class="bg-gray-800 border border-gray-700 rounded-xl p-5
            hover:border-indigo-500/50 hover:shadow-lg hover:shadow-indigo-500/5
            transition-all duration-200 group cursor-pointer">
    <div class="flex justify-between items-start mb-3">
        <a href="/vault/{{ entry.id }}" class="font-semibold text-lg text-white
                group-hover:text-indigo-400 transition-colors">
            {{ entry.title }}
        </a>
        <button onclick="toggleFavorite({{ entry.id }}, this)"
                class="text-xl {{ 'text-yellow-400' if entry.is_favorite else 'text-gray-600' }}
                       hover:scale-110 transition-transform">
            {{ '★' if entry.is_favorite else '☆' }}
        </button>
    </div>
    <p class="text-gray-400 text-sm mb-1">{{ entry.username or 'No username' }}</p>
    <p class="text-gray-600 text-xs mb-4 truncate">{{ entry.url or '' }}</p>
    <div class="flex gap-3 pt-3 border-t border-gray-700/50">
        <button onclick="copyPassword({{ entry.id }})"
                class="text-sm text-emerald-400 hover:text-emerald-300 flex items-center gap-1">
            📋 Copy
        </button>
        <a href="/vault/{{ entry.id }}"
           class="text-sm text-gray-400 hover:text-gray-300 flex items-center gap-1">
            👁 View
        </a>
        <a href="/vault/{{ entry.id }}/edit"
           class="text-sm text-gray-400 hover:text-gray-300 flex items-center gap-1">
            ✏️ Edit
        </a>
        <button onclick="confirmDelete({{ entry.id }}, '{{ entry.title }}')"
                class="text-sm text-red-400/60 hover:text-red-400 ml-auto">
            🗑️
        </button>
    </div>
</div>
```

#### Component: Empty State
```html
{% if not entries %}
<div class="text-center py-16">
    <div class="text-6xl mb-4">🔒</div>
    <h3 class="text-xl font-semibold text-gray-300 mb-2">Your vault is empty</h3>
    <p class="text-gray-500 mb-6">Start securing your passwords by adding your first entry.</p>
    <a href="/vault/new"
       class="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700
              text-white px-6 py-3 rounded-lg transition-colors font-medium">
        + Add Your First Password
    </a>
</div>
{% endif %}
```

---

### 📋 Master Feature ↔ Route Mapping Matrix

Every feature, which route implements it, which template renders it, and which JS function powers it:

| Feature | Route | Method | Template | JS Function | Auth |
|---|---|---|---|---|---|
| Landing page | `/` | GET | `landing.html` | — | ❌ |
| Show signup form | `/signup` | GET | `auth/signup.html` | `updatePasswordStrength()` | ❌ |
| Process signup | `/signup` | POST | — (redirect) | — | ❌ |
| Show login form | `/login` | GET | `auth/login.html` | — | ❌ |
| Process login | `/login` | POST | — (redirect) | — | ❌ |
| Logout | `/logout` | GET | — (redirect) | — | ✅ |
| Dashboard | `/vault/dashboard` | GET | `vault/dashboard.html` | — | ✅ |
| Search entries | `/vault/dashboard?search=X` | GET | `vault/dashboard.html` | — | ✅ |
| Filter by folder | `/vault/dashboard?folder_id=X` | GET | `vault/dashboard.html` | — | ✅ |
| Filter favorites | `/vault/dashboard?favorites_only=true` | GET | `vault/dashboard.html` | — | ✅ |
| New entry form | `/vault/new` | GET | `vault/entry_form.html` | `generatePassword()` | ✅ |
| Save new entry | `/vault/new` | POST | — (redirect) | — | ✅ |
| View entry | `/vault/{id}` | GET | `vault/entry_detail.html` | `revealPassword()` | ✅ |
| Edit entry form | `/vault/{id}/edit` | GET | `vault/entry_form.html` | `generatePassword()` | ✅ |
| Save edits | `/vault/{id}/edit` | POST | — (redirect) | — | ✅ |
| Delete entry | `/vault/{id}/delete` | POST | — (redirect) | `confirmDelete()` | ✅ |
| Copy password | `/api/entries/{id}/password` | GET | — (JSON) | `copyPassword()` | ✅ |
| Reveal password | `/api/entries/{id}/password` | GET | — (JSON) | `revealPassword()` | ✅ |
| Toggle favorite | `/api/entries/{id}/toggle-favorite` | POST | — (JSON) | `toggleFavorite()` | ✅ |
| Generate password | `/api/generate-password` | GET | — (JSON) | `generatePassword()` | ✅ |
| Vault stats | `/api/stats` | GET | — (JSON) | — | ✅ |
| List folders | `/folders` | GET | `folders/folders.html` | — | ✅ |
| Create folder | `/folders/new` | POST | — (redirect) | — | ✅ |
| Delete folder | `/folders/{id}/delete` | POST | — (redirect) | `confirmDelete()` | ✅ |
| View folder entries | `/vault/dashboard?folder_id=X` | GET | `vault/dashboard.html` | — | ✅ |
| Profile page | `/profile` | GET | `profile/profile.html` | — | ✅ |
| Update profile | `/profile/update` | POST | — (redirect) | — | ✅ |
| Change password | `/profile/change-password` | POST | — (redirect) | — | ✅ |
| 404 error | Any invalid URL | — | `errors/404.html` | — | ❌ |
| 500 error | Server error | — | `errors/500.html` | — | ❌ |

**Total: 10 pages · 28 routes · 11 JS functions · 3 models · 3 tables**

---

### 🛡️ Security UX Checklist

Things to implement for a secure user experience:

| # | Security Feature | Implementation | Priority |
|---|---|---|---|
| 1 | HTTP-only cookies for JWT | `response.set_cookie(..., httponly=True)` | 🔴 Critical |
| 2 | SameSite cookie attribute | `samesite="lax"` prevents CSRF | 🔴 Critical |
| 3 | IDOR protection on every endpoint | Always filter by `user_id == current_user.id` | 🔴 Critical |
| 4 | Password hashing with bcrypt | Never store plain master passwords | 🔴 Critical |
| 5 | Vault password encryption | Fernet encryption before DB storage | 🔴 Critical |
| 6 | Input validation (server-side) | Pydantic schemas + manual checks in routes | 🔴 Critical |
| 7 | Auto-hide revealed passwords | 10-second timeout in JavaScript | 🟡 Important |
| 8 | Secure password in cookie scope | `secure=True` in production (HTTPS) | 🟡 Important |
| 9 | Rate limiting on login | Prevent brute-force (use `slowapi` package) | 🟡 Important |
| 10 | Session timeout notification | Warn user before JWT expires | 🟢 Nice-to-have |
| 11 | Keyboard shortcut hints | Show Ctrl+K for search in UI | 🟢 Nice-to-have |

---

*End of Product Design Section — Section 16*

---
