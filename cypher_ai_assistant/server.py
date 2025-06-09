from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
from gtts import gTTS
import os

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Voice Assistant API is running."

@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    if 'text' not in data:
        return jsonify({'error': 'Missing "text" field in request.'}), 400
    
    text = data['text']
    tts = gTTS(text=text, lang='en')
    filename = "output.mp3"
    tts.save(filename)
    
    return jsonify({'message': f'Successfully converted to speech: {text}', 'audio_file': filename})

@app.route('/listen', methods=['GET'])
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        return jsonify({'transcript': command})
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'}), 400
    except sr.RequestError as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
