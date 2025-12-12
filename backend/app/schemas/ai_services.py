"""
AI services schemas
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from ..models.project import DifficultyLevel


class FeasibilityAnalysisRequest(BaseModel):
    title: str
    summary: str
    description: str
    goal: str
    team_size: int
    expected_duration_weeks: int
    stack: List[str]
    target_type: str  # "PERSONAL_PORTFOLIO", "CONTEST", "BUSINESS_MVP"


class FeasibilityAnalysisResponse(BaseModel):
    feasibility_score: float  # 0-100
    difficulty_level_ai: DifficultyLevel
    risk_factors: List[str]
    missing_roles: List[str]
    over_scoped_features: List[str]
    recommendations: str
    auto_project_proposal: str


class TimelineGenerationRequest(BaseModel):
    features: List[str]
    team_size: int
    members: Optional[List[Dict[str, str]]] = None  # [{"role": "FE", "experience_level": "MID"}]
    hours_per_week: int
    duration_weeks: int


class TimelineTask(BaseModel):
    week: int
    summary: str
    tasks: List[str]


class WBSItem(BaseModel):
    id: str
    name: str
    parent_id: Optional[str] = None
    estimate_hours: int


class TimelineGenerationResponse(BaseModel):
    timeline: List[TimelineTask]
    wbs: List[WBSItem]
    risks: List[str]
    bottlenecks: List[str]
    architecture_suggestion: str


class LearningRoadmapRequest(BaseModel):
    user_id: str
    project_id: str
    target_stack: List[str]
    days_available_per_week: int
    weeks_until_project_critical_phase: int


class LearningPhase(BaseModel):
    day_range: str
    focus_topic: str
    resources: List[str]
    practice_tasks: List[str]


class LearningRoadmapResponse(BaseModel):
    roadmap: List[LearningPhase]
    checkpoint_quiz_ideas: List[str]
    summary_for_leader: str


class ProjectMonitoringRequest(BaseModel):
    commit_activity: Optional[Dict[str, Any]] = None
    meeting_summaries: Optional[List[str]] = None
    task_progress: Optional[List[Dict[str, str]]] = None


class ProjectMonitoringResponse(BaseModel):
    health_score: float  # 0-100
    risk_level: str  # "LOW", "MEDIUM", "HIGH"
    issues_detected: List[str]
    recommendations: List[str]


class PortfolioGenerationRequest(BaseModel):
    user_id: str
    role_in_project: str
    tech_stack_used: List[str]
    contributions: str
    repo_links: List[str]


class InterviewQA(BaseModel):
    question: str
    answer: str


class PortfolioGenerationResponse(BaseModel):
    portfolio_text: str
    interview_qas: List[InterviewQA]
    raw_markdown: str