"""Day-3 deterministic response strategy layer.

This module converts the existing emotion/intent analysis into concise internal
guidance for the prompt builder. It does not perform emotion detection and does
not bypass the safety layer.
"""

from typing import Dict


STRATEGIES = {
    "happiness": {
        "strategy_name": "achievement_celebration",
        "response_goal": "Celebrate the good news and make the user's effort feel seen.",
        "guidance": "Praise effort or a meaningful detail; an appropriate brief blessing is optional.",
    },
    "pride": {
        "strategy_name": "achievement_celebration",
        "response_goal": "Recognize the achievement while reinforcing effort and intrinsic worth.",
        "guidance": "Celebrate without making personal worth depend only on results or comparison.",
    },
    "disappointment": {
        "strategy_name": "failure_support",
        "response_goal": "Acknowledge disappointment before helping the user move forward.",
        "guidance": "Reassure without minimizing; offer one practical next step when appropriate.",
    },
    "sadness": {
        "strategy_name": "sadness_presence",
        "response_goal": "Provide empathy and emotional presence before advice.",
        "guidance": "Listen first, avoid forced positivity, and ask a gentle question when useful.",
    },
    "stress": {
        "strategy_name": "stress_calm",
        "response_goal": "Validate the pressure and reduce cognitive load.",
        "guidance": "Help the user slow down and choose one manageable next step; do not overload with advice.",
    },
    "fear": {
    "strategy_name": "reassurance",
    "response_goal": "Acknowledge the fear and provide calm, supportive reassurance.",
    "guidance": "Validate the user's fear without minimizing it; encourage one manageable next step and avoid overwhelming advice.",
},

    "neutral": {
        "strategy_name": "natural_conversation",
        "response_goal": "Respond naturally without manufacturing an emotional state.",
        "guidance": "Match the conversational purpose and keep warmth light and appropriate.",
    },
}

DEFAULT_STRATEGY = {
    "strategy_name": "emotion_aware_support",
    "response_goal": "Acknowledge the user's state and respond appropriately to their intent.",
    "guidance": "Use the detected emotion and intent without forcing a fixed response template.",
}


def build_strategy(analysis: Dict) -> Dict:
    """Return deterministic internal guidance from the existing analysis."""
    if analysis.get("urgency") == "high" and analysis.get("intent") == "safety_support":
        return {
            "strategy_name": "safety_first",
            "response_goal": "Prioritize immediate safety and encourage appropriate real-world help.",
            "guidance": "Do not let ordinary emotional strategy override the existing safety behavior.",
        }

    strategy = STRATEGIES.get(analysis.get("emotion"), DEFAULT_STRATEGY).copy()
    if analysis.get("intent") == "parenting_guidance":
        strategy = {
            "strategy_name": "practical_guidance",
            "response_goal": "Give clear, supportive guidance that matches the user's question.",
            "guidance": "Use relevant retrieved knowledge and keep the answer practical and respectful.",
        }
    return strategy
