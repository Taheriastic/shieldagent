<p align="center"># ShieldAgent 🛡️

  <img src="frontend/public/shield.svg" alt="ShieldAgent Logo" width="120" height="120">

</p>**AI-Powered SOC 2 Compliance Automation Platform**



<h1 align="center">🛡️ ShieldAgent</h1>ShieldAgent automates SOC 2 evidence collection by analyzing your security documents, configurations, and policies using AI. It covers all 5 Trust Service Categories with 50+ controls for comprehensive compliance assessment.



<p align="center">![License](https://img.shields.io/badge/license-MIT-blue.svg)

  <strong>AI-Powered SOC 2 Compliance Automation Platform</strong>![Python](https://img.shields.io/badge/python-3.11+-blue.svg)

</p>![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)

![React](https://img.shields.io/badge/React-18-blue.svg)

<p align="center">![SOC 2](https://img.shields.io/badge/SOC_2-50%2B_Controls-success.svg)

  <a href="#-features">Features</a> •

  <a href="#-quick-start">Quick Start</a> •## 🎯 Features

  <a href="#-architecture">Architecture</a> •

  <a href="#-api-reference">API</a> •- **📄 Document Upload**: Upload PDFs, CSVs, JSON, and text configuration files

  <a href="#-soc-2-coverage">SOC 2 Coverage</a> •- **🤖 AI-Powered Analysis**: Uses Google Gemini to analyze security policies and evidence

  <a href="#-testing">Testing</a>- **🔍 Comprehensive Coverage**: 50+ SOC 2 controls across all Trust Service Categories

</p>- **📊 Risk Scoring**: Intelligent risk calculation with weighted category scores

- **📈 Compliance Dashboard**: Real-time compliance scores and evidence tracking

<p align="center">- **🚨 Gap Analysis**: Identifies compliance gaps with severity ratings

  <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python">- **📋 Remediation Tracking**: Prioritized remediation plans with time estimates

  <img src="https://img.shields.io/badge/FastAPI-0.109-green.svg" alt="FastAPI">- **📑 PDF Reports**: Generate audit-ready compliance reports

  <img src="https://img.shields.io/badge/React-18-blue.svg" alt="React">- **⚡ Quick Scan Mode**: Fast assessment using 8 critical controls

  <img src="https://img.shields.io/badge/TypeScript-5.0-blue.svg" alt="TypeScript">- **🔄 Full Scan Mode**: Comprehensive analysis of all 50+ controls

  <img src="https://img.shields.io/badge/SOC_2-51_Controls-success.svg" alt="SOC 2">

  <img src="https://img.shields.io/badge/Test_Coverage-Comprehensive-brightgreen.svg" alt="Tests">## 🏗️ Architecture

  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">

</p>```

┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐

---│  React Frontend │────▶│  FastAPI Backend │────▶│  PostgreSQL DB  │

└─────────────────┘     └────────┬────────┘     └─────────────────┘

## 📋 Table of Contents                                 │

                                 ▼

- [Overview](#-overview)                        ┌─────────────────┐

- [Features](#-features)                        │   Redis Queue   │

- [Quick Start](#-quick-start)                        └────────┬────────┘

- [Architecture](#-architecture)                                 │

- [SOC 2 Coverage](#-soc-2-coverage)                                 ▼

- [API Reference](#-api-reference)                        ┌─────────────────┐     ┌─────────────────┐

- [Frontend Guide](#-frontend-guide)                        │  Celery Worker  │────▶│  Google Gemini  │

- [Configuration](#-configuration)                        └─────────────────┘     └─────────────────┘

- [Testing](#-testing)```

- [Deployment](#-deployment)

- [Contributing](#-contributing)## 🚀 Quick Start



---### Prerequisites



## 🌟 Overview- Docker & Docker Compose

- Python 3.11+ (for local development)

**ShieldAgent** is a comprehensive AI-powered platform that automates SOC 2 compliance evidence collection and gap analysis. Upload your security policies, configurations, and documentation, and let our AI analyze them against all 51 SOC 2 Trust Service Criteria controls.- Node.js 18+ (for frontend development)



### Why ShieldAgent?### Using Docker (Recommended)



| Traditional Compliance | With ShieldAgent |```bash

|----------------------|------------------|# Clone the repository

| 📅 Weeks of manual review | ⚡ Minutes with AI analysis |git clone https://github.com/Taheriastic/shieldagent.git

| 📝 Spreadsheet tracking | 📊 Real-time dashboard |cd shieldagent

| 🔍 Point-in-time audits | 🔄 Continuous monitoring |

| 💰 Expensive consultants | 🤖 Automated assessment |# Copy environment file

| 📋 Paper-based evidence | 🔗 Direct document linking |cp backend/.env.example backend/.env



---# Edit .env and add your Gemini API key

# GEMINI_API_KEY=your-api-key-here

## ✨ Features

# Start all services

### 🔍 Document Analysismake docker-up

- **Multi-format Support**: PDF, CSV, JSON, TXT, and Markdown files

- **AI-Powered Review**: Google Gemini analyzes documents against controls# API will be available at http://localhost:8000

- **Evidence Extraction**: Automatic quote extraction from documents# Docs at http://localhost:8000/docs

- **Batch Processing**: Analyze multiple documents simultaneously```



### 📊 Compliance Dashboard### Local Development

- **Real-time Scores**: Overall compliance percentage and risk level

- **Category Breakdown**: Scores by Trust Service Category```bash

- **Gap Visualization**: Interactive charts showing compliance gaps# Install backend dependencies

- **Trend Tracking**: Historical compliance score trendscd backend

python -m venv venv

### 🎯 Risk Assessmentsource venv/bin/activate  # On Windows: venv\Scripts\activate

- **Weighted Scoring**: Industry-standard category weightingpip install -r requirements.txt

- **Risk Levels**: Critical, High, Medium, Low, Minimal classifications

- **Audit Readiness**: Automated readiness assessment# Start PostgreSQL and Redis (via Docker)

- **Remediation Estimates**: Time-to-fix calculationsdocker-compose up -d postgres redis



### 📋 Remediation Tracking# Run the API

- **Prioritized Tasks**: Gaps sorted by severity and impactuvicorn main:app --reload

- **Progress Tracking**: Task completion monitoring

- **Time Estimates**: Hours-to-remediate calculations# In another terminal, start Celery worker

- **Recommendations**: AI-generated remediation suggestionscelery -A worker.celery_app worker --loglevel=info

```

### 📑 Reporting

- **PDF Reports**: Audit-ready compliance reports## 📋 SOC 2 Trust Service Categories Coverage

- **Executive Summaries**: High-level findings for leadership

- **Evidence Packages**: Compiled evidence for auditors### Security (Common Criteria) - 33 Controls

- **Gap Reports**: Detailed gap analysis documentation| Category | Controls | Description |

|----------|----------|-------------|

---| CC1 - Control Environment | CC1.1-CC1.5 | Integrity, board oversight, org structure, competence, accountability |

| CC2 - Communication | CC2.1-CC2.3 | Information quality, internal/external communication |

## 🚀 Quick Start| CC3 - Risk Assessment | CC3.1-CC3.4 | Risk objectives, identification, fraud risk, change risk |

| CC4 - Monitoring | CC4.1-CC4.2 | Ongoing monitoring, deficiency communication |

### Prerequisites| CC5 - Control Activities | CC5.1-CC5.3 | Control selection, technology controls, policy implementation |

| CC6 - Logical/Physical Access | CC6.1-CC6.8 | Access security, registration, removal, restrictions, boundaries |

- **Docker & Docker Compose** (recommended)| CC7 - System Operations | CC7.1-CC7.5 | Vulnerability detection, monitoring, incident response, recovery |

- **Python 3.11+** (for local development)| CC8 - Change Management | CC8.1 | Change management process |

- **Node.js 18+** (for frontend development)| CC9 - Risk Mitigation | CC9.1-CC9.2 | Risk mitigation activities, vendor risk management |

- **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))

### Availability (A) - 3 Controls

### Option 1: Docker (Recommended) 🐳| Control | Title |

|---------|-------|

```bash| A1.1 | Capacity Planning |

# Clone the repository| A1.2 | Backup and Recovery |

git clone https://github.com/Taheriastic/shieldagent.git| A1.3 | Recovery Plan Testing |

cd shieldagent

### Processing Integrity (PI) - 5 Controls

# Copy environment file and configure| Control | Title |

cp backend/.env.example backend/.env|---------|-------|

| PI1.1 | Data Processing Objectives |

# Edit .env and add your Gemini API key| PI1.2 | Input Controls |

# GEMINI_API_KEY=your-api-key-here| PI1.3 | Processing Controls |

| PI1.4 | Output Controls |

# Start all services| PI1.5 | Data Retention |

make docker-up

### Confidentiality (C) - 2 Controls

# Or using docker-compose directly| Control | Title |

docker-compose up -d|---------|-------|

```| C1.1 | Confidential Information Identification |

| C1.2 | Confidential Information Disposal |

**Access the application:**

- 🌐 **Frontend**: http://localhost:5173### Privacy (P) - 8 Controls

- 🔌 **API**: http://localhost:8000| Control | Title |

- 📚 **API Docs**: http://localhost:8000/docs|---------|-------|

- 📖 **ReDoc**: http://localhost:8000/redoc| P1.1 | Privacy Notice |

| P2.1 | Consent |

### Option 2: Local Development 💻| P3.1 | Data Minimization |

| P4.1 | Data Use |

```bash| P5.1 | Data Subject Rights |

# Clone repository| P6.1 | Data Quality |

git clone https://github.com/Taheriastic/shieldagent.git| P7.1 | Data Security |

cd shieldagent| P8.1 | Third-Party Disclosure |



# === Backend Setup ===## 🔌 API Endpoints

cd backend

### Authentication

# Create virtual environment- `POST /api/auth/register` - Register new user

python -m venv venv- `POST /api/auth/login` - Login and get JWT token

source venv/bin/activate  # Windows: venv\Scripts\activate- `GET /api/auth/me` - Get current user



# Install dependencies### Documents

pip install -r requirements.txt- `POST /api/documents/upload` - Upload document

- `GET /api/documents` - List documents

# Configure environment- `GET /api/documents/{id}` - Get document

cp .env.example .env- `DELETE /api/documents/{id}` - Delete document

# Edit .env with your settings

### Jobs (Analysis)

# Start PostgreSQL and Redis (via Docker)- `POST /api/jobs/evidence-run` - Start compliance analysis

docker-compose up -d postgres redis- `GET /api/jobs` - List jobs

- `GET /api/jobs/{id}` - Get job status

# Run database migrations- `GET /api/jobs/{id}/evidence` - Get evidence items

alembic upgrade head- `GET /api/jobs/{id}/gaps` - Get gap report



# Start the API server### Controls

uvicorn main:app --reload --host 0.0.0.0 --port 8000- `GET /api/controls` - List compliance controls

- `GET /api/controls/categories` - List control categories

# In another terminal, start Celery worker- `GET /api/controls/summary` - Get control statistics

celery -A worker.celery_app worker --loglevel=info- `GET /api/controls/{control_id}` - Get control details



# === Frontend Setup ===### Risk Analysis

cd ../frontend- `POST /api/risk/calculate` - Calculate risk score from results

- `GET /api/risk/demo` - Get demo risk analysis

# Install dependencies- `POST /api/risk/remediation-plan` - Generate remediation plan

npm install- `GET /api/risk/audit-readiness` - Get audit readiness assessment



# Start development server### Reports

npm run dev- `GET /api/reports/{job_id}/pdf` - Generate PDF compliance report

```- `GET /api/reports/{job_id}/executive-summary` - Get executive summary



### Option 3: Demo Mode (No API Key Required) 🎮## 📁 Sample Documents



```bashThe `sample_documents/` folder contains example documents for testing:

# Run the demo script to see capabilities

cd backend| File | Description | Controls Covered |

python demo_soc2_analysis.py --scan-type quick|------|-------------|------------------|

| `security_policy.json` | Comprehensive security policy | CC1-CC9, P1-P8 |

# For full analysis demo| `user_access_list.csv` | User access and MFA status | CC6.1-CC6.3 |

python demo_soc2_analysis.py --scan-type full| `incident_response_plan.md` | IR procedures and team | CC7.2-CC7.5 |

```| `vendor_risk_assessment.json` | Vendor security assessments | CC9.2 |

| `bcdr_plan.json` | Business continuity & DR | A1.1-A1.3 |

---| `change_management_log.csv` | Change records | CC8.1 |

| `risk_assessment.json` | Risk register | CC3.1-CC3.4, CC9.1 |

## 🏗️ Architecture

## 🧪 Testing

```

┌─────────────────────────────────────────────────────────────────┐```bash

│                         Client Layer                            │# Run all tests

│  ┌─────────────────────────────────────────────────────────┐   │make test

│  │              React + TypeScript Frontend                 │   │

│  │    • Tailwind CSS  • React Query  • React Router        │   │# Run with coverage

│  └─────────────────────────────────────────────────────────┘   │make test-cov

└─────────────────────────────────────────────────────────────────┘

                              │# Run specific test file

                              ▼cd backend && pytest tests/unit/test_auth.py -v

┌─────────────────────────────────────────────────────────────────┐```

│                         API Layer                               │

│  ┌─────────────────────────────────────────────────────────┐   │## 📁 Project Structure

│  │                    FastAPI Backend                       │   │

│  │  • JWT Auth  • Async/Await  • Pydantic Validation       │   │```

│  │  • OpenAPI Docs  • CORS  • Rate Limiting                │   │shieldagent/

│  └─────────────────────────────────────────────────────────┘   │├── backend/

└─────────────────────────────────────────────────────────────────┘│   ├── api/              # FastAPI routes

                              ││   ├── core/             # Config, security, logging

              ┌───────────────┼───────────────┐│   ├── models/           # SQLAlchemy models

              ▼               ▼               ▼│   ├── schemas/          # Pydantic schemas

┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐│   ├── services/         # Business logic

│   PostgreSQL     │ │    Redis     │ │  Celery Worker   ││   ├── worker/           # Celery tasks

│   • User data    │ │  • Sessions  │ │  • Async jobs    ││   ├── tests/            # Test suite

│   • Documents    │ │  • Caching   │ │  • AI analysis   ││   └── main.py           # Application entry

│   • Evidence     │ │  • Queue     │ │  • PDF reports   │├── frontend/             # React application

│   • Jobs         │ │              │ │                  │├── docker-compose.yml

└──────────────────┘ └──────────────┘ └──────────────────┘├── Makefile

                                              │└── README.md

                                              ▼```

                              ┌──────────────────────────┐

                              │     Google Gemini AI     │## 🎨 Screenshots

                              │  • Document analysis     │

                              │  • Evidence extraction   │### Compliance Dashboard

                              │  • Gap identification    │- Real-time compliance score visualization

                              └──────────────────────────┘- Category breakdown by Trust Service Criteria

```- Gap identification with severity ratings

- Audit readiness indicator

### 📁 Project Structure

### Analysis Results

```- Control-by-control evidence mapping

shieldagent/- AI confidence scores

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
