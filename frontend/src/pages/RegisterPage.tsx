import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { useAuth } from '../contexts/AuthContext'
import { Eye, EyeOff, AlertCircle } from 'lucide-react'

interface RegisterFormData {
  email: string
  password: string
  confirmPassword: string
  name: string
  role: 'LEADER' | 'MEMBER' | 'BOTH'
  bio?: string
  region?: string
  available_hours_per_week?: number
  domain_knowledge?: string
  experience_level: 'BEGINNER' | 'JUNIOR' | 'MID' | 'SENIOR'
  project_experience?: string
  tech_stack?: string
  preferred_positions?: string
}

export const RegisterPage: React.FC = () => {
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  const { register: registerUser } = useAuth()
  const navigate = useNavigate()

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors }
  } = useForm<RegisterFormData>()

  const password = watch('password')

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true)
    setError(null)

    try {
      const registerData = {
        ...data,
        tech_stack: data.tech_stack ? data.tech_stack.split(',').map(s => s.trim()) : [],
        preferred_positions: data.preferred_positions ? data.preferred_positions.split(',').map(s => s.trim()) : []
      }
      
      // Remove confirmPassword from the data
      const { confirmPassword, ...submitData } = registerData
      
      await registerUser(submitData)
      navigate('/dashboard')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="card">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Create Your Account</h1>
          <p className="text-gray-600">Join ProjectMate AI and start building amazing projects</p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
            <div className="flex">
              <AlertCircle className="h-5 w-5 text-red-400" />
              <div className="ml-3">
                <p className="text-sm text-red-800">{error}</p>
              </div>
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Basic Information */}
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                Full Name *
              </label>
              <input
                {...register('name', { required: 'Name is required' })}
                type="text"
                className="input"
                placeholder="Enter your full name"
              />
              {errors.name && (
                <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
              )}
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                Email Address *
              </label>
              <input
                {...register('email', {
                  required: 'Email is required',
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: 'Invalid email address'
                  }
                })}
                type="email"
                className="input"
                placeholder="Enter your email"
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
              )}
            </div>
          </div>

          {/* Password */}
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                Password *
              </label>
              <div className="relative">
                <input
                  {...register('password', {
                    required: 'Password is required',
                    minLength: {
                      value: 8,
                      message: 'Password must be at least 8 characters'
                    }
                  })}
                  type={showPassword ? 'text' : 'password'}
                  className="input pr-10"
                  placeholder="Create a password"
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <EyeOff className="h-5 w-5 text-gray-400" />
                  ) : (
                    <Eye className="h-5 w-5 text-gray-400" />
                  )}
                </button>
              </div>
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
              )}
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-2">
                Confirm Password *
              </label>
              <div className="relative">
                <input
                  {...register('confirmPassword', {
                    required: 'Please confirm your password',
                    validate: value => value === password || 'Passwords do not match'
                  })}
                  type={showConfirmPassword ? 'text' : 'password'}
                  className="input pr-10"
                  placeholder="Confirm your password"
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                >
                  {showConfirmPassword ? (
                    <EyeOff className="h-5 w-5 text-gray-400" />
                  ) : (
                    <Eye className="h-5 w-5 text-gray-400" />
                  )}
                </button>
              </div>
              {errors.confirmPassword && (
                <p className="mt-1 text-sm text-red-600">{errors.confirmPassword.message}</p>
              )}
            </div>
          </div>

          {/* Role and Experience */}
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="role" className="block text-sm font-medium text-gray-700 mb-2">
                Role *
              </label>
              <select
                {...register('role', { required: 'Role is required' })}
                className="input"
              >
                <option value="">Select your role</option>
                <option value="LEADER">Project Leader</option>
                <option value="MEMBER">Team Member</option>
                <option value="BOTH">Both Leader & Member</option>
              </select>
              {errors.role && (
                <p className="mt-1 text-sm text-red-600">{errors.role.message}</p>
              )}
            </div>

            <div>
              <label htmlFor="experience_level" className="block text-sm font-medium text-gray-700 mb-2">
                Experience Level *
              </label>
              <select
                {...register('experience_level', { required: 'Experience level is required' })}
                className="input"
              >
                <option value="">Select experience level</option>
                <option value="BEGINNER">Beginner</option>
                <option value="JUNIOR">Junior</option>
                <option value="MID">Mid-level</option>
                <option value="SENIOR">Senior</option>
              </select>
              {errors.experience_level && (
                <p className="mt-1 text-sm text-red-600">{errors.experience_level.message}</p>
              )}
            </div>
          </div>

          {/* Optional Profile Information */}
          <div>
            <label htmlFor="bio" className="block text-sm font-medium text-gray-700 mb-2">
              Bio
            </label>
            <textarea
              {...register('bio')}
              rows={3}
              className="input"
              placeholder="Tell us about yourself..."
            />
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="region" className="block text-sm font-medium text-gray-700 mb-2">
                Region
              </label>
              <input
                {...register('region')}
                type="text"
                className="input"
                placeholder="e.g., San Francisco, CA"
              />
            </div>

            <div>
              <label htmlFor="available_hours_per_week" className="block text-sm font-medium text-gray-700 mb-2">
                Available Hours per Week
              </label>
              <input
                {...register('available_hours_per_week', {
                  valueAsNumber: true,
                  min: { value: 1, message: 'Must be at least 1 hour' },
                  max: { value: 168, message: 'Cannot exceed 168 hours per week' }
                })}
                type="number"
                className="input"
                placeholder="e.g., 20"
              />
              {errors.available_hours_per_week && (
                <p className="mt-1 text-sm text-red-600">{errors.available_hours_per_week.message}</p>
              )}
            </div>
          </div>

          <div>
            <label htmlFor="tech_stack" className="block text-sm font-medium text-gray-700 mb-2">
              Technical Skills
            </label>
            <input
              {...register('tech_stack')}
              type="text"
              className="input"
              placeholder="e.g., React, Node.js, Python, AWS (comma-separated)"
            />
            <p className="mt-1 text-sm text-gray-500">Separate multiple skills with commas</p>
          </div>

          <div>
            <label htmlFor="preferred_positions" className="block text-sm font-medium text-gray-700 mb-2">
              Preferred Positions
            </label>
            <input
              {...register('preferred_positions')}
              type="text"
              className="input"
              placeholder="e.g., Frontend Developer, Backend Developer, UI/UX Designer (comma-separated)"
            />
            <p className="mt-1 text-sm text-gray-500">Separate multiple positions with commas</p>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full btn btn-primary"
          >
            {isLoading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Already have an account?{' '}
            <Link to="/login" className="font-medium text-primary-600 hover:text-primary-500">
              Sign in here
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}