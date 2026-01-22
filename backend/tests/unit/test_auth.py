"""
Unit tests for authentication service.
"""

import pytest
from core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
)


class TestPasswordHashing:
    """Tests for password hashing functions."""

    def test_password_hash_creates_different_hash(self):
        """Hashing the same password twice should create different hashes."""
        password = "testpassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 != hash2

    def test_password_verification_succeeds_with_correct_password(self):
        """Correct password should verify successfully."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_password_verification_fails_with_wrong_password(self):
        """Wrong password should fail verification."""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)
        assert verify_password(wrong_password, hashed) is False


class TestJWTTokens:
    """Tests for JWT token functions."""

    def test_create_and_decode_token(self):
        """Token should be creatable and decodable."""
        user_id = "test-user-id-123"
        token = create_access_token(data={"sub": user_id})
        
        assert token is not None
        assert isinstance(token, str)
        
        payload = decode_access_token(token)
        assert payload is not None
        assert payload.get("sub") == user_id

    def test_decode_invalid_token_returns_none(self):
        """Invalid token should return None."""
        invalid_token = "invalid.token.here"
        payload = decode_access_token(invalid_token)
        assert payload is None

    def test_token_contains_expiration(self):
        """Token payload should contain expiration."""
        token = create_access_token(data={"sub": "test"})
        payload = decode_access_token(token)
        assert "exp" in payload
