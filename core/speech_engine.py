from gtts import gTTS
import os

def say(text):
    tts = gTTS(text)
    tts.save("response.mp3")
    os.system("mpg123 response.mp3")  # or use any MP3 player
