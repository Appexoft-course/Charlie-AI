import os
from fastapi import APIRouter, Depends, HTTPException
from redis.asyncio import Redis

from app.models.schemas import ChatRequest, ChatResponse
from app.services.orchestrator import process_chat_message

# Create a router to group all lesson-related endpoints
router = APIRouter(prefix="/lesson", tags=["Lesson Flow"])

async def get_redis() -> Redis:
    """
    Dependency function to provide a Redis connection to our endpoints.
    FastAPI will automatically call this when an endpoint needs Redis.
    """
    import redis.asyncio as aioredis
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    return aioredis.from_url(redis_url, decode_responses=True)

@router.post("/chat", response_model=ChatResponse)
async def chat_with_charlie(
    request_data: ChatRequest, 
    redis_client: Redis = Depends(get_redis)
):
    """
    Main endpoint for the frontend. 
    Receives the child's transcribed speech and returns Charlie's LLM-generated response.
    """
    try:
        # Pass the data to our core state machine (orchestrator)
        response = await process_chat_message(
            redis_client=redis_client,
            session_id=request_data.session_id,
            user_message=request_data.user_message
        )
        return response
    
    except Exception as e:
        # If something goes terribly wrong, return a 500 error gracefully
        print(f"Error processing chat: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Charlie's brain got a little dizzy. Please try again!"
        )