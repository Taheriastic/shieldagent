# ShieldAgent

AI-powered SOC 2 compliance automation tool that automates evidence collection and gap analysis.

## 🚀 Project Overview

ShieldAgent is a production-grade web application that:
- Accepts document uploads (PDFs, CSVs, JSON configs)
- Runs AI-powered + deterministic checks against SOC 2 compliance controls
- Generates evidence items, compliance scores, and gap reports
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

## 📝 License

MIT License

---

**Built for demonstrating full-stack + AI engineering skills**
