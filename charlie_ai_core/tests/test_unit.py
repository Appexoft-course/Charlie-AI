import pytest
from unittest.mock import AsyncMock

from app.models.schemas import SessionData, LessonState
from app.services.orchestrator import get_session, process_chat_message

def test_session_data_defaults():
    """
    UNIT TEST 1: Testing the Pydantic data model directly.
    Ensures that when a new session is created, all default values 
    (state, mistakes, word index) are set correctly.
    """
    # Create a session with only the required fields
    session = SessionData(
        session_id="unit_user_1", 
        words_to_learn=["apple", "banana"]
    )
    
    # Assert defaults are properly initialized
    assert session.current_state == LessonState.GREETING
    assert session.current_word_index == 0
    assert session.mistakes_count == 0
    assert session.current_word == "apple"

@pytest.mark.asyncio
async def test_get_session_creates_new():
    """
    UNIT TEST 2: Testing the session retrieval logic in isolation.
    If Redis returns None (user not found), it should create and return a new session.
    """
    # Create a fake Redis client that returns None
    mock_redis = AsyncMock()
    mock_redis.get.return_value = None
    
    session = await get_session(mock_redis, "new_unit_user")
    
    # Verify the output
    assert session.session_id == "new_unit_user"
    assert session.current_state == LessonState.GREETING
    # Verify that the function attempted to save the new session to Redis
    mock_redis.set.assert_called_once()

@pytest.mark.asyncio
async def test_process_chat_greeting_state():
    """
    UNIT TEST 3: Testing the State Machine transition (GREETING -> LEARNING).
    We isolate the 'process_chat_message' function and feed it a specific state.
    """
    mock_redis = AsyncMock()
    
    # Simulate an existing user session currently in the GREETING state
    initial_session = SessionData(
        session_id="user_greeting", 
        current_state=LessonState.GREETING, 
        words_to_learn=["cat"]
    )
    # Configure the fake Redis to return this session
    mock_redis.get.return_value = initial_session.model_dump_json()

    # Call the core logic function directly (bypassing FastAPI completely)
    response = await process_chat_message(
        redis_client=mock_redis, 
        session_id="user_greeting", 
        user_message="hello!"
    )

    # Verify that the state machine transitioned correctly
    assert response.current_state == LessonState.LEARNING
    assert response.action == "WAVE"
    assert "Hello" in response.charlie_reply