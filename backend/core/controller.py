from rapidfuzz import fuzz

from ai.ai_brain import generate_response

from modules.automation.system_control import COMMANDS


def detect_command(user_input):

    user_input = user_input.lower()

    best_match = None
    highest_score = 0

    for command in COMMANDS.keys():

        score = fuzz.partial_ratio(user_input, command)

        if score > highest_score:
            highest_score = score
            best_match = command

    # Threshold
    if highest_score >= 70:
        return best_match

    return None


def process_input(user_input):

    detected_command = detect_command(user_input)

    if detected_command:

        action = COMMANDS[detected_command]

        return action()

    return generate_response(user_input)