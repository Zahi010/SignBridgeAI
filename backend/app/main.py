from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from backend.app.core.config import settings
from backend.app.api.router import api_router
from backend.app.database.seed import seed_database

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered Indian Sign Language (ISL) educational translation platform for engineering education.",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for video and avatar assets
data_dir = settings.DATA_DIR
if data_dir.exists():
    app.mount("/data", StaticFiles(directory=str(data_dir)), name="data")

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.on_event("startup")
def on_startup():
    print(f"[{settings.PROJECT_NAME}] Starting up. Initializing database and verifying seed data...")
    seed_database()

@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "health": f"{settings.API_V1_PREFIX}/health",
        "zero_fabrication_policy": "Strictly Enforced"
    }

