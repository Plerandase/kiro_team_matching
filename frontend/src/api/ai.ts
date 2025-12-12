import { apiClient } from './client'

export interface FeasibilityAnalysisRequest {
  title: string
  summary: string
  description: string
  goal: string
  team_size: number
  expected_duration_weeks: number
  stack: string[]
  target_type: 'PERSONAL_PORTFOLIO' | 'CONTEST' | 'BUSINESS_MVP'
}

export interface FeasibilityAnalysisResponse {
  feasibility_score: number
  difficulty_level_ai: 'EASY' | 'MEDIUM' | 'HARD'
  risk_factors: string[]
  missing_roles: string[]
  over_scoped_features: string[]
  recommendations: string
  auto_project_proposal: string
}

export interface TimelineGenerationRequest {
  features: string[]
  team_size: number
  members?: Array<{ role: string; experience_level: string }>
  hours_per_week: number
  duration_weeks: number
}

export interface TimelineTask {
  week: number
  summary: string
  tasks: string[]
}

export interface WBSItem {
  id: string
  name: string
  parent_id?: string
  estimate_hours: number
}

export interface TimelineGenerationResponse {
  timeline: TimelineTask[]
  wbs: WBSItem[]
  risks: string[]
  bottlenecks: string[]
  architecture_suggestion: string
}

export interface LearningRoadmapRequest {
  user_id: string
  project_id: string
  target_stack: string[]
  days_available_per_week: number
  weeks_until_project_critical_phase: number
}

export interface LearningPhase {
  day_range: string
  focus_topic: string
  resources: string[]
  practice_tasks: string[]
}

export interface LearningRoadmapResponse {
  roadmap: LearningPhase[]
  checkpoint_quiz_ideas: string[]
  summary_for_leader: string
}

export interface ProjectMonitoringRequest {
  commit_activity?: Record<string, any>
  meeting_summaries?: string[]
  task_progress?: Array<{ task: string; status: string }>
}

export interface ProjectMonitoringResponse {
  health_score: number
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH'
  issues_detected: string[]
  recommendations: string[]
}

export interface PortfolioGenerationRequest {
  user_id: string
  role_in_project: string
  tech_stack_used: string[]
  contributions: string
  repo_links: string[]
}

export interface InterviewQA {
  question: string
  answer: string
}

export interface PortfolioGenerationResponse {
  portfolio_text: string
  interview_qas: InterviewQA[]
  raw_markdown: string
}

export const aiApi = {
  // Project feasibility analysis
  analyzeFeasibility: async (data: FeasibilityAnalysisRequest): Promise<FeasibilityAnalysisResponse> => {
    const response = await apiClient.post('/ai/projects/feasibility', data)
    return response.data
  },

  // Timeline generation
  generateTimeline: async (projectId: string, data: TimelineGenerationRequest): Promise<TimelineGenerationResponse> => {
    const response = await apiClient.post(`/ai/projects/${projectId}/timeline`, data)
    return response.data
  },

  // Learning roadmap
  generateLearningRoadmap: async (data: LearningRoadmapRequest): Promise<LearningRoadmapResponse> => {
    const response = await apiClient.post('/ai/learning-path', data)
    return response.data
  },

  // Project monitoring
  monitorProject: async (projectId: string, data: ProjectMonitoringRequest): Promise<ProjectMonitoringResponse> => {
    const response = await apiClient.post(`/ai/projects/${projectId}/monitor`, data)
    return response.data
  },

  // Portfolio generation
  generatePortfolio: async (projectId: string, data: PortfolioGenerationRequest): Promise<PortfolioGenerationResponse> => {
    const response = await apiClient.post(`/ai/projects/${projectId}/portfolio`, data)
    return response.data
  }
}