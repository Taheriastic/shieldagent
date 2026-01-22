# ShieldAgent

An AI-powered SOC 2 compliance automation platform that analyzes your security documents and produces evidence, gap analysis, risk scoring, and audit-ready PDF reports.

## Quick Start

### 0. Prerequisites
- Python 3.11 (for local backend development).
- Node.js 18 (for frontend development).
- A Google Gemini API key (`GEMINIAPIKEY`).

### 1. Start Database Services (Docker)
```bash
docker compose up postgres redis -d
```
This starts PostgreSQL and Redis used by the backend + Celery worker.

### 2. Configure Environment
```bash
cp .env.example .env
```
Set at least:
- `GEMINIAPIKEY` (Google AI Studio key).
- `SECRETKEY` (JWT signing key; use a strong random string).

### 3. Start Backend API
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload --port 8000
```
✅ API runs at: **http://localhost:8000**  
✅ API Docs at: **http://localhost:8000/docs**  
Test it: `http://localhost:8000/api/health`

### 4. Start Celery Worker (new terminal)
```bash
cd backend
source venv/bin/activate
celery -A worker.celeryapp worker --loglevel=info
```
Celery processes background analysis jobs.

### 5. Start Frontend (new terminal)
```bash
cd frontend
npm install  # first time only
npm run dev
```
✅ Frontend runs at: **http://localhost:5173**

***

## API Endpoints

Base URL: `http://localhost:8000/api`

**Health**
- `GET /api/health` — Health check.

**Authentication**
- `POST /api/auth/register` — Register a new user.
- `POST /api/auth/login` — Login and receive JWT token.
- `GET /api/auth/me` — Get current user info (requires authentication).

**Documents**
- `POST /api/documents/upload` — Upload a document (PDF, CSV, JSON, TXT, MD).
- `GET /api/documents` — List documents.
- `GET /api/documents/:id` — Get document details.
- `DELETE /api/documents/:id` — Delete a document.

**Jobs (Analysis)**
- `POST /api/jobs/evidence-run` — Start a compliance analysis (quick/full).
- `GET /api/jobs` — List jobs.
- `GET /api/jobs/:id` — Get job status/details.
- `GET /api/jobs/:id/evidence` — Get evidence results.
- `GET /api/jobs/:id/gaps` — Get compliance gaps.

**Controls**
- `GET /api/controls` — List SOC 2 controls.
- `GET /api/controls/categories` — List control categories.
- `GET /api/controls/summary` — Control statistics.
- `GET /api/controls/:id` — Control details.

**Risk**
- `POST /api/risk/calculate` — Calculate risk score from results.
- `GET /api/risk/demo` — Demo risk analysis.
- `POST /api/risk/remediation-plan` — Generate remediation plan.

**Reports**
- `GET /api/reports/:jobId/pdf` — Download PDF compliance report.

***

## Using API in React (fetch)

```js
// Login (OAuth2 password flow style)
const login = async (email, password) => {
  const res = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ username: email, password })
  });
  return res.json();
};

// Upload document
const uploadDocument = async (file, token) => {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch('/api/documents/upload', {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: formData
  });
  return res.json();
};
```

***

## Project Structure

```
backend/                 # FastAPI backend
  api/                   # Route handlers (auth, documents, jobs, risk, reports, controls)
  core/                  # Config, security, dependencies
  models/                # SQLAlchemy models
  schemas/               # Pydantic schemas
  services/              # Business logic (Gemini AI, risk, PDF, documents, jobs)
  worker/                # Celery configuration + tasks
  alembic/               # Database migrations
  tests/                 # Unit + integration tests
  main.py                # FastAPI app entry
frontend/                # React + TypeScript + Vite frontend
  src/
docker-compose.yml       # Postgres + Redis + services
sampledocuments/         # Example docs for testing
docs/                    # Contributing / usage docs
```
