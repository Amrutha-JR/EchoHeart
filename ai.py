# ai.py
import os
from transformers import pipeline
from openai import OpenAI

# Load emotion detector (downloads once the first time)
emotion_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base"
)

# Use environment variable for your OpenAI key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_emotion(text):
    return emotion_model(text)[0]["label"]

def get_ai_response(user_text, mood):
    system_msg = (
        f"You are EchoHeart, a supportive AI companion. "
        f"Always be empathetic, kind, and encouraging. "
        f"The user is currently feeling {mood.lower()}."
        f"If the mood is negative (like angry, sad, anxious, stressed), "
        f"include one short, practical coping suggestion. "
        f"If the mood is positive (like happy, excited, proud), "
        f"just respond warmly without suggesting coping actions."
    )
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_text}
        ],
        max_tokens=200
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    print("💚 EchoHeart – Your AI Companion")
    print("Type 'exit' to quit.\n")
    while True:
        user = input("You: ")
        if user.lower() == "exit":
            print("EchoHeart: I'll miss you, friend 💚")
            break
        mood = get_emotion(user)
        reply = get_ai_response(user, mood)
        print("EchoHeart:", reply)
