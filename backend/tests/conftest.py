"""
Pytest configuration and fixtures for ShieldAgent tests.
"""

import asyncio
from typing import AsyncGenerator
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from main import app
from db import Base
from core.dependencies import get_db
from core.security import get_password_hash
from models.user import User
from models.document import Document
from models.job import Job, JobStatus


# Test database URL (use SQLite for testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test HTTP client with overridden database dependency."""
    
    async def override_get_db():
        yield test_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(test_db: AsyncSession) -> User:
    """Create a test user in the database."""
    user = User(
        id=uuid4(),
        email="test@example.com",
        hashed_password=get_password_hash("testpassword123"),
        full_name="Test User",
        is_active=True,
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest_asyncio.fixture
async def test_user_token(test_user: User) -> str:
    """Get a valid JWT token for the test user."""
    from core.security import create_access_token
    return create_access_token(data={"sub": str(test_user.id)})


@pytest_asyncio.fixture
async def auth_headers(test_user_token: str) -> dict:
    """Get authorization headers with a valid token."""
    return {"Authorization": f"Bearer {test_user_token}"}


@pytest_asyncio.fixture
async def test_document(test_db: AsyncSession, test_user: User) -> Document:
    """Create a test document in the database."""
    document = Document(
        id=uuid4(),
        user_id=test_user.id,
        filename="test_doc_123.json",
        original_filename="test_document.json",
        file_type="json",
        file_path="/tmp/test_doc_123.json",
        file_size=1024,
    )
    test_db.add(document)
    await test_db.commit()
    await test_db.refresh(document)
    return document


@pytest_asyncio.fixture
async def test_job(test_db: AsyncSession, test_user: User) -> Job:
    """Create a test job in the database."""
    job = Job(
        id=uuid4(),
        user_id=test_user.id,
        job_type="soc2",
        scan_type="quick",
        status=JobStatus.PENDING.value,
        progress=0,
        total_controls=8,
    )
    test_db.add(job)
    await test_db.commit()
    await test_db.refresh(job)
    return job


@pytest.fixture
def sample_security_policy() -> dict:
    """Return a sample security policy for testing."""
    return {
        "organization": "Test Corp",
        "document_type": "Security Policy",
        "access_control_policy": {
            "authentication": {
                "mfa_required": True,
                "password_requirements": {
                    "min_length": 12,
                    "require_uppercase": True,
                }
            }
        }
    }


@pytest.fixture
def sample_user_access_csv() -> str:
    """Return sample user access CSV content."""
    return """user_id,username,email,role,mfa_enabled,status
U001,john.smith,john@test.com,admin,true,active
U002,jane.doe,jane@test.com,user,true,active
U003,bob.wilson,bob@test.com,user,false,inactive"""
