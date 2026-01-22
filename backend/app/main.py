from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import api_router
from .database import init_db

app = FastAPI(
    title="Scrapey",
    description="Reddit Heatmap for Places of Interest",
    version="1.0.0"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
def startup_event():
    """Initialize database on startup."""
    init_db()


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "ok", "app": "Scrapey"}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
