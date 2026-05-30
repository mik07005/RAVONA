import time
from modules.voice.speech_to_text import listen
from modules.voice.text_to_speech import speak

from core.controller import process_input


while True:

    user_input = listen()

    if not user_input:
        continue

    if "stop aura" in user_input.lower():
        speak("Goodbye.")
        break

    response = process_input(user_input)

    speak(response)
    time.sleep(1)