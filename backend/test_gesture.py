# NOTE:
# This is a corrected TEMPLATE of test_gesture.py showing the
# proper placement of Cursor Mode logic.
# Cursor movement is intentionally NOT implemented yet.

import cv2
import time

from modules.gesture.hand_detector import HandDetector
from modules.gesture.swipe_detector import SwipeDetector
from modules.gesture.open_palm_detector import OpenPalmDetector
from modules.gesture.collapse_detector import CollapseDetector
from modules.gesture.cursor_detector import CursorDetector
from modules.gesture.mode_manager import ModeManager
from modules.gesture.gesture_engine import GestureEngine
from modules.gesture.gesture_actions import (
    next_window,
    previous_window,
    task_view
)

cap = cv2.VideoCapture(0)

detector = HandDetector()

gesture_detector = SwipeDetector()

palm_detector = OpenPalmDetector()

collapse_detector = CollapseDetector()

cursor_detector = CursorDetector()

manager = ModeManager()

engine = GestureEngine(detector, manager)

gesture_text = ""

last_gesture_time = 0

GESTURE_COOLDOWN = 1.0

while True:

    success, frame = cap.read()

    if not success:
        break

    current_time = time.time()

    frame, hands = detector.detect_hands(frame)

    engine.process(
        frame,
        hands,
        current_time
    )

    for hand in hands:

        landmarks = hand["landmarks"]
        fingers = detector.fingers_up(hand)

        

        

        

        if manager.is_navigation():

                if (
                    current_time - last_gesture_time
                ) < GESTURE_COOLDOWN:
                    continue

                if collapse_detector.is_collapsed(
                    landmarks
                ):

                    if manager.collapse_timer is None:
                        manager.collapse_timer = time.time()

                    elif (
                        time.time() - manager.collapse_timer
                    ) > 0.5:

                        gesture_text = "TASK VIEW"
                        print("TASK VIEW")

                        task_view()

                        manager.enter_idle()
                        gesture_detector.start_x = None
                        manager.reset_collapse_timer()
                        last_gesture_time = time.time()

                        continue

                else:
                    manager.reset_collapse_timer()

                

        cv2.putText(
            frame,
            f"Navigation: {manager.is_navigation()}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"Cursor: {manager.is_cursor()}",
            (20,70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,0),
            2
        )

    if gesture_text:

        cv2.putText(
            frame,
            gesture_text,
            (20,110),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )

    cv2.imshow("NOVA Gesture Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
