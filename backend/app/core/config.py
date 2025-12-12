"""
Core configuration settings for ProjectMate AI
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://username:password@localhost:5432/projectmate_ai"
    test_database_url: str = "postgresql://username:password@localhost:5432/projectmate_ai_test"
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # AI Provider
    ai_provider: str = "openai"  # openai or bedrock
    openai_api_key: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # S3
    s3_bucket_name: str = "projectmate-ai-uploads"
    s3_region: str = "us-east-1"
    
    # Application
    debug: bool = True
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Penalty system
    max_no_show_count: int = 3
    penalty_duration_days: int = 30
    
    # AI Usage limits
    portfolio_generation_limit: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()