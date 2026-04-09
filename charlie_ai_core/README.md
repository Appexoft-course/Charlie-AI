# 🦊 Charlie AI - English Teacher Core

This is the core backend service for **Charlie AI**, an animated fox that teaches English to kids (4-8 years old). Built with FastAPI, Redis, and Groq (Llama 3.1).

## 🚀 Architecture & Approach

As requested in the test task, this core handles the lesson flow and LLM character generation without the voice part.

1. **Lesson Flow Management (State Machine):**
   - The flow is managed by an `Orchestrator` service. 
   - State (`GREETING` -> `LEARNING` -> `FAREWELL`) and user progress (current word, mistake count) are temporarily stored in **Redis**. 
   - This ensures the API remains stateless, scalable, and memory-efficient.

2. **LLM Integration (Groq):**
   - Used **Groq** for ultra-low latency (crucial for voice AI).
   - **Prompt Engineering:** Instead of letting the LLM talk freely, I enforce a strict JSON output using Pydantic templates. The LLM must generate an `internal_thought` (Chain-of-Thought) before responding, which drastically reduces hallucinations and improves logic.

3. **Handling Real-World Situations (Edge Cases):**
   - *Silence / "I don't know":* The system prompt instructs Charlie to give hints (e.g., animal sounds) instead of giving the answer directly.
   - *Off-topic:* The LLM uses the context to gently guide the child back to the current target word.
   - *Partial answers:* The prompt allows minor typos (like "ca" for "cat") to avoid discouraging the child.
   - *API Failure:* Implemented a fallback response (`try/except` in `llm_client.py`) so if the Groq API fails, Charlie naturally asks the child to repeat the phrase.

## 🛠 Prerequisites

- Docker and Docker Compose
- Groq API Key (Get it free at [console.groq.com](https://console.groq.com/))

## ⚙️ How to Run

1. Clone the repository.
2. Rename `.env.example` to `.env` and insert your API key:
   ```env
   GROQ_API_KEY="gsk_your_key_here"