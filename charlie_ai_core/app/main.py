from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.models import ChatRequest
from app.core.engine import process_chat_message

app = FastAPI()

@app.post("/api/v1/lesson/chat")
async def chat_endpoint(request: ChatRequest):
    return await process_chat_message(request.session_id, request.user_message)
