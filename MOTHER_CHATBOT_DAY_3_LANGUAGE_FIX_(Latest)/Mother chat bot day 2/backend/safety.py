def safety_check(message: str, response: str):
    # Lightweight Day-2 guard. Day 4 can expand evaluation and safety coverage.
    risky_terms = [
        "suicide", "suicidal", "kill myself", "self harm", "self-harm",
        "hurt myself", "hurting myself", "harm myself", "harming myself",
        "end my life", "take my own life", "want to die", "don't want to live",
        "do not want to live"
    ]
    low = message.lower()
    if any(t in low for t in risky_terms):
        return (
            "I'm really glad you told me. Your safety matters right now. "
            "Please move away from anything you could use to hurt yourself and "
            "contact a trusted person who can stay with you. If you may act on "
            "these thoughts or are in immediate danger, contact your local "
            "emergency service or go to the nearest emergency department now."
        )
    return response
