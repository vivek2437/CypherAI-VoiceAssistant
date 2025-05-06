import os
import speech_recognition as sr
import win32com.client
import webbrowser
import openai
import datetime

# ——— Configure OpenAI API key ———
# Set your key here (for testing only) or use an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

# ——— Text-to-speech setup (Windows only) ———
speaker = win32com.client.Dispatch("SAPI.SpVoice")

def say(text: str):
    """Speak the given text."""
    print(f"Cypher AI: {text}")
    speaker.Speak(text)

def take_command() -> str:
    """Listen to user's voice and return recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        query = recognizer.recognize_google(audio, language="en-IN")
        print(f"User: {query}")
        return query.lower()
    except Exception as e:
        print("Recognition error:", e)
        return ""

def ask_openai(prompt: str) -> str:
    """Send prompt to OpenAI GPT and return response."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Cypher A.I., a helpful voice assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, I encountered an error talking to OpenAI: {e}"

def main():
    say("Hello Sir, I am Cypher AI. You can say, for example, 'Open YouTube', 'What’s the time', or just ask me anything.")

    sites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "stackoverflow": "https://stackoverflow.com"
    }

    while True:
        command = take_command()

        if not command:
            say("Sorry, I didn't catch that. Please try again.")
            continue

        # 1. Open a website
        opened = False
        for name, url in sites.items():
            if f"open {name}" in command:
                say(f"Opening {name}, Sir.")
                webbrowser.open(url)
                opened = True
                break
        if opened:
            continue

        # 2. Tell the time
        if "what is the time" in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            say(f"Sir, the time is {now}")
            continue

        # 3. Exit
        if any(x in command for x in ["exit", "quit", "goodbye"]):
            say("Goodbye, Sir. Have a great day!")
            break

        # 4. Fallback to OpenAI for other queries
        response = ask_openai(command)
        say(response)

if __name__ == "__main__":
    main()
