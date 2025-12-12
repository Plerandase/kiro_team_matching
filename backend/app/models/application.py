"""
Project application and team member models
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, Float, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum


class ApplicationStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class ProjectApplication(Base):
    __tablename__ = "project_applications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    applied_position = Column(String, nullable=False)  # "FE", "BE", "PM", etc.
    motivation = Column(Text, nullable=False)
    portfolio_link = Column(String, nullable=True)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    fit_score_ai = Column(Float, nullable=True)  # AI-calculated fit score (0-1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="applications")
    user = relationship("User", back_populates="applications")
    
    def can_be_accepted(self) -> bool:
        """Check if application can be accepted"""
        return self.status == ApplicationStatus.PENDING
    
    def can_be_rejected(self) -> bool:
        """Check if application can be rejected"""
        return self.status == ApplicationStatus.PENDING


class TeamMember(Base):
    __tablename__ = "team_members"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    role_in_project = Column(String, nullable=False)  # "FE", "BE", "PM", etc.
    is_leader = Column(Boolean, default=False)
    performance_score = Column(Float, nullable=True)  # For future evaluation system
    joined_at = Column(DateTime, default=datetime.utcnow)
    left_at = Column(DateTime, nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="team_members")
    user = relationship("User", back_populates="team_memberships")
    
    def is_active_member(self) -> bool:
        """Check if team member is currently active"""
        return self.left_at is None