import win32com.client

speaker = win32com.client.Dispatch("SAPI.SpVoice")

def say(text: str):
    """Speak out the given text using the Windows SAPI text-to-speech engine."""
    speaker.Speak(text)
