# MAA Project — Thoughtful AI Companion

A modern, professional AI chatbot MVP featuring emotion-aware responses, retrieval-augmented generation (RAG), personalized memory, and safety-first design.

## Features

- **Emotion & Intent Analysis:** Deterministic detection of user emotional state and intent
- **Response Strategy:** Personalized guidance based on detected emotion
- **Retrieval-Augmented Generation (RAG):** Knowledge-grounded responses from a curated corpus
- **Short-Term Memory:** Session-based conversation history
- **Long-Term Memory:** Persistent user facts (name, preferences) stored separately from public RAG
- **Safety First:** Crisis detection with immediate support resources
- **Modern UI:** Professional, responsive web interface
- **Professional Persona:** Warm, empathetic, boundaryaware responses

## Architecture

User message
→ emotion/intent analysis
→ response strategy
→ query builder
→ Chroma vector search (RAG)
→ session history
→ user long-term memory
→ mother persona + prompt engineering
→ Gemini LLM
→ safety check
→ response

## Included

- `data/clean/` normalized Day-1 datasets
- `data/processed/rag_chunks.jsonl` Day-2-ready RAG corpus
- `data/processed/corpus_manifest.json`
- `rag/build_index.py` vector-index builder
- `rag/test_retrieval.py` retrieval smoke test
- `evaluation/day2_retrieval_tests.jsonl` 48 test inputs
- `backend/` FastAPI, retrieval, embeddings, emotion/strategy, memory, safety and LLM modules
- `frontend/index.html` minimal Day-3 chat UI
- `evaluation/day3_conversations.jsonl` 20 Day-3 conversation test starters
- `evaluation/test_day3_contract.py` deterministic Day-3 contract tests
- `docs/day3_implementation.md` Day-3 implementation notes
- `prompts/mother_system.md` retained as the high-priority persona
- `docs/day2_implementation.md`
- `docs/rag.md`
- `docs/day2_checklist.md`
- `.env.example`
- `requirements.txt`

## Installation

1. Create virtual environment:
```bash
python -m venv .venv
```

2. Activate:
```bash
# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy environment template and add Gemini API key:
```bash
copy .env.example .env
```

Edit `.env` and add your `GEMINI_API_KEY`:
```
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.6-flash
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHROMA_PATH=./rag/chroma_db
CHROMA_COLLECTION=mother_chatbot_v1
TOP_K=5
MAX_HISTORY_MESSAGES=12
```

## Starting the Backend

```bash
cd path/to/project
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

The server will start at:
```
http://127.0.0.1:8000/
```

## Using the Chatbot

1. **Open the UI:** Navigate to `http://127.0.0.1:8000/` in your browser
2. **Type a message** in the input field
3. **Press Enter or click Send** to submit
4. The chatbot will analyze emotion, search the knowledge base, and provide a personalized response
5. Chat history persists within the session
6. User preferences and facts are saved to long-term memory when explicitly stated

## API Endpoints

### Health Check
```
GET /health
```
Returns: `{"status": "ok", "service": "mother-chatbot", "rag_chunks": <count>}`

### Chat (Main Endpoint)
```
POST /chat
Content-Type: application/json

{
  "user_id": "unique_user_identifier",
  "session_id": "unique_session_identifier", 
  "message": "user message text"
}
```

Response:
```json
{
  "session_id": "session_id",
  "analysis": {
    "emotion": "detected_emotion",
    "secondary_emotion": "secondary_emotion",
    "intent": "user_intent",
    "urgency": "normal|high",
    "language": "English|Roman Urdu|Urdu",
    "confidence": 0.85
  },
  "response": "chatbot response text",
  "retrieved": [
    {
      "chunk_id": "id",
      "text": "retrieved context",
      "metadata": {...},
      "distance": 0.123
    }
  ]
}
```

### Delete User Memory
```
DELETE /memory/{user_id}
```
Removes all stored long-term facts for a user.

## Project Structure

- `backend/` — FastAPI application, RAG retrieval, emotion analysis, response strategy, memory management, safety checking, and LLM integration
- `frontend/index.html` — Professional responsive web UI
- `rag/` — Vector database (Chroma) and retrieval system
- `data/` — Knowledge corpus and conversation data
- `prompts/` — System persona definition
- `memory/` — SQLite database for session history and user facts
- `evaluation/` — Test sets and evaluation results
- `docs/` — Technical documentation

## Evaluation & Limitations

- See `docs/evaluation.md` for MVP evaluation methodology and test coverage
- See `docs/limitations.md` for current constraints and known limitations
- See `evaluation/results.csv` for representative test results

## Performance Optimizations

- **Gemini Client Caching:** Client initialized once and reused for all requests
- **Persona File Caching:** System prompt cached in memory after first read
- **Vector Search:** Fast approximate similarity search using Chroma's HNSW indexing
- **Session Memory:** Efficient SQLite queries with index support

## License & Attribution

This project integrates Google Gemini for LLM responses and Sentence Transformers for semantic embeddings.
