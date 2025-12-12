"""
AI feature usage tracking and verification models
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, Float, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum


class AIFeatureType(str, enum.Enum):
    PORTFOLIO_GENERATION = "PORTFOLIO_GENERATION"
    INTERVIEW_GUIDE = "INTERVIEW_GUIDE"
    TEST_GENERATION = "TEST_GENERATION"
    FEASIBILITY_ANALYSIS = "FEASIBILITY_ANALYSIS"
    TIMELINE_GENERATION = "TIMELINE_GENERATION"
    LEARNING_ROADMAP = "LEARNING_ROADMAP"
    MEETING_SUMMARY = "MEETING_SUMMARY"
    PROJECT_MONITORING = "PROJECT_MONITORING"


class AIFeatureUsage(Base):
    __tablename__ = "ai_feature_usage"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    feature_type = Column(Enum(AIFeatureType), nullable=False)
    count = Column(Integer, default=0)
    last_used_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="ai_feature_usage")
    user = relationship("User", back_populates="ai_feature_usage")
    
    def can_use_feature(self, limit: int) -> bool:
        """Check if feature can be used based on usage limit"""
        return self.count < limit
    
    def increment_usage(self):
        """Increment usage count and update timestamp"""
        self.count += 1
        self.last_used_at = datetime.utcnow()


class VerificationEmailTemplate(Base):
    __tablename__ = "verification_email_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True)
    s3_bucket = Column(String, nullable=False)
    s3_key = Column(String, nullable=False)
    parsed_text_ai = Column(Text, nullable=True)  # OCR extracted text
    hash_signature = Column(String, nullable=True)  # Simple text hash
    verified = Column(Boolean, nullable=True)
    similarity_score = Column(Float, nullable=True)  # 0-1 similarity score
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="verification_templates")
    project = relationship("Project", back_populates="verification_templates")
    
    def is_suspicious(self, threshold: float = 0.9) -> bool:
        """Check if template is suspicious based on similarity score"""
        return self.similarity_score is not None and self.similarity_score >= threshold