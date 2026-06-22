"""
OPAL Unified System - Main FastAPI Application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uvicorn

from app.core.config import settings
from app.core.logging_config import logger
from app.api.v1 import auth, fats, reference, summit
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="FATS Management System for Subaru Telescope",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add timeout middleware
class TimeoutMiddleware(BaseHTTPMiddleware):
    """Middleware to handle request timeouts"""
    async def dispatch(self, request: Request, call_next):
        import asyncio
        start_time = time.time()
        try:
            # Set 90 second timeout for all requests (increased for large queries)
            response = await asyncio.wait_for(call_next(request), timeout=90.0)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            return response
        except asyncio.TimeoutError:
            process_time = time.time() - start_time
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Request timeout: {request.url.path} took >90s")
            return JSONResponse(
                status_code=504,
                content={"message": "Request timeout", "detail": "The request took too long to process"}
            )
        except Exception as e:
            process_time = time.time() - start_time
            import logging
            logger = logging.getLogger(__name__)
            if process_time > 30:  # Log slow requests (>30s)
                logger.warning(f"Slow request: {request.url.path} took {process_time:.2f}s")
            raise

# Add timeout middleware first
app.add_middleware(TimeoutMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(fats.router, prefix="/api/v1/fats", tags=["FATS"])
app.include_router(reference.router, prefix="/api/v1/reference", tags=["Reference Data"])
app.include_router(summit.router, prefix="/api/v1/summit", tags=["Summit Logging"])

# Mount static files for image serving (if needed for direct access)
upload_dir = Path(settings.upload_dir)
upload_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(upload_dir)), name="uploads")

# Root endpoint
@app.get("/")
async def root():
    """
    Welcome endpoint
    """
    return {
        "message": "Welcome to OPAL Unified System",
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs"
    }

# Health check endpoint (no database dependency for fast response)
@app.get("/health")
async def health_check():
    """
    Health check endpoint - fast response without database
    """
    return {
        "status": "healthy",
        "service": "OPAL Unified System",
        "databases": ["MariaDB", "sumlogs"]
    }

# Database health check endpoint
@app.get("/health/db")
async def health_check_db():
    """
    Database health check endpoint
    """
    from app.db.session import mariadb_engine, summit_engine
    from sqlalchemy import text
    db_status = {
        "mariadb": "disconnected",
        "sumlogs": "disconnected",
    }
    try:
        async with mariadb_engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            result.fetchone()
        db_status["mariadb"] = "connected"

        if summit_engine is not None:
            async with summit_engine.connect() as conn:
                result = await conn.execute(text("SELECT 1"))
                result.fetchone()
            db_status["sumlogs"] = "connected"

        return {
            "status": "healthy",
            "databases": db_status
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "databases": db_status,
                "error": str(e) if settings.debug else "Database connection failed"
            }
        )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler
    """
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error",
            "detail": str(exc) if settings.debug else "An error occurred"
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
