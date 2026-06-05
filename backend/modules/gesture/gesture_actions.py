import pyautogui


def next_window():

    pyautogui.hotkey(
        "alt",
        "tab"
    )


def previous_window():

    pyautogui.hotkey(
        "alt",
        "shift",
        "tab"
    )


def task_view():

    pyautogui.hotkey(
        "win",
        "tab"
    )