# Keeply — Secure Password Manager & Browser Extension

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?style=flat-square)](https://fastapi.tiangolo.com/)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Vercel-000000?style=flat-square&logo=vercel)](https://keeply-liard.vercel.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](https://opensource.org/licenses/MIT)

Keeply is an open-source, self-hostable password manager with a clean web UI and a companion browser extension that automatically captures credentials as you log into sites and saves them to your vault in one click.

**Live Demo:** [keeply-liard.vercel.app](https://keeply-liard.vercel.app)

---

## How Keeply Secures Your Data

| Layer | What Keeply Does |
|---|---|
| **Vault passwords** | Encrypted at rest using **AES-256-GCM** — authenticated encryption with a unique random nonce per entry. Nothing is ever written in plain-text. |
| **Master password** | Hashed using **bcrypt** (salted, work-factor tunable). Cannot be reversed or looked up in a rainbow table. |
| **API access** | Protected by signed **JWT bearer tokens** (`HS256`), scoped per-user, with configurable expiry. |

---

## Key Features

- **Browser extension** — auto-captures login form submissions and saves to vault
- **Secure email recovery** — password reset via `aiosmtplib` with spam-resistant headers
- **Responsive UI** — works seamlessly across mobile, tablet, and desktop
- **Folders & favourites** — organise vault entries with custom folders and icons
- **Password generator** — built-in generator inside the vault entry form

---

## Browser Extension

The **Keeply Helper** extension runs in Chrome and Edge (Manifest V3). It silently detects when you submit a login form and queues the credentials for one-click saving.

### Install the Extension

1. Download the **Keeply Extension** from the project folder or the **[Google Drive folder](https://drive.google.com/drive/folders/14dhHNQyaRP8oGkEaLduTT8ITKxGXVJ5P?usp=sharing)**.
   - Extract the downloaded files (if they are in a ZIP) and locate the `keeply-extension/` folder.
2. Open Chrome and go to `chrome://extensions` (or `edge://extensions`).
3. Enable **Developer mode** (toggle in the top-right corner).
4. Click **Load unpacked** and select the `keeply-extension/` folder.
5. Pin the **Keeply** icon to your toolbar for quick access.

### Connect to Your Account

1. Click the **Keeply icon** in the toolbar.
2. Set the **Server URL**:
   - **Production** → `https://keeply-liard.vercel.app` *(default)*
   - **Local dev** → `http://127.0.0.1:8000`
3. Enter your **email** and **master password**, then click **Link Extension**.
4. The status dot turns green — you're connected.

### Capture & Save Credentials

1. Visit any site with a login form (GitHub, Netflix, etc.).
2. Fill in your credentials and submit.
3. Open the Keeply extension — a pending credential card appears.
4. Click **Save to Vault** to store it, or **Dismiss** to discard.

---

## API Documentation

FastAPI exposes interactive docs out of the box. Start the server, then visit:

| Interface | URL |
|---|---|
| **Swagger UI** | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) |
| **ReDoc** | [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) |

Click **Authorize** in Swagger UI and paste your JWT token to test any protected endpoint interactively.

---

## Running Locally

### Prerequisites
- Python **3.10+**
- A PostgreSQL database (e.g. [Supabase](https://supabase.com/) free tier works great)

### Setup Steps

**1. Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate.bat       # Windows
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure environment variables**
```bash
cp .env.example .env
```
Fill in `.env` with your database credentials, a generated `SECRET_KEY`, and SMTP settings. See `.env.example` for all fields.

You can generate a secure, random `SECRET_KEY` using the following Python command:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**4. Apply database migrations**
```bash
alembic upgrade head
```

**5. Start the server**
```bash
uvicorn main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) — register an account and start using your local vault.

---

## Project Structure

```
├── config/             # Settings & environment loader
├── database/           # Async SQLAlchemy engine & session
├── keeply-extension/   # Chrome/Edge Manifest V3 extension
├── models/             # ORM models (User, VaultEntry, Folder)
├── routers/            # Route handlers (auth, vault, folders, profile)
├── schemas/            # Pydantic request/response schemas
├── services/           # Business logic (auth, vault, folders)
├── static/             # CSS, JS, icons
├── templates/          # Jinja2 HTML templates
├── utils/              # Encryption & email helpers
├── main.py             # FastAPI application entrypoint
└── requirements.txt    # Python dependencies
```

## Contributing

Contributions are welcome! If you want to help improve Keeply:
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

Please make sure to run code checks locally and write tests where applicable.

---

## Acknowledgments

Special thanks to the open-source projects and hosting platforms that make Keeply possible:
- **[FastAPI](https://fastapi.tiangolo.com/)** — for the high-performance, developer-friendly backend API framework.
- **[Vercel](https://vercel.com/)** — for hosting the production application.
- **[SQLAlchemy](https://www.sqlalchemy.org/)** & **[Alembic](https://alembic.sqlalchemy.org/)** — for the database ORM and migration toolkit.
- **[Supabase](https://supabase.com/)** — for the managed PostgreSQL database instance.
- **[Tailwind CSS](https://tailwindcss.com/)** — for clean, utility-first UI styling.
- **[Jinja2](https://jinja.palletsprojects.com/)** — for server-side HTML template rendering.
