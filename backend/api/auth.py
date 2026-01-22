"""
Authentication API endpoints.
Handles user registration, login, and token management.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.dependencies import DbSession, CurrentUserId
from schemas.user import UserCreate, UserResponse, Token
from services.user_service import UserService

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_data: UserCreate,
    db: DbSession,
) -> UserResponse:
    """
    Register a new user account.
    
    Args:
        user_data: User registration data (email, password, full_name).
        db: Database session.
    
    Returns:
        The created user information.
    
    Raises:
        HTTPException: If email is already registered.
    """
    service = UserService(db)
    
    try:
        user = await service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
    return UserResponse.model_validate(user)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: DbSession = None,
) -> Token:
    """
    Authenticate user and return JWT access token.
    
    Uses OAuth2 password flow with username (email) and password.
    
    Args:
        form_data: OAuth2 form with username and password.
        db: Database session.
    
    Returns:
        JWT access token.
    
    Raises:
        HTTPException: If credentials are invalid.
    """
    service = UserService(db)
    
    user = await service.authenticate_user(
        email=form_data.username,
        password=form_data.password,
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled",
        )
    
    return service.create_token_for_user(user)


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user_id: CurrentUserId,
    db: DbSession,
) -> UserResponse:
    """
    Get the currently authenticated user's information.
    
    Args:
        user_id: The authenticated user's ID from JWT.
        db: Database session.
    
    Returns:
        Current user information.
    
    Raises:
        HTTPException: If user not found.
    """
    from uuid import UUID
    
    service = UserService(db)
    user = await service.get_user_by_id(UUID(user_id))
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return UserResponse.model_validate(user)
