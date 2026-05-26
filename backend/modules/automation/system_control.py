import os
import webbrowser
from datetime import datetime


def open_youtube():
    webbrowser.open("https://www.youtube.com")
    return "Opening YouTube"


def open_google():
    webbrowser.open("https://www.google.com")
    return "Opening Google"


def open_vs_code():
    os.system("code")
    return "Opening VS Code"


def open_notepad():
    os.system("notepad")
    return "Opening Notepad"


def get_time():
    current_time = datetime.now().strftime("%I:%M %p")
    return f"The current time is {current_time}"


# Command Registry
COMMANDS = {
    "youtube": open_youtube,
    "google": open_google,
    "vs code": open_vs_code,
    "vscode": open_vs_code,
    "notepad": open_notepad,
    "time": get_time
}