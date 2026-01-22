"""
User service for authentication and user management.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import get_password_hash, verify_password, create_access_token
from models.user import User
from schemas.user import UserCreate, UserResponse, Token


class UserService:
    """Service class for user-related operations."""

    def __init__(self, db: AsyncSession) -> None:
        """
        Initialize the user service.

        Args:
            db: Async database session.
        """
        self.db = db

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Get a user by their email address.

        Args:
            email: The user's email address.

        Returns:
            The User object if found, None otherwise.
        """
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        """
        Get a user by their ID.

        Args:
            user_id: The user's UUID.

        Returns:
            The User object if found, None otherwise.
        """
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user.

        Args:
            user_data: The user creation data.

        Returns:
            The newly created User object.

        Raises:
            ValueError: If a user with this email already exists.
        """
        # Check if user already exists
        existing_user = await self.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("A user with this email already exists")

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> User | None:
        """
        Authenticate a user with email and password.

        Args:
            email: The user's email address.
            password: The plain text password.

        Returns:
            The User object if authentication successful, None otherwise.
        """
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create_token_for_user(self, user: User) -> Token:
        """
        Create a JWT access token for a user.

        Args:
            user: The User object.

        Returns:
            Token object containing the access token.
        """
        access_token = create_access_token(
            data={"sub": str(user.id)}
        )
        return Token(access_token=access_token)
