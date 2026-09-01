# Known Limitations & Constraints

This document clearly outlines current constraints and limitations of the MAA Project MVP.

## System Constraints

### 1. SentenceTransformer Model Initialization (Critical)

**Limitation:** Backend cannot start on Windows systems with insufficient paging file configuration.

**Details:**
- The `sentence-transformers` library loads the embedding model (all-MiniLM-L6-v2) into memory during `Retriever` initialization
- On systems with low VM/paging file limits, this triggers OS error 1455: "The paging file is too small for this operation to complete"
- This occurs at `backend/retriever.py:13` during app startup before any request handling
- Result: `/chat` endpoint unreachable until the system constraint is resolved

**Not a Code Defect:** This is a system resource limitation, not a bug in the application code.

**Workarounds:**
- Increase Windows paging file size (manual system configuration)
- Run on a system with higher available RAM
- Run on macOS/Linux (where paging file defaults are typically larger)
- Run in a cloud environment with adequate memory allocation

**Impact:** Prevents functional testing of end-to-end request flows on resource-constrained systems.

## Performance Characteristics

### 2. Gemini API Latency

**Limitation:** Response time depends on Google's Gemini API service latency and available quota.

**Details:**
- The LLM call in `backend/llm.py:generate()` is inherently network-dependent
- Google's API may have variable response times (typically 1-5 seconds for generation)
- Rate limiting (429 errors) possible under high volume
- Quota exhaustion handled with fallback message

**Mitigations Already Implemented:**
- Gemini client is cached (initialized once, reused)
- Quota errors are caught and handled gracefully
- Fallback response provided if service unavailable

**Not Addressed:**
- Client-side request batching/queueing
- Response caching for identical inputs
- Timeout configuration (uses library defaults)

## Evaluation Coverage

### 3. Representative Test Set (Not Exhaustive)

**Limitation:** Evaluation includes 8 representative test cases, not a comprehensive 100+ test suite.

**Details:**
- `evaluation/results.csv` covers representative scenarios:
  - 1 each for: achievement, failure, sadness, stress, fear, parenting, neutral
  - 1 safety test (executable via code inspection)
- Full functional test suite execution blocked by the SentenceTransformer startup issue
- Test methodology is sound but scope is limited by time constraints

**Coverage:**
- ✅ Emotion categories: 6/10 major emotions represented
- ✅ Intent types: parenting_guidance, safety_support, natural_conversation
- ✅ Safety behavior: Verified through code review
- ❌ Latency measurements: Cannot execute
- ❌ Retrieval relevance: Cannot execute
- ❌ Multi-language flows: Cannot execute (Urdu/Roman Urdu)

**Recommendation:** Full 100+ test campaign appropriate for production phase.

## Architecture Limitations

### 4. RAG Retrieval Determinism

**Limitation:** Vector similarity search results depend on query and index quality.

**Details:**
- Chroma HNSW indexing is approximate (not exact nearest neighbor)
- Retrieval relevance varies with:
  - Query formulation in `backend/query_builder.py`
  - Embedding model quality (all-MiniLM-L6-v2 is CPU-efficient but not state-of-the-art)
  - Knowledge base completeness and organization
- No explicit relevance feedback loop in MVP

**Scope:**
- TOP_K default is 5 chunks
- Cannot be tested without backend initialization

### 5. Emotion Detection Coverage

**Limitation:** Emotion detection is keyword-based and deterministic, not ML-based.

**Details:**
- `backend/emotion_baseline.py` uses regex and keyword matching
- Works well for clear emotion signals but may miss nuance
- No confidence threshold filtering (always returns best match)
- Multilingual support limited to English, Urdu, Roman Urdu keywords

**Strengths:**
- Deterministic (same input → same output)
- Fast (no model inference)
- Transparent (rules are visible in code)
- Reliable for crisis detection

**Trade-offs:**
- May misclassify ambiguous inputs
- Keyword list is manually maintained
- No learning from user feedback

### 6. Long-Term Memory Scope

**Limitation:** Long-term memory only stores explicitly stated facts, not inferred preferences.

**Details:**
- Only saves:
  - User's stated name (when explicitly provided)
  - User's stated language preference (when explicitly requested)
- Does not infer or store:
  - Emotional patterns
  - Topic preferences
  - Interaction history beyond session
- Memory is per-user, not per-demographic or cohort

**Rationale:** Privacy-first design; only stores what the user explicitly consents to.

## Behavioral Limitations

### 7. Session Isolation

**Limitation:** Sessions are isolated; no cross-session learning.

**Details:**
- Each session is independent in conversation flow
- User facts are available but not conversation patterns
- No adaptive response improvement over time
- No A/B testing or variant tracking

### 8. Gemini Model Version Lock

**Limitation:** Model is set to `gemini-3.6-flash` via `.env`.

**Details:**
- No automatic model updates
- Behavior may change when Google updates the model server-side
- No fallback to alternative models in code

### 9. Single-Model Architecture

**Limitation:** Only Gemini is supported as the LLM.

**Details:**
- Would require code changes to swap LLM providers
- No abstraction layer for LLM switching
- No support for local/offline LLM alternatives

## Development Limitations

### 10. Frontend Framework Dependencies

**Limitation:** Frontend is vanilla HTML/CSS/JS; no reactive framework.

**Details:**
- Manual DOM manipulation
- No state management library
- Scaling to complex features would benefit from React/Vue
- Current approach is sufficient for MVP

### 11. Deployment Not Included

**Limitation:** MVP is development-only; no production deployment included.

**Details:**
- No Docker/containerization
- No reverse proxy configuration
- No horizontal scaling setup
- No monitoring/alerting
- No CDN for static assets
- No database backup strategy

## Documentation Completeness

### 12. Persona Boundaries

**Limitation:** The mother persona is defined but boundaries are not exhaustively tested.

**Details:**
- Persona is documented in `prompts/mother_system.md`
- Safety behavior is enforced for crisis signals
- Other boundary testing (e.g., inappropriate requests) is limited

## Summary of Impact

| Limitation | Severity | Impact | Workaround |
|-----------|----------|--------|-----------|
| SentenceTransformer startup | 🔴 Critical | Backend unavailable | Increase VM; use resource-rich system |
| Gemini latency | 🟡 Medium | Slower responses | Cache/batch requests |
| Representative test set | 🟡 Medium | Limited confidence | Run full tests on working system |
| Keyword-based emotions | 🟢 Low | Occasional misclassification | Use as baseline; add ML layer later |
| No cross-session learning | 🟢 Low | Limited personalization | Add analytics layer in v2 |
| Vanilla frontend | 🟢 Low | Limited scalability | Upgrade to framework in v2 |
| No deployment setup | 🟡 Medium | Not production-ready | Add containerization for v2 |

## Future Work

To address these limitations in subsequent phases:

1. **System Requirement:** Document minimum RAM/paging file requirements
2. **Latency:** Implement client-side caching and request batching
3. **Testing:** Run full 100+ test suite on resource-adequate system
4. **Emotion:** Add optional ML-based emotion classifier
5. **Personalization:** Implement cross-session preference learning (with consent)
6. **Frontend:** Migrate to React/Vue if complexity increases
7. **Deployment:** Add Docker, monitoring, and production deployment guides
8. **LLM:** Abstract LLM provider for easier switching
