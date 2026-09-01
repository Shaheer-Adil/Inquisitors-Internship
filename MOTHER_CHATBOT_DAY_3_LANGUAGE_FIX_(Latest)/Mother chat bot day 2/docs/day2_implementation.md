# Day 2 Implementation Notes

Day 2 established the working FastAPI/Uvicorn backend, deterministic emotion/intent analysis, query construction, Chroma retrieval, short-term session memory, Gemini generation, and a final safety guard.

The current Day-3 release preserves those components and adds a dedicated response-strategy layer, an appropriate long-term memory table, the Day-3 persona, a minimal chat UI, and Day-3 evaluation assets.

Gemini configuration uses `GEMINI_API_KEY` and `GEMINI_MODEL` in the local `.env` file. The API key must never be committed to source code or distributed in the project ZIP.
