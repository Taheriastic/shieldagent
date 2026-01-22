.PHONY: help install dev test lint format clean docker-up docker-down docker-logs

# Default target
help:
	@echo "ShieldAgent - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install     - Install Python dependencies"
	@echo "  make dev         - Start development server"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up   - Start all services with Docker Compose"
	@echo "  make docker-down - Stop all Docker services"
	@echo "  make docker-logs - View Docker logs"
	@echo ""
	@echo "Testing:"
	@echo "  make test        - Run all tests"
	@echo "  make test-cov    - Run tests with coverage"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint        - Run linters (ruff + mypy)"
	@echo "  make format      - Format code with ruff"
	@echo ""
	@echo "Database:"
	@echo "  make db-migrate  - Run database migrations"
	@echo "  make db-upgrade  - Apply pending migrations"

# Install dependencies
install:
	cd backend && pip install -r requirements.txt

# Start development server (local, requires DB running)
dev:
	cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Docker commands
docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-build:
	docker-compose build --no-cache

docker-restart:
	docker-compose restart

# Testing
test:
	cd backend && pytest tests/ -v

test-cov:
	cd backend && pytest tests/ -v --cov=. --cov-report=html --cov-report=term

# Linting and formatting
lint:
	cd backend && ruff check .
	cd backend && mypy . --ignore-missing-imports

format:
	cd backend && ruff check . --fix
	cd backend && ruff format .

# Database migrations
db-migrate:
	cd backend && alembic revision --autogenerate -m "$(msg)"

db-upgrade:
	cd backend && alembic upgrade head

db-downgrade:
	cd backend && alembic downgrade -1

# Clean up
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete

# Create .env from example
setup-env:
	cp backend/.env.example backend/.env
	@echo "Created backend/.env - Please update with your settings"
