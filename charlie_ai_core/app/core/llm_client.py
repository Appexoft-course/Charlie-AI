import json
from groq import AsyncGroq
from app.core.config import settings

# Initialize the Groq client once
groq_client = AsyncGroq(api_key=settings.GROQ_API_KEY)

async def analyze_intent_with_llm(prompt: str) -> str:
    """
    Calls the LLM forcing a strict JSON output.
    Returns only the string value of the 'intent' key.
    """
    response = await groq_client.chat.completions.create(
        messages=[{"role": "system", "content": prompt}],
        model="llama-3.1-8b-instant", 
        response_format={"type": "json_object"}
    )
    data = json.loads(response.choices[0].message.content)
    return data.get("intent", "incorrect")

async def generate_speech_with_llm(prompt: str) -> str:
    """
    Calls the LLM in standard text mode.
    Returns the exact words Charlie should say.
    """
    response = await groq_client.chat.completions.create(
        messages=[{"role": "system", "content": prompt}],
        model="llama-3.1-8b-instant" 
    )
    return response.choices[0].message.content.strip()