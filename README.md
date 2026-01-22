# ShieldAgent# 🛡️ ShieldAgent<p align="center"># ShieldAgent 🛡️



An AI-powered SOC 2 compliance automation platform that analyzes your security documents and provides instant compliance insights. Upload policies, configurations, and documentation — get comprehensive gap analysis, risk scores, and audit-ready reports.



**AI-Powered SOC 2 Compliance Automation Platform**  <img src="frontend/public/shield.svg" alt="ShieldAgent Logo" width="120" height="120">

## Documentation Guide



This main README provides a high-level overview of the ShieldAgent project, including:

- **Quick Start Instructions**: Steps to run the application using Docker.ShieldAgent automates SOC 2 evidence collection by analyzing your security documents using AI. Upload your policies, configurations, and documentation — get instant compliance insights.</p>**AI-Powered SOC 2 Compliance Automation Platform**

- **Project Structure**: A breakdown of the folder and file organization.

- **API Endpoints**: A summary of the available backend API routes.

- **Environment Variables**: Key configuration options for the project.

- **Alternate Development Setup**: Instructions for running the project locally without Docker.[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)



For more detailed information about specific parts of the project, refer to the following:[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)



- **Frontend Documentation**: The `frontend/README.md` contains details about the React-based frontend, including its architecture, available scripts, development setup, and testing. It provides insights into component structure, hooks, and state management patterns.[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com)<h1 align="center">🛡️ ShieldAgent</h1>ShieldAgent automates SOC 2 evidence collection by analyzing your security documents, configurations, and policies using AI. It covers all 5 Trust Service Categories with 50+ controls for comprehensive compliance assessment.



- **Backend Documentation**: The `backend/README.md` provides an in-depth look at the FastAPI-based backend, including its project structure, API endpoints, authentication, database setup, and testing. It also includes instructions for running the backend locally or with Docker.[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org)



Testing instructions for both the frontend and backend are detailed in their respective READMEs.



---

## Deployment Guide

