import re
from typing import Dict

# Day-2 baseline only. Day 3 can replace/upgrade this with a dedicated classifier.
# The rules below are intentionally deterministic so the API analysis is stable
# for common Day-2 scenarios and does not depend on the LLM.
KEYWORDS = {
    "happiness": ["happy", "happier", "glad", "khush", "khushi", "خوش", "mubarak", "great news", "wonderful news"],
    "pride": ["proud", "fakhar", "فخر", "first position", "first place", "achieve", "achievement", "promotion"],
    "sadness": ["sad", "cry", "crying", "udaas", "dil udaas", "اداس", "رو رہا", "rona", "heartbroken"],
    "disappointment": ["failed", "fail", "disappointed", "disappointing", "disappoint", "didn't get selected", "did not get selected", "nahi hua", "ناکام", "مایوس", "result was disappointing", "result was not good"],
    "stress": [
        "stress", "stressed", "pressure", "tension", "tensed", "overwhelmed", "overloaded",
        "piling up", "pile up", "too much work", "too much to do", "so much work", "swamped",
        "don't know where to start", "do not know where to start", "can't keep up", "cannot keep up",
        "پریشان", "ٹینشن", "pressure", "pareshan", "bohat pareshan"
    ],
"fear": ["afraid", "scared", "scared about", "fear", "nervous", "nervousness", "dar", "ڈر", "khauf", "خوف"],    "anger": ["angry", "anger", "gussa", "غصہ", "furious", "irritated"],
    "loneliness": ["lonely", "alone", "akela", "اکیلا", "تنہا", "nobody understands", "no one understands", "nobody to talk"],
    "gratitude": ["thank you", "thanks", "shukriya", "شکریہ", "grateful"],
    "low_motivation": ["can't start", "cannot start", "no motivation", "lazy", "mann nahi", "دل نہیں", "don't feel like starting", "do not feel like starting"],
    "confusion": ["confused", "samajh nahi", "سمجھ نہیں", "what should i do", "what should i do next", "kya karun"],
    "worry": ["worried", "worry", "worrying", "fikr", "فکر", "concerned"],
    "frustration": ["frustrated", "frustration", "tang", "تنگ", "fed up"],
    "homesickness": ["miss home", "ghar yaad", "گھر یاد", "homesick"],
}

# Safety phrases are checked before ordinary emotion scoring so a crisis signal
# cannot be hidden by a weaker emotion such as sadness or loneliness.
SAFETY_TERMS = [
    "hurt myself", "hurting myself", "harm myself", "harming myself", "self harm", "self-harm", "kill myself",
    "suicide", "suicidal", "end my life", "take my own life", "want to die",
    "don't want to live", "do not want to live", "unsafe right now"
]

PARENTING_MARKERS = [
    "child", "children", "parent", "parents", "parenting", "kid", "kids",
    "my son", "my daughter", "communication skills", "help my child"
]


def detect_language(text: str) -> str:
    if re.search(r"[\u0600-\u06FF]", text):
        # Distinguish Urdu script from Arabic is unnecessary for this MVP.
        return "Urdu"
    roman_markers = ["hai", "mujhe", "meri", "mera", "ammi", "beta", "aaj", "bohat", "kyun", "kya", "nahi", "karna"]
    lower = text.lower()
    if any(w in lower.split() for w in roman_markers):
        return "Roman Urdu"
    return "English"


def _contains_any(text: str, phrases: list[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def analyze(text: str) -> Dict:
    lower = text.lower()

    # 1. Safety takes priority over all ordinary emotion labels.
    if _contains_any(lower, SAFETY_TERMS):
        return {
            "emotion": "hurt",
            "secondary_emotion": "none",
            "intent": "safety_support",
            "urgency": "high",
            "language": detect_language(text),
            "confidence": 0.95,
        }

    # 2. Parenting questions are not an emotional state by themselves.
    # Keep emotion=neutral but expose the correct intent so retrieval can target
    # parenting guidance rather than daily conversation.
    if _contains_any(lower, PARENTING_MARKERS):
        return {
            "emotion": "neutral",
            "secondary_emotion": "none",
            "intent": "parenting_guidance",
            "urgency": "normal",
            "language": detect_language(text),
            "confidence": 0.80,
        }

    scores = {}
    for emotion, words in KEYWORDS.items():
        scores[emotion] = sum(1 for w in words if w in lower)

    best = max(scores, key=scores.get)
    if scores[best] == 0:
        best = "neutral"
        confidence = 0.45
    else:
        confidence = min(0.95, 0.60 + 0.08 * scores[best])

    secondary = "none"
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    if len(ranked) > 1 and ranked[1][1] > 0:
        secondary = ranked[1][0]

    intent_map = {
        "happiness": "achievement_or_good_news",
        "pride": "achievement",
        "sadness": "emotional_support",
        "disappointment": "failure_or_disappointment",
        "stress": "stress_support",
        "fear": "reassurance",
        "anger": "deescalation",
        "loneliness": "connection",
        "gratitude": "gratitude",
        "low_motivation": "motivation",
        "confusion": "advice",
        "worry": "reassurance",
        "frustration": "emotional_support",
        "homesickness": "emotional_support",
    }
    intent = intent_map.get(best, "daily_conversation")

    # Explicit stress signals should win over generic confusion when the user
    # describes being overloaded and unable to decide where to begin.
    if _contains_any(lower, [
        "overwhelmed", "piling up", "too much work", "too much to do",
        "so much work", "don't know where to start", "do not know where to start",
        "can't keep up", "cannot keep up"
    ]):
        best = "stress"
        intent = "stress_support"
        confidence = max(confidence, 0.76)

    urgency = "normal"
    if _contains_any(lower, ["urgent", "emergency", "unsafe", "danger"]):
        urgency = "high"

    return {
        "emotion": best,
        "secondary_emotion": secondary,
        "intent": intent,
        "urgency": urgency,
        "language": detect_language(text),
        "confidence": round(confidence, 2),
    }
