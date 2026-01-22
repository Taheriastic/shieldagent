"""
Tests for API authentication endpoints.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestRegisterEndpoint:
    """Tests for user registration endpoint."""

    async def test_register_success(self, client: AsyncClient):
        """Successful registration should return user data."""
        response = await client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "securepassword123",
                "full_name": "New User",
            },
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["full_name"] == "New User"
        assert data["is_active"] is True
        assert "id" in data
        assert "password" not in data
        assert "hashed_password" not in data

    async def test_register_duplicate_email(self, client: AsyncClient):
        """Registration with existing email should fail."""
        user_data = {
            "email": "duplicate@example.com",
            "password": "securepassword123",
        }
        
        # First registration
        response1 = await client.post("/api/auth/register", json=user_data)
        assert response1.status_code == 201
        
        # Duplicate registration
        response2 = await client.post("/api/auth/register", json=user_data)
        assert response2.status_code == 400
        assert "already exists" in response2.json()["detail"].lower()

    async def test_register_invalid_email(self, client: AsyncClient):
        """Registration with invalid email should fail validation."""
        response = await client.post(
            "/api/auth/register",
            json={
                "email": "not-an-email",
                "password": "securepassword123",
            },
        )
        
        assert response.status_code == 422  # Validation error

    async def test_register_short_password(self, client: AsyncClient):
        """Registration with short password should fail validation."""
        response = await client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "password": "short",  # Less than 8 chars
            },
        )
        
        assert response.status_code == 422

    async def test_register_without_full_name(self, client: AsyncClient):
        """Registration without full_name should succeed."""
        response = await client.post(
            "/api/auth/register",
            json={
                "email": "noname@example.com",
                "password": "securepassword123",
            },
        )
        
        assert response.status_code == 201
        assert response.json()["full_name"] is None


@pytest.mark.asyncio
class TestLoginEndpoint:
    """Tests for user login endpoint."""

    async def test_login_success(self, client: AsyncClient):
        """Successful login should return JWT token."""
        # Register first
        await client.post(
            "/api/auth/register",
            json={
                "email": "login@example.com",
                "password": "securepassword123",
            },
        )
        
        # Login
        response = await client.post(
            "/api/auth/login",
            data={
                "username": "login@example.com",
                "password": "securepassword123",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 50

    async def test_login_wrong_password(self, client: AsyncClient):
        """Login with wrong password should fail."""
        # Register
        await client.post(
            "/api/auth/register",
            json={
                "email": "wrongpw@example.com",
                "password": "correctpassword",
            },
        )
        
        # Login with wrong password
        response = await client.post(
            "/api/auth/login",
            data={
                "username": "wrongpw@example.com",
                "password": "wrongpassword",
            },
        )
        
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()

    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Login with non-existent user should fail."""
        response = await client.post(
            "/api/auth/login",
            data={
                "username": "nonexistent@example.com",
                "password": "anypassword",
            },
        )
        
        assert response.status_code == 401

    async def test_login_missing_fields(self, client: AsyncClient):
        """Login without required fields should fail."""
        response = await client.post(
            "/api/auth/login",
            data={"username": "test@example.com"},
        )
        
        assert response.status_code == 422


@pytest.mark.asyncio
class TestMeEndpoint:
    """Tests for current user endpoint."""

    async def test_get_me_authenticated(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Authenticated request should return user info."""
        response = await client.get("/api/auth/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "email" in data
        assert data["email"] == "test@example.com"

    async def test_get_me_unauthenticated(self, client: AsyncClient):
        """Unauthenticated request should fail."""
        response = await client.get("/api/auth/me")
        
        assert response.status_code == 401

    async def test_get_me_invalid_token(self, client: AsyncClient):
        """Request with invalid token should fail."""
        response = await client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid_token"},
        )
        
        assert response.status_code == 401

    async def test_get_me_malformed_header(self, client: AsyncClient):
        """Request with malformed auth header should fail."""
        response = await client.get(
            "/api/auth/me",
            headers={"Authorization": "NotBearer token"},
        )
        
        assert response.status_code == 401
