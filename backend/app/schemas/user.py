"""
User-related Pydantic schemas
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr
from ..models.user import UserRole, ExperienceLevel


class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: UserRole
    bio: Optional[str] = None
    region: Optional[str] = None
    available_hours_per_week: Optional[int] = None
    domain_knowledge: Optional[str] = None
    experience_level: ExperienceLevel = ExperienceLevel.BEGINNER


class UserCreate(UserBase):
    password: str
    project_experience: Optional[str] = None
    certifications: Optional[List[str]] = None
    tech_stack: Optional[List[str]] = None
    preferred_positions: Optional[List[str]] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    region: Optional[str] = None
    available_hours_per_week: Optional[int] = None
    domain_knowledge: Optional[str] = None
    experience_level: Optional[ExperienceLevel] = None
    project_experience: Optional[str] = None
    certifications: Optional[List[str]] = None
    tech_stack: Optional[List[str]] = None
    preferred_positions: Optional[List[str]] = None


class UserResponse(UserBase):
    id: str
    is_active: bool
    no_show_count: int
    penalty_until: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    project_experience: Optional[str] = None
    certifications: Optional[List[str]] = None
    tech_stack: Optional[List[str]] = None
    preferred_positions: Optional[List[str]] = None
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    refresh_token: str