import time

from modules.voice.speech_to_text import listen
from modules.voice.text_to_speech import speak

from modules.voice.wake_word import wait_for_wake_word

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
    "that's it",
    "thank you that's all",
    "i'm done",
    "we are done",
    "thank you that's it"
]


while True:

    # -------------------------
    # Sleep Mode
    # -------------------------

    print("💤 Waiting for wake word...")

    wait_for_wake_word()

    speak("Yes?")

    print("🟢 Conversation Mode Activated")

    # -------------------------
    # Conversation Mode
    # -------------------------

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

            print("💤 Returning to sleep mode...")

            break

        print("🤔 Thinking...")

        response = process_input(user_input)

        print("🗣️ Speaking...")

        speak(response)

        time.sleep(1)