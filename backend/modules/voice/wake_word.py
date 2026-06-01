from modules.voice.speech_to_text import listen


WAKE_WORDS = [
    "hey nova",
    "hi nova",
    "nova"
]


def wait_for_wake_word():

    while True:

        text = listen().lower()

        if any(
            wake_word in text
            for wake_word in WAKE_WORDS
        ):

            return True