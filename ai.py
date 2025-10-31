# ai.py
import os
import openai
from typing import Literal

# Use the classic openai client (pin to 1.30.1 in requirements)
openai.api_key = os.environ.get("OPENAI_API_KEY")

# allowed labels you want - change if you want more
EMOTION_LABELS = ["happy", "sad", "angry", "anxious", "neutral", "excited", "proud", "stressed"]

def classify_emotion(text: str) -> str:
    """
    Ask OpenAI to return a single-word label from EMOTION_LABELS that best matches the input.
    Deterministic (temperature=0) and constrained to output one label only.
    """
    prompt = (
        "Classify the user's emotion using one single word from this list:\n"
        f"{', '.join(EMOTION_LABELS)}\n\n"
        "User text:\n"
        f"{text}\n\n"
        "Return only the single label (one word) exactly matching the list above, nothing else."
    )

    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # you can change to any model you have access to
        messages=[{"role": "user", "content": prompt}],
        max_tokens=6,
        temperature=0
    )
    label = resp.choices[0].message.content.strip().lower()
    # fallback: if model returns unexpected, try to sanitize
    if label not in EMOTION_LABELS:
        # crude fallback: pick neutral if unknown
        return "neutral"
    return label

def get_ai_response(user_text: str, mood: str) -> str:
    system_msg = (
        f"You are EchoHeart, a supportive AI companion. "
        f"Always be empathetic, kind, and encouraging. "
        f"The user is currently feeling {mood}. "
        f"If the mood is negative (like angry, sad, anxious, stressed), "
        f"include one short, practical coping suggestion (one sentence). "
        f"If the mood is positive (like happy, excited, proud), "
        f"just respond warmly without suggesting coping actions. Keep responses short (max ~120-150 words)."
    )
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_text}
        ],
        max_tokens=250,
        temperature=0.5
    )
    return resp.choices[0].message.content.strip()

# Helper used by server
def get_emotion(text: str) -> str:
    try:
        return classify_emotion(text)
    except Exception:
        # fail-safe
        return "neutral"
