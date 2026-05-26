from ai.ai_brain import generate_response

from modules.automation.system_control import (
    open_youtube,
    open_google,
    open_vs_code,
    open_notepad,
    get_time
)


def process_input(user_input):

    command = user_input.lower()

    # Automation Commands
    if "open youtube" in command:
        return open_youtube()

    elif "open google" in command:
        return open_google()

    elif "open vs code" in command:
        return open_vs_code()

    elif "open notepad" in command:
        return open_notepad()

    elif "time" in command:
        return get_time()

    # AI Response
    else:
        return generate_response(user_input)