from .config import settings

QUOTA_FALLBACK = "I'm here with you. The AI service is temporarily unavailable, but we can continue shortly."

# Cache Gemini client to eliminate initialization overhead per request
_gemini_client = None

def _get_gemini_client():
    global _gemini_client
    if _gemini_client is None and settings.gemini_api_key:
        from google import genai
        _gemini_client = genai.Client(api_key=settings.gemini_api_key)
    return _gemini_client

def _is_quota_error(error: Exception) -> bool:
    status_code = getattr(error, "status_code", None) or getattr(error, "code", None)
    message = str(error).upper()
    return str(status_code) == "429" or "RESOURCE_EXHAUSTED" in message or "RATE LIMIT" in message


def generate(prompt: str) -> str:
    if not settings.gemini_api_key:
        return "Gemini API key is not configured yet. The Day-2 retrieval pipeline is working; add GEMINI_API_KEY to generate the final response."

    client = _get_gemini_client()
    from google.genai import types

    config = types.GenerateContentConfig(max_output_tokens=250)

    models_to_try = [settings.llm_model]
    if settings.llm_model != "gemini-3.5-flash-lite":
        models_to_try.append("gemini-3.5-flash-lite")

    last_error = None
    for model_name in models_to_try:
        try:
            result = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config,
            )
            if result and result.text:
                return result.text
        except Exception as error:
            last_error = error
            print(f"[Gemini generation error for {model_name}] {type(error).__name__}: {error}")
            import traceback
            traceback.print_exc()
            if _is_quota_error(error):
                continue
            raise RuntimeError(f"Gemini generation failed [{type(error).__name__}]: {error}") from error

    if last_error and _is_quota_error(last_error):
        return QUOTA_FALLBACK

    raise RuntimeError("Gemini returned an empty response.")


def generate_stream(prompt: str):
    """
    Stream a concise Gemini response.
    Keeps the existing Gemini client cache, includes model fallback for rate limits,
    and handles API errors clearly without hiding tracebacks.
    """
    if not settings.gemini_api_key:
        yield (
            "Gemini API key is not configured yet. "
            "Please add GEMINI_API_KEY to the .env file."
        )
        return

    client = _get_gemini_client()
    from google.genai import types

    config = types.GenerateContentConfig(
        max_output_tokens=250,
    )

    models_to_try = [settings.llm_model]
    if settings.llm_model != "gemini-3.5-flash-lite":
        models_to_try.append("gemini-3.5-flash-lite")

    last_error = None
    for model_name in models_to_try:
        try:
            response_stream = client.models.generate_content_stream(
                model=model_name,
                contents=prompt,
                config=config,
            )

            produced_any = False
            for chunk in response_stream:
                text = getattr(chunk, "text", None)
                if text:
                    produced_any = True
                    yield text

            if produced_any:
                return

        except Exception as error:
            last_error = error
            print(f"[Gemini streaming error for {model_name}] {type(error).__name__}: {error}")
            import traceback
            traceback.print_exc()
            if _is_quota_error(error):
                continue
            else:
                yield f"[Gemini Stream Error ({type(error).__name__}): {error}]"
                return

    if last_error and _is_quota_error(last_error):
        yield QUOTA_FALLBACK
    else:
        yield f"[Gemini Stream Failure: {last_error}]"