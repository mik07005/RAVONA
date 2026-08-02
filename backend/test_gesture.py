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

    if engine.gesture_text:

        cv2.putText(
            frame,
            engine.gesture_text,
            (20, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    if engine.cursor_controller.calibration.is_active():

        cv2.putText(
            frame,
            "CALIBRATION MODE",
            (20, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "Move finger to TOP LEFT",
            (20, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

    cv2.imshow("NOVA Gesture Test", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("c"):

        engine.cursor_controller.calibration.start()

    elif key == ord(" "):

        if engine.cursor_controller.calibration.is_active():

            engine.cursor_controller.calibration.save_current_point(
                engine.cursor_controller.calibration.current_x,
                engine.cursor_controller.calibration.current_y
        )

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
