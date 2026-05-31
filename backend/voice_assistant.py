import time

from modules.voice.speech_to_text import listen
from modules.voice.text_to_speech import speak

from core.controller import process_input


STOP_COMMANDS = [
    "stop",
    "stop aura",
    "stop all",
    "goodbye",
    "bye",
    "exit",
    "quit",
    "see you soon",
    "see you later",
    "talk to you later",
    "catch you later",
    "that's all",
    "thank you that's all"
]


while True:

    user_input = listen()

    if not user_input:
        continue

    if any(
        cmd in user_input.lower()
        for cmd in STOP_COMMANDS
    ):

        speak(
            "Goodbye. See you soon and have a great day."
        )

        break

    print("🤔 Thinking...")

    response = process_input(user_input)

    print("🗣️ Speaking...")

    speak(response)

    time.sleep(1)