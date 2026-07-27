import pyautogui


class CursorController:

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()

    def move_cursor(self, landmarks):

        index_tip = landmarks[8]

        x = index_tip[1]
        y = index_tip[2]

        print(f"Cursor: ({x}, {y})")