# ShieldAgent 🛡️

**AI-Powered SOC 2 Compliance Automation Platform**

ShieldAgent automates SOC 2 evidence collection by analyzing your security documents, configurations, and policies using AI and deterministic checks.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![React](https://img.shields.io/badge/React-18-blue.svg)

## 🎯 Features

- **Document Upload**: Upload PDFs, CSVs, and JSON configuration files
- **AI-Powered Analysis**: Uses Google Gemini to analyze security policies
- **Deterministic Checks**: Automated validation of configs (MFA, encryption, etc.)
- **Compliance Dashboard**: Real-time compliance scores and evidence tracking
- **Gap Reports**: Identifies compliance gaps with remediation suggestions
- **8 SOC 2 Controls**: Covers key security, availability, and risk controls

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

## 📋 SOC 2 Controls Implemented

| Control ID | Title | Type | File Type |
|------------|-------|------|-----------|
| CC6.1 | Multi-Factor Authentication | Deterministic | CSV |
| CC6.2 | Password Complexity Policy | AI | PDF |
| CC6.6 | Vendor Risk Assessment | Deterministic | CSV |
| CC7.2 | Incident Response Plan | AI | PDF |
| CC5.2 | Code Review Enforcement | Deterministic | JSON |
| CC9.1 | Risk Assessment Process | AI | PDF |
| A1.1 | Encryption in Transit | Deterministic | JSON |
| A1.2 | Encryption at Rest | Deterministic | JSON |

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

### Jobs
- `POST /api/jobs/evidence-run` - Start compliance analysis
- `GET /api/jobs` - List jobs
- `GET /api/jobs/{id}` - Get job status
- `GET /api/jobs/{id}/evidence` - Get evidence items
- `GET /api/jobs/{id}/gaps` - Get gap report

### Controls
- `GET /api/controls` - List compliance controls

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

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance async API framework
- **SQLAlchemy 2.0** - Async ORM with PostgreSQL
- **Celery** - Distributed task queue
- **Redis** - Message broker & caching
- **Google Gemini** - AI-powered document analysis
- **Pydantic** - Data validation

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **React Query** - Data fetching
- **Recharts** - Visualizations

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 👨‍💻 Author

**Taher** - [GitHub](https://github.com/Taheriastic)

---

Built with ❤️ for demonstrating full-stack + AI engineering skills.
- Displays results in a professional dashboard

## 🛠️ Tech Stack

### Backend
- Python 3.11
- FastAPI 0.109.0
- PostgreSQL 16
- SQLAlchemy 2.0.25 + Alembic
- Celery 5.3.6 + Redis 7.2
- Google Gemini API (LLM integration)

### Frontend
- React 18 + TypeScript
- Vite
- Tailwind CSS
- React Query + Axios

### Infrastructure
- Docker + Docker Compose
- GitHub Actions (CI/CD)
- Railway (deployment)

## 📁 Project Structure

```
shieldagent/
├── backend/           # FastAPI application
├── frontend/          # React application
├── docker/            # Docker configurations
└── .github/workflows/ # CI/CD pipelines
```

## 🚦 Getting Started

Coming soon...


---

**Built for demonstrating full-stack + AI engineering skills**