<p align="center">![License](https://img.shields.io/badge/license-MIT-blue.svg)

### Quick Start (Docker)

## 📋 Table of Contents

The easiest way to run the application is with Docker.

  <strong>AI-Powered SOC 2 Compliance Automation Platform</strong>![Python](https://img.shields.io/badge/python-3.11+-blue.svg)

0. **Prerequisites**

- [Docker](https://docs.docker.com/get-docker/)- [Features](#-features)

- [Docker Compose](https://docs.docker.com/compose/install/)

- [Google Gemini API Key](https://makersuite.google.com/app/apikey)- [Quick Start](#-quick-start)</p>![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)



1. **Set up environment variables:**- [Architecture](#-architecture)

   ```bash

   cp .env.example .env- [SOC 2 Coverage](#-soc-2-coverage)![React](https://img.shields.io/badge/React-18-blue.svg)

   ```

   Edit `.env` and configure:- [API Reference](#-api-reference)

   - `GEMINI_API_KEY` - Your Google Gemini API key (required)

   - `SECRET_KEY` - JWT signing key (required, min 32 chars)- [Development](#-development)<p align="center">![SOC 2](https://img.shields.io/badge/SOC_2-50%2B_Controls-success.svg)



2. **Build, create and start containers:**- [Testing](#-testing)

   ```bash

   docker compose up- [Deployment](#-deployment)  <a href="#-features">Features</a> •

   ```

   Or use the start script:

   ```bash

   ./start.sh---  <a href="#-quick-start">Quick Start</a> •## 🎯 Features

   ```



What you get:

- PostgreSQL 16 on `5432`## ✨ Features  <a href="#-architecture">Architecture</a> •

- Redis 7 on `6379`

- Backend API on `http://localhost:8000`

- Frontend on `http://localhost:5173`

- API Docs at `http://localhost:8000/docs`| Feature | Description |  <a href="#-api-reference">API</a> •- **📄 Document Upload**: Upload PDFs, CSVs, JSON, and text configuration files

- Health at `http://localhost:8000/api/health` → `{"status": "healthy"}`

|---------|-------------|

`docker-compose.yml` wires all environment variables (including `DATABASE_URL`) for you.

| 📄 **Document Upload** | Support for PDF, CSV, JSON, TXT, and MD files |  <a href="#-soc-2-coverage">SOC 2 Coverage</a> •- **🤖 AI-Powered Analysis**: Uses Google Gemini to analyze security policies and evidence



### Continued Operations with Docker| 🤖 **AI Analysis** | Google Gemini-powered document analysis |



#### Making Changes and Switching Branches| 🔍 **51 Controls** | Complete SOC 2 Trust Service Criteria coverage |  <a href="#-testing">Testing</a>- **🔍 Comprehensive Coverage**: 50+ SOC 2 controls across all Trust Service Categories

Docker caches image layers, so when switching branches or making changes, Docker may use cached images that contain older code. To ensure you're running the latest code:

| ⚡ **Quick Scan** | Fast 8-control assessment for rapid insights |

```bash

# Stop containers and remove volumes (use -v if you expect DB schema changes)| 🔄 **Full Scan** | Comprehensive 51-control deep analysis |</p>- **📊 Risk Scoring**: Intelligent risk calculation with weighted category scores

docker compose down -v

| 📊 **Risk Scoring** | Weighted risk calculation across categories |

# Rebuild images without cache to ensure fresh builds

docker compose build --no-cache| 🚨 **Gap Analysis** | Identifies gaps with severity ratings |- **📈 Compliance Dashboard**: Real-time compliance scores and evidence tracking



# Start services with rebuilt images| 📋 **Remediation** | Prioritized action plans with time estimates |

docker compose up

```| 📑 **PDF Reports** | Audit-ready compliance reports |<p align="center">- **🚨 Gap Analysis**: Identifies compliance gaps with severity ratings



#### Docker Commands



```bash---  <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python">- **📋 Remediation Tracking**: Prioritized remediation plans with time estimates

# Start services (foreground)

docker compose up



# Start services (background)## 🚀 Quick Start  <img src="https://img.shields.io/badge/FastAPI-0.109-green.svg" alt="FastAPI">- **📑 PDF Reports**: Generate audit-ready compliance reports

docker compose up -d



# View logs

docker compose logs -f### Prerequisites  <img src="https://img.shields.io/badge/React-18-blue.svg" alt="React">- **⚡ Quick Scan Mode**: Fast assessment using 8 critical controls



# Stop services

docker compose down

- Docker & Docker Compose  <img src="https://img.shields.io/badge/TypeScript-5.0-blue.svg" alt="TypeScript">- **🔄 Full Scan Mode**: Comprehensive analysis of all 50+ controls

# Rebuild after code changes

docker compose up --build- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))



# Delete the database (for reinitialization)  <img src="https://img.shields.io/badge/SOC_2-51_Controls-success.svg" alt="SOC 2">

docker compose down -v

```### 1. Clone & Configure



  <img src="https://img.shields.io/badge/Test_Coverage-Comprehensive-brightgreen.svg" alt="Tests">## 🏗️ Architecture

### Environment Variables

```bash

The application can be customized using environment variables. A template file `.env.example` is provided with all available options.

git clone https://github.com/Taheriastic/shieldagent.git  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">

#### Available Environment Variables

cd shieldagent

| Variable | Description | Default |

|----------|-------------|---------|</p>```

| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://shieldagent:shieldagent@localhost:5432/shieldagent` |

| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |# Create environment file

| `SECRET_KEY` | JWT signing key (**MUST change in production**) | `dev-secret-key-change-in-production` |

| `GEMINI_API_KEY` | Google Gemini API key (**required**) | None |cp .env.example .env┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐

| `DEBUG` | Enable debug mode | `False` |

| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | `http://localhost:5173` |```

| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration time | `30` |

---│  React Frontend │────▶│  FastAPI Backend │────▶│  PostgreSQL DB  │

**⚠️ Security Warning**: Never commit your `.env` file to version control. The `.env` file is already in `.gitignore`.

Edit `.env` and add your Gemini API key:

---

└─────────────────┘     └────────┬────────┘     └─────────────────┘

## Alternate Development Setup

```env

For development, you may want to run the services directly on your machine instead of in Docker containers.

GEMINI_API_KEY=your_api_key_here## 📋 Table of Contents                                 │

**Note**: This requires more setup than using Docker. The Docker approach (above) is recommended for simplicity.

SECRET_KEY=your_secret_key_here

### 0. Prerequisites

```                                 ▼

1. **Start PostgreSQL and Redis** (required for backend):

   ```bash

   docker compose up postgres redis -d

   ```### 2. Start with Docker- [Overview](#-overview)                        ┌─────────────────┐

   This starts only the database containers. The backend and frontend will run directly on your machine.



2. **Set up environment variables**:

   ```bash```bash- [Features](#-features)                        │   Redis Queue   │

   cp .env.example .env

   # Edit .env with your GEMINI_API_KEY# Start all services

   ```

docker-compose up -d- [Quick Start](#-quick-start)                        └────────┬────────┘

### 1. Start Backend API



```bash

cd backend# Or use the start script- [Architecture](#-architecture)                                 │



# Create virtual environment./start.sh

python -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate```- [SOC 2 Coverage](#-soc-2-coverage)                                 ▼



# Install dependencies

pip install -r requirements.txt

### 3. Access the App- [API Reference](#-api-reference)                        ┌─────────────────┐     ┌─────────────────┐

# Run database migrations

alembic upgrade head



# Start server| Service | URL |- [Frontend Guide](#-frontend-guide)                        │  Celery Worker  │────▶│  Google Gemini  │

uvicorn main:app --reload --port 8000

```|---------|-----|



✅ API runs at: **http://localhost:8000**| Frontend | http://localhost:5173 |- [Configuration](#-configuration)                        └─────────────────┘     └─────────────────┘



Test it: Open http://localhost:8000/docs in your browser| Backend API | http://localhost:8000 |



### 2. Start Celery Worker (in new terminal)| API Docs | http://localhost:8000/docs |- [Testing](#-testing)```



```bash

cd backend

source venv/bin/activate### 4. First Steps- [Deployment](#-deployment)

celery -A worker.celery_app worker --loglevel=info

```



✅ Worker processes background analysis jobs1. **Sign up** at http://localhost:5173/signup- [Contributing](#-contributing)## 🚀 Quick Start



### 3. Start Frontend (in new terminal)2. **Upload** your security documents (policies, configs, etc.)



```bash3. **Run analysis** — choose Quick Scan (8 controls) or Full Scan (51 controls)

cd frontend

npm install  # first time only4. **Review results** and download your compliance report

npm run dev

```---### Prerequisites



✅ Frontend runs at: **http://localhost:5173**---



---



## API Endpoints## 🏗️ Architecture



All endpoints start with `/api/`:## 🌟 Overview- Docker & Docker Compose



**Authentication:**```

- `POST /api/auth/register` - Register a new user

- `POST /api/auth/login` - Login and receive JWT token┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐- Python 3.11+ (for local development)

- `GET /api/auth/me` - Get current user info (requires authentication)

│  React + Vite   │────▶│  FastAPI        │────▶│  PostgreSQL     │

**Documents:**

- `POST /api/documents/upload` - Upload a document (PDF, CSV, JSON, TXT, MD)│  (Frontend)     │     │  (Backend)      │     │  (Database)     │**ShieldAgent** is a comprehensive AI-powered platform that automates SOC 2 compliance evidence collection and gap analysis. Upload your security policies, configurations, and documentation, and let our AI analyze them against all 51 SOC 2 Trust Service Criteria controls.- Node.js 18+ (for frontend development)

- `GET /api/documents` - List all documents for current user

- `GET /api/documents/:id` - Get specific document└─────────────────┘     └────────┬────────┘     └─────────────────┘

- `DELETE /api/documents/:id` - Delete a document

                                 │

**Analysis Jobs:**

- `POST /api/jobs/evidence-run` - Start compliance analysis                                 ▼

- `GET /api/jobs` - List all jobs for current user

- `GET /api/jobs/:id` - Get job status and details                        ┌─────────────────┐### Why ShieldAgent?### Using Docker (Recommended)

- `GET /api/jobs/:id/evidence` - Get evidence results

- `GET /api/jobs/:id/gaps` - Get compliance gaps                        │  Redis + Celery │



**Risk & Reports:**                        │  (Task Queue)   │

- `GET /api/risk/:job_id/score` - Get risk scores by category

- `GET /api/risk/:job_id/remediation` - Get prioritized remediation plan                        └────────┬────────┘

- `GET /api/reports/:job_id/pdf` - Download PDF compliance report

                                 │| Traditional Compliance | With ShieldAgent |```bash

**Controls:**

- `GET /api/controls` - List all SOC 2 controls                                 ▼

- `GET /api/controls/:id` - Get specific control details

                        ┌─────────────────┐|----------------------|------------------|# Clone the repository

**Health:**

- `GET /api/health` - Health check endpoint                        │  Google Gemini  │



---                        │  (AI Analysis)  │| 📅 Weeks of manual review | ⚡ Minutes with AI analysis |git clone https://github.com/Taheriastic/shieldagent.git



## Troubleshooting                        └─────────────────┘



Here are some common issues and their resolutions:```| 📝 Spreadsheet tracking | 📊 Real-time dashboard |cd shieldagent



- **Port Already in Use**:

  - Stop any processes using the conflicting port or change the port in the `.env` file.

### Tech Stack| 🔍 Point-in-time audits | 🔄 Continuous monitoring |

- **Database Connection Issues**:

  - Verify the `DATABASE_URL` is correct and PostgreSQL is running.

  - Check with: `docker compose ps` to see container status.

| Layer | Technology || 💰 Expensive consultants | 🤖 Automated assessment |# Copy environment file

- **Redis Connection Issues**:

  - Ensure Redis is running: `docker compose up redis -d`|-------|------------|

  - Check the `REDIS_URL` environment variable.

| Frontend | React 18, TypeScript, Vite, TailwindCSS || 📋 Paper-based evidence | 🔗 Direct document linking |cp backend/.env.example backend/.env

- **Gemini API Errors**:

  - Verify your `GEMINI_API_KEY` is valid and has quota remaining.| Backend | Python 3.11, FastAPI, SQLAlchemy, Pydantic |

  - Check the backend logs: `docker compose logs backend`

| Database | PostgreSQL 16 |

- **Frontend Not Loading**:

  - Check the browser console for errors.| Queue | Redis 7, Celery |

  - Ensure the frontend service is running: `docker compose logs frontend`

| AI | Google Gemini 1.5 Flash |---# Edit .env and add your Gemini API key

- **Analysis Jobs Stuck in "pending"**:

  - Ensure the Celery worker is running.| Auth | JWT (OAuth2 Password Flow) |

  - Check worker logs: `docker compose logs celery`

# GEMINI_API_KEY=your-api-key-here

---

---

## Architecture Overview

## ✨ Features

The ShieldAgent application follows a modular architecture with clear separation between frontend, backend, and infrastructure layers:

## 🔒 SOC 2 Coverage

```

┌─────────────────────────────────────────────────────────────────┐# Start all services

│                      Docker Containers                          │

│                                                                 │ShieldAgent covers all **5 Trust Service Categories** with **51 controls**:

│  ┌───────────────────────────────────────────────────────────┐  │

│  │                  Frontend (React + Vite)                  │  │### 🔍 Document Analysismake docker-up

│  │  - User Interface with TailwindCSS                        │  │

│  │  - API Communication via Axios                            │  │### Trust Service Categories

│  │  - State Management with React Hooks                      │  │

│  │  - TypeScript for Type Safety                             │  │- **Multi-format Support**: PDF, CSV, JSON, TXT, and Markdown files

│  └───────────────────────────────────────────────────────────┘  │

│                              │                                  │| Category | Controls | Description |

│                              ▼                                  │

│  ┌───────────────────────────────────────────────────────────┐  │|----------|----------|-------------|- **AI-Powered Review**: Google Gemini analyzes documents against controls# API will be available at http://localhost:8000

│  │                   Backend (FastAPI)                       │  │

│  │  - REST API Endpoints (/api/*)                            │  │| **CC** - Common Criteria | 29 | Security policies, access controls, risk management |

│  │  - JWT Authentication (OAuth2 Password Flow)              │  │

│  │  - Pydantic Schema Validation                             │  │| **A** - Availability | 3 | System uptime, disaster recovery, capacity planning |- **Evidence Extraction**: Automatic quote extraction from documents# Docs at http://localhost:8000/docs

│  │  - Async SQLAlchemy ORM                                   │  │

│  └───────────────────────────────────────────────────────────┘  │| **PI** - Processing Integrity | 5 | Data accuracy, completeness, authorization |

│                              │                                  │

│              ┌───────────────┼───────────────┐                  │| **C** - Confidentiality | 2 | Data classification, encryption, protection |- **Batch Processing**: Analyze multiple documents simultaneously```

│              ▼               ▼               ▼                  │

│  ┌─────────────────┐ ┌─────────────┐ ┌─────────────────────┐   │| **P** - Privacy | 8 | Personal data handling, consent, retention |

│  │   PostgreSQL    │ │    Redis    │ │   Celery Worker     │   │

│  │  - User Data    │ │  - Task     │ │  - Background Jobs  │   │

│  │  - Documents    │ │    Queue    │ │  - AI Analysis      │   │

│  │  - Evidence     │ │  - Caching  │ │  - Gemini API Calls │   │### Scan Modes

│  │  - Jobs         │ │             │ │                     │   │

│  └─────────────────┘ └─────────────┘ └─────────────────────┘   │### 📊 Compliance Dashboard### Local Development

│                                              │                  │

│                                              ▼                  │**Quick Scan (8 controls)** — Fast assessment covering critical areas:

│                              ┌───────────────────────────────┐  │

│                              │      Google Gemini API        │  │- CC6.1: Logical Access Security- **Real-time Scores**: Overall compliance percentage and risk level

│                              │  - Document Analysis          │  │

│                              │  - Evidence Extraction        │  │- CC6.2: User Registration & Authorization

│                              │  - Gap Identification         │  │

│                              └───────────────────────────────┘  │- CC6.3: Access Removal- **Category Breakdown**: Scores by Trust Service Category```bash

└─────────────────────────────────────────────────────────────────┘

```- CC7.2: Security Monitoring



### Data Flow- CC8.1: Change Management- **Gap Visualization**: Interactive charts showing compliance gaps# Install backend dependencies



1. **User Authentication**: User registers/logs in → Backend validates → JWT token issued- A1.2: Disaster Recovery

2. **Document Upload**: User uploads file → Backend stores in filesystem → Metadata saved to PostgreSQL

3. **Analysis Request**: User starts scan → Job created → Task queued in Redis- C1.1: Confidentiality Policies- **Trend Tracking**: Historical compliance score trendscd backend

4. **AI Processing**: Celery worker picks up task → Sends to Gemini API → Results stored

5. **Results Display**: Frontend polls job status → Fetches evidence/gaps → Renders dashboard- P3.1: Data Collection Practices



### Key Featurespython -m venv venv



- **Frontend**:**Full Scan (51 controls)** — Complete SOC 2 compliance check

  - Built with React 18 and TypeScript

  - Vite for fast development and builds### 🎯 Risk Assessmentsource venv/bin/activate  # On Windows: venv\Scripts\activate

  - TailwindCSS for styling

  - Custom hooks for authentication and API calls---



- **Backend**:- **Weighted Scoring**: Industry-standard category weightingpip install -r requirements.txt

  - FastAPI with async/await support

  - SQLAlchemy 2.0 with async sessions## 📡 API Reference

  - Pydantic for request/response validation

  - Alembic for database migrations- **Risk Levels**: Critical, High, Medium, Low, Minimal classifications



- **AI Analysis**:### Authentication

  - Google Gemini 1.5 Flash for document analysis

  - 51 SOC 2 controls mapped to Trust Service Categories- **Audit Readiness**: Automated readiness assessment# Start PostgreSQL and Redis (via Docker)

  - Quick scan (8 controls) and full scan (51 controls) modes

  - Weighted risk scoring algorithm```bash



- **Infrastructure**:# Register- **Remediation Estimates**: Time-to-fix calculationsdocker-compose up -d postgres redis

  - PostgreSQL for persistent storage

  - Redis for task queue and cachingPOST /api/auth/register

  - Celery for background job processing

  - Docker Compose for orchestration{



---  "email": "user@example.com",



## Project Structure  "password": "securepassword",### 📋 Remediation Tracking# Run the API



```  "full_name": "John Doe"

shieldagent/

├── backend/}- **Prioritized Tasks**: Gaps sorted by severity and impactuvicorn main:app --reload

│   ├── api/                  # API route handlers

│   │   ├── auth.py           # Authentication endpoints

│   │   ├── documents.py      # Document management

│   │   ├── jobs.py           # Analysis jobs# Login- **Progress Tracking**: Task completion monitoring

│   │   ├── reports.py        # PDF generation

│   │   ├── risk.py           # Risk scoringPOST /api/auth/login

│   │   ├── controls.py       # SOC 2 controls

│   │   └── health.py         # Health checksContent-Type: application/x-www-form-urlencoded- **Time Estimates**: Hours-to-remediate calculations# In another terminal, start Celery worker

│   ├── core/                 # Core configuration

│   │   ├── config.py         # Settings management

│   │   ├── security.py       # JWT & password hashing

│   │   └── dependencies.py   # FastAPI dependenciesusername=user@example.com&password=securepassword- **Recommendations**: AI-generated remediation suggestionscelery -A worker.celery_app worker --loglevel=info

│   ├── models/               # SQLAlchemy models

│   ├── schemas/              # Pydantic schemas

│   ├── services/             # Business logic

│   │   ├── gemini_service.py # AI integration# Response```

│   │   ├── risk_calculator.py# Risk scoring

│   │   └── soc2_controls.py  # Control definitions{

│   ├── worker/               # Celery configuration

│   ├── alembic/              # Database migrations  "access_token": "eyJ...",### 📑 Reporting

│   ├── tests/                # Unit tests

│   ├── main.py               # FastAPI application  "token_type": "bearer"

│   └── requirements.txt

├── frontend/}- **PDF Reports**: Audit-ready compliance reports## 📋 SOC 2 Trust Service Categories Coverage

│   ├── src/

│   │   ├── components/       # Reusable UI components```

│   │   ├── pages/            # Page components

│   │   ├── hooks/            # Custom React hooks- **Executive Summaries**: High-level findings for leadership

│   │   ├── lib/              # Utilities and API client

│   │   └── types/            # TypeScript definitions### Documents

│   ├── package.json

│   └── vite.config.ts- **Evidence Packages**: Compiled evidence for auditors### Security (Common Criteria) - 33 Controls

├── sample_documents/         # Example files for testing

├── docker-compose.yml```bash

├── Makefile

├── start.sh# Upload document- **Gap Reports**: Detailed gap analysis documentation| Category | Controls | Description |

├── stop.sh

└── README.mdPOST /api/documents/upload

```

Authorization: Bearer <token>|----------|----------|-------------|

---

Content-Type: multipart/form-data

## SOC 2 Coverage

---| CC1 - Control Environment | CC1.1-CC1.5 | Integrity, board oversight, org structure, competence, accountability |

ShieldAgent covers all **5 Trust Service Categories** with **51 controls**:

file: <your-document.pdf>

| Category | Controls | Description |

|----------|----------|-------------|| CC2 - Communication | CC2.1-CC2.3 | Information quality, internal/external communication |

| **CC** - Common Criteria | 29 | Security policies, access controls, risk management |

| **A** - Availability | 3 | System uptime, disaster recovery, capacity planning |# List documents

| **PI** - Processing Integrity | 5 | Data accuracy, completeness, authorization |

| **C** - Confidentiality | 2 | Data classification, encryption, protection |GET /api/documents## 🚀 Quick Start| CC3 - Risk Assessment | CC3.1-CC3.4 | Risk objectives, identification, fraud risk, change risk |

| **P** - Privacy | 8 | Personal data handling, consent, retention |

Authorization: Bearer <token>

### Scan Modes

```| CC4 - Monitoring | CC4.1-CC4.2 | Ongoing monitoring, deficiency communication |

**Quick Scan (8 controls)** — Fast assessment (~30 seconds):

- CC6.1: Logical Access Security

- CC6.2: User Registration & Authorization

- CC6.3: Access Removal### Analysis Jobs### Prerequisites| CC5 - Control Activities | CC5.1-CC5.3 | Control selection, technology controls, policy implementation |

- CC7.2: Security Monitoring

- CC8.1: Change Management

- A1.2: Disaster Recovery

- C1.1: Confidentiality Policies```bash| CC6 - Logical/Physical Access | CC6.1-CC6.8 | Access security, registration, removal, restrictions, boundaries |

- P3.1: Data Collection Practices

# Start analysis

**Full Scan (51 controls)** — Comprehensive analysis (~2-5 minutes)

POST /api/jobs/evidence-run- **Docker & Docker Compose** (recommended)| CC7 - System Operations | CC7.1-CC7.5 | Vulnerability detection, monitoring, incident response, recovery |

---

Authorization: Bearer <token>

## Testing

{- **Python 3.11+** (for local development)| CC8 - Change Management | CC8.1 | Change management process |

### Backend Tests

  "document_ids": ["uuid-1", "uuid-2"],

```bash

cd backend  "scan_type": "quick"  # or "full"- **Node.js 18+** (for frontend development)| CC9 - Risk Mitigation | CC9.1-CC9.2 | Risk mitigation activities, vendor risk management |

pytest tests/unit/ -v

}

# With coverage

pytest tests/unit/ -v --cov=. --cov-report=html- **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))

```

# Get job status

### Frontend Tests

GET /api/jobs/{job_id}### Availability (A) - 3 Controls

```bash

cd frontendAuthorization: Bearer <token>

npm run lint

npm run build### Option 1: Docker (Recommended) 🐳| Control | Title |

```

# Get evidence results

### CI Pipeline

GET /api/jobs/{job_id}/evidence|---------|-------|

GitHub Actions runs on every PR:

- ✅ Backend unit tests (166 tests)Authorization: Bearer <token>

- ✅ Frontend lint and build

- ✅ Security scan (Safety + Trivy)```bash| A1.1 | Capacity Planning |

- ✅ Docker build verification

# Get compliance gaps

---

GET /api/jobs/{job_id}/gaps# Clone the repository| A1.2 | Backup and Recovery |

## License

Authorization: Bearer <token>

MIT License - see [LICENSE](LICENSE) for details.

```git clone https://github.com/Taheriastic/shieldagent.git| A1.3 | Recovery Plan Testing |

---



## Contributing

### Risk & Reportscd shieldagent

1. Fork the repository

2. Create a feature branch (`git checkout -b feature/amazing-feature`)

3. Commit your changes (`git commit -m 'Add amazing feature'`)

4. Push to the branch (`git push origin feature/amazing-feature`)```bash### Processing Integrity (PI) - 5 Controls

5. Open a Pull Request

# Get risk scores

All PRs must pass CI checks before merging.

GET /api/risk/{job_id}/score# Copy environment file and configure| Control | Title |

Authorization: Bearer <token>

cp backend/.env.example backend/.env|---------|-------|

# Get remediation plan

GET /api/risk/{job_id}/remediation| PI1.1 | Data Processing Objectives |

Authorization: Bearer <token>

# Edit .env and add your Gemini API key| PI1.2 | Input Controls |

# Generate PDF report

GET /api/reports/{job_id}/pdf# GEMINI_API_KEY=your-api-key-here| PI1.3 | Processing Controls |

Authorization: Bearer <token>

```| PI1.4 | Output Controls |



### Full API Documentation# Start all services| PI1.5 | Data Retention |



Interactive docs available at: http://localhost:8000/docsmake docker-up



---### Confidentiality (C) - 2 Controls



## 💻 Development# Or using docker-compose directly| Control | Title |



### Local Setup (Without Docker)docker-compose up -d|---------|-------|



**Backend:**```| C1.1 | Confidential Information Identification |



```bash| C1.2 | Confidential Information Disposal |

cd backend

**Access the application:**

# Create virtual environment

python -m venv venv- 🌐 **Frontend**: http://localhost:5173### Privacy (P) - 8 Controls

source venv/bin/activate  # Windows: venv\Scripts\activate

- 🔌 **API**: http://localhost:8000| Control | Title |

# Install dependencies

pip install -r requirements.txt- 📚 **API Docs**: http://localhost:8000/docs|---------|-------|



# Set environment variables- 📖 **ReDoc**: http://localhost:8000/redoc| P1.1 | Privacy Notice |

export DATABASE_URL="postgresql+asyncpg://user:pass@localhost:5432/shieldagent"

export REDIS_URL="redis://localhost:6379/0"| P2.1 | Consent |

export SECRET_KEY="your-secret-key"

export GEMINI_API_KEY="your-gemini-key"### Option 2: Local Development 💻| P3.1 | Data Minimization |



# Run migrations| P4.1 | Data Use |

alembic upgrade head

```bash| P5.1 | Data Subject Rights |

# Start server

uvicorn main:app --reload --port 8000# Clone repository| P6.1 | Data Quality |

```

git clone https://github.com/Taheriastic/shieldagent.git| P7.1 | Data Security |

**Frontend:**

cd shieldagent| P8.1 | Third-Party Disclosure |

```bash

cd frontend



# Install dependencies# === Backend Setup ===## 🔌 API Endpoints

npm install

cd backend

# Start dev server

npm run dev### Authentication

```

# Create virtual environment- `POST /api/auth/register` - Register new user

**Celery Worker:**

python -m venv venv- `POST /api/auth/login` - Login and get JWT token

```bash

cd backendsource venv/bin/activate  # Windows: venv\Scripts\activate- `GET /api/auth/me` - Get current user

celery -A worker.celery_app worker --loglevel=info

```



### Project Structure# Install dependencies### Documents



```pip install -r requirements.txt- `POST /api/documents/upload` - Upload document

shieldagent/

├── backend/- `GET /api/documents` - List documents

│   ├── api/              # API route handlers

│   │   ├── auth.py       # Authentication endpoints# Configure environment- `GET /api/documents/{id}` - Get document

│   │   ├── documents.py  # Document upload/management

│   │   ├── jobs.py       # Analysis job managementcp .env.example .env- `DELETE /api/documents/{id}` - Delete document

│   │   ├── reports.py    # PDF report generation

│   │   └── risk.py       # Risk scoring & remediation# Edit .env with your settings

│   ├── core/             # Config, security, dependencies

│   ├── models/           # SQLAlchemy models### Jobs (Analysis)

│   ├── schemas/          # Pydantic schemas

│   ├── services/         # Business logic# Start PostgreSQL and Redis (via Docker)- `POST /api/jobs/evidence-run` - Start compliance analysis

│   │   ├── gemini_service.py      # AI analysis

│   │   ├── document_service.py    # Document processingdocker-compose up -d postgres redis- `GET /api/jobs` - List jobs

│   │   ├── risk_calculator.py     # Risk scoring

│   │   ├── soc2_controls.py       # Control definitions- `GET /api/jobs/{id}` - Get job status

│   │   └── pdf_report.py          # Report generation

│   ├── worker/           # Celery tasks# Run database migrations- `GET /api/jobs/{id}/evidence` - Get evidence items

│   ├── tests/            # Unit tests

│   ├── main.py           # FastAPI app entryalembic upgrade head- `GET /api/jobs/{id}/gaps` - Get gap report

│   └── requirements.txt

├── frontend/

│   ├── src/

│   │   ├── components/   # React components# Start the API server### Controls

│   │   ├── pages/        # Page components

│   │   │   ├── Dashboard.tsxuvicorn main:app --reload --host 0.0.0.0 --port 8000- `GET /api/controls` - List compliance controls

│   │   │   ├── DocumentsPage.tsx

│   │   │   ├── AnalysisPage.tsx- `GET /api/controls/categories` - List control categories

│   │   │   └── ControlsPage.tsx

│   │   ├── hooks/        # Custom hooks# In another terminal, start Celery worker- `GET /api/controls/summary` - Get control statistics

│   │   ├── lib/          # Utilities

│   │   └── types/        # TypeScript typescelery -A worker.celery_app worker --loglevel=info- `GET /api/controls/{control_id}` - Get control details

│   ├── package.json

│   └── vite.config.ts

├── docker-compose.yml

└── README.md# === Frontend Setup ===### Risk Analysis

```

cd ../frontend- `POST /api/risk/calculate` - Calculate risk score from results

---

- `GET /api/risk/demo` - Get demo risk analysis

## 🧪 Testing

# Install dependencies- `POST /api/risk/remediation-plan` - Generate remediation plan

### Backend Tests

npm install- `GET /api/risk/audit-readiness` - Get audit readiness assessment

```bash

cd backend



# Run all tests# Start development server### Reports

pytest tests/unit/ -v

npm run dev- `GET /api/reports/{job_id}/pdf` - Generate PDF compliance report

# Run with coverage

pytest tests/unit/ -v --cov=. --cov-report=html```- `GET /api/reports/{job_id}/executive-summary` - Get executive summary



# Run specific test file

pytest tests/unit/test_auth_api.py -v

```### Option 3: Demo Mode (No API Key Required) 🎮## 📁 Sample Documents



**Test Coverage:**

- 166 unit tests covering all API endpoints

- Authentication & authorization tests```bashThe `sample_documents/` folder contains example documents for testing:

- Document service tests

- Risk calculation tests# Run the demo script to see capabilities

- Control mapping tests

cd backend| File | Description | Controls Covered |

### Frontend Tests

python demo_soc2_analysis.py --scan-type quick|------|-------------|------------------|

```bash

cd frontend| `security_policy.json` | Comprehensive security policy | CC1-CC9, P1-P8 |



# Type check# For full analysis demo| `user_access_list.csv` | User access and MFA status | CC6.1-CC6.3 |

npx tsc --noEmit

python demo_soc2_analysis.py --scan-type full| `incident_response_plan.md` | IR procedures and team | CC7.2-CC7.5 |

# Lint

npm run lint```| `vendor_risk_assessment.json` | Vendor security assessments | CC9.2 |



# Build (includes type check)| `bcdr_plan.json` | Business continuity & DR | A1.1-A1.3 |

npm run build

```---| `change_management_log.csv` | Change records | CC8.1 |



### CI Pipeline| `risk_assessment.json` | Risk register | CC3.1-CC3.4, CC9.1 |



The GitHub Actions CI pipeline runs on every PR:## 🏗️ Architecture



| Job | Description |## 🧪 Testing

|-----|-------------|

| ✅ Backend Tests | pytest with SQLite test database |```

| ✅ Frontend Build | TypeScript + Vite build |

| ✅ Security Scan | Safety + Trivy vulnerability scan |┌─────────────────────────────────────────────────────────────────┐```bash

| ✅ Docker Build | Build backend and frontend containers |

│                         Client Layer                            │# Run all tests

All checks must pass before merging.

│  ┌─────────────────────────────────────────────────────────┐   │make test

---

│  │              React + TypeScript Frontend                 │   │

## 🚢 Deployment

│  │    • Tailwind CSS  • React Query  • React Router        │   │# Run with coverage

### Docker Compose (Production)

│  └─────────────────────────────────────────────────────────┘   │make test-cov

```bash

# Build and start└─────────────────────────────────────────────────────────────────┘

docker-compose -f docker-compose.yml up -d --build

                              │# Run specific test file

# View logs

docker-compose logs -f                              ▼cd backend && pytest tests/unit/test_auth.py -v



# Stop┌─────────────────────────────────────────────────────────────────┐```

docker-compose down

```│                         API Layer                               │



### Environment Variables│  ┌─────────────────────────────────────────────────────────┐   │## 📁 Project Structure



| Variable | Description | Required |│  │                    FastAPI Backend                       │   │

|----------|-------------|----------|

| `DATABASE_URL` | PostgreSQL connection string | Yes |│  │  • JWT Auth  • Async/Await  • Pydantic Validation       │   │```

| `REDIS_URL` | Redis connection string | Yes |

| `SECRET_KEY` | JWT signing key (min 32 chars) | Yes |│  │  • OpenAPI Docs  • CORS  • Rate Limiting                │   │shieldagent/

| `GEMINI_API_KEY` | Google Gemini API key | Yes |

| `DEBUG` | Enable debug mode | No |│  └─────────────────────────────────────────────────────────┘   │├── backend/

| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | No |

└─────────────────────────────────────────────────────────────────┘│   ├── api/              # FastAPI routes

### Database Migrations

                              ││   ├── core/             # Config, security, logging

```bash

cd backend              ┌───────────────┼───────────────┐│   ├── models/           # SQLAlchemy models



# Create new migration              ▼               ▼               ▼│   ├── schemas/          # Pydantic schemas

alembic revision --autogenerate -m "description"

┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐│   ├── services/         # Business logic

# Apply migrations

alembic upgrade head│   PostgreSQL     │ │    Redis     │ │  Celery Worker   ││   ├── worker/           # Celery tasks



# Rollback│   • User data    │ │  • Sessions  │ │  • Async jobs    ││   ├── tests/            # Test suite

alembic downgrade -1

```│   • Documents    │ │  • Caching   │ │  • AI analysis   ││   └── main.py           # Application entry



---│   • Evidence     │ │  • Queue     │ │  • PDF reports   │├── frontend/             # React application



## 🔐 Security│   • Jobs         │ │              │ │                  │├── docker-compose.yml



- **Authentication**: JWT tokens with configurable expiration└──────────────────┘ └──────────────┘ └──────────────────┘├── Makefile

- **Password Hashing**: bcrypt with automatic salting

- **CORS**: Configurable allowed origins                                              │└── README.md

- **Input Validation**: Pydantic schema validation

- **SQL Injection**: SQLAlchemy ORM protection                                              ▼```

- **Dependency Scanning**: Safety + Trivy in CI

                              ┌──────────────────────────┐

---

                              │     Google Gemini AI     │## 🎨 Screenshots

## 📄 License

                              │  • Document analysis     │

MIT License - see [LICENSE](LICENSE) for details.

                              │  • Evidence extraction   │### Compliance Dashboard

---

                              │  • Gap identification    │- Real-time compliance score visualization

## 🤝 Contributing

                              └──────────────────────────┘- Category breakdown by Trust Service Criteria

1. Fork the repository

2. Create a feature branch (`git checkout -b feature/amazing-feature`)```- Gap identification with severity ratings

3. Commit your changes (`git commit -m 'Add amazing feature'`)

4. Push to the branch (`git push origin feature/amazing-feature`)- Audit readiness indicator

5. Open a Pull Request

### 📁 Project Structure

All PRs must pass CI checks before merging.

### Analysis Results

---

```- Control-by-control evidence mapping

<p align="center">

  Built with ❤️ for compliance automationshieldagent/- AI confidence scores

</p>

├── 📂 backend/                    # FastAPI Backend Application- Direct evidence quotes from documents

│   ├── 📂 api/                    # API Route Handlers- Remediation recommendations

│   │   ├── auth.py               # 🔐 Authentication endpoints

│   │   ├── documents.py          # 📄 Document management## 🛠️ Tech Stack

│   │   ├── jobs.py               # ⚙️ Analysis job management

│   │   ├── controls.py           # 📋 SOC 2 controls listing### Backend

│   │   ├── risk.py               # 📊 Risk analysis endpoints- **FastAPI** - High-performance async API framework

│   │   ├── reports.py            # 📑 Report generation- **SQLAlchemy 2.0** - Async ORM with PostgreSQL

│   │   └── health.py             # 💚 Health check endpoint- **Celery** - Distributed task queue for background analysis

│   │- **Redis** - Message broker & caching

│   ├── 📂 core/                   # Core Application Components- **Google Gemini** - AI-powered document analysis

│   │   ├── config.py             # ⚙️ Settings management- **Pydantic** - Data validation and serialization

│   │   ├── security.py           # 🔒 JWT & password hashing- **PyMuPDF** - PDF text extraction

│   │   ├── dependencies.py       # 🔗 FastAPI dependencies- **ReportLab** - PDF report generation

│   │   └── logging.py            # 📝 Structured logging

│   │### Frontend

│   ├── 📂 models/                 # SQLAlchemy ORM Models- **React 18** - Modern UI framework

│   │   ├── user.py               # 👤 User model- **TypeScript** - Type safety

│   │   ├── document.py           # 📄 Document model- **Tailwind CSS** - Utility-first styling

│   │   ├── job.py                # ⚙️ Analysis job model- **React Query** - Server state management

│   │   ├── control.py            # 📋 Control model- **Recharts** - Data visualizations

│   │   └── evidence.py           # 🔍 Evidence & Gap models- **React Router** - Client-side routing

│   │

│   ├── 📂 schemas/                # Pydantic Schemas### Infrastructure

│   │   ├── user.py               # User request/response- **Docker & Docker Compose** - Containerization

│   │   ├── document.py           # Document schemas- **PostgreSQL 16** - Primary database

│   │   ├── job.py                # Job schemas- **Redis 7** - Message broker

│   │   ├── control.py            # Control schemas

│   │   └── evidence.py           # Evidence schemas## 📊 Risk Scoring Algorithm

│   │

│   ├── 📂 services/               # Business Logic ServicesShieldAgent uses a weighted scoring system based on SOC 2 auditor focus areas:

│   │   ├── user_service.py       # 👤 User operations

│   │   ├── document_service.py   # 📄 Document handling```

│   │   ├── job_service.py        # ⚙️ Job managementCategory Weights:

│   │   ├── gemini_service.py     # 🤖 AI integration├── Security (CC controls)    35%

│   │   ├── soc2_controls.py      # 📋 51 SOC 2 controls├── Availability              20%

│   │   ├── risk_calculator.py    # 📊 Risk scoring├── Processing Integrity      15%

│   │   ├── remediation_tracker.py # 📋 Remediation tracking├── Confidentiality          15%

│   │   └── pdf_report.py         # 📑 PDF generation└── Privacy                  15%

│   │```

│   ├── 📂 worker/                 # Celery Background Tasks

│   │   ├── celery_app.py         # ⚙️ Celery configuration**Risk Levels:**

│   │   └── tasks.py              # 🔄 Async task definitions- 🟢 **Minimal** (90-100): Audit ready

│   │- 🟡 **Low** (75-89): Almost ready

│   ├── 📂 tests/                  # Comprehensive Test Suite- 🟠 **Medium** (60-74): Needs work

│   │   ├── conftest.py           # 🧪 Shared fixtures- 🔴 **High** (40-59): Significant gaps

│   │   ├── 📂 unit/              # Unit tests- ⚫ **Critical** (<40): Not ready

│   │   │   ├── test_security.py

│   │   │   ├── test_auth_api.py## 📄 License

│   │   │   ├── test_documents_api.py

│   │   │   ├── test_jobs_api.pyMIT License - see [LICENSE](LICENSE) for details.

│   │   │   ├── test_controls_api.py

│   │   │   ├── test_soc2_controls.py## 👨‍� Author

│   │   │   ├── test_risk_calculator.py

│   │   │   ├── test_user_service.py**Taher** - [GitHub](https://github.com/Taheriastic)

│   │   │   └── test_health.py

│   │   └── 📂 integration/       # Integration tests---

│   │       └── test_gemini_service.py

│   │Built with ❤️ for demonstrating full-stack + AI engineering skills.

│   ├── 📂 alembic/                # Database Migrations
│   ├── main.py                    # 🚀 Application entry point
│   ├── db.py                      # 🗄️ Database configuration
│   └── requirements.txt           # 📦 Python dependencies
│
├── 📂 frontend/                   # React Frontend Application
│   ├── 📂 src/
│   │   ├── 📂 components/        # Reusable UI components
│   │   │   ├── 📂 ui/           # Base UI components
│   │   │   ├── 📂 dashboard/    # Dashboard components
│   │   │   ├── 📂 layout/       # Layout components
│   │   │   └── 📂 onboarding/   # Onboarding flow
│   │   │
│   │   ├── 📂 pages/            # Page components
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── DocumentsPage.tsx
│   │   │   ├── ControlsPage.tsx
│   │   │   ├── AnalysisPage.tsx
│   │   │   └── JobDetailsPage.tsx
│   │   │
│   │   ├── 📂 hooks/            # Custom React hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useDocuments.ts
│   │   │   ├── useJobs.ts
│   │   │   └── useControls.ts
│   │   │
│   │   ├── 📂 lib/              # Utilities & API client
│   │   ├── 📂 types/            # TypeScript type definitions
│   │   └── App.tsx              # Root component
│   │
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── 📂 sample_documents/           # Example documents for testing
│   ├── security_policy.json      # Comprehensive security policy
│   ├── user_access_list.csv      # User access & MFA status
│   ├── incident_response_plan.md # IR procedures
│   ├── vendor_risk_assessment.json
│   ├── bcdr_plan.json            # Business continuity & DR
│   ├── change_management_log.csv
│   └── risk_assessment.json      # Risk register
│
├── 📂 .github/workflows/          # CI/CD Pipeline
│   └── ci.yml                    # GitHub Actions workflow
│
├── docker-compose.yml             # 🐳 Docker orchestration
├── Makefile                       # 🔧 Development commands
├── demo_soc2_analysis.py          # 🎮 Demo script
└── README.md                      # 📖 This file
```

---

## 📊 SOC 2 Coverage

ShieldAgent covers **all 51 SOC 2 Trust Service Criteria controls** across 5 categories:

### 🔒 Security (Common Criteria) - 33 Controls

| Category | Controls | Focus Areas |
|----------|----------|-------------|
| **CC1** Control Environment | CC1.1-CC1.5 | Integrity, board oversight, structure, competence, accountability |
| **CC2** Communication | CC2.1-CC2.3 | Information quality, internal/external communication |
| **CC3** Risk Assessment | CC3.1-CC3.4 | Risk objectives, identification, fraud risk, change risk |
| **CC4** Monitoring | CC4.1-CC4.2 | Ongoing monitoring, deficiency communication |
| **CC5** Control Activities | CC5.1-CC5.3 | Control selection, technology controls, policies |
| **CC6** Logical/Physical Access | CC6.1-CC6.8 | Access security, registration, removal, boundaries |
| **CC7** System Operations | CC7.1-CC7.5 | Vulnerability management, monitoring, incident response |
| **CC8** Change Management | CC8.1 | Change management process |
| **CC9** Risk Mitigation | CC9.1-CC9.2 | Risk mitigation, vendor management |

### ⚡ Availability (A) - 3 Controls

| Control | Title | What It Checks |
|---------|-------|----------------|
| A1.1 | Capacity Planning | Resource monitoring, scalability planning |
| A1.2 | Backup and Recovery | Backup policies, RTO/RPO, disaster recovery |
| A1.3 | Recovery Plan Testing | DR test schedules, results, improvements |

### ✅ Processing Integrity (PI) - 5 Controls

| Control | Title | What It Checks |
|---------|-------|----------------|
| PI1.1 | Data Processing Objectives | Processing specifications, accuracy standards |
| PI1.2 | Input Controls | Input validation, data entry controls |
| PI1.3 | Processing Controls | Processing accuracy, reconciliation |
| PI1.4 | Output Controls | Output validation, distribution controls |
| PI1.5 | Data Retention | Retention schedules, archive procedures |

### 🔐 Confidentiality (C) - 2 Controls

| Control | Title | What It Checks |
|---------|-------|----------------|
| C1.1 | Confidential Information ID | Data classification, inventory, labeling |
| C1.2 | Confidential Disposal | Secure disposal, media sanitization |

### 👤 Privacy (P) - 8 Controls

| Control | Title | What It Checks |
|---------|-------|----------------|
| P1.1 | Privacy Notice | Privacy policy, data collection disclosure |
| P2.1 | Consent | Consent collection, opt-in/opt-out |
| P3.1 | Data Minimization | Collection limitation, purpose specification |
| P4.1 | Data Use | Use limitation, purpose alignment |
| P5.1 | Data Subject Rights | Access requests, correction, deletion |
| P6.1 | Data Quality | Data accuracy, validation |
| P7.1 | Data Security | Personal data encryption, access controls |
| P8.1 | Third-Party Disclosure | Data sharing agreements, sub-processors |

### 📊 Risk Scoring Algorithm

```
Category Weights:
├── Security (CC)           35%
├── Availability            20%
├── Processing Integrity    15%
├── Confidentiality         15%
└── Privacy                 15%
                           ────
                           100%
```

**Risk Levels:**
| Score Range | Risk Level | Audit Readiness |
|-------------|------------|-----------------|
| 90-100 | 🟢 Minimal | Ready |
| 75-89 | 🟡 Low | Almost Ready |
| 60-74 | 🟠 Medium | Needs Work |
| 40-59 | 🔴 High | Significant Gaps |
| 0-39 | ⚫ Critical | Not Ready |

---

## 🔌 API Reference

### Base URL
```
http://localhost:8000/api
```

### 🔐 Authentication

ShieldAgent uses JWT Bearer token authentication.

```bash
# Register a new user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123"}'

# Login and get token
curl -X POST http://localhost:8000/api/auth/login \
  -d "username=user@example.com&password=securepass123"

# Use token in subsequent requests
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer <your-token>"
```

### 📚 Endpoints

#### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/register` | Register new user |
| `POST` | `/auth/login` | Login & get JWT token |
| `GET` | `/auth/me` | Get current user info |

#### Documents
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/documents/upload` | Upload document |
| `GET` | `/documents` | List all documents |
| `GET` | `/documents/{id}` | Get document details |
| `DELETE` | `/documents/{id}` | Delete document |

#### Jobs (Analysis)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/jobs/evidence-run` | Start compliance analysis |
| `GET` | `/jobs` | List all jobs |
| `GET` | `/jobs/{id}` | Get job status |
| `GET` | `/jobs/{id}/evidence` | Get evidence items |
| `GET` | `/jobs/{id}/gaps` | Get compliance gaps |

#### Controls
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/controls` | List controls |
| `GET` | `/controls/categories` | Get categories |
| `GET` | `/controls/summary` | Get statistics |
| `GET` | `/controls/{id}` | Get control details |

#### Risk Analysis
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/risk/calculate` | Calculate risk score |
| `GET` | `/risk/demo` | Get demo analysis |
| `POST` | `/risk/remediation-plan` | Generate plan |

#### Reports
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/reports/{job_id}/pdf` | Download PDF report |
| `GET` | `/reports/{job_id}/executive-summary` | Get summary |

#### Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |

### 💡 Example: Complete Analysis Flow

```bash
# 1. Register and login
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -d "username=user@example.com&password=securepass123" | jq -r '.access_token')

# 2. Upload documents
DOC_ID=$(curl -s -X POST http://localhost:8000/api/documents/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@sample_documents/security_policy.json" | jq -r '.id')

# 3. Start analysis job
JOB_ID=$(curl -s -X POST http://localhost:8000/api/jobs/evidence-run \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"framework\": \"soc2\", \"document_ids\": [\"$DOC_ID\"]}" | jq -r '.id')

# 4. Check job status (poll until completed)
curl -s http://localhost:8000/api/jobs/$JOB_ID \
  -H "Authorization: Bearer $TOKEN" | jq '.status'

# 5. Get evidence results
curl -s http://localhost:8000/api/jobs/$JOB_ID/evidence \
  -H "Authorization: Bearer $TOKEN" | jq

# 6. Get compliance gaps
curl -s http://localhost:8000/api/jobs/$JOB_ID/gaps \
  -H "Authorization: Bearer $TOKEN" | jq

# 7. Download PDF report
curl -s http://localhost:8000/api/reports/$JOB_ID/pdf \
  -H "Authorization: Bearer $TOKEN" -o compliance_report.pdf
```

---

## 🎨 Frontend Guide

### Pages

| Page | Route | Description |
|------|-------|-------------|
| 📊 Dashboard | `/` | Overview with compliance score, recent jobs |
| 📄 Documents | `/documents` | Upload and manage documents |
| 📋 Controls | `/controls` | Browse all 51 SOC 2 controls |
| ⚙️ Job Details | `/jobs/:id` | View analysis progress and results |
| 🔍 Analysis | `/analysis/:id` | Detailed evidence and gap view |

### Key Components

| Component | Description |
|-----------|-------------|
| `ComplianceScore` | Circular progress showing overall score |
| `ControlCard` | Individual control with status indicator |
| `GapsReport` | List of identified gaps with severity |
| `RecentJobs` | Job history with status badges |
| `CategoryChart` | Radar chart of category scores |

---

## ⚙️ Configuration

### Environment Variables

Create `backend/.env` with:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/shieldagent

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Google Gemini AI
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-1.5-flash

# Upload Settings
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=52428800  # 50MB
```

### Docker Configuration

Modify `docker-compose.yml` for production:

```yaml
services:
  backend:
    environment:
      - DATABASE_URL=postgresql+asyncpg://...
      - GEMINI_API_KEY=${GEMINI_API_KEY}
```

---

## 🧪 Testing

ShieldAgent includes a comprehensive test suite with unit and integration tests.

### Running Tests

```bash
cd backend

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=. --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_auth_api.py -v

# Run specific test class
pytest tests/unit/test_security.py::TestPasswordHashing -v

# Run tests matching pattern
pytest -k "test_login" -v

# Run with parallel execution (faster)
pytest -n auto
```

### Test Structure

```
tests/
├── conftest.py                    # Shared fixtures (db, client, user)
├── unit/                          # Unit Tests
│   ├── test_security.py           # Password hashing, JWT tokens
│   ├── test_auth_api.py           # Auth endpoints (register, login)
│   ├── test_documents_api.py      # Document CRUD operations
│   ├── test_jobs_api.py           # Job creation, status, evidence
│   ├── test_controls_api.py       # Controls listing, filtering
│   ├── test_soc2_controls.py      # SOC 2 control definitions
│   ├── test_risk_calculator.py    # Risk scoring algorithm
│   ├── test_user_service.py       # User service functions
│   └── test_health.py             # Health check endpoint
└── integration/                   # Integration Tests
    └── test_gemini_service.py     # AI service integration
```

### Test Categories

| Category | Tests | Description |
|----------|-------|-------------|
| **Security** | 6 | Password hashing, JWT generation/validation |
| **Auth API** | 8 | User registration, login, token refresh |
| **Documents API** | 7 | Upload, list, get, delete documents |
| **Jobs API** | 8 | Job creation, status, evidence, gaps |
| **Controls API** | 6 | List, filter, search controls |
| **SOC 2 Controls** | 10 | Control definitions, categories |
| **Risk Calculator** | 8 | Risk scoring, levels, recommendations |
| **User Service** | 5 | User CRUD operations |
| **Integration** | 4 | Gemini AI service tests |

### Coverage Report

```bash
# Generate HTML coverage report
pytest --cov=. --cov-report=html

# Open coverage report
open htmlcov/index.html
```

---

## 🚀 Deployment

### 🐳 Docker Production Build

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# Scale workers
docker-compose -f docker-compose.prod.yml up -d --scale celery-worker=4
```

### ☁️ Cloud Deployment

**AWS:**
```bash
# Deploy with ECS
aws ecs create-cluster --cluster-name shieldagent
# ... configure task definitions and services
```

**Kubernetes:**
```bash
# Apply manifests
kubectl apply -f k8s/
```

### 🔧 Manual Deployment

1. **Set up PostgreSQL** and **Redis** servers
2. **Configure environment variables**
3. **Run migrations**: `alembic upgrade head`
4. **Start with Gunicorn**:
   ```bash
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
   ```
5. **Start Celery worker**:
   ```bash
   celery -A worker.celery_app worker --loglevel=info --concurrency=4
   ```
6. **Build frontend**: `cd frontend && npm run build`
7. **Serve static files** with Nginx

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | High-performance async API framework |
| **SQLAlchemy 2.0** | Async ORM with PostgreSQL |
| **Celery** | Distributed task queue |
| **Redis** | Message broker & caching |
| **Google Gemini** | AI-powered document analysis |
| **Pydantic** | Data validation |
| **PyMuPDF** | PDF text extraction |
| **ReportLab** | PDF report generation |
| **pytest** | Testing framework |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | UI framework |
| **TypeScript** | Type safety |
| **Tailwind CSS** | Styling |
| **React Query** | Server state management |
| **Recharts** | Data visualizations |
| **React Router** | Routing |
| **Vite** | Build tool |

### Infrastructure
| Technology | Purpose |
|------------|---------|
| **Docker** | Containerization |
| **PostgreSQL 16** | Primary database |
| **Redis 7** | Message broker |
| **GitHub Actions** | CI/CD |

---

## 📁 Sample Documents

The `sample_documents/` folder contains example documents for testing:

| File | Description | Controls Covered |
|------|-------------|------------------|
| `security_policy.json` | Comprehensive security policy | CC1-CC9, P1-P8 |
| `user_access_list.csv` | User access and MFA status | CC6.1-CC6.3 |
| `incident_response_plan.md` | IR procedures and team | CC7.2-CC7.5 |
| `vendor_risk_assessment.json` | Vendor security assessments | CC9.2 |
| `bcdr_plan.json` | Business continuity & DR | A1.1-A1.3 |
| `change_management_log.csv` | Change records | CC8.1 |
| `risk_assessment.json` | Risk register | CC3.1-CC3.4, CC9.1 |

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Guidelines

- ✅ Follow PEP 8 for Python code
- ✅ Use TypeScript strict mode for frontend
- ✅ Write tests for new features
- ✅ Update documentation as needed
- ✅ Keep commits atomic and descriptive

### Code of Conduct

Please be respectful and inclusive. We're all here to learn and build great software together.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Taher** - [GitHub](https://github.com/Taheriastic)

---

<p align="center">
  Built with ❤️ for demonstrating full-stack + AI engineering skills
</p>

<p align="center">
  <sub>
    ShieldAgent - Making SOC 2 compliance accessible for everyone 🛡️
  </sub>
</p>

<p align="center">
  <a href="#️-shieldagent">Back to Top ⬆️</a>
</p>
