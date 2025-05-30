import os
import speech_recognition as sr
import win32com.client
import webbrowser
import datetime
import requests

# Initialize the Windows text-to-speech engine
speaker = win32com.client.Dispatch("SAPI.SpVoice")

def say(text: str):
    """
    Speak out the given text using the Windows SAPI text-to-speech engine.
    """
    speaker.Speak(text)

def takec() -> str:
    """
    Listen to the user's voice through the microphone and convert it to text.
    Uses Google's speech recognition with Indian English accent.
    Returns the recognized text in lowercase.
    If recognition fails, returns an empty string.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # Adjust for ambient noise for 0.5 seconds to improve accuracy
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        # Listen to the user's input with a max phrase time limit of 5 seconds
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        # Use Google Speech Recognition to convert audio to text
        query = recognizer.recognize_google(audio, language="en-IN")
        print(f"User said: {query}")
        return query.lower()
    except Exception as e:
        # If an error occurs (like no speech recognized), print it and return empty string
        print("Error:", e)
        return ""

def ask_gemini(prompt: str) -> str:
    """
    Send a prompt to the Google Gemini API to get an AI-generated response.
    Returns the response text if successful.
    If there's an error (e.g., network or API issues), returns an error message.
    """
    API_KEY = "AIzaSyD4C2J8lCysRgUSW4t4CgjMrkqftJQPcGk"  # Replace with your Gemini API key
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:
        # Post the prompt to Gemini API
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise error for bad responses
        result = response.json()
        # Extract and return the AI-generated text
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Sorry, I encountered an error using Gemini: {e}"

if __name__ == "__main__":
    # Greet the user when the program starts
    say("Hello Sir, I am Cypher AI.")

    # Dictionary mapping site names to URLs for quick access
    sites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "stackoverflow": "https://stackoverflow.com"
    }

    while True:
        # Take voice input from the user
        text = takec()
        
        # If nothing was recognized, ask the user to try again
        if not text:
            say("Sorry, I didn't catch that. Please try again.")
            continue

        opened = False
        # Check if the user asked to open any known website
        for name, url in sites.items():
            if f"open {name}" in text:
                say(f"Opening {name}, Sir.")
                webbrowser.open(url)
                opened = True
                break
        if opened:
            # If a site was opened, go back to listening for next command
            continue

        # If the user asked for the current time
        if "what is the time" in text:
            now = datetime.datetime.now().strftime("%I:%M %p")  # Format time like 08:30 AM
            say(f"Sir, the time is {now}")
            continue

        # If the user wants to exit the assistant
        if any(cmd in text for cmd in ("exit", "quit", "goodbye")):
            say("Goodbye, Sir. Have a great day!")
            break

        # For any other input, get AI response from Gemini API and speak it
        ai_reply = ask_gemini(text)
        say(ai_reply)
