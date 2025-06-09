# server.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from core.speech_engine import say
from core.recognizer import takec
from core.gemini_api import ask_gemini

app = Flask(__name__)
CORS(app)  # Enable CORS so Lovable can call your API

@app.route("/api/speak", methods=["POST"])
def speak():
    text = request.json.get("text", "")
    say(text)
    return jsonify({"status": "spoken", "text": text})

@app.route("/api/listen", methods=["GET"])
def listen():
    text = takec()
    return jsonify({"text": text})

@app.route("/api/ai", methods=["POST"])
def ai_reply():
    prompt = request.json.get("prompt", "")
    reply = ask_gemini(prompt)
    return jsonify({"reply": reply})

@app.route("/")
def home():
    return "Cypher AI Assistant API is running."

if __name__ == "__main__":
    app.run(debug=True)
