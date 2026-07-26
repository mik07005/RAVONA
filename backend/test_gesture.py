import cv2
import time

from modules.gesture.hand_detector import HandDetector
from modules.gesture.mode_manager import ModeManager
from modules.gesture.gesture_engine import GestureEngine

cap = cv2.VideoCapture(0)

detector = HandDetector()


manager = ModeManager()

engine = GestureEngine(detector, manager)


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

    if engine.gesture_text:

        cv2.putText(
            frame,
            engine.gesture_text,
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
