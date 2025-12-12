"""
User model for authentication and profile management
"""
import uuid
from datetime import datetime, timedelta
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..core.database import Base
from ..core.config import settings
import enum


class UserRole(str, enum.Enum):
    LEADER = "LEADER"
    MEMBER = "MEMBER"
    BOTH = "BOTH"


class ExperienceLevel(str, enum.Enum):
    BEGINNER = "BEGINNER"
    JUNIOR = "JUNIOR"
    MID = "MID"
    SENIOR = "SENIOR"


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    bio = Column(Text, nullable=True)
    region = Column(String, nullable=True)
    available_hours_per_week = Column(Integer, nullable=True)
    domain_knowledge = Column(Text, nullable=True)
    experience_level = Column(Enum(ExperienceLevel), default=ExperienceLevel.BEGINNER)
    project_experience = Column(Text, nullable=True)
    certifications = Column(Text, nullable=True)  # JSON string
    tech_stack = Column(Text, nullable=True)  # JSON string
    preferred_positions = Column(Text, nullable=True)  # JSON string
    is_active = Column(Boolean, default=True)
    no_show_count = Column(Integer, default=0)
    penalty_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    led_projects = relationship("Project", back_populates="leader", foreign_keys="Project.leader_id")
    applications = relationship("ProjectApplication", back_populates="user")
    team_memberships = relationship("TeamMember", back_populates="user")
    sent_messages = relationship("ChatMessage", back_populates="sender")
    created_meeting_notes = relationship("MeetingNote", back_populates="created_by_user")
    ai_feature_usage = relationship("AIFeatureUsage", back_populates="user")
    verification_templates = relationship("VerificationEmailTemplate", back_populates="user")
    
    def is_under_penalty(self) -> bool:
        """Check if user is currently under penalty"""
        if self.penalty_until is None:
            return False
        return datetime.utcnow() < self.penalty_until
    
    def apply_penalty(self):
        """Apply penalty for no-show behavior"""
        self.no_show_count += 1
        if self.no_show_count >= settings.max_no_show_count:
            self.penalty_until = datetime.utcnow() + timedelta(days=settings.penalty_duration_days)
    
    def can_create_projects(self) -> bool:
        """Check if user can create projects"""
        return self.role in [UserRole.LEADER, UserRole.BOTH] and not self.is_under_penalty()
    
    def can_apply_to_projects(self) -> bool:
        """Check if user can apply to projects"""
        return self.is_active and not self.is_under_penalty()