"""
Project-related Pydantic schemas
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel
from ..models.project import ProjectCategory, RemoteType, RecruitmentStatus, DifficultyLevel


class ProjectBase(BaseModel):
    title: str
    summary: str
    description: str
    category: ProjectCategory
    goal: str
    expected_duration_weeks: int
    start_date: Optional[date] = None
    remote_type: RemoteType
    tech_stack_required: Optional[List[str]] = None
    positions_needed: Optional[Dict[str, int]] = None
    difficulty_level_manual: Optional[DifficultyLevel] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    category: Optional[ProjectCategory] = None
    goal: Optional[str] = None
    expected_duration_weeks: Optional[int] = None
    start_date: Optional[date] = None
    remote_type: Optional[RemoteType] = None
    recruitment_status: Optional[RecruitmentStatus] = None
    tech_stack_required: Optional[List[str]] = None
    positions_needed: Optional[Dict[str, int]] = None
    difficulty_level_manual: Optional[DifficultyLevel] = None


class ProjectResponse(ProjectBase):
    id: str
    leader_id: str
    recruitment_status: RecruitmentStatus
    difficulty_level_ai: Optional[DifficultyLevel] = None
    feasibility_score: Optional[float] = None
    risk_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    projects: List[ProjectResponse]
    total: int
    page: int
    size: int


class ProjectSearchFilters(BaseModel):
    category: Optional[ProjectCategory] = None
    remote_type: Optional[RemoteType] = None
    difficulty_level: Optional[DifficultyLevel] = None
    tech_stack: Optional[List[str]] = None
    page: int = 1
    size: int = 20