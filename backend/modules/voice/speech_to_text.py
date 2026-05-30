import speech_recognition as sr


def listen():

    recognizer = sr.Recognizer()

    recognizer.pause_threshold = 1.5
    recognizer.energy_threshold = 300

    with sr.Microphone() as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=1)

        audio = recognizer.listen(
            source,
            timeout=5,
            phrase_time_limit=10
        )

    try:

        text = recognizer.recognize_google(audio)

        print(f"You said: {text}")

        return text

    except Exception as e:

        print(f"Speech Error: {e}")

        return ""