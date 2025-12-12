"""
Application and team member schemas
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from ..models.application import ApplicationStatus


class ApplicationBase(BaseModel):
    applied_position: str
    motivation: str
    portfolio_link: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationResponse(ApplicationBase):
    id: str
    project_id: str
    user_id: str
    status: ApplicationStatus
    fit_score_ai: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus


class TeamMemberResponse(BaseModel):
    id: str
    project_id: str
    user_id: str
    role_in_project: str
    is_leader: bool
    performance_score: Optional[float] = None
    joined_at: datetime
    left_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True