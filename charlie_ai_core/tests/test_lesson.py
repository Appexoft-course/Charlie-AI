import pytest
from fastapi.testclient import TestClient
import uuid
from unittest.mock import AsyncMock, patch

from app.main import app
from app.models.llm import GroqEvaluationResult

# Create a test client that will simulate HTTP requests to our FastAPI application
client = TestClient(app)

def test_health_check():
    """
    Test the health check endpoint to ensure the server is running
    and can establish a connection with the Redis database.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert "OK" in response.json()["api_status"]

# We use @patch to mock the external call to the Groq API.
# This prevents our tests from consuming real API limits and makes them run instantly.
# We replace 'evaluate_child_response' with an AsyncMock object.
@patch("app.services.orchestrator.evaluate_child_response", new_callable=AsyncMock)
def test_lesson_flow(mock_llm):
    """
    Test the core State Machine logic of the lesson.
    Verifies the transition from the GREETING state to the LEARNING state,
    and ensures that the LLM response is processed correctly.
    """
    
    # 1. Setup the mocked LLM response
    # We define exactly what our fake AI should return when called
    mock_llm.return_value = GroqEvaluationResult(
        internal_thought="The child said cat correctly.",
        charlie_reply="Yes, it's a cat! 🐱",
        is_word_mastered=True,
        suggested_action="CLAP"
    )

    # Use a unique session ID for testing to isolate data
    session_id = f"test_{uuid.uuid4()}"

    # --- STAGE 1: Send the initial message to trigger the GREETING state ---
    response_1 = client.post(
        "/api/v1/lesson/chat", 
        json={"session_id": session_id, "user_message": "hello"}
    )
    
    # Verify the HTTP status and the structural integrity of the response
    assert response_1.status_code == 200
    data_1 = response_1.json()
    
    # Verify that the state machine correctly transitioned to LEARNING
    assert data_1["current_state"] == "LEARNING"
    assert data_1["action"] == "WAVE"
    assert "Hello" in data_1["charlie_reply"]

    # --- STAGE 2: Send a message to simulate the child answering (LEARNING state) ---
    # This request will trigger our mocked LLM instead of the real Groq API
    response_2 = client.post(
        "/api/v1/lesson/chat", 
        json={"session_id": session_id, "user_message": "cat"}
    )
    
    assert response_2.status_code == 200
    data_2 = response_2.json()
    
    # Verify that the application correctly integrated the mocked AI response
    assert data_2["charlie_reply"] == "Yes, it's a cat! 🐱"
    assert data_2["action"] == "CLAP"
    
    # Verify that our mocked function was actually called exactly once
    mock_llm.assert_called_once()