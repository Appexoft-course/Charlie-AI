import json
from groq import AsyncGroq
from app.models.llm import GroqEvaluationResult
from app.core.config import settings
from app.core.prompts import get_charlie_system_prompt

# Явно передаємо ключ з нашого конфігу
client = AsyncGroq(api_key=settings.GROQ_API_KEY)
MODEL_NAME = "llama-3.1-8b-instant"

async def evaluate_child_response(current_word: str, child_message: str, mistakes_count: int) -> GroqEvaluationResult:
    # 1. Отримуємо промпт з нашого нового файлу
    system_prompt = get_charlie_system_prompt(current_word, mistakes_count)
    
    try:
        chat_completion = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Child said: {child_message}"}
            ],
            model=MODEL_NAME,
            temperature=0.6,
            response_format={"type": "json_object"}
        )
        
        response_text = chat_completion.choices[0].message.content
        parsed_data = json.loads(response_text)
        return GroqEvaluationResult(**parsed_data)
        
    except Exception as e:
        print(f"Groq API Error: {e}")
        return GroqEvaluationResult(
            charlie_reply="Oops, my internet tail got a bit tangled! 🦊 Can you say that again?",
            is_word_mastered=False,
            suggested_action="THINKING",
            internal_thought="Fallback triggered due to API connection error."
        )