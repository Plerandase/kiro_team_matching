"""
AI prompt templates for various features
"""
from typing import Dict, List, Any


class PromptTemplates:
    """Collection of prompt templates for AI services"""
    
    @staticmethod
    def feasibility_analysis_prompt(
        title: str,
        summary: str,
        description: str,
        goal: str,
        team_size: int,
        duration_weeks: int,
        tech_stack: List[str],
        target_type: str
    ) -> str:
        """Generate prompt for project feasibility analysis"""
        return f"""
Analyze the feasibility of this project and provide a detailed assessment:

Project Title: {title}
Summary: {summary}
Description: {description}
Goal: {goal}
Team Size: {team_size} people
Duration: {duration_weeks} weeks
Technology Stack: {', '.join(tech_stack)}
Target Type: {target_type}

Please provide your analysis in the following format:

FEASIBILITY SCORE: [0-100 score where 0=impossible, 40=high risk, 70=feasible, 100=very achievable]

DIFFICULTY LEVEL: [EASY/MEDIUM/HARD based on technical complexity and team requirements]

RISK FACTORS:
- [List specific risks that could impact project success]

MISSING ROLES:
- [List any critical roles/skills missing from the team composition]

OVER-SCOPED FEATURES:
- [List features that seem too ambitious for the given constraints]

RECOMMENDATIONS:
[Provide specific actionable recommendations to improve feasibility]

PROJECT PROPOSAL OUTLINE:
[Generate a brief project proposal structure that addresses the identified issues]

Consider the target type when evaluating:
- PERSONAL_PORTFOLIO: Focus on learning and demonstration value
- CONTEST: Consider competition deadlines and judging criteria
- BUSINESS_MVP: Evaluate market viability and technical feasibility
"""
    
    @staticmethod
    def timeline_generation_prompt(
        features: List[str],
        team_size: int,
        team_members: List[Dict[str, str]],
        hours_per_week: int,
        duration_weeks: int
    ) -> str:
        """Generate prompt for project timeline creation"""
        team_info = ""
        if team_members:
            team_info = "\nTeam Composition:\n"
            for member in team_members:
                team_info += f"- {member.get('role', 'Unknown')}: {member.get('experience_level', 'Unknown')} level\n"
        
        return f"""
Create a detailed project timeline and work breakdown structure for this project:

Features to Implement:
{chr(10).join(f'- {feature}' for feature in features)}

Team Size: {team_size} people
Available Hours per Week: {hours_per_week} hours total
Project Duration: {duration_weeks} weeks
{team_info}

Please provide your response in the following format:

WEEKLY TIMELINE:
Week 1:
- Summary: [Brief description of week's focus]
- Tasks: [List of specific tasks]

Week 2:
- Summary: [Brief description of week's focus]
- Tasks: [List of specific tasks]

[Continue for all weeks...]

WORK BREAKDOWN STRUCTURE:
1. [Main Component]
   1.1 [Sub-task] - [Estimated hours]
   1.2 [Sub-task] - [Estimated hours]
2. [Main Component]
   2.1 [Sub-task] - [Estimated hours]

IDENTIFIED RISKS:
- [List potential scheduling and technical risks]

BOTTLENECKS:
- [List likely bottlenecks and dependencies]

ARCHITECTURE SUGGESTIONS:
[Provide high-level technical architecture recommendations]

Adjust the timeline complexity based on team experience levels:
- BEGINNER teams: More time for learning and simpler tasks
- MID/SENIOR teams: More aggressive timelines and complex features
"""
    
    @staticmethod
    def learning_roadmap_prompt(
        target_technologies: List[str],
        current_experience: str,
        days_per_week: int,
        weeks_available: int,
        project_context: str
    ) -> str:
        """Generate prompt for personalized learning roadmap"""
        return f"""
Create a personalized learning roadmap for a team member who needs to learn new technologies:

Target Technologies: {', '.join(target_technologies)}
Current Experience Level: {current_experience}
Available Study Time: {days_per_week} days per week
Time Until Critical Phase: {weeks_available} weeks
Project Context: {project_context}

Please provide your response in the following format:

LEARNING ROADMAP:
Week 1 (Days 1-{days_per_week}):
- Focus Topic: [Main learning objective]
- Resources: [List of recommended tutorials, docs, courses]
- Practice Tasks: [Hands-on exercises to reinforce learning]

Week 2 (Days {days_per_week + 1}-{days_per_week * 2}):
- Focus Topic: [Main learning objective]
- Resources: [List of recommended tutorials, docs, courses]
- Practice Tasks: [Hands-on exercises to reinforce learning]

[Continue for all weeks...]

CHECKPOINT QUIZ IDEAS:
- [Questions team leader can ask to assess progress]
- [Practical challenges to test understanding]

LEADER SUMMARY:
[Brief summary for team leader about what to expect and how to support learning]

Tailor the roadmap based on experience level:
- BEGINNER: Start with fundamentals, more guided resources
- JUNIOR: Focus on practical application and best practices
- MID: Advanced concepts and optimization techniques
- SENIOR: Architecture patterns and team leadership aspects
"""
    
    @staticmethod
    def meeting_summary_prompt(
        raw_text: str,
        include_actions: bool = True,
        include_next_agenda: bool = False
    ) -> str:
        """Generate prompt for meeting summarization"""
        action_instruction = "\nACTION ITEMS:\n- [List specific tasks with responsible parties]" if include_actions else ""
        agenda_instruction = "\nNEXT MEETING AGENDA:\n- [Suggest agenda items based on current progress and issues]" if include_next_agenda else ""
        
        return f"""
Analyze this meeting transcript and create a structured summary:

MEETING TRANSCRIPT:
{raw_text}

Please provide your response in the following format:

MEETING SUMMARY:
[Concise overview of what was discussed and decided]

KEY DECISIONS:
- [List important decisions made during the meeting]

DISCUSSION POINTS:
- [Main topics that were discussed]
{action_instruction}{agenda_instruction}

Focus on extracting actionable information and clear outcomes from the discussion.
"""
    
    @staticmethod
    def project_monitoring_prompt(
        commit_activity: Dict[str, Any],
        meeting_summaries: List[str],
        task_progress: List[Dict[str, str]]
    ) -> str:
        """Generate prompt for project health monitoring"""
        commit_info = f"Commit Activity: {commit_activity}" if commit_activity else "No commit data available"
        meeting_info = f"Recent Meeting Summaries:\n" + "\n".join(f"- {summary}" for summary in meeting_summaries) if meeting_summaries else "No meeting summaries available"
        task_info = f"Task Progress:\n" + "\n".join(f"- {task['task']}: {task['status']}" for task in task_progress) if task_progress else "No task progress data available"
        
        return f"""
Analyze the current health and progress of this project:

{commit_info}

{meeting_info}

{task_info}

Please provide your analysis in the following format:

HEALTH SCORE: [0-100 where 0=critical issues, 50=concerning, 80=healthy, 100=excellent]

RISK LEVEL: [LOW/MEDIUM/HIGH based on identified issues]

ISSUES DETECTED:
- [List specific problems or warning signs]

RECOMMENDATIONS:
- [Actionable suggestions to improve project health]

Consider these factors in your analysis:
- Code contribution patterns and frequency
- Team communication and meeting outcomes
- Task completion rates and blockers
- Overall project momentum and engagement
"""
    
    @staticmethod
    def portfolio_generation_prompt(
        role: str,
        tech_stack: List[str],
        contributions: str,
        project_context: str
    ) -> str:
        """Generate prompt for portfolio content creation"""
        return f"""
Create professional portfolio content for a team member based on their project contributions:

Role in Project: {role}
Technologies Used: {', '.join(tech_stack)}
Personal Contributions: {contributions}
Project Context: {project_context}

Please provide your response in the following format:

PORTFOLIO PROJECT DESCRIPTION (STAR Format):
Situation: [Context and project background]
Task: [Specific responsibilities and challenges]
Action: [What you did and how you approached problems]
Result: [Outcomes and impact of your work]

TECHNICAL HIGHLIGHTS:
1. [Key technical achievement with specific details]
2. [Another significant contribution or skill demonstration]
3. [Problem-solving example or innovation]
4. [Additional technical accomplishment]
5. [Learning or growth demonstration]

CHALLENGES AND SOLUTIONS:
[Describe a significant challenge faced and how it was overcome]

INTERVIEW QUESTIONS AND ANSWERS:
Q: [Relevant technical question about the project]
A: [Detailed answer demonstrating knowledge and experience]

Q: [Behavioral question about teamwork or problem-solving]
A: [STAR format answer based on project experience]

Q: [Question about specific technology or approach used]
A: [Technical explanation with project examples]

[Continue with 3-5 more relevant Q&A pairs]

Focus on creating content that demonstrates both technical skills and professional growth.
"""