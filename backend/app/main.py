from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.routes.upload import router as upload_router
from app.routes.query import router as query_router


app = FastAPI(
    title="Multi-Document RAG System",
    description="RAG system that knows when not to answer",
    version="1.0.0"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API routes
app.include_router(upload_router)
app.include_router(query_router)


# Frontend path
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"


# Serve CSS, JavaScript, etc.
app.mount(
    "/frontend",
    StaticFiles(directory=FRONTEND_DIR),
    name="frontend"
)


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "RAG API is running"
    }


# Main website
@app.get("/")
def home():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )