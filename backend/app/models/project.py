"""
Project model for project management and team formation
"""
import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, Date, Float, JSON, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum


class ProjectCategory(str, enum.Enum):
    CONTEST = "CONTEST"
    BUSINESS = "BUSINESS"
    STUDY = "STUDY"
    ETC = "ETC"


class RemoteType(str, enum.Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    HYBRID = "HYBRID"


class RecruitmentStatus(str, enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"


class DifficultyLevel(str, enum.Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    leader_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Enum(ProjectCategory), nullable=False)
    goal = Column(String, nullable=False)
    expected_duration_weeks = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=True)
    remote_type = Column(Enum(RemoteType), nullable=False)
    recruitment_status = Column(Enum(RecruitmentStatus), default=RecruitmentStatus.OPEN)
    tech_stack_required = Column(Text, nullable=True)  # JSON string
    positions_needed = Column(JSON, nullable=True)  # {"FE": 2, "BE": 1, "DESIGNER": 1}
    difficulty_level_manual = Column(Enum(DifficultyLevel), nullable=True)
    difficulty_level_ai = Column(Enum(DifficultyLevel), nullable=True)
    feasibility_score = Column(Float, nullable=True)  # 0-100
    risk_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    leader = relationship("User", back_populates="led_projects", foreign_keys=[leader_id])
    applications = relationship("ProjectApplication", back_populates="project")
    team_members = relationship("TeamMember", back_populates="project")
    chat_rooms = relationship("ChatRoom", back_populates="project")
    meeting_notes = relationship("MeetingNote", back_populates="project")
    ai_feature_usage = relationship("AIFeatureUsage", back_populates="project")
    verification_templates = relationship("VerificationEmailTemplate", back_populates="project")
    
    def get_team_size(self) -> int:
        """Get current team size including leader"""
        return len(self.team_members) + 1  # +1 for leader
    
    def get_needed_positions_count(self) -> int:
        """Get total number of positions needed"""
        if not self.positions_needed:
            return 0
        return sum(self.positions_needed.values())
    
    def is_team_complete(self) -> bool:
        """Check if team has all required positions filled"""
        if not self.positions_needed:
            return True
        
        current_positions = {}
        for member in self.team_members:
            pos = member.role_in_project
            current_positions[pos] = current_positions.get(pos, 0) + 1
        
        for position, needed_count in self.positions_needed.items():
            if current_positions.get(position, 0) < needed_count:
                return False
        
        return True
    
    def can_transition_to_in_progress(self) -> bool:
        """Check if project can transition to IN_PROGRESS status"""
        return (
            self.recruitment_status == RecruitmentStatus.OPEN and
            self.is_team_complete()
        )