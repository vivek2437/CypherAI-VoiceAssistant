import speech_recognition as sr

def takec() -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        query = recognizer.recognize_google(audio, language="en-IN")
        print(f"User said: {query}")
        return query.lower()
    except Exception as e:
        print("Error:", e)
        return ""

