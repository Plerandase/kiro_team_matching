"""
User profile management router
"""
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.deps import get_current_user, get_current_active_user
from ..models.user import User
from ..schemas.user import UserResponse, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user's profile information
    """
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        name=current_user.name,
        role=current_user.role,
        bio=current_user.bio,
        region=current_user.region,
        available_hours_per_week=current_user.available_hours_per_week,
        domain_knowledge=current_user.domain_knowledge,
        experience_level=current_user.experience_level,
        is_active=current_user.is_active,
        no_show_count=current_user.no_show_count,
        penalty_until=current_user.penalty_until,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        project_experience=current_user.project_experience,
        certifications=json.loads(current_user.certifications) if current_user.certifications else None,
        tech_stack=json.loads(current_user.tech_stack) if current_user.tech_stack else None,
        preferred_positions=json.loads(current_user.preferred_positions) if current_user.preferred_positions else None
    )


@router.patch("/me", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile information
    """
    # Update fields if provided
    update_data = user_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if field in ["certifications", "tech_stack", "preferred_positions"]:
            # Convert lists to JSON strings
            if value is not None:
                setattr(current_user, field, json.dumps(value))
            else:
                setattr(current_user, field, None)
        else:
            setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        name=current_user.name,
        role=current_user.role,
        bio=current_user.bio,
        region=current_user.region,
        available_hours_per_week=current_user.available_hours_per_week,
        domain_knowledge=current_user.domain_knowledge,
        experience_level=current_user.experience_level,
        is_active=current_user.is_active,
        no_show_count=current_user.no_show_count,
        penalty_until=current_user.penalty_until,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        project_experience=current_user.project_experience,
        certifications=json.loads(current_user.certifications) if current_user.certifications else None,
        tech_stack=json.loads(current_user.tech_stack) if current_user.tech_stack else None,
        preferred_positions=json.loads(current_user.preferred_positions) if current_user.preferred_positions else None
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_profile(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get another user's public profile information
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Return public profile (excluding sensitive information)
    return UserResponse(
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
        no_show_count=0,  # Hide sensitive penalty information
        penalty_until=None,
        created_at=user.created_at,
        updated_at=user.updated_at,
        project_experience=user.project_experience,
        certifications=json.loads(user.certifications) if user.certifications else None,
        tech_stack=json.loads(user.tech_stack) if user.tech_stack else None,
        preferred_positions=json.loads(user.preferred_positions) if user.preferred_positions else None
    )