# ShieldAgent# ShieldAgent# 



An AI-powered SOC 2 compliance automation platform that analyzes your security documents and produces evidence, gap analysis, risk scoring, and audit-ready PDF reports.



## Quick StartAn AI-powered SOC 2 compliance automation platform that analyzes your security documents and produces evidence, gap analysis, risk scoring, and audit-ready PDF reports.An AI-powered SOC 2 compliance automation platform that analyzes your security documents and produces evidence, gap analysis, risk scoring, and audit-ready PDF reports.



### 0. Prerequisites

- Docker & Docker Compose

- Python 3.11## Quick Start## Quick Start

- Node.js 18

- Google Gemini API key



### 1. Start Database Services### 0. Prerequisites### 0. Prerequisites

```bash

docker compose up postgres redis -d- Docker & Docker Compose- Python 3.11 (for local backend development).

```

- Python 3.11- Node.js 18 (for frontend development).

### 2. Configure Environment

```bash- Node.js 18- A Google Gemini API key (`GEMINIAPIKEY`).

cd backend

cp .env.example .env- Google Gemini API key

```

Edit `.env` and set:### 1. Start Database Services (Docker)

- `GEMINI_API_KEY` - Your Google Gemini API key

- `SECRET_KEY` - JWT signing key (any random string)### 1. Start Database Services```bash



### 3. Setup & Start Backend```bashdocker compose up postgres redis -d

```bash

cd backenddocker compose up postgres redis -d```

python -m venv venv

source venv/bin/activate```This starts PostgreSQL and Redis used by the backend + Celery worker.

pip install -r requirements.txt

alembic upgrade head

uvicorn main:app --reload --port 8000

```### 2. Configure Environment### 2. Configure Environment

✅ API: http://localhost:8000  

✅ Docs: http://localhost:8000/docs```bash```bash



### 4. Start Celery Worker (new terminal)cd backendcp .env.example .env

```bash

cd backendcp .env.example .env```

source venv/bin/activate

celery -A worker.celery_app worker --loglevel=info```Set at least:

```

Edit `.env` and set:- `GEMINIAPIKEY` (Google AI Studio key).

### 5. Start Frontend (new terminal)

```bash- `GEMINI_API_KEY` - Your Google Gemini API key- `SECRETKEY` (JWT signing key; use a strong random string).

cd frontend

npm install- `SECRET_KEY` - JWT signing key (any random string)

npm run dev

```### 3. Start Backend API

✅ Frontend: http://localhost:5173

### 3. Setup & Start Backend```bash

### Quick Start Script

If you have the backend venv already setup:```bashcd backend

```bash

./start.shcd backendpython -m venv venv

```

python -m venv venvsource venv/bin/activate

---

source venv/bin/activatepip install -r requirements.txt

## API Endpoints

pip install -r requirements.txtalembic upgrade head

**Authentication**

- `POST /api/auth/register` - Register new useralembic upgrade headuvicorn main:app --reload --port 8000

- `POST /api/auth/login` - Login (returns JWT)

- `GET /api/auth/me` - Current user infouvicorn main:app --reload --port 8000```



**Documents**```✅ API runs at: **http://localhost:8000**  

- `POST /api/documents/upload` - Upload document

- `GET /api/documents` - List documents✅ API: **http://localhost:8000**✅ API Docs at: **http://localhost:8000/docs**  

- `DELETE /api/documents/:id` - Delete document

✅ Docs: **http://localhost:8000/docs**Test it: `http://localhost:8000/api/health`

**Analysis Jobs**

- `POST /api/jobs/evidence-run` - Start analysis (quick/full scan)

- `GET /api/jobs/:id` - Job status

- `GET /api/jobs/:id/evidence` - Evidence results### 4. Start Celery Worker (new terminal)### 4. Start Celery Worker (new terminal)

- `GET /api/jobs/:id/gaps` - Compliance gaps

```bash```bash

**Controls**

- `GET /api/controls?scan_type=quick` - Quick scan controls (8)cd backendcd backend

- `GET /api/controls?scan_type=full` - Full scan controls (51)

source venv/bin/activatesource venv/bin/activate

**Reports**

- `GET /api/reports/:jobId/pdf` - Download PDF reportcelery -A worker.celery_app worker --loglevel=infocelery -A worker.celeryapp worker --loglevel=info



---``````



## Quick Scan Controls (8)Celery processes background analysis jobs.



| Control | Category | Description |### 5. Start Frontend (new terminal)

|---------|----------|-------------|

| CC6.1 | Logical Access | Logical Access Security |```bash### 5. Start Frontend (new terminal)

| CC6.2 | Logical Access | User Registration |

| CC6.3 | Logical Access | Access Removal |cd frontend```bash

| CC7.2 | System Operations | Security Monitoring |

| CC7.3 | System Operations | Incident Response |npm installcd frontend

| CC8.1 | Change Management | Change Management Process |

| CC9.1 | Risk Mitigation | Risk Mitigation Activities |npm run devnpm install  # first time only

| A1.2 | Availability | Backup and Recovery |

```npm run dev

---

✅ Frontend: **http://localhost:5173**```

## Project Structure

✅ Frontend runs at: **http://localhost:5173**

```

backend/### Quick Start Script (Alternative)

  api/           # Route handlers

  services/      # Business logic (Gemini AI, risk, PDF)If you already have the backend venv setup:***

  models/        # SQLAlchemy models

  worker/        # Celery tasks```bash

  main.py        # FastAPI app

frontend/./start.sh## API Endpoints

  src/

    pages/       # React pages```

    components/  # UI components

    hooks/       # Data fetchingBase URL: `http://localhost:8000/api`

docker-compose.yml

start.sh         # Quick start script---

stop.sh          # Stop all services

```**Health**



---## API Endpoints- `GET /api/health` — Health check.



## Testing



```bash**Authentication****Authentication**

# Backend tests

cd backend- `POST /api/auth/register` - Register new user- `POST /api/auth/register` — Register a new user.

pytest tests/unit/ -v

- `POST /api/auth/login` - Login (returns JWT)- `POST /api/auth/login` — Login and receive JWT token.

# Frontend build

cd frontend- `GET /api/auth/me` - Current user info- `GET /api/auth/me` — Get current user info (requires authentication).

npm run build

```


**Documents****Documents**

- `POST /api/documents/upload` - Upload document- `POST /api/documents/upload` — Upload a document (PDF, CSV, JSON, TXT, MD).

- `GET /api/documents` - List documents- `GET /api/documents` — List documents.

- `DELETE /api/documents/:id` - Delete document- `GET /api/documents/:id` — Get document details.

- `DELETE /api/documents/:id` — Delete a document.

**Analysis Jobs**

- `POST /api/jobs/evidence-run` - Start analysis (quick/full scan)**Jobs (Analysis)**

- `GET /api/jobs/:id` - Job status- `POST /api/jobs/evidence-run` — Start a compliance analysis (quick/full).

- `GET /api/jobs/:id/evidence` - Evidence results- `GET /api/jobs` — List jobs.

- `GET /api/jobs/:id/gaps` - Compliance gaps- `GET /api/jobs/:id` — Get job status/details.

- `GET /api/jobs/:id/evidence` — Get evidence results.

**Controls**- `GET /api/jobs/:id/gaps` — Get compliance gaps.

- `GET /api/controls?scan_type=quick` - Quick scan controls (8)

- `GET /api/controls?scan_type=full` - Full scan controls (51)**Controls**

- `GET /api/controls` — List SOC 2 controls.

**Reports**- `GET /api/controls/categories` — List control categories.

- `GET /api/reports/:jobId/pdf` - Download PDF report- `GET /api/controls/summary` — Control statistics.

- `GET /api/controls/:id` — Control details.

---

**Risk**

## Quick Scan Controls (8)- `POST /api/risk/calculate` — Calculate risk score from results.

- `GET /api/risk/demo` — Demo risk analysis.

| Control | Category | Description |- `POST /api/risk/remediation-plan` — Generate remediation plan.

|---------|----------|-------------|

| CC6.1 | Logical Access | Logical Access Security |**Reports**

| CC6.2 | Logical Access | User Registration |- `GET /api/reports/:jobId/pdf` — Download PDF compliance report.

| CC6.3 | Logical Access | Access Removal |

| CC7.2 | System Operations | Security Monitoring |***

| CC7.3 | System Operations | Incident Response |

| CC8.1 | Change Management | Change Management Process |## Using API in React (fetch)

| CC9.1 | Risk Mitigation | Risk Mitigation Activities |

| A1.2 | Availability | Backup and Recovery |```js

// Login (OAuth2 password flow style)

---const login = async (email, password) => {

  const res = await fetch('/api/auth/login', {

## Project Structure    method: 'POST',

    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },

```    body: new URLSearchParams({ username: email, password })

backend/  });

  api/           # Route handlers  return res.json();

  services/      # Business logic (Gemini AI, risk, PDF)};

  models/        # SQLAlchemy models

  worker/        # Celery tasks// Upload document

  main.py        # FastAPI appconst uploadDocument = async (file, token) => {

frontend/  const formData = new FormData();

  src/  formData.append('file', file);

    pages/       # React pages

    components/  # UI components  const res = await fetch('/api/documents/upload', {

    hooks/       # Data fetching    method: 'POST',

docker-compose.yml    headers: { Authorization: `Bearer ${token}` },

start.sh         # Quick start script    body: formData

stop.sh          # Stop all services  });

```  return res.json();

};

---```



## Testing***



```bash## Project Structure

# Backend tests

cd backend```

pytest tests/unit/ -vbackend/                 # FastAPI backend

  api/                   # Route handlers (auth, documents, jobs, risk, reports, controls)

# Frontend build  core/                  # Config, security, dependencies

cd frontend  models/                # SQLAlchemy models

npm run build  schemas/               # Pydantic schemas

```  services/              # Business logic (Gemini AI, risk, PDF, documents, jobs)

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
