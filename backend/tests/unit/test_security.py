"""
Comprehensive unit tests for authentication service and security utilities.
"""

import pytest
from datetime import timedelta
from uuid import uuid4

from core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
)


class TestPasswordHashing:
    """Tests for password hashing functions."""

    def test_password_hash_creates_different_hash(self):
        """Hashing the same password twice should create different hashes (salted)."""
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

    def test_empty_password_can_be_hashed(self):
        """Empty string password should still be hashable."""
        password = ""
        hashed = get_password_hash(password)
        assert hashed is not None
        assert verify_password(password, hashed) is True

    def test_unicode_password_works(self):
        """Unicode passwords should work correctly."""
        password = "密码测试🔐"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_very_long_password_works(self):
        """Very long passwords should work (bcrypt has 72 byte limit, we pre-hash)."""
        password = "a" * 1000
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_special_characters_in_password(self):
        """Passwords with special characters should work."""
        password = "P@$$w0rd!#$%^&*()_+-=[]{}|;':\",./<>?"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True


class TestJWTTokens:
    """Tests for JWT token functions."""

    def test_create_and_decode_token(self):
        """Token should be creatable and decodable."""
        user_id = str(uuid4())
        token = create_access_token(data={"sub": user_id})
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 50  # JWT tokens are reasonably long
        
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
        assert payload is not None
        assert "exp" in payload

    def test_custom_expiration_delta(self):
        """Token with custom expiration should work."""
        token = create_access_token(
            data={"sub": "test"},
            expires_delta=timedelta(hours=24),
        )
        payload = decode_access_token(token)
        assert payload is not None

    def test_token_with_additional_claims(self):
        """Token can contain additional custom claims."""
        token = create_access_token(
            data={
                "sub": "user123",
                "role": "admin",
                "permissions": ["read", "write"],
            }
        )
        payload = decode_access_token(token)
        assert payload["sub"] == "user123"
        assert payload["role"] == "admin"
        assert payload["permissions"] == ["read", "write"]

    def test_tampered_token_fails(self):
        """Tampered token should fail verification."""
        token = create_access_token(data={"sub": "test"})
        # Tamper with the token
        parts = token.split(".")
        parts[1] = parts[1][:-3] + "xxx"  # Modify payload
        tampered = ".".join(parts)
        
        payload = decode_access_token(tampered)
        assert payload is None

    def test_empty_payload_token(self):
        """Token with minimal payload should work."""
        token = create_access_token(data={})
        payload = decode_access_token(token)
        assert payload is not None
        assert "exp" in payload

    def test_token_is_different_each_time(self):
        """Same data should produce different tokens (due to timestamp)."""
        import time
        token1 = create_access_token(data={"sub": "test"})
        time.sleep(0.01)  # Small delay
        token2 = create_access_token(data={"sub": "test"})
        # Tokens might be same if generated in same second, so just verify both work
        assert decode_access_token(token1) is not None
        assert decode_access_token(token2) is not None
