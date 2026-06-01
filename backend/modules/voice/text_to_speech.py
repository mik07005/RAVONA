import pyttsx3
import re


def clean_text(text):

    text = re.sub(r"\*+", "", text)

    text = re.sub(r"#+", "", text)

    text = re.sub(r"`+", "", text)

    return text


def speak(text):

    text = clean_text(text)

    print(f"NOVA : {text}")

    engine = pyttsx3.init()

    engine.setProperty("rate", 180)

    engine.say(text)

    engine.runAndWait()

    engine.stop()