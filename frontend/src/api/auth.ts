import { apiClient } from './client'

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  name: string
  role: 'LEADER' | 'MEMBER' | 'BOTH'
  bio?: string
  region?: string
  available_hours_per_week?: number
  domain_knowledge?: string
  experience_level?: 'BEGINNER' | 'JUNIOR' | 'MID' | 'SENIOR'
  project_experience?: string
  certifications?: string[]
  tech_stack?: string[]
  preferred_positions?: string[]
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: {
    id: string
    email: string
    name: string
    role: 'LEADER' | 'MEMBER' | 'BOTH'
    bio?: string
    region?: string
    experience_level: 'BEGINNER' | 'JUNIOR' | 'MID' | 'SENIOR'
    tech_stack?: string[]
    preferred_positions?: string[]
    is_active: boolean
    no_show_count: number
    penalty_until?: string
    created_at: string
    updated_at: string
  }
}

export const authApi = {
  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const response = await apiClient.post('/auth/login', data)
    return response.data
  },

  register: async (data: RegisterRequest): Promise<AuthResponse> => {
    const response = await apiClient.post('/auth/register', data)
    return response.data
  },

  refresh: async (refreshToken: string): Promise<{ access_token: string }> => {
    const response = await apiClient.post('/auth/refresh', {
      refresh_token: refreshToken
    })
    return response.data
  }
}