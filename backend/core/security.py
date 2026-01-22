"""
Security utilities for authentication and authorization.
Handles password hashing and JWT token management.
"""

from datetime import datetime, timedelta, timezone
from typing import Any
import hashlib

from jose import JWTError, jwt
from passlib.context import CryptContext

from core.config import settings

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _prepare_password(password: str) -> str:
    """
    Prepare password for bcrypt by hashing if too long.
    bcrypt has a 72-byte limit, so we pre-hash longer passwords.
    """
    # Encode to bytes to check actual byte length
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Pre-hash with SHA-256 and use hex digest (64 chars, within limit)
        return hashlib.sha256(password_bytes).hexdigest()
    return password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password: The plain text password to verify.
        hashed_password: The hashed password to compare against.
    
    Returns:
        True if the password matches, False otherwise.
    """
    prepared = _prepare_password(plain_password)
    return pwd_context.verify(prepared, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a plain password using bcrypt.
    
    Args:
        password: The plain text password to hash.
    
    Returns:
        The hashed password string.
    """
    prepared = _prepare_password(password)
    return pwd_context.hash(prepared)


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: The payload data to encode in the token.
        expires_delta: Optional custom expiration time.
    
    Returns:
        The encoded JWT token string.
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm,
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any] | None:
    """
    Decode and verify a JWT access token.
    
    Args:
        token: The JWT token string to decode.
    
    Returns:
        The decoded payload if valid, None if invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        return payload
    except JWTError:
        return None
