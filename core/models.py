from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """Schema for the incoming chat request from the frontend."""
    session_id: str = Field(..., examples=["user_123"])
    user_message: str = Field(..., examples=["hello fox"])

class SessionState(BaseModel):
    """Schema for the internal in-memory session state."""
    state: str = "GREETING"
    current_word: str = "cat"