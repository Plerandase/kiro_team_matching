import { apiClient } from './client'

export interface Project {
  id: string
  leader_id: string
  title: string
  summary: string
  description: string
  category: 'CONTEST' | 'BUSINESS' | 'STUDY' | 'ETC'
  goal: string
  expected_duration_weeks: number
  start_date?: string
  remote_type: 'ONLINE' | 'OFFLINE' | 'HYBRID'
  recruitment_status: 'OPEN' | 'CLOSED' | 'IN_PROGRESS' | 'FINISHED'
  tech_stack_required?: string[]
  positions_needed?: Record<string, number>
  difficulty_level_manual?: 'EASY' | 'MEDIUM' | 'HARD'
  difficulty_level_ai?: 'EASY' | 'MEDIUM' | 'HARD'
  feasibility_score?: number
  risk_notes?: string
  created_at: string
  updated_at: string
}

export interface ProjectCreateRequest {
  title: string
  summary: string
  description: string
  category: 'CONTEST' | 'BUSINESS' | 'STUDY' | 'ETC'
  goal: string
  expected_duration_weeks: number
  start_date?: string
  remote_type: 'ONLINE' | 'OFFLINE' | 'HYBRID'
  tech_stack_required?: string[]
  positions_needed?: Record<string, number>
  difficulty_level_manual?: 'EASY' | 'MEDIUM' | 'HARD'
}

export interface ProjectListResponse {
  projects: Project[]
  total: number
  page: number
  size: number
}

export interface ProjectSearchParams {
  category?: 'CONTEST' | 'BUSINESS' | 'STUDY' | 'ETC'
  remote_type?: 'ONLINE' | 'OFFLINE' | 'HYBRID'
  difficulty_level?: 'EASY' | 'MEDIUM' | 'HARD'
  tech_stack?: string
  page?: number
  size?: number
}

export interface ProjectApplication {
  id: string
  project_id: string
  user_id: string
  applied_position: string
  motivation: string
  portfolio_link?: string
  status: 'PENDING' | 'ACCEPTED' | 'REJECTED'
  fit_score_ai?: number
  created_at: string
  updated_at: string
}

export interface ApplicationRequest {
  applied_position: string
  motivation: string
  portfolio_link?: string
}

export interface TeamMember {
  id: string
  project_id: string
  user_id: string
  role_in_project: string
  is_leader: boolean
  performance_score?: number
  joined_at: string
  left_at?: string
}

export const projectsApi = {
  // Project CRUD
  create: async (data: ProjectCreateRequest): Promise<Project> => {
    const response = await apiClient.post('/projects', data)
    return response.data
  },

  list: async (params?: ProjectSearchParams): Promise<ProjectListResponse> => {
    const response = await apiClient.get('/projects', { params })
    return response.data
  },

  getById: async (id: string): Promise<Project> => {
    const response = await apiClient.get(`/projects/${id}`)
    return response.data
  },

  update: async (id: string, data: Partial<ProjectCreateRequest>): Promise<Project> => {
    const response = await apiClient.patch(`/projects/${id}`, data)
    return response.data
  },

  // Applications
  apply: async (projectId: string, data: ApplicationRequest): Promise<ProjectApplication> => {
    const response = await apiClient.post(`/projects/${projectId}/apply`, data)
    return response.data
  },

  getApplications: async (projectId: string): Promise<ProjectApplication[]> => {
    const response = await apiClient.get(`/projects/${projectId}/applications`)
    return response.data
  },

  acceptApplication: async (projectId: string, applicationId: string): Promise<void> => {
    await apiClient.post(`/projects/${projectId}/applications/${applicationId}/accept`)
  },

  rejectApplication: async (projectId: string, applicationId: string): Promise<void> => {
    await apiClient.post(`/projects/${projectId}/applications/${applicationId}/reject`)
  },

  // Team management
  getTeam: async (projectId: string): Promise<TeamMember[]> => {
    const response = await apiClient.get(`/projects/${projectId}/team`)
    return response.data
  }
}