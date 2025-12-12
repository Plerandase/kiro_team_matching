"""
Project management router for CRUD operations and team management
"""
import json
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from ..core.database import get_db
from ..core.deps import get_current_active_user, require_leader_role
from ..models.user import User
from ..models.project import Project, ProjectCategory, RemoteType, DifficultyLevel
from ..models.application import ProjectApplication, TeamMember, ApplicationStatus
from ..schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse, ProjectSearchFilters
)
from ..schemas.application import ApplicationCreate, ApplicationResponse, ApplicationStatusUpdate, TeamMemberResponse

router = APIRouter()


@router.post("", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(require_leader_role),
    db: Session = Depends(get_db)
):
    """
    Create a new project (leaders only)
    """
    # Convert lists to JSON strings for storage
    tech_stack_json = json.dumps(project_data.tech_stack_required) if project_data.tech_stack_required else None
    
    db_project = Project(
        leader_id=current_user.id,
        title=project_data.title,
        summary=project_data.summary,
        description=project_data.description,
        category=project_data.category,
        goal=project_data.goal,
        expected_duration_weeks=project_data.expected_duration_weeks,
        start_date=project_data.start_date,
        remote_type=project_data.remote_type,
        tech_stack_required=tech_stack_json,
        positions_needed=project_data.positions_needed,
        difficulty_level_manual=project_data.difficulty_level_manual
    )
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    return ProjectResponse(
        id=str(db_project.id),
        leader_id=str(db_project.leader_id),
        title=db_project.title,
        summary=db_project.summary,
        description=db_project.description,
        category=db_project.category,
        goal=db_project.goal,
        expected_duration_weeks=db_project.expected_duration_weeks,
        start_date=db_project.start_date,
        remote_type=db_project.remote_type,
        recruitment_status=db_project.recruitment_status,
        tech_stack_required=json.loads(db_project.tech_stack_required) if db_project.tech_stack_required else None,
        positions_needed=db_project.positions_needed,
        difficulty_level_manual=db_project.difficulty_level_manual,
        difficulty_level_ai=db_project.difficulty_level_ai,
        feasibility_score=db_project.feasibility_score,
        risk_notes=db_project.risk_notes,
        created_at=db_project.created_at,
        updated_at=db_project.updated_at
    )


@router.get("", response_model=ProjectListResponse)
async def list_projects(
    category: Optional[ProjectCategory] = Query(None),
    remote_type: Optional[RemoteType] = Query(None),
    difficulty_level: Optional[DifficultyLevel] = Query(None),
    tech_stack: Optional[str] = Query(None),  # Comma-separated list
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    List projects with filtering and pagination
    """
    query = db.query(Project)
    
    # Apply filters
    if category:
        query = query.filter(Project.category == category)
    
    if remote_type:
        query = query.filter(Project.remote_type == remote_type)
    
    if difficulty_level:
        query = query.filter(
            or_(
                Project.difficulty_level_manual == difficulty_level,
                Project.difficulty_level_ai == difficulty_level
            )
        )
    
    if tech_stack:
        # Filter by tech stack (simple contains check)
        tech_list = [tech.strip() for tech in tech_stack.split(",")]
        for tech in tech_list:
            query = query.filter(Project.tech_stack_required.contains(tech))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * size
    projects = query.offset(offset).limit(size).all()
    
    # Convert to response format
    project_responses = []
    for project in projects:
        project_responses.append(ProjectResponse(
            id=str(project.id),
            leader_id=str(project.leader_id),
            title=project.title,
            summary=project.summary,
            description=project.description,
            category=project.category,
            goal=project.goal,
            expected_duration_weeks=project.expected_duration_weeks,
            start_date=project.start_date,
            remote_type=project.remote_type,
            recruitment_status=project.recruitment_status,
            tech_stack_required=json.loads(project.tech_stack_required) if project.tech_stack_required else None,
            positions_needed=project.positions_needed,
            difficulty_level_manual=project.difficulty_level_manual,
            difficulty_level_ai=project.difficulty_level_ai,
            feasibility_score=project.feasibility_score,
            risk_notes=project.risk_notes,
            created_at=project.created_at,
            updated_at=project.updated_at
        ))
    
    return ProjectListResponse(
        projects=project_responses,
        total=total,
        page=page,
        size=size
    )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get project details by ID
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return ProjectResponse(
        id=str(project.id),
        leader_id=str(project.leader_id),
        title=project.title,
        summary=project.summary,
        description=project.description,
        category=project.category,
        goal=project.goal,
        expected_duration_weeks=project.expected_duration_weeks,
        start_date=project.start_date,
        remote_type=project.remote_type,
        recruitment_status=project.recruitment_status,
        tech_stack_required=json.loads(project.tech_stack_required) if project.tech_stack_required else None,
        positions_needed=project.positions_needed,
        difficulty_level_manual=project.difficulty_level_manual,
        difficulty_level_ai=project.difficulty_level_ai,
        feasibility_score=project.feasibility_score,
        risk_notes=project.risk_notes,
        created_at=project.created_at,
        updated_at=project.updated_at
    )


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_update: ProjectUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update project (leader only)
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check if user is the project leader
    if str(project.leader_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only project leader can update the project"
        )
    
    # Update fields if provided
    update_data = project_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if field == "tech_stack_required" and value is not None:
            setattr(project, field, json.dumps(value))
        else:
            setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    
    return ProjectResponse(
        id=str(project.id),
        leader_id=str(project.leader_id),
        title=project.title,
        summary=project.summary,
        description=project.description,
        category=project.category,
        goal=project.goal,
        expected_duration_weeks=project.expected_duration_weeks,
        start_date=project.start_date,
        remote_type=project.remote_type,
        recruitment_status=project.recruitment_status,
        tech_stack_required=json.loads(project.tech_stack_required) if project.tech_stack_required else None,
        positions_needed=project.positions_needed,
        difficulty_level_manual=project.difficulty_level_manual,
        difficulty_level_ai=project.difficulty_level_ai,
        feasibility_score=project.feasibility_score,
        risk_notes=project.risk_notes,
        created_at=project.created_at,
        updated_at=project.updated_at
    )


@router.post("/{project_id}/apply", response_model=ApplicationResponse)
async def apply_to_project(
    project_id: str,
    application_data: ApplicationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Apply to join a project
    """
    # Check if project exists and is open for recruitment
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if project.recruitment_status != "OPEN":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project is not open for recruitment"
        )
    
    # Check if user already applied
    existing_application = db.query(ProjectApplication).filter(
        and_(
            ProjectApplication.project_id == project_id,
            ProjectApplication.user_id == current_user.id
        )
    ).first()
    
    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied to this project"
        )
    
    # Create application
    db_application = ProjectApplication(
        project_id=project_id,
        user_id=current_user.id,
        applied_position=application_data.applied_position,
        motivation=application_data.motivation,
        portfolio_link=application_data.portfolio_link
    )
    
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    
    return ApplicationResponse(
        id=str(db_application.id),
        project_id=str(db_application.project_id),
        user_id=str(db_application.user_id),
        applied_position=db_application.applied_position,
        motivation=db_application.motivation,
        portfolio_link=db_application.portfolio_link,
        status=db_application.status,
        fit_score_ai=db_application.fit_score_ai,
        created_at=db_application.created_at,
        updated_at=db_application.updated_at
    )


@router.get("/{project_id}/applications", response_model=List[ApplicationResponse])
async def get_project_applications(
    project_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all applications for a project (leader only)
    """
    # Check if project exists and user is the leader
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if str(project.leader_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only project leader can view applications"
        )
    
    applications = db.query(ProjectApplication).filter(
        ProjectApplication.project_id == project_id
    ).all()
    
    return [
        ApplicationResponse(
            id=str(app.id),
            project_id=str(app.project_id),
            user_id=str(app.user_id),
            applied_position=app.applied_position,
            motivation=app.motivation,
            portfolio_link=app.portfolio_link,
            status=app.status,
            fit_score_ai=app.fit_score_ai,
            created_at=app.created_at,
            updated_at=app.updated_at
        )
        for app in applications
    ]


@router.post("/{project_id}/applications/{app_id}/accept")
async def accept_application(
    project_id: str,
    app_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Accept a project application (leader only)
    """
    # Verify project and leadership
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project or str(project.leader_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only project leader can accept applications"
        )
    
    # Get application
    application = db.query(ProjectApplication).filter(
        and_(
            ProjectApplication.id == app_id,
            ProjectApplication.project_id == project_id
        )
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    if application.status != ApplicationStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Application is not pending"
        )
    
    # Accept application and create team member
    application.status = ApplicationStatus.ACCEPTED
    
    team_member = TeamMember(
        project_id=project_id,
        user_id=application.user_id,
        role_in_project=application.applied_position,
        is_leader=False
    )
    
    db.add(team_member)
    db.commit()
    
    return {"message": "Application accepted successfully"}


@router.post("/{project_id}/applications/{app_id}/reject")
async def reject_application(
    project_id: str,
    app_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Reject a project application (leader only)
    """
    # Verify project and leadership
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project or str(project.leader_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only project leader can reject applications"
        )
    
    # Get application
    application = db.query(ProjectApplication).filter(
        and_(
            ProjectApplication.id == app_id,
            ProjectApplication.project_id == project_id
        )
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    if application.status != ApplicationStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Application is not pending"
        )
    
    # Reject application
    application.status = ApplicationStatus.REJECTED
    db.commit()
    
    return {"message": "Application rejected successfully"}


@router.get("/{project_id}/team", response_model=List[TeamMemberResponse])
async def get_project_team(
    project_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get project team members
    """
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Get team members
    team_members = db.query(TeamMember).filter(
        TeamMember.project_id == project_id
    ).all()
    
    return [
        TeamMemberResponse(
            id=str(member.id),
            project_id=str(member.project_id),
            user_id=str(member.user_id),
            role_in_project=member.role_in_project,
            is_leader=member.is_leader,
            performance_score=member.performance_score,
            joined_at=member.joined_at,
            left_at=member.left_at
        )
        for member in team_members
    ]