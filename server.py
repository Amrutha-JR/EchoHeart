import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from ai import get_emotion, get_ai_response

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    """API endpoint for chatting with EchoHeart."""
    data = request.get_json() or {}
    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "message is required"}), 400

    mood = get_emotion(user_message)
    reply = get_ai_response(user_message, mood)
    return jsonify({"reply": reply, "mood": mood})

@app.route("/", defaults={"path": "splash.html"})
@app.route("/<path:path>")
def serve(path):
    """Serve frontend static files."""
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
