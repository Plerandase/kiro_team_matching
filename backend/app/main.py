"""
ProjectMate AI FastAPI Application
Main application entry point with routing and middleware configuration
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import create_tables
from .routers import auth, users, projects, chat, ai_services

# Create FastAPI application
app = FastAPI(
    title="ProjectMate AI",
    description="Project team matching and AI-powered project assistance platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(chat.router, prefix="/chat", tags=["communication"])
app.include_router(ai_services.router, prefix="/ai", tags=["ai-services"])


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    create_tables()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ProjectMate AI API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )