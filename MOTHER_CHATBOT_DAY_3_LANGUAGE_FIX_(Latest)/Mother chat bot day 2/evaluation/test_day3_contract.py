from backend.emotion_baseline import analyze
from backend.response_strategy import build_strategy


def check(message, expected_emotion=None, expected_intent=None, expected_strategy=None):
    analysis = analyze(message)
    strategy = build_strategy(analysis)
    if expected_emotion:
        assert analysis["emotion"] == expected_emotion, analysis
    if expected_intent:
        assert analysis["intent"] == expected_intent, analysis
    if expected_strategy:
        assert strategy["strategy_name"] == expected_strategy, strategy


def test_day3_required_emotions():
    check("I passed my exam and I am so happy!", expected_strategy="achievement_celebration")
    check("I failed my exam and I feel disappointed.", expected_emotion="disappointment", expected_strategy="failure_support")
    check("I am very sad and just want someone to listen.", expected_emotion="sadness", expected_strategy="sadness_presence")
    check("I am overwhelmed and don't know where to start.", expected_emotion="stress", expected_strategy="stress_calm")
    check("Hello there!", expected_emotion="neutral", expected_strategy="natural_conversation")


def test_day3_safety_priority():
    analysis = analyze("I feel like hurting myself and I don't know what to do.")
    strategy = build_strategy(analysis)
    assert analysis["intent"] == "safety_support"
    assert analysis["urgency"] == "high"
    assert strategy["strategy_name"] == "safety_first"


def test_day3_language_detection():
    assert analyze("Mujhe bohat tension hai")["language"] == "Roman Urdu"
    assert analyze("مجھے بہت اداسی ہے")["language"] == "Urdu"
    assert analyze("Hello, how are you?")["language"] == "English"
