"""
AI services router for all AI-powered features
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.deps import get_current_active_user
from ..models.user import User
from ..services.ai_project import AIProjectService
from ..services.ai_learning import AILearningService
from ..schemas.ai_services import (
    FeasibilityAnalysisRequest, FeasibilityAnalysisResponse,
    TimelineGenerationRequest, TimelineGenerationResponse,
    LearningRoadmapRequest, LearningRoadmapResponse,
    ProjectMonitoringRequest, ProjectMonitoringResponse,
    PortfolioGenerationRequest, PortfolioGenerationResponse
)

router = APIRouter()


@router.post("/projects/feasibility", response_model=FeasibilityAnalysisResponse)
async def analyze_project_feasibility(
    request: FeasibilityAnalysisRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Analyze project feasibility and provide recommendations
    """
    try:
        result = await AIProjectService.analyze_feasibility(request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Feasibility analysis failed: {str(e)}"
        )


@router.post("/projects/{project_id}/timeline", response_model=TimelineGenerationResponse)
async def generate_project_timeline(
    project_id: str,
    request: TimelineGenerationRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Generate project timeline and work breakdown structure
    """
    # TODO: Verify user has access to project
    try:
        result = await AIProjectService.generate_timeline(request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Timeline generation failed: {str(e)}"
        )


@router.post("/learning-path", response_model=LearningRoadmapResponse)
async def generate_learning_roadmap(
    request: LearningRoadmapRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Generate personalized learning roadmap
    """
    try:
        result = await AILearningService.generate_learning_roadmap(request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Learning roadmap generation failed: {str(e)}"
        )


@router.post("/projects/{project_id}/monitor", response_model=ProjectMonitoringResponse)
async def monitor_project_health(
    project_id: str,
    request: ProjectMonitoringRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Monitor project health and detect issues
    """
    # TODO: Verify user has access to project
    try:
        result = await AIProjectService.monitor_project_health(request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Project monitoring failed: {str(e)}"
        )


@router.post("/projects/{project_id}/portfolio", response_model=PortfolioGenerationResponse)
async def generate_portfolio(
    project_id: str,
    request: PortfolioGenerationRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Generate portfolio content and interview guide (usage limited)
    """
    # TODO: Verify user has access to project
    try:
        result = await AILearningService.generate_portfolio(request, db)
        return result
    except Exception as e:
        if "limit exceeded" in str(e):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Portfolio generation failed: {str(e)}"
        )