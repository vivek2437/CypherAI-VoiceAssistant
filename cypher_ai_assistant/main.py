from core.speech_engine import say
from core.recognizer import takec
from core.gemini_api import ask_gemini
from core.site_opener import open_site
from core.utils import get_current_time

def main():
    say("Hello Sir, I am Cypher AI.")
    
    while True:
        text = takec()

        if not text:
            say("Sorry, I didn't catch that. Please try again.")
            continue

        if open_site(text):
            continue

        if "what is the time" in text:
            say(f"Sir, the time is {get_current_time()}")
            continue

        if any(cmd in text for cmd in ("exit", "quit", "goodbye")):
            say("Goodbye, Sir. Have a great day!")
            break

        ai_reply = ask_gemini(text)
        say(ai_reply)

if __name__ == "__main__":
    main()
