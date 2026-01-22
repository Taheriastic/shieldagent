# ShieldAgent 🛡️

**AI-Powered SOC 2 Compliance Automation Platform**

ShieldAgent automates SOC 2 evidence collection by analyzing your security documents, configurations, and policies using AI. It covers all 5 Trust Service Categories with 50+ controls for comprehensive compliance assessment.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![React](https://img.shields.io/badge/React-18-blue.svg)
![SOC 2](https://img.shields.io/badge/SOC_2-50%2B_Controls-success.svg)

## 🎯 Features

- **📄 Document Upload**: Upload PDFs, CSVs, JSON, and text configuration files
- **🤖 AI-Powered Analysis**: Uses Google Gemini to analyze security policies and evidence
- **🔍 Comprehensive Coverage**: 50+ SOC 2 controls across all Trust Service Categories
- **📊 Risk Scoring**: Intelligent risk calculation with weighted category scores
- **📈 Compliance Dashboard**: Real-time compliance scores and evidence tracking
- **🚨 Gap Analysis**: Identifies compliance gaps with severity ratings
- **📋 Remediation Tracking**: Prioritized remediation plans with time estimates
- **📑 PDF Reports**: Generate audit-ready compliance reports
- **⚡ Quick Scan Mode**: Fast assessment using 8 critical controls
- **🔄 Full Scan Mode**: Comprehensive analysis of all 50+ controls

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  React Frontend │────▶│  FastAPI Backend │────▶│  PostgreSQL DB  │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   Redis Queue   │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │  Celery Worker  │────▶│  Google Gemini  │
                        └─────────────────┘     └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/Taheriastic/shieldagent.git
cd shieldagent

# Copy environment file
cp backend/.env.example backend/.env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your-api-key-here

# Start all services
make docker-up

# API will be available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### Local Development

```bash
# Install backend dependencies
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start PostgreSQL and Redis (via Docker)
docker-compose up -d postgres redis

# Run the API
uvicorn main:app --reload

# In another terminal, start Celery worker
celery -A worker.celery_app worker --loglevel=info
```

## 📋 SOC 2 Trust Service Categories Coverage

### Security (Common Criteria) - 33 Controls
| Category | Controls | Description |
|----------|----------|-------------|
| CC1 - Control Environment | CC1.1-CC1.5 | Integrity, board oversight, org structure, competence, accountability |
| CC2 - Communication | CC2.1-CC2.3 | Information quality, internal/external communication |
| CC3 - Risk Assessment | CC3.1-CC3.4 | Risk objectives, identification, fraud risk, change risk |
| CC4 - Monitoring | CC4.1-CC4.2 | Ongoing monitoring, deficiency communication |
| CC5 - Control Activities | CC5.1-CC5.3 | Control selection, technology controls, policy implementation |
| CC6 - Logical/Physical Access | CC6.1-CC6.8 | Access security, registration, removal, restrictions, boundaries |
| CC7 - System Operations | CC7.1-CC7.5 | Vulnerability detection, monitoring, incident response, recovery |
| CC8 - Change Management | CC8.1 | Change management process |
| CC9 - Risk Mitigation | CC9.1-CC9.2 | Risk mitigation activities, vendor risk management |

### Availability (A) - 3 Controls
| Control | Title |
|---------|-------|
| A1.1 | Capacity Planning |
| A1.2 | Backup and Recovery |
| A1.3 | Recovery Plan Testing |

### Processing Integrity (PI) - 5 Controls
| Control | Title |
|---------|-------|
| PI1.1 | Data Processing Objectives |
| PI1.2 | Input Controls |
| PI1.3 | Processing Controls |
| PI1.4 | Output Controls |
| PI1.5 | Data Retention |

### Confidentiality (C) - 2 Controls
| Control | Title |
|---------|-------|
| C1.1 | Confidential Information Identification |
| C1.2 | Confidential Information Disposal |

### Privacy (P) - 8 Controls
| Control | Title |
|---------|-------|
| P1.1 | Privacy Notice |
| P2.1 | Consent |
| P3.1 | Data Minimization |
| P4.1 | Data Use |
| P5.1 | Data Subject Rights |
| P6.1 | Data Quality |
| P7.1 | Data Security |
| P8.1 | Third-Party Disclosure |

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user

### Documents
- `POST /api/documents/upload` - Upload document
- `GET /api/documents` - List documents
- `GET /api/documents/{id}` - Get document
- `DELETE /api/documents/{id}` - Delete document

### Jobs (Analysis)
- `POST /api/jobs/evidence-run` - Start compliance analysis
- `GET /api/jobs` - List jobs
- `GET /api/jobs/{id}` - Get job status
- `GET /api/jobs/{id}/evidence` - Get evidence items
- `GET /api/jobs/{id}/gaps` - Get gap report

### Controls
- `GET /api/controls` - List compliance controls
- `GET /api/controls/categories` - List control categories
- `GET /api/controls/summary` - Get control statistics
- `GET /api/controls/{control_id}` - Get control details

### Risk Analysis
- `POST /api/risk/calculate` - Calculate risk score from results
- `GET /api/risk/demo` - Get demo risk analysis
- `POST /api/risk/remediation-plan` - Generate remediation plan
- `GET /api/risk/audit-readiness` - Get audit readiness assessment

### Reports
- `GET /api/reports/{job_id}/pdf` - Generate PDF compliance report
- `GET /api/reports/{job_id}/executive-summary` - Get executive summary

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

## 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
cd backend && pytest tests/unit/test_auth.py -v
```

## 📁 Project Structure

```
shieldagent/
├── backend/
│   ├── api/              # FastAPI routes
│   ├── core/             # Config, security, logging
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   ├── worker/           # Celery tasks
│   ├── tests/            # Test suite
│   └── main.py           # Application entry
├── frontend/             # React application
├── docker-compose.yml
├── Makefile
└── README.md
```

## 🎨 Screenshots

### Compliance Dashboard
- Real-time compliance score visualization
- Category breakdown by Trust Service Criteria
- Gap identification with severity ratings
- Audit readiness indicator

### Analysis Results
- Control-by-control evidence mapping
- AI confidence scores
- Direct evidence quotes from documents
- Remediation recommendations

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance async API framework
- **SQLAlchemy 2.0** - Async ORM with PostgreSQL
- **Celery** - Distributed task queue for background analysis
- **Redis** - Message broker & caching
- **Google Gemini** - AI-powered document analysis
- **Pydantic** - Data validation and serialization
- **PyMuPDF** - PDF text extraction
- **ReportLab** - PDF report generation

### Frontend
- **React 18** - Modern UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **React Query** - Server state management
- **Recharts** - Data visualizations
- **React Router** - Client-side routing

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **PostgreSQL 16** - Primary database
- **Redis 7** - Message broker

## 📊 Risk Scoring Algorithm

ShieldAgent uses a weighted scoring system based on SOC 2 auditor focus areas:

```
Category Weights:
├── Security (CC controls)    35%
├── Availability              20%
├── Processing Integrity      15%
├── Confidentiality          15%
└── Privacy                  15%
```

**Risk Levels:**
- 🟢 **Minimal** (90-100): Audit ready
- 🟡 **Low** (75-89): Almost ready
- 🟠 **Medium** (60-74): Needs work
- 🔴 **High** (40-59): Significant gaps
- ⚫ **Critical** (<40): Not ready

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 👨‍� Author

**Taher** - [GitHub](https://github.com/Taheriastic)

---

Built with ❤️ for demonstrating full-stack + AI engineering skills.
