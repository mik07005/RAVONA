import cv2

from modules.gesture.hand_detector import HandDetector
from modules.gesture.swipe_detector import SwipeDetector

from modules.gesture.gesture_actions import (
    previous_window,
    next_window
)


cap = cv2.VideoCapture(0)

detector = HandDetector()

gesture_detector = SwipeDetector()

gesture_text = ""


while True:

    success, frame = cap.read()

    if not success:
        break

    frame, hands = detector.detect_hands(frame)

    for hand in hands:

        landmarks = hand["landmarks"]

        if len(landmarks) > 12:

            index_x = landmarks[8][1]
            index_y = landmarks[8][2]

            middle_x = landmarks[12][1]
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

            gesture = gesture_detector.detect_swipe(
                track_x,
                track_y
            )

            if gesture:

                gesture_text = (
                    f"Swipe {gesture}"
                )

                print(
                    gesture_text
                )

                if gesture == "LEFT":

                    previous_window()

                elif gesture == "RIGHT":

                    next_window()

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
        "AURA X Gesture Test",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()

cv2.destroyAllWindows()