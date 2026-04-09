import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis
from app.core.config import settings

# Import our lesson router
from app.api import lesson

# Initialize the FastAPI application
app = FastAPI(
    title="Charlie AI Core",
    description="Backend for Charlie the English Teacher Fox 🦊",
    version="0.1.0"
)

# Set up CORS (Cross-Origin Resource Sharing)
# This is required so your frontend (React, Unity, etc.) can make requests to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Attach the lesson routes to the main app under the /api/v1 prefix
app.include_router(lesson.router, prefix="/api/v1")

# Set up Redis connection (URL is provided by docker-compose environment)
REDIS_URL = settings.REDIS_URL
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

@app.get("/", tags=["Health"])
async def root():
    """
    Basic endpoint to check if the root URL is responding.
    """
    return {"message": "Hello! Charlie AI core is running! 🦊"}

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health-check endpoint for production monitoring.
    Verifies that the API is running and can connect to the Redis database.
    """
    try:
        # Attempt to ping the Redis server
        ping = await redis_client.ping()
        redis_status = "Connected 🟢" if ping else "Disconnected 🔴"
    except Exception as e:
        # Catch any connection errors (e.g., Redis container is down)
        redis_status = f"Error 🔴: {str(e)}"
        
    return {
        "api_status": "OK 🟢",
        "redis_status": redis_status
    }