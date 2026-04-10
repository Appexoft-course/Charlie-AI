from fastapi import FastAPI
from core.models import ChatRequest
from core.engine import process_chat_message

app = FastAPI()

@app.post("/api/v1/lesson/chat")
async def chat_endpoint(request: ChatRequest):
    return await process_chat_message(request.session_id, request.user_message)
