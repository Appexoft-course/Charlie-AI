from redis.asyncio import Redis
from app.models.schemas import SessionData, LessonState

# Базові слова для тестового уроку
DEFAULT_WORDS = ["cat", "dog", "bird"]

async def get_session(redis_client: Redis, session_id: str) -> SessionData:
    """
    Отримує стан сесії з Redis. 
    Якщо сесії немає (новий урок), створює базову.
    """
    data = await redis_client.get(session_id)
    if data:
        return SessionData.model_validate_json(data)
    
    # Ініціалізація нового уроку
    new_session = SessionData(
        session_id=session_id,
        current_state=LessonState.GREETING,
        words_to_learn=DEFAULT_WORDS
    )
    await save_session(redis_client, new_session)
    return new_session

async def save_session(redis_client: Redis, session_data: SessionData):
    """Зберігає поточний стан уроку в Redis на 1 годину."""
    await redis_client.set(
        session_data.session_id, 
        session_data.model_dump_json(),
        ex=3600  # Час життя сесії: 3600 секунд (1 година)
    )