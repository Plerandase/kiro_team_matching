"""
Authentication router for user registration, login, and token management
"""
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, verify_token
from ..models.user import User
from ..schemas.user import UserCreate, UserLogin, TokenResponse, RefreshTokenRequest, UserResponse

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    
    # Convert lists to JSON strings for storage
    certifications_json = json.dumps(user_data.certifications) if user_data.certifications else None
    tech_stack_json = json.dumps(user_data.tech_stack) if user_data.tech_stack else None
    preferred_positions_json = json.dumps(user_data.preferred_positions) if user_data.preferred_positions else None
    
    db_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        name=user_data.name,
        role=user_data.role,
        bio=user_data.bio,
        region=user_data.region,
        available_hours_per_week=user_data.available_hours_per_week,
        domain_knowledge=user_data.domain_knowledge,
        experience_level=user_data.experience_level,
        project_experience=user_data.project_experience,
        certifications=certifications_json,
        tech_stack=tech_stack_json,
        preferred_positions=preferred_positions_json
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Generate tokens
    access_token = create_access_token(data={"sub": str(db_user.id)})
    refresh_token = create_refresh_token(data={"sub": str(db_user.id)})
    
    # Convert user to response format
    user_response = UserResponse(
        id=str(db_user.id),
        email=db_user.email,
        name=db_user.name,
        role=db_user.role,
        bio=db_user.bio,
        region=db_user.region,
        available_hours_per_week=db_user.available_hours_per_week,
        domain_knowledge=db_user.domain_knowledge,
        experience_level=db_user.experience_level,
        is_active=db_user.is_active,
        no_show_count=db_user.no_show_count,
        penalty_until=db_user.penalty_until,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
        project_experience=db_user.project_experience,
        certifications=json.loads(db_user.certifications) if db_user.certifications else None,
        tech_stack=json.loads(db_user.tech_stack) if db_user.tech_stack else None,
        preferred_positions=json.loads(db_user.preferred_positions) if db_user.preferred_positions else None
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user_response
    )


@router.post("/login", response_model=TokenResponse)
async def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT tokens
    """
    # Find user by email
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Generate tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    # Convert user to response format
    user_response = UserResponse(
        id=str(user.id),
        email=user.email,
        name=user.name,
        role=user.role,
        bio=user.bio,
        region=user.region,
        available_hours_per_week=user.available_hours_per_week,
        domain_knowledge=user.domain_knowledge,
        experience_level=user.experience_level,
        is_active=user.is_active,
        no_show_count=user.no_show_count,
        penalty_until=user.penalty_until,
        created_at=user.created_at,
        updated_at=user.updated_at,
        project_experience=user.project_experience,
        certifications=json.loads(user.certifications) if user.certifications else None,
        tech_stack=json.loads(user.tech_stack) if user.tech_stack else None,
        preferred_positions=json.loads(user.preferred_positions) if user.preferred_positions else None
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user_response
    )


@router.post("/refresh", response_model=dict)
async def refresh_access_token(refresh_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token
    """
    # Verify refresh token
    payload = verify_token(refresh_data.refresh_token, token_type="refresh")
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Verify user still exists
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Generate new access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }