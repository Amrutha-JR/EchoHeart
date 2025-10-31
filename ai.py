# ai.py
import os
from transformers import pipeline
from openai import OpenAI

# Load emotion detection model (downloads once)
emotion_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base"
)

# Create OpenAI client using the new v1.x interface
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_emotion(text):
    """Detects emotion label from text using transformer model."""
    result = emotion_model(text)[0]
    return result["label"]

def get_ai_response(user_text, mood):
    """Generates empathetic response using OpenAI GPT model."""
    system_message = (
        f"You are EchoHeart, a supportive and caring AI companion. "
        f"The user is feeling {mood.lower()}. "
        f"If the mood is negative (like sad, angry, anxious, stressed), include a small coping tip. "
        f"If the mood is positive (like happy, excited, proud), reply warmly and encouragingly."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_text}
        ],
        max_tokens=200,
        temperature=0.7
    )

    return response.choices[0].message.content
