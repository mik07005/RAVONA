import cv2

from modules.gesture.hand_detector import HandDetector


cap = cv2.VideoCapture(0)

detector = HandDetector()


while True:

    success, frame = cap.read()

    if not success:
        break

    frame, landmarks = detector.detect_hands(
        frame
    )

    fingers = detector.fingers_up(
        landmarks
    )

    count = sum(fingers)

    cv2.putText(
        frame,
        f"Fingers: {count}",
        (20, 60),
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