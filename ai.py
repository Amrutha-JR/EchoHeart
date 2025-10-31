import os
import requests
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Use Hugging Face Inference API model for emotion detection
HF_API_URL = "https://api-inference.huggingface.co/models/bhadresh-savani/distilbert-base-uncased-emotion"
HF_TOKEN = os.environ.get("HF_API_KEY")  # Add this in Railway variables

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def get_emotion(text):
    try:
        payload = {"inputs": text}
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=10)
        data = response.json()

        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
            emotions = data[0]
            top_emotion = max(emotions, key=lambda x: x["score"])
            return top_emotion["label"].lower()
        else:
            return "neutral"
    except Exception as e:
        print("Emotion detection error:", e)
        return "neutral"

# GPT-based emotional response
def get_ai_response(user_text, mood):
    system_prompt = (
        f"You are EchoHeart, a kind and friendly AI friend. "
        f"The user seems {mood}. Respond with empathy, care, and warmth."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            max_tokens=200,
            temperature=0.8,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("AI response error:", e)
        return "I'm having a bit of trouble replying right now, but you're doing great 💛"

if __name__ == "__main__":
    print("💚 EchoHeart AI with real emotion detection!")
    while True:
        user = input("You: ")
        if user.lower() == "exit":
            break
        mood = get_emotion(user)
        print(f"(Detected: {mood})")
        reply = get_ai_response(user, mood)
        print("EchoHeart:", reply)
