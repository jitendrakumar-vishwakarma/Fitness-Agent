"""
FastAPI entry point for Fitness AI Agent
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, goals, summaries, health
from app.config import settings

app = FastAPI(
    title="Fitness AI Agent API",
    description="AI-powered fitness tracking and goal management system",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=(
        settings.ALLOWED_ORIGINS.split(",")
        if isinstance(settings.ALLOWED_ORIGINS, str)
        else settings.ALLOWED_ORIGINS
    ),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(goals.router, prefix="/api", tags=["goals"])
app.include_router(summaries.router, prefix="/api", tags=["summaries"])


@app.get("/")
async def root():
    return {"message": "Fitness AI Agent API", "version": "1.0.0", "status": "running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
