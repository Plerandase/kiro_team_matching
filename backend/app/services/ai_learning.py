"""
AI-powered learning and portfolio services
"""
import re
import json
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from ..ai.client import call_ai
from ..ai.prompts import PromptTemplates
from ..models.ai_usage import AIFeatureUsage, AIFeatureType
from ..schemas.ai_services import (
    LearningRoadmapRequest, LearningRoadmapResponse, LearningPhase,
    PortfolioGenerationRequest, PortfolioGenerationResponse, InterviewQA
)
from ..core.config import settings


class AILearningService:
    """Service for AI-powered learning and portfolio generation"""
    
    @staticmethod
    async def generate_learning_roadmap(request: LearningRoadmapRequest) -> LearningRoadmapResponse:
        """
        Generate personalized learning roadmap using AI
        """
        try:
            # Generate AI prompt
            prompt = PromptTemplates.learning_roadmap_prompt(
                target_technologies=request.target_stack,
                current_experience="Intermediate",  # TODO: Get from user profile
                days_per_week=request.days_available_per_week,
                weeks_available=request.weeks_until_project_critical_phase,
                project_context=f"Project {request.project_id} preparation"
            )
            
            # Call AI service
            ai_response = await call_ai(prompt)
            
            # Parse AI response
            parsed_response = AILearningService._parse_roadmap_response(ai_response, request.weeks_until_project_critical_phase)
            
            return LearningRoadmapResponse(**parsed_response)
            
        except Exception as e:
            # Fallback response if AI fails
            return LearningRoadmapResponse(
                roadmap=[
                    LearningPhase(
                        day_range="Week 1",
                        focus_topic="Technology fundamentals",
                        resources=["Official documentation", "Online tutorials"],
                        practice_tasks=["Build simple examples", "Complete exercises"]
                    )
                ],
                checkpoint_quiz_ideas=["Basic concept questions", "Practical implementation tasks"],
                summary_for_leader="Team member is learning required technologies. Manual guidance recommended due to AI service unavailability."
            )
    
    @staticmethod
    def _parse_roadmap_response(ai_response: str, weeks_available: int) -> Dict[str, Any]:
        """Parse AI response for learning roadmap"""
        roadmap = []
        
        # Extract learning phases
        for week in range(1, weeks_available + 1):
            week_pattern = f"Week {week}"
            week_match = re.search(f"{week_pattern}.*?(?=Week {week + 1}:|CHECKPOINT QUIZ IDEAS:|$)", ai_response, re.DOTALL)
            
            if week_match:
                week_content = week_match.group(0)
                
                # Extract focus topic
                focus_match = re.search(r"Focus Topic:\s*(.+)", week_content)
                focus_topic = focus_match.group(1).strip() if focus_match else f"Week {week} learning"
                
                # Extract resources
                resources = AILearningService._extract_list_from_section(week_content, "Resources:")
                
                # Extract practice tasks
                practice_tasks = AILearningService._extract_list_from_section(week_content, "Practice Tasks:")
                
                # Determine day range
                day_range = f"Week {week}"
                
                roadmap.append(LearningPhase(
                    day_range=day_range,
                    focus_topic=focus_topic,
                    resources=resources or ["Study materials to be determined"],
                    practice_tasks=practice_tasks or ["Hands-on practice exercises"]
                ))
        
        # Extract checkpoint quiz ideas
        checkpoint_quiz_ideas = AILearningService._extract_list_from_text(ai_response, "CHECKPOINT QUIZ IDEAS:")
        
        # Extract leader summary
        summary_for_leader = AILearningService._extract_text_from_section(ai_response, "LEADER SUMMARY:")
        
        return {
            "roadmap": roadmap,
            "checkpoint_quiz_ideas": checkpoint_quiz_ideas,
            "summary_for_leader": summary_for_leader
        }
    
    @staticmethod
    async def generate_portfolio(request: PortfolioGenerationRequest, db: Session) -> PortfolioGenerationResponse:
        """
        Generate portfolio content with usage limit enforcement
        """
        # Check usage limits
        usage = db.query(AIFeatureUsage).filter(
            AIFeatureUsage.project_id == request.user_id,  # Using user_id as project context
            AIFeatureUsage.user_id == request.user_id,
            AIFeatureUsage.feature_type == AIFeatureType.PORTFOLIO_GENERATION
        ).first()
        
        if not usage:
            usage = AIFeatureUsage(
                project_id=request.user_id,
                user_id=request.user_id,
                feature_type=AIFeatureType.PORTFOLIO_GENERATION,
                count=0
            )
            db.add(usage)
        
        if not usage.can_use_feature(settings.portfolio_generation_limit):
            raise Exception(f"Portfolio generation limit exceeded. Maximum {settings.portfolio_generation_limit} uses allowed.")
        
        try:
            # Generate AI prompt
            prompt = PromptTemplates.portfolio_generation_prompt(
                role=request.role_in_project,
                tech_stack=request.tech_stack_used,
                contributions=request.contributions,
                project_context="Team collaboration project"
            )
            
            # Call AI service
            ai_response = await call_ai(prompt)
            
            # Parse AI response
            parsed_response = AILearningService._parse_portfolio_response(ai_response)
            
            # Increment usage count
            usage.increment_usage()
            db.commit()
            
            return PortfolioGenerationResponse(**parsed_response)
            
        except Exception as e:
            if "limit exceeded" in str(e):
                raise e
            
            # Fallback response if AI fails
            return PortfolioGenerationResponse(
                portfolio_text="Portfolio content generation unavailable. Please create manually.",
                interview_qas=[
                    InterviewQA(
                        question="Tell me about your role in this project.",
                        answer="Please prepare this answer based on your specific contributions."
                    )
                ],
                raw_markdown="# Portfolio Content\n\nManual creation recommended due to AI service unavailability."
            )
    
    @staticmethod
    def _parse_portfolio_response(ai_response: str) -> Dict[str, Any]:
        """Parse AI response for portfolio generation"""
        # Extract portfolio text (STAR format)
        portfolio_text = AILearningService._extract_text_from_section(ai_response, "PORTFOLIO PROJECT DESCRIPTION")
        
        # Extract interview Q&As
        interview_qas = []
        qa_section = AILearningService._extract_text_from_section(ai_response, "INTERVIEW QUESTIONS AND ANSWERS:")
        
        if qa_section:
            # Simple parsing for Q&A pairs
            qa_pairs = re.findall(r'Q:\s*(.*?)\nA:\s*(.*?)(?=\nQ:|$)', qa_section, re.DOTALL)
            for question, answer in qa_pairs[:5]:  # Limit to 5 Q&As
                interview_qas.append(InterviewQA(
                    question=question.strip(),
                    answer=answer.strip()
                ))
        
        # Create markdown version
        raw_markdown = f"""# Portfolio Project

## Project Description
{portfolio_text}

## Technical Highlights
{AILearningService._extract_text_from_section(ai_response, "TECHNICAL HIGHLIGHTS:")}

## Challenges and Solutions
{AILearningService._extract_text_from_section(ai_response, "CHALLENGES AND SOLUTIONS:")}

## Interview Preparation
"""
        
        for qa in interview_qas:
            raw_markdown += f"\n**Q:** {qa.question}\n**A:** {qa.answer}\n"
        
        return {
            "portfolio_text": portfolio_text,
            "interview_qas": interview_qas,
            "raw_markdown": raw_markdown
        }
    
    @staticmethod
    def _extract_list_from_section(text: str, section_header: str) -> List[str]:
        """Extract list items from a section within text"""
        pattern = f"{section_header}(.*?)(?=\n[A-Za-z ]+:|$)"
        match = re.search(pattern, text, re.DOTALL)
        
        if not match:
            return []
        
        section_content = match.group(1).strip()
        lines = section_content.split('\n')
        items = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('-') or line.startswith('•'):
                items.append(line[1:].strip())
            elif line and len(line) > 3:
                items.append(line)
        
        return items[:5]  # Limit to 5 items
    
    @staticmethod
    def _extract_list_from_text(text: str, section_header: str) -> List[str]:
        """Extract list items from a section in full text"""
        pattern = f"{section_header}(.*?)(?=\n[A-Z][A-Z ]+:|$)"
        match = re.search(pattern, text, re.DOTALL)
        
        if not match:
            return []
        
        section_content = match.group(1).strip()
        lines = section_content.split('\n')
        items = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('-') or line.startswith('•'):
                items.append(line[1:].strip())
            elif line and len(line) > 3 and not line.isupper():
                items.append(line)
        
        return items[:10]  # Limit to 10 items
    
    @staticmethod
    def _extract_text_from_section(text: str, section_header: str) -> str:
        """Extract text content from a section"""
        pattern = f"{section_header}(.*?)(?=\n[A-Z][A-Z ]+:|$)"
        match = re.search(pattern, text, re.DOTALL)
        
        if not match:
            return "Content not available."
        
        return match.group(1).strip()