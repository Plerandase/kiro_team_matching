import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Zap, Users, Brain, Target, ArrowRight } from 'lucide-react'

export const LandingPage: React.FC = () => {
  const { user } = useAuth()

  return (
    <div className="max-w-7xl mx-auto">
      {/* Hero Section */}
      <div className="text-center py-20">
        <h1 className="text-5xl font-bold text-gray-900 mb-6">
          Build Amazing Projects with
          <span className="text-primary-600"> AI-Powered</span> Teams
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          ProjectMate AI connects developers, designers, and project managers while providing 
          intelligent assistance for project planning, team collaboration, and portfolio generation.
        </p>
        <div className="flex items-center justify-center space-x-4">
          {user ? (
            <Link to="/dashboard" className="btn btn-primary text-lg px-8 py-3">
              Go to Dashboard
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          ) : (
            <>
              <Link to="/register" className="btn btn-primary text-lg px-8 py-3">
                Get Started Free
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link to="/projects" className="btn btn-outline text-lg px-8 py-3">
                Browse Projects
              </Link>
            </>
          )}
        </div>
      </div>

      {/* Features Section */}
      <div className="py-20 bg-white rounded-2xl shadow-sm">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Everything You Need for Successful Projects
          </h2>
          <p className="text-lg text-gray-600">
            From team formation to project completion, we've got you covered
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div className="text-center">
            <div className="bg-primary-100 rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <Users className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Team Matching</h3>
            <p className="text-gray-600">
              Find the perfect team members based on skills, experience, and project requirements
            </p>
          </div>

          <div className="text-center">
            <div className="bg-primary-100 rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <Brain className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">AI Assistant</h3>
            <p className="text-gray-600">
              Get intelligent project analysis, timeline generation, and personalized learning roadmaps
            </p>
          </div>

          <div className="text-center">
            <div className="bg-primary-100 rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <Target className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Project Planning</h3>
            <p className="text-gray-600">
              Automated feasibility analysis and work breakdown structures for better project outcomes
            </p>
          </div>

          <div className="text-center">
            <div className="bg-primary-100 rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <Zap className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Portfolio Builder</h3>
            <p className="text-gray-600">
              Automatically generate professional portfolios and interview preparation materials
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="text-center py-20">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Ready to Build Something Amazing?
        </h2>
        <p className="text-lg text-gray-600 mb-8">
          Join thousands of developers already using ProjectMate AI
        </p>
        {!user && (
          <Link to="/register" className="btn btn-primary text-lg px-8 py-3">
            Start Your First Project
            <ArrowRight className="ml-2 h-5 w-5" />
          </Link>
        )}
      </div>
    </div>
  )
}