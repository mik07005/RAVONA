import pyautogui


def previous_window():

    pyautogui.hotkey(
        "alt",
        "shift",
        "esc"
    )


def next_window():

    pyautogui.hotkey(
        "alt",
        "esc"
    )


def task_view():

    pyautogui.hotkey(
        "win",
        "tab"
    )