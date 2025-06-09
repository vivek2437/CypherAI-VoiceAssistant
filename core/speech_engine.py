import pyttsx3

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

def say(text: str):
    """Speak out the given text using pyttsx3 (cross-platform TTS engine)."""
    engine.say(text)
    engine.runAndWait()
