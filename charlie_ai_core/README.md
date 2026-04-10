#  Charlie AI - English Teacher for Kids

A core backend service for an interactive English lesson flow, powered by AI. Charlie is an 8-year-old fox from London who guides kids (ages 4-8) through a vocabulary mini-lesson.

## Architecture & Technical Decisions

Working with kids requires strict control over the educational flow. A pure LLM agent approach is prone to hallucinations, skipping logic, or discussing off-topic subjects indefinitely. 

To solve this, this API service uses a **Hybrid FSM + Two-Step LLM Pipeline**:

1. **Finite State Machine (FSM):** The lesson logic (`engine.py`) is rigidly controlled by Python code (e.g., GREETING -> LEARNING). This guarantees the lesson never derails and frontend animations remain predictable.
2. **Two-Step LLM Pipeline (`llm_client.py` & `prompts.py`):**
   * **Agent 1: Evaluator (JSON Mode):** Analyzes the child's raw input and categorizes intent (`correct`, `incorrect`, `silence`, etc.). This acts as a strict, unemotional logic gate.
   * **Agent 2: Persona Generator:** Receives the evaluated intent and the target word to generate an empathetic, context-aware, and character-accurate response (strictly text, no emojis). 

## Quick Start

This project is built with **FastAPI** and uses **uv** for lightning-fast dependency management inside a highly optimized **Docker** container. It works seamlessly across all platforms.

### Prerequisites
* Docker & Docker Compose installed
* A Groq API Key

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd charlie_ai