# Day 2 Completion Checklist

- [x] Python + FastAPI stack
- [x] Embedding model configuration
- [x] Chroma vector database configuration
- [x] Required project folder structure
- [x] Cleaned source datasets
- [x] Processed RAG chunks
- [x] Chunk metadata: source_id/content_type/topic/emotion/intent/language
- [x] Persistent corpus manifest
- [x] Top-k retrieval (default 5)
- [x] Query built from message + emotion/intent
- [x] Persona kept separate from retrieved reference context
- [x] RAG prompt builder
- [x] SQLite session memory
- [x] GET /health
- [x] POST /chat
- [x] Basic safety guard
- [x] Deterministic stress-overload detection for overwhelmed/piling-up messages
- [x] Parenting guidance intent detection
- [x] Safety-signal routing with high urgency
- [x] Retrieval/emotion test set with 51 queries
- [ ] Install Python dependencies and download the embedding model
- [ ] Add a real LLM API key and run live generation
- [ ] Run retrieval tests against the local Chroma collection

The last three are environment/runtime actions that cannot be honestly marked as executed inside the ZIP without the user's local environment and API credentials.
