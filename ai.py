import os
from transformers import pipeline
from openai import OpenAI

# Load Hugging Face emotion model (lightweight & accurate)
emotion_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base"
)

# Initialize OpenAI client (make sure OPENAI_API_KEY is set in Railway)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_emotion(text):
    """Detect the user's emotion from text."""
    try:
        return emotion_model(text)[0]["label"]
    except Exception as e:
        print("Emotion detection error:", e)
        return "neutral"

def get_ai_response(user_text, mood):
    """Generate EchoHeart's empathetic reply based on mood."""
    system_msg = (
        f"You are EchoHeart, a friendly AI companion who provides emotional support. "
        f"The user feels {mood.lower()}. "
        f"If the mood is negative (angry, sad, anxious, lonely, stressed), respond empathetically "
        f"and include one short, practical coping suggestion (e.g., breathing, journaling, music). "
        f"If the mood is positive (happy, proud, excited), respond warmly and encouragingly without advice."
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
    print("💚 EchoHeart is ready to chat!")
    while True:
        user = input("You: ")
        if user.lower() == "exit":
            print("EchoHeart: Take care, my friend 💚")
            break
        mood = get_emotion(user)
        reply = get_ai_response(user, mood)
        print("EchoHeart:", reply)
