# Day 3 Implementation

This release extends the working Day-2 RAG backend without replacing the RAG or Gemini integration.

## Added
- Deterministic response strategy module: `backend/response_strategy.py`.
- Long-term memory table in the existing SQLite memory database, kept separate from public RAG.
- Explicit language-preference memory capture only when the user asks for a response language.
- Long-term memory deletion endpoint: `DELETE /memory/{user_id}`.
- Day-3 persona rules in `prompts/mother_system.md`.
- Minimal Day-3 web UI in `frontend/index.html`.
- Twenty Day-3 test conversation starters in `evaluation/day3_conversations.jsonl`.
- Contract tests in `evaluation/test_day3_contract.py`.

## Preserved
- Existing emotion taxonomy and deterministic classifier.
- Chroma retrieval database and retriever.
- Gemini integration and `.env` configuration.
- Existing short-term session memory.
- Existing final safety guard.
- Public `/chat` response schema.

## Pipeline
Frontend → `/chat` → emotion/intent → response strategy → query builder → vector search → short-term memory → appropriate long-term memory → persona + RAG prompt → Gemini → safety → response.

## Testing
The 20-conversation file is a test corpus. Runtime tests that call Gemini require the user's configured `.env` and should be run locally.
