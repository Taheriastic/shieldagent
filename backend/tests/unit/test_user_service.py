"""
Tests for user service.
"""

import pytest
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service import UserService
from schemas.user import UserCreate
from models.user import User


@pytest.mark.asyncio
class TestUserServiceCreate:
    """Tests for user creation."""

    async def test_create_user_success(self, test_db: AsyncSession):
        """Creating a new user should succeed."""
        service = UserService(test_db)
        
        user_data = UserCreate(
            email="newuser@example.com",
            password="securepassword123",
            full_name="New User",
        )
        
        user = await service.create_user(user_data)
        
        assert user is not None
        assert user.email == "newuser@example.com"
        assert user.full_name == "New User"
        assert user.is_active is True
        assert user.hashed_password != "securepassword123"  # Should be hashed

    async def test_create_user_duplicate_email(
        self, test_db: AsyncSession, test_user: User
    ):
        """Creating user with existing email should fail."""
        service = UserService(test_db)
        
        user_data = UserCreate(
            email=test_user.email,  # Same as existing user
            password="anotherpassword",
        )
        
        with pytest.raises(ValueError) as exc_info:
            await service.create_user(user_data)
        
        assert "already exists" in str(exc_info.value).lower()

    async def test_create_user_without_full_name(self, test_db: AsyncSession):
        """Creating user without full_name should succeed."""
        service = UserService(test_db)
        
        user_data = UserCreate(
            email="noname@example.com",
            password="securepassword123",
        )
        
        user = await service.create_user(user_data)
        
        assert user.full_name is None


@pytest.mark.asyncio
class TestUserServiceGet:
    """Tests for user retrieval."""

    async def test_get_user_by_email_exists(
        self, test_db: AsyncSession, test_user: User
    ):
        """Getting existing user by email should succeed."""
        service = UserService(test_db)
        
        user = await service.get_user_by_email(test_user.email)
        
        assert user is not None
        assert user.id == test_user.id
        assert user.email == test_user.email

    async def test_get_user_by_email_not_exists(self, test_db: AsyncSession):
        """Getting non-existent user by email should return None."""
        service = UserService(test_db)
        
        user = await service.get_user_by_email("nonexistent@example.com")
        
        assert user is None

    async def test_get_user_by_id_exists(
        self, test_db: AsyncSession, test_user: User
    ):
        """Getting existing user by ID should succeed."""
        service = UserService(test_db)
        
        user = await service.get_user_by_id(test_user.id)
        
        assert user is not None
        assert user.id == test_user.id

    async def test_get_user_by_id_not_exists(self, test_db: AsyncSession):
        """Getting non-existent user by ID should return None."""
        service = UserService(test_db)
        
        fake_id = uuid4()
        user = await service.get_user_by_id(fake_id)
        
        assert user is None


@pytest.mark.asyncio
class TestUserServiceAuthenticate:
    """Tests for user authentication."""

    async def test_authenticate_success(self, test_db: AsyncSession):
        """Authentication with correct credentials should succeed."""
        service = UserService(test_db)
        
        # Create user first
        user_data = UserCreate(
            email="auth@example.com",
            password="correctpassword",
        )
        await service.create_user(user_data)
        
        # Authenticate
        user = await service.authenticate_user(
            email="auth@example.com",
            password="correctpassword",
        )
        
        assert user is not None
        assert user.email == "auth@example.com"

    async def test_authenticate_wrong_password(self, test_db: AsyncSession):
        """Authentication with wrong password should fail."""
        service = UserService(test_db)
        
        # Create user
        user_data = UserCreate(
            email="wrongpw@example.com",
            password="correctpassword",
        )
        await service.create_user(user_data)
        
        # Authenticate with wrong password
        user = await service.authenticate_user(
            email="wrongpw@example.com",
            password="wrongpassword",
        )
        
        assert user is None

    async def test_authenticate_nonexistent_user(self, test_db: AsyncSession):
        """Authentication for non-existent user should fail."""
        service = UserService(test_db)
        
        user = await service.authenticate_user(
            email="nonexistent@example.com",
            password="anypassword",
        )
        
        assert user is None


@pytest.mark.asyncio
class TestUserServiceToken:
    """Tests for token creation."""

    async def test_create_token_for_user(
        self, test_db: AsyncSession, test_user: User
    ):
        """Token creation should return valid token."""
        service = UserService(test_db)
        
        token = service.create_token_for_user(test_user)
        
        assert token is not None
        assert token.access_token is not None
        assert len(token.access_token) > 50
        assert token.token_type == "bearer"

    async def test_token_can_be_decoded(
        self, test_db: AsyncSession, test_user: User
    ):
        """Created token should be decodable."""
        from core.security import decode_access_token
        
        service = UserService(test_db)
        token = service.create_token_for_user(test_user)
        
        payload = decode_access_token(token.access_token)
        
        assert payload is not None
        assert payload["sub"] == str(test_user.id)
