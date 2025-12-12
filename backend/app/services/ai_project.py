"""
AI-powered project analysis services
"""
import re
import json
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from ..ai.client import call_ai
from ..ai.prompts import PromptTemplates
from ..models.project import Project, DifficultyLevel
from ..schemas.ai_services import (
    FeasibilityAnalysisRequest, FeasibilityAnalysisResponse,
    TimelineGenerationRequest, TimelineGenerationResponse, TimelineTask, WBSItem,
    ProjectMonitoringRequest, ProjectMonitoringResponse
)


class AIProjectService:
    """Service for AI-powered project analysis and planning"""
    
    @staticmethod
    async def analyze_feasibility(request: FeasibilityAnalysisRequest) -> FeasibilityAnalysisResponse:
        """
        Analyze project feasibility using AI
        """
        try:
            # Generate AI prompt
            prompt = PromptTemplates.feasibility_analysis_prompt(
                title=request.title,
                summary=request.summary,
                description=request.description,
                goal=request.goal,
                team_size=request.team_size,
                duration_weeks=request.expected_duration_weeks,
                tech_stack=request.stack,
                target_type=request.target_type
            )
            
            # Call AI service
            ai_response = await call_ai(prompt)
            
            # Parse AI response
            parsed_response = AIProjectService._parse_feasibility_response(ai_response)
            
            return FeasibilityAnalysisResponse(**parsed_response)
            
        except Exception as e:
            # Fallback response if AI fails
            return FeasibilityAnalysisResponse(
                feasibility_score=50.0,
                difficulty_level_ai=DifficultyLevel.MEDIUM,
                risk_factors=["AI analysis unavailable", "Manual review required"],
                missing_roles=["Technical reviewer"],
                over_scoped_features=["Unable to analyze scope"],
                recommendations="Please review project manually due to AI service unavailability.",
                auto_project_proposal="Manual project planning recommended."
            )
    
    @staticmethod
    def _parse_feasibility_response(ai_response: str) -> Dict[str, Any]:
        """Parse AI response for feasibility analysis"""
        # Extract feasibility score
        score_match = re.search(r'FEASIBILITY SCORE:\s*(\d+)', ai_response)
        feasibility_score = float(score_match.group(1)) if score_match else 50.0
        
        # Extract difficulty level
        difficulty_match = re.search(r'DIFFICULTY LEVEL:\s*(EASY|MEDIUM|HARD)', ai_response)
        difficulty_level = difficulty_match.group(1) if difficulty_match else "MEDIUM"
        
        # Extract sections
        risk_factors = AIProjectService._extract_list_section(ai_response, "RISK FACTORS:")
        missing_roles = AIProjectService._extract_list_section(ai_response, "MISSING ROLES:")
        over_scoped_features = AIProjectService._extract_list_section(ai_response, "OVER-SCOPED FEATURES:")
        
        # Extract recommendations and proposal
        recommendations = AIProjectService._extract_text_section(ai_response, "RECOMMENDATIONS:")
        auto_project_proposal = AIProjectService._extract_text_section(ai_response, "PROJECT PROPOSAL OUTLINE:")
        
        return {
            "feasibility_score": feasibility_score,
            "difficulty_level_ai": DifficultyLevel(difficulty_level),
            "risk_factors": risk_factors,
            "missing_roles": missing_roles,
            "over_scoped_features": over_scoped_features,
            "recommendations": recommendations,
            "auto_project_proposal": auto_project_proposal
        }
    
    @staticmethod
    async def generate_timeline(request: TimelineGenerationRequest) -> TimelineGenerationResponse:
        """
        Generate project timeline and WBS using AI
        """
        try:
            # Generate AI prompt
            prompt = PromptTemplates.timeline_generation_prompt(
                features=request.features,
                team_size=request.team_size,
                team_members=request.members or [],
                hours_per_week=request.hours_per_week,
                duration_weeks=request.duration_weeks
            )
            
            # Call AI service
            ai_response = await call_ai(prompt)
            
            # Parse AI response
            parsed_response = AIProjectService._parse_timeline_response(ai_response, request.duration_weeks)
            
            return TimelineGenerationResponse(**parsed_response)
            
        except Exception as e:
            # Fallback response if AI fails
            return TimelineGenerationResponse(
                timeline=[
                    TimelineTask(
                        week=1,
                        summary="Project setup and planning",
                        tasks=["Set up development environment", "Define project structure", "Create initial documentation"]
                    ),
                    TimelineTask(
                        week=2,
                        summary="Core development begins",
                        tasks=["Implement basic features", "Set up testing framework", "Create CI/CD pipeline"]
                    )
                ],
                wbs=[
                    WBSItem(id="1", name="Project Setup", parent_id=None, estimate_hours=20),
                    WBSItem(id="1.1", name="Environment Setup", parent_id="1", estimate_hours=8),
                    WBSItem(id="1.2", name="Documentation", parent_id="1", estimate_hours=12)
                ],
                risks=["AI service unavailable", "Manual planning required"],
                bottlenecks=["Resource allocation", "Technical dependencies"],
                architecture_suggestion="Please consult with technical lead for architecture recommendations."
            )
    
    @staticmethod
    def _parse_timeline_response(ai_response: str, duration_weeks: int) -> Dict[str, Any]:
        """Parse AI response for timeline generation"""
        timeline = []
        wbs = []
        
        # Extract weekly timeline
        for week in range(1, duration_weeks + 1):
            week_pattern = f"Week {week}:"
            week_match = re.search(f"{week_pattern}.*?(?=Week {week + 1}:|WORK BREAKDOWN STRUCTURE:|$)", ai_response, re.DOTALL)
            
            if week_match:
                week_content = week_match.group(0)
                summary_match = re.search(r"Summary:\s*(.+)", week_content)
                tasks_section = re.search(r"Tasks:\s*(.*?)(?=\n\n|\n[A-Z]|$)", week_content, re.DOTALL)
                
                summary = summary_match.group(1).strip() if summary_match else f"Week {week} activities"
                tasks = []
                
                if tasks_section:
                    task_lines = tasks_section.group(1).strip().split('\n')
                    tasks = [line.strip('- ').strip() for line in task_lines if line.strip().startswith('-')]
                
                timeline.append(TimelineTask(
                    week=week,
                    summary=summary,
                    tasks=tasks or [f"Continue development work for week {week}"]
                ))
        
        # Extract WBS (simplified parsing)
        wbs_section = AIProjectService._extract_text_section(ai_response, "WORK BREAKDOWN STRUCTURE:")
        wbs_lines = wbs_section.split('\n') if wbs_section else []
        
        for i, line in enumerate(wbs_lines[:10]):  # Limit to 10 items
            if line.strip() and any(char.isdigit() for char in line):
                wbs.append(WBSItem(
                    id=str(i + 1),
                    name=line.strip(),
                    parent_id=None,
                    estimate_hours=8  # Default estimate
                ))
        
        # Extract other sections
        risks = AIProjectService._extract_list_section(ai_response, "IDENTIFIED RISKS:")
        bottlenecks = AIProjectService._extract_list_section(ai_response, "BOTTLENECKS:")
        architecture_suggestion = AIProjectService._extract_text_section(ai_response, "ARCHITECTURE SUGGESTIONS:")
        
        return {
            "timeline": timeline,
            "wbs": wbs,
            "risks": risks,
            "bottlenecks": bottlenecks,
            "architecture_suggestion": architecture_suggestion
        }
    
    @staticmethod
    async def monitor_project_health(request: ProjectMonitoringRequest) -> ProjectMonitoringResponse:
        """
        Monitor project health and detect issues using AI
        """
        try:
            # Generate AI prompt
            prompt = PromptTemplates.project_monitoring_prompt(
                commit_activity=request.commit_activity or {},
                meeting_summaries=request.meeting_summaries or [],
                task_progress=request.task_progress or []
            )
            
            # Call AI service
            ai_response = await call_ai(prompt)
            
            # Parse AI response
            parsed_response = AIProjectService._parse_monitoring_response(ai_response)
            
            return ProjectMonitoringResponse(**parsed_response)
            
        except Exception as e:
            # Fallback response if AI fails
            return ProjectMonitoringResponse(
                health_score=70.0,
                risk_level="MEDIUM",
                issues_detected=["AI monitoring unavailable", "Manual review recommended"],
                recommendations=["Check project status manually", "Ensure team communication is active"]
            )
    
    @staticmethod
    def _parse_monitoring_response(ai_response: str) -> Dict[str, Any]:
        """Parse AI response for project monitoring"""
        # Extract health score
        score_match = re.search(r'HEALTH SCORE:\s*(\d+)', ai_response)
        health_score = float(score_match.group(1)) if score_match else 70.0
        
        # Extract risk level
        risk_match = re.search(r'RISK LEVEL:\s*(LOW|MEDIUM|HIGH)', ai_response)
        risk_level = risk_match.group(1) if risk_match else "MEDIUM"
        
        # Extract issues and recommendations
        issues_detected = AIProjectService._extract_list_section(ai_response, "ISSUES DETECTED:")
        recommendations = AIProjectService._extract_list_section(ai_response, "RECOMMENDATIONS:")
        
        return {
            "health_score": health_score,
            "risk_level": risk_level,
            "issues_detected": issues_detected,
            "recommendations": recommendations
        }
    
    @staticmethod
    def _extract_list_section(text: str, section_header: str) -> List[str]:
        """Extract list items from a section"""
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
            elif line and not line.isupper():
                items.append(line)
        
        return items[:5]  # Limit to 5 items
    
    @staticmethod
    def _extract_text_section(text: str, section_header: str) -> str:
        """Extract text content from a section"""
        pattern = f"{section_header}(.*?)(?=\n[A-Z][A-Z ]+:|$)"
        match = re.search(pattern, text, re.DOTALL)
        
        if not match:
            return "No information available."
        
        return match.group(1).strip()
    
    @staticmethod
    async def store_feasibility_results(project_id: str, results: FeasibilityAnalysisResponse, db: Session):
        """Store feasibility analysis results in project"""
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            project.difficulty_level_ai = results.difficulty_level_ai
            project.feasibility_score = results.feasibility_score
            project.risk_notes = json.dumps({
                "risk_factors": results.risk_factors,
                "missing_roles": results.missing_roles,
                "over_scoped_features": results.over_scoped_features,
                "recommendations": results.recommendations
            })
            db.commit()