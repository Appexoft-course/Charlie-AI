from redis.asyncio import Redis

from app.models.schemas import LessonState, ChatResponse
from app.services.llm_client import evaluate_child_response

# Імпортуємо функції для роботи з базою з нашого нового файлу!
from app.services.session_store import get_session, save_session

async def process_chat_message(redis_client: Redis, session_id: str, user_message: str) -> ChatResponse:
    """
    The core State Machine. It decides what Charlie should do based on 
    the current lesson state and the child's input.
    """
    # Звертаємось до сховища за сесією
    session = await get_session(redis_client, session_id)
    
    # ---------------------------------------------------------
    # STATE 1: GREETING
    # ---------------------------------------------------------
    if session.current_state == LessonState.GREETING:
        session.current_state = LessonState.LEARNING
        await save_session(redis_client, session)
        
        return ChatResponse(
            charlie_reply="Hello! I'm Charlie the Fox! 🦊 Are you ready to play and learn some English words?",
            action="WAVE",
            current_state=session.current_state
        )

    # ---------------------------------------------------------
    # STATE 2: LEARNING (The core loop with LLM)
    # ---------------------------------------------------------
    elif session.current_state == LessonState.LEARNING:
        current_word = session.current_word
        
        llm_result = await evaluate_child_response(
            current_word=current_word,
            child_message=user_message,
            mistakes_count=session.mistakes_count
        )
        
        if llm_result.is_word_mastered:
            session.current_word_index += 1
            session.mistakes_count = 0 
            
            if session.current_word_index >= len(session.words_to_learn):
                session.current_state = LessonState.FAREWELL
        else:
            session.mistakes_count += 1
            
        await save_session(redis_client, session)
        
        return ChatResponse(
            charlie_reply=llm_result.charlie_reply,
            action=llm_result.suggested_action,
            current_state=session.current_state
        )

    # ---------------------------------------------------------
    # STATE 3: FAREWELL
    # ---------------------------------------------------------
    elif session.current_state == LessonState.FAREWELL:
        return ChatResponse(
            charlie_reply="You did an amazing job today! 🎉 Bye-bye! See you next time!",
            action="CLAP",
            current_state=session.current_state,
            is_finished=True
        )

    return ChatResponse(
        charlie_reply="Oops! Let's start over! 🦊",
        action="THINKING",
        current_state=LessonState.GREETING
    )