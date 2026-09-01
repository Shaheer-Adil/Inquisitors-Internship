from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from .schemas import ChatRequest, ChatResponse, EmotionAnalysis, RetrievedChunk
from .emotion_baseline import analyze
from .response_strategy import build_strategy
from .query_builder import build_query
from .retriever import Retriever
from .memory import (
    append,
    delete_user_memory,
    get_history,
    get_long_term_memory,
    maybe_save_explicit_name,
    maybe_save_explicit_language_preference,
)
from .prompt_builder import build_prompt
from .llm import generate, generate_stream
from .safety import safety_check

app = FastAPI(title="Mother-like Chatbot API", version="0.3.0")
retriever = Retriever()
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

# Cache persona file to eliminate disk I/O per request
_persona_cache = None

def _get_persona():
    global _persona_cache
    if _persona_cache is None:
        persona_path = Path(__file__).resolve().parent.parent / "prompts" / "mother_system.md"
        _persona_cache = persona_path.read_text(encoding="utf-8")
    return _persona_cache

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/health")
def health():
    return {"status": "ok", "service": "mother-chatbot", "rag_chunks": retriever.count()}


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.delete("/memory/{user_id}")
def delete_memory(user_id: str):
    return {"user_id": user_id, "deleted": delete_user_memory(user_id)}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    analysis = analyze(req.message)
    strategy = build_strategy(analysis)
    query = build_query(req.message, analysis)
    context = retriever.search(query)
    history = get_history(req.session_id)
    maybe_save_explicit_name(req.user_id, req.message)
    long_term_memory = get_long_term_memory(req.user_id)

    persona = _get_persona()
    prompt = build_prompt(
        persona, analysis, strategy, context, history, long_term_memory, req.message
    )
    try:
        response = safety_check(req.message, generate(prompt))
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail="The AI service is temporarily unavailable.") from error

    append(req.session_id, "user", req.message)
    append(req.session_id, "assistant", response)
    maybe_save_explicit_language_preference(req.user_id, req.message, analysis["language"])

    return ChatResponse(
        session_id=req.session_id,
        analysis=EmotionAnalysis(**analysis),
        response=response,
        retrieved=[RetrievedChunk(**c) for c in context],
    )


@app.post("/chat/stream")
def chat_stream(req: ChatRequest):
    """
    Streaming version of /chat endpoint.
    Streams generated response text as it is produced by Gemini.
    Saves complete response to memory after streaming completes.
    """
    # Safety check on input message first
    safety_override = safety_check(req.message, "")
    if safety_override:
        append(req.session_id, "user", req.message)
        append(req.session_id, "assistant", safety_override)
        return StreamingResponse(iter([safety_override]), media_type="text/plain")

    # Do all the preprocessing exactly like /chat
    analysis = analyze(req.message)
    strategy = build_strategy(analysis)
    query = build_query(req.message, analysis)
    context = retriever.search(query)
    history = get_history(req.session_id)
    maybe_save_explicit_name(req.user_id, req.message)
    long_term_memory = get_long_term_memory(req.user_id)

    persona = _get_persona()
    prompt = build_prompt(
        persona, analysis, strategy, context, history, long_term_memory, req.message
    )
    
    # Save user message to memory
    append(req.session_id, "user", req.message)
    
    # Create a generator that streams response and saves to memory
    def stream_and_save():
        accumulated_response = []
        try:
            for chunk in generate_stream(prompt):
                accumulated_response.append(chunk)
                yield chunk
        finally:
            complete_response = "".join(accumulated_response)
            from .llm import QUOTA_FALLBACK
            # Only save to memory if we have a valid assistant response (not error fallback)
            if complete_response and complete_response not in (
                "I encountered a temporary error. Please try again.",
                QUOTA_FALLBACK,
            ):
                append(req.session_id, "assistant", complete_response)
            maybe_save_explicit_language_preference(req.user_id, req.message, analysis["language"])
    
    return StreamingResponse(stream_and_save(), media_type="text/plain")