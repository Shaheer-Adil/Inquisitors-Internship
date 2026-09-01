def build_query(message: str, analysis: dict) -> str:
    parts=[
        message,
        f"emotion={analysis['emotion']}",
        f"secondary_emotion={analysis.get('secondary_emotion','none')}",
        f"intent={analysis['intent']}",
        f"language={analysis['language']}"
    ]
    return " | ".join(parts)
