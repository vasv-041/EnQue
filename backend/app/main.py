"""FastAPI application entry point for EnQue backend.
Wires all routers complying with PRD Section 11:
- /api/auth
- /api/brands
- /api/data
- /api/audience
- /api/content
- /api/agents
- /api/memory
- /api/experiments
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.db import engine, Base
from backend.api import auth, brands, data, audience, content, memory, experiments
from backend.app.routers import agents

# Auto-create all tables in DB if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EnQue API",
    description="AI-Powered Audience Intelligence & Content Optimization Platform",
    version="1.0.0"
)

# Enable CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth.router)
app.include_router(brands.router)
app.include_router(data.router)
app.include_router(audience.router)
app.include_router(content.router)
app.include_router(memory.router)
app.include_router(experiments.router)
app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app": "EnQue API",
        "version": "1.0.0"
    }
