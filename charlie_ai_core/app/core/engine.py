import logging
from app.core.models import SessionState
from app.core.prompts import get_evaluator_prompt, get_persona_prompt
from app.core.llm_client import analyze_intent_with_llm, generate_speech_with_llm

# Configure standard Python logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SESSIONS_DB: dict[str, SessionState] = {}

async def process_chat_message(session_id: str, user_message: str) -> dict:
    """
    Core state machine logic orchestrating the Agentic flow.
    Uses standard Python logging for tracking execution.
    """
    logger.info(f"Received message from [{session_id}]: '{user_message}'")

    # 1. Fetch or create session
    if session_id not in SESSIONS_DB:
        logger.info(f"Creating new session for [{session_id}]")
        SESSIONS_DB[session_id] = SessionState()
    
    session = SESSIONS_DB[session_id]

    # 2. Greeting Logic
    if session.state == "GREETING":
        logger.info(f"State transition: GREETING -> LEARNING for [{session_id}]")
        session.state = "LEARNING"
        return {
            "charlie_reply": "Hello! I'm Charlie the Fox! Let's learn some words. What is this? ",
            "action": "WAVE"
        }

    


    logger.info(f"Agent 1 (Evaluator) analyzing word: '{session.current_word}'")
    eval_prompt = get_evaluator_prompt(session.current_word, user_message)
    intent = await analyze_intent_with_llm(eval_prompt)

    logger.info(f"Evaluator classified intent as: '{intent}'")

    action = "NOD" # Default action
    if intent == "correct":
        action = "CLAP"
        # Using .info instead of .success since standard logging doesn't have .success
        logger.info(f"Word '{session.current_word}' mastered by [{session_id}]! Moving to next word.")
        session.current_word = "dog" 
    elif intent == "silence":
        action = "THINK"
    elif intent == "incorrect":
        action = "WAVE"




    logger.info(f"Agent 2 (Persona) generating response for intent '{intent}'")
    persona_prompt = get_persona_prompt(session.current_word, intent)
    charlie_reply = await generate_speech_with_llm(persona_prompt)
    
    logger.info(f"Charlie replies: '{charlie_reply}' (Action: {action})")

    return {
        "charlie_reply": charlie_reply,
        "action": action
    }