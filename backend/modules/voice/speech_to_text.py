import speech_recognition as sr


def listen():

    recognizer = sr.Recognizer()

    recognizer.pause_threshold = 1.5
    recognizer.energy_threshold = 300

    try:

        with sr.Microphone() as source:

            print("🎤 Listening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        text = recognizer.recognize_google(audio)

        print(f"You said: {text}")

        return text

    except sr.WaitTimeoutError:

        print("⌛ No speech detected")

        return ""

    except sr.UnknownValueError:

        print("🤔 Sorry, I didn't catch that")

        return ""

    except sr.RequestError:

        print("🌐 Speech service unavailable")

        return ""

    except Exception as e:

        print(f"Speech Error: {e}")

        return ""