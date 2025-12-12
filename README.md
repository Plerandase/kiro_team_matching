# ProjectMate AI

A comprehensive SaaS platform that combines project team matching with AI-powered project assistance and automated portfolio generation. Built with FastAPI backend and React frontend.

## 🚀 Features

### Core Platform
- **User Authentication**: JWT-based authentication with role management (Leader/Member/Both)
- **Project Management**: Create, search, and manage projects with detailed metadata
- **Team Formation**: Application and approval workflow for team building
- **Communication**: Project-based chat rooms with message history

### AI-Powered Features
- **Project Feasibility Analysis**: Evaluate project scope and provide recommendations
- **Timeline Generation**: Create detailed project schedules and work breakdown structures
- **Learning Roadmaps**: Generate personalized learning paths for team members
- **Meeting Summarization**: AI-powered meeting notes and action item extraction
- **Portfolio Generation**: Create professional portfolio content and interview guides (usage limited)
- **Project Monitoring**: Health analysis and issue detection

### Additional Features
- **Penalty System**: No-show behavior tracking and participation restrictions
- **Usage Limits**: Configurable limits for AI feature usage
- **Verification System**: Email template similarity analysis for fraud detection

## 🏗️ Architecture

```
ProjectMate AI/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── ai/             # AI integration modules
│   │   ├── core/           # Core configuration
│   │   ├── models/         # SQLAlchemy models
│   │   ├── routers/        # API endpoints
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── alembic/            # Database migrations
│   └── requirements.txt
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── api/           # API client
│   │   ├── components/    # React components
│   │   ├── contexts/      # React contexts
│   │   └── pages/         # Page components
│   └── package.json
└── .kiro/specs/           # Project specifications
```

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **AI Integration**: OpenAI GPT-4 and AWS Bedrock support
- **Migrations**: Alembic for database schema management

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios with interceptors
- **State Management**: React Query + Context API
- **Routing**: React Router v6

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 12+
- OpenAI API key or AWS credentials (for AI features)

### Backend Setup

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Setup database**:
```bash
# Create PostgreSQL database
createdb projectmate_ai

# Run migrations
alembic upgrade head
```

6. **Start backend server**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Start development server**:
```bash
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## ⚙️ Configuration

### Backend Environment Variables

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/projectmate_ai

# JWT Security
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# AI Provider (choose one)
AI_PROVIDER=openai  # or bedrock
OPENAI_API_KEY=your-openai-api-key
# OR for AWS Bedrock:
# AWS_ACCESS_KEY_ID=your-aws-access-key
# AWS_SECRET_ACCESS_KEY=your-aws-secret-key
# AWS_REGION=us-east-1

# Application Settings
CORS_ORIGINS=["http://localhost:3000"]
MAX_NO_SHOW_COUNT=3
PENALTY_DURATION_DAYS=30
PORTFOLIO_GENERATION_LIMIT=3
```

### Frontend Environment Variables

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key API Endpoints

#### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/refresh` - Token refresh

#### Projects
- `GET /projects` - List projects with filtering
- `POST /projects` - Create project (leaders only)
- `GET /projects/{id}` - Get project details
- `POST /projects/{id}/apply` - Apply to project

#### AI Services
- `POST /ai/projects/feasibility` - Project feasibility analysis
- `POST /ai/projects/{id}/timeline` - Timeline generation
- `POST /ai/learning-path` - Learning roadmap generation
- `POST /ai/projects/{id}/portfolio` - Portfolio generation

#### Communication
- `GET /chat/projects/{id}/chatrooms` - Get chat rooms
- `POST /chat/chatrooms/{id}/messages` - Send message
- `POST /chat/projects/{id}/meeting-notes/ai-summarize` - AI meeting summary

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Production Considerations

1. **Security**:
   - Change default SECRET_KEY
   - Use strong database passwords
   - Enable HTTPS in production
   - Configure proper CORS origins

2. **Database**:
   - Use connection pooling
   - Set up database backups
   - Monitor database performance

3. **AI Services**:
   - Monitor API usage and costs
   - Implement proper error handling
   - Set up usage alerts

4. **Frontend**:
   - Build for production: `npm run build`
   - Serve static files with CDN
   - Configure environment variables

## 🔧 Development

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Code Style

- Backend: Follow PEP 8, use type hints
- Frontend: Use TypeScript, follow React best practices
- Both: Write comprehensive docstrings/comments

## 📋 Project Status

This is an MVP implementation focusing on core functionality:

### ✅ Completed Features
- User authentication and profile management
- Project CRUD operations with search/filtering
- Team application and approval workflow
- Chat system with message history
- AI feasibility analysis
- AI meeting summarization
- AI portfolio generation with usage limits
- Basic project structure and configuration

### 🚧 Planned Features
- Timeline and WBS generation service
- Learning roadmap generation system
- Project monitoring and health analysis
- Email template verification system
- Real-time chat with WebSocket
- Advanced search and recommendations
- Mobile responsive design improvements

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the API documentation at `/docs`
- Review the project specifications in `.kiro/specs/`
- Open an issue for bugs or feature requests

## 🙏 Acknowledgments

- Built with FastAPI and React
- AI powered by OpenAI GPT-4
- UI components styled with Tailwind CSS
- Database management with SQLAlchemy and Alembic