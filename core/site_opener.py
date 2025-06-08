import webbrowser
from .speech_engine import say

sites = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "stackoverflow": "https://stackoverflow.com"
}

def open_site(command: str) -> bool:
    for name, url in sites.items():
        if f"open {name}" in command:
            say(f"Opening {name}, Sir.")
            webbrowser.open(url)
            return True
    return False
