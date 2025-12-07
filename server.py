# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from ai import get_emotion, get_ai_response

app = Flask(__name__)
CORS(app)  # allow calls from your local index.html

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "message is required"}), 400

    mood = get_emotion(user_message)
    reply = get_ai_response(user_message, mood)
    return jsonify({"reply": reply, "mood": mood})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
