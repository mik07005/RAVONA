import cv2
import mediapipe as mp


class HandDetector:

    def __init__(self):

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.mp_draw = mp.solutions.drawing_utils

    def detect_hands(self, frame):

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        self.results = self.hands.process(rgb)

        all_hands = []

        if self.results.multi_hand_landmarks:

            for hand_index, hand_landmarks in enumerate(
                self.results.multi_hand_landmarks
            ):

                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

                hand_type = (
                    self.results.multi_handedness[
                        hand_index
                    ]
                    .classification[0]
                    .label
                )

                # Webcam mirrored
                if hand_type == "Right":
                    hand_type = "Left"
                else:
                    hand_type = "Right"

                h, w, c = frame.shape

                hand_landmarks_list = []

                for idx, lm in enumerate(
                    hand_landmarks.landmark
                ):

                    cx = int(lm.x * w)
                    cy = int(lm.y * h)
                    cz = lm.z

                    hand_landmarks_list.append(
                        [idx, cx, cy, cz]
                    )

                hand_data = {
                    "type": hand_type,
                    "landmarks": hand_landmarks_list
                }

                all_hands.append(hand_data)

        return frame, all_hands

    def fingers_up(self, hand):

        landmarks = hand["landmarks"]
        hand_type = hand["type"]

        if not landmarks:
            return []

        fingers = []

        thumb_tip_x = landmarks[4][1]
        index_mcp_x = landmarks[5][1]

        if hand_type == "Right":

            fingers.append(
                1 if thumb_tip_x < index_mcp_x
                else 0
            )

        else:

            fingers.append(
                1 if thumb_tip_x > index_mcp_x
                else 0
            )

        fingers.append(
            1 if landmarks[8][2]
            < landmarks[6][2]
            else 0
        )

        fingers.append(
            1 if landmarks[12][2]
            < landmarks[10][2]
            else 0
        )

        fingers.append(
            1 if landmarks[16][2]
            < landmarks[14][2]
            else 0
        )

        fingers.append(
            1 if landmarks[20][2]
            < landmarks[18][2]
            else 0
        )

        return fingers