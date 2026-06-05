import cv2
import time

from modules.gesture.hand_detector import HandDetector
from modules.gesture.swipe_detector import SwipeDetector
from modules.gesture.open_palm_detector import OpenPalmDetector
from modules.gesture.collapse_detector import CollapseDetector

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

navigation_mode = False

palm_start_time = None

collapse_start_time = None

gesture_text = ""

# --------------------
# Gesture Cooldown
# --------------------

last_gesture_time = 0

GESTURE_COOLDOWN = 1.0


while True:

    success, frame = cap.read()

    if not success:
        break

    current_time = time.time()

    frame, hands = detector.detect_hands(frame)

    for hand in hands:

        landmarks = hand["landmarks"]

        fingers = detector.fingers_up(
            hand
        )

        # --------------------
        # Open Palm Detection
        # --------------------

        if palm_detector.is_open_palm(
            fingers
        ):

            if palm_start_time is None:

                palm_start_time = time.time()

            elif (
                time.time() - palm_start_time
            ) > 0.5 and not navigation_mode:

                navigation_mode = True

                gesture_text = (
                    "Navigation Mode"
                )

                print(
                    "Navigation Mode Activated"
                )

        else:

            palm_start_time = None

        # --------------------
        # Tracking Point
        # --------------------

        if len(landmarks) > 12:

            index_x = landmarks[8][1]
            middle_x = landmarks[12][1]

            index_y = landmarks[8][2]
            middle_y = landmarks[12][2]

            track_x = (
                index_x + middle_x
            ) // 2

            track_y = (
                index_y + middle_y
            ) // 2

            cv2.circle(
                frame,
                (track_x, track_y),
                10,
                (255, 0, 255),
                cv2.FILLED
            )

            # --------------------
            # Navigation Mode
            # --------------------

            if navigation_mode:

                # --------------------
                # Global Cooldown
                # --------------------

                if (
                    current_time
                    - last_gesture_time
                ) < GESTURE_COOLDOWN:

                    continue

                # --------------------
                # Five Finger Collapse
                # --------------------

                if collapse_detector.is_collapsed(
                    landmarks
                ):

                    if collapse_start_time is None:

                        collapse_start_time = (
                            time.time()
                        )

                    elif (
                        time.time()
                        - collapse_start_time
                    ) > 0.5:

                        gesture_text = (
                            "TASK VIEW"
                        )

                        print(
                            "TASK VIEW"
                        )

                        task_view()

                        navigation_mode = False

                        gesture_detector.start_x = None

                        collapse_start_time = None

                        last_gesture_time = (
                            time.time()
                        )

                        continue

                else:

                    collapse_start_time = None

                # --------------------
                # Arm Swipe Detector
                # --------------------

                if (
                    gesture_detector.start_x
                    is None
                ):

                    gesture_detector.arm(
                        track_x,
                        track_y
                    )

                # --------------------
                # Swipe Detection
                # --------------------

                gesture = (
                    gesture_detector.detect_swipe(
                        track_x,
                        track_y
                    )
                )

                if gesture:

                    gesture_text = (
                        gesture.replace(
                            "_",
                            " "
                        )
                    )

                    print(
                        gesture_text
                    )

                    if gesture == (
                        "NEXT_WINDOW"
                    ):

                        next_window()

                    elif gesture == (
                        "PREVIOUS_WINDOW"
                    ):

                        previous_window()

                    navigation_mode = False

                    gesture_detector.start_x = None

                    collapse_start_time = None

                    last_gesture_time = (
                        time.time()
                    )

        cv2.putText(
            frame,
            f"Navigation: {navigation_mode}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    if gesture_text:

        cv2.putText(
            frame,
            gesture_text,
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "NOVA Gesture Test",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()

cv2.destroyAllWindows()