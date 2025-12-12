# ProjectMate AI Backend

A FastAPI-based backend for the ProjectMate AI platform, providing project team matching and AI-powered project assistance.

## Features

- **User Authentication**: JWT-based authentication with role management
- **Project Management**: Create, search, and manage projects with team formation
- **Team Communication**: Chat rooms and AI-powered meeting summarization
- **AI Services**: Project feasibility analysis, timeline generation, learning roadmaps, and portfolio creation
- **Usage Limits**: Configurable limits for AI feature usage

## Tech Stack

- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **AI Integration**: OpenAI GPT-4 and AWS Bedrock support
- **Migrations**: Alembic for database schema management

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- OpenAI API key or AWS credentials (for AI features)

### Installation

1. **Clone and setup environment**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Setup database**:
```bash
# Create PostgreSQL database
createdb projectmate_ai

# Run migrations
alembic upgrade head
```

4. **Start development server**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Environment Configuration

### Required Variables

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/projectmate_ai

# JWT Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# AI Provider (choose one)
AI_PROVIDER=openai  # or bedrock
OPENAI_API_KEY=your-openai-api-key
# OR for AWS Bedrock:
# AWS_ACCESS_KEY_ID=your-aws-access-key
# AWS_SECRET_ACCESS_KEY=your-aws-secret-key
# AWS_REGION=us-east-1
```

### Optional Variables

```env
# CORS Origins
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]

# Penalty System
MAX_NO_SHOW_COUNT=3
PENALTY_DURATION_DAYS=30

# AI Usage Limits
PORTFOLIO_GENERATION_LIMIT=3

# Redis (for caching)
REDIS_URL=redis://localhost:6379/0

# S3 (for file uploads)
S3_BUCKET_NAME=projectmate-ai-uploads
S3_REGION=us-east-1
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database Migrations

### Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations:
```bash
alembic upgrade head
```

### Rollback migrations:
```bash
alembic downgrade -1  # Rollback one migration
alembic downgrade base  # Rollback all migrations
```

## Project Structure

```
backend/
├── app/
│   ├── ai/                 # AI integration modules
│   │   ├── client.py       # AI client abstraction
│   │   └── prompts.py      # AI prompt templates
│   ├── core/               # Core configuration
│   │   ├── config.py       # Settings management
│   │   ├── database.py     # Database connection
│   │   ├── deps.py         # FastAPI dependencies
│   │   └── security.py     # Authentication utilities
│   ├── models/             # SQLAlchemy models
│   │   ├── user.py         # User and authentication
│   │   ├── project.py      # Project management
│   │   ├── application.py  # Applications and team members
│   │   ├── chat.py         # Communication models
│   │   └── ai_usage.py     # AI usage tracking
│   ├── routers/            # API route handlers
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── users.py        # User management
│   │   ├── projects.py     # Project CRUD
│   │   ├── chat.py         # Communication
│   │   └── ai_services.py  # AI-powered features
│   ├── schemas/            # Pydantic schemas
│   │   ├── user.py         # User request/response models
│   │   ├── project.py      # Project schemas
│   │   ├── application.py  # Application schemas
│   │   ├── chat.py         # Communication schemas
│   │   └── ai_services.py  # AI service schemas
│   ├── services/           # Business logic
│   │   ├── ai_project.py   # AI project services
│   │   └── ai_learning.py  # AI learning services
│   └── main.py             # FastAPI application
├── alembic/                # Database migrations
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
└── README.md              # This file
```

## Key Features

### Authentication & Authorization
- JWT-based authentication with access and refresh tokens
- Role-based access control (LEADER, MEMBER, BOTH)
- Penalty system for no-show behavior
- Secure password hashing with bcrypt

### Project Management
- Project creation and management with detailed metadata
- Advanced search and filtering capabilities
- Team application and approval workflow
- Automatic team composition tracking

### AI-Powered Features
- **Feasibility Analysis**: Evaluate project scope and provide recommendations
- **Timeline Generation**: Create detailed project schedules and work breakdown structures
- **Learning Roadmaps**: Generate personalized learning paths for team members
- **Meeting Summarization**: AI-powered meeting notes and action item extraction
- **Portfolio Generation**: Create professional portfolio content and interview guides
- **Project Monitoring**: Health analysis and issue detection

### Communication
- Project-based chat rooms with message history
- Meeting note management with AI summarization
- Team collaboration tools

## Testing

Run tests with pytest:
```bash
pytest
```

## Deployment

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

4. **Monitoring**:
   - Set up application logging
   - Monitor API performance
   - Track AI feature usage

## Contributing

1. Follow PEP 8 style guidelines
2. Add type hints to all functions
3. Write docstrings for public methods
4. Include tests for new features
5. Update API documentation

## License

This project is licensed under the MIT License.