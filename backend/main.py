"""
AI Studio - FastAPI Backend
Main application entry point
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from database.db import init_db, close_db
from utils.config import settings
from utils.portable_paths import ensure_data_directories
from api.routes import chat, models, embeddings, lora, system_prompts


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Application lifespan manager - handles startup and shutdown
    """
    # Startup
    logger.info("Starting AI Studio Backend...")
    
    # Ensure data directories exist
    ensure_data_directories()
    logger.info("Data directories verified")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    # TODO: Initialize model manager
    # TODO: Initialize ChromaDB
    # TODO: Load default settings
    
    logger.info("AI Studio Backend started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Studio Backend...")
    
    # Close database connections
    await close_db()
    logger.info("Database connections closed")
    
    # TODO: Unload models
    # TODO: Close ChromaDB connections
    
    logger.info("AI Studio Backend shutdown complete")


# Initialize FastAPI app
app = FastAPI(
    title="AI Studio API",
    description="Backend API for AI Studio - Local AI Chat Application",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS for Electron frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative dev port
        "app://*",  # Electron app protocol
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "version": "0.1.0",
        "database": "connected",
    }


@app.get("/")
async def root():
    """
    Root endpoint - API information
    """
    return {
        "name": "AI Studio API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
    }


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An unexpected error occurred",
        },
    )


# Include API routes
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(models.router, prefix="/api/models", tags=["models"])
app.include_router(embeddings.router, prefix="/api/embeddings", tags=["embeddings"])
app.include_router(lora.router, prefix="/api/lora", tags=["lora"])
app.include_router(system_prompts.router, prefix="/api/system-prompts", tags=["system-prompts"])


if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
