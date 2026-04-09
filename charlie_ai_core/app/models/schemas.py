from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class LessonState(str, Enum):
    """
    Enum representing the current step of the lesson flow.
    Using an Enum prevents typos and restricts states to valid ones.
    """
    GREETING = "GREETING"
    LEARNING = "LEARNING"
    FINAL_RECAP = "FINAL_RECAP"
    FAREWELL = "FAREWELL"

class ChatRequest(BaseModel):
    """
    Schema for the incoming request from the frontend.
    """
    session_id: str = Field(
        ..., 
        description="Unique identifier for the child's current lesson session.",
        example="session_user_123"
    )
    user_message: str = Field(
        ..., 
        description="The transcribed text of what the child just said.",
        example="Look, a dog!"
    )

class ChatResponse(BaseModel):
    """
    Schema for the outgoing response to the frontend.
    """
    charlie_reply: str = Field(
        ..., 
        description="The exact text Charlie should say (to be sent to Text-to-Speech)."
    )
    action: str = Field(
        default="IDLE", 
        description="Animation or UI trigger for the frontend (e.g., 'SMILE', 'SHOW_CAT', 'CLAP')."
    )
    current_state: LessonState = Field(
        ..., 
        description="The state of the lesson after processing this turn."
    )
    is_finished: bool = Field(
        default=False, 
        description="Flag indicating if the lesson is completely over."
    )

class SessionData(BaseModel):
    """
    Schema for storing the state machine data in Redis.
    This acts as Charlie's 'memory' during the lesson.
    """
    session_id: str
    current_state: LessonState = LessonState.GREETING
    words_to_learn: List[str] = Field(default_factory=list)
    current_word_index: int = 0
    mistakes_count: int = 0
    
    @property
    def current_word(self) -> Optional[str]:
        """Helper property to get the active word."""
        if self.current_word_index < len(self.words_to_learn):
            return self.words_to_learn[self.current_word_index]
        return None