from pydantic import BaseModel, Field

class GroqEvaluationResult(BaseModel):
    """
    Schema used to enforce structured JSON output from the Groq LLM.
    The LLM must populate these fields based on the context and the child's answer.
    """
    charlie_reply: str = Field(
        ...,
        description="Charlie's verbal response to the child. Must be short, encouraging, A0 English level, max 2 sentences."
    )
    is_word_mastered: bool = Field(
        ...,
        description="True ONLY if the child successfully named the current target word or answered the question correctly."
    )
    suggested_action: str = Field(
        ...,
        description="Suggested UI action based on the context. Options: 'SHOW_IMAGE', 'CELEBRATE', 'THINKING', 'TALK'."
    )
    internal_thought: str = Field(
        ...,
        description="Hidden field for Chain-of-Thought reasoning. Why did Charlie give this response?"
    ) 