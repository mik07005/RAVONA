import cv2
import time

from modules.gesture.swipe_detector import SwipeDetector
from modules.gesture.open_palm_detector import OpenPalmDetector
from modules.gesture.collapse_detector import CollapseDetector
from modules.gesture.cursor_detector import CursorDetector
from modules.gesture.mode_manager import ModeManager

from modules.gesture.gesture_actions import (
    next_window,
    previous_window,
    task_view
)


class GestureEngine:

    def __init__(self, detector, manager):

        self.detector = detector

        self.gesture_detector = SwipeDetector()

        self.palm_detector = OpenPalmDetector()

        self.collapse_detector = CollapseDetector()

        self.cursor_detector = CursorDetector()

        self.manager = manager

        self.gesture_text = ""

        self.last_gesture_time = 0

        self.GESTURE_COOLDOWN = 1.0


    def process(self, frame, hands, current_time):

        

        for hand in hands:

            landmarks = hand["landmarks"]

            fingers = self.detector.fingers_up(hand)

            self.handle_open_palm(fingers)
            self.handle_cursor_mode(fingers)
            self.handle_navigation(
                frame,
                landmarks,
                current_time
            )

    def handle_open_palm(self, fingers):

        if self.palm_detector.is_open_palm(fingers):

            if self.manager.palm_timer is None:

                self.manager.palm_timer = time.time()

            elif (
                time.time() - self.manager.palm_timer
            ) > 0.5 and self.manager.is_idle():

                self.manager.enter_navigation()

                self.gesture_text = "Navigation Mode"

                print("Navigation Mode Activated")

        else:

            self.manager.reset_palm_timer()


    def handle_cursor_mode(self, fingers):

        if self.cursor_detector.is_cursor_gesture(fingers):

            if not self.manager.cursor_lock:

                if self.manager.cursor_timer is None:
                    self.manager.cursor_timer = time.time()

                elif (time.time() - self.manager.cursor_timer) > 0.5:

                    if self.manager.is_cursor():
                        self.manager.enter_idle()
                        self.gesture_text = "Cursor Mode OFF"
                        print("Cursor Mode Deactivated")

                    else:
                        self.manager.enter_cursor()
                        self.gesture_text = "Cursor Mode"
                        print("Cursor Mode Activated")

                    self.manager.lock_cursor()

        else:

            self.manager.reset_cursor_timer()
            self.manager.unlock_cursor()

    def calculate_tracking_point(self, landmarks):

        if len(landmarks) <= 12:
            return None

        index_x = landmarks[8][1]
        middle_x = landmarks[12][1]

        index_y = landmarks[8][2]
        middle_y = landmarks[12][2]

        track_x = (index_x + middle_x) // 2
        track_y = (index_y + middle_y) // 2

        return track_x, track_y

    def check_swipe(self, track_x, track_y, current_time):

        if self.gesture_detector.start_x is None:

            self.gesture_detector.arm(
                track_x,
                track_y
            )

        gesture = self.gesture_detector.detect_swipe(
            track_x,
            track_y
        )

        if not gesture:
            return

        self.gesture_text = gesture.replace("_", " ")

        print(self.gesture_text)

        if gesture == "NEXT_WINDOW":
            next_window()

        elif gesture == "PREVIOUS_WINDOW":
            previous_window()

        self.manager.enter_idle()

        self.gesture_detector.start_x = None

        self.last_gesture_time = current_time

    def handle_navigation(
        self,
        frame,
        landmarks,
        current_time
    ):
        tracking_point = self.calculate_tracking_point(landmarks)

        if tracking_point is None:
            return

        track_x, track_y = tracking_point

        cv2.circle(
            frame,
            (track_x, track_y),
            10,
            (255, 0, 255),
            cv2.FILLED
        )
        if not self.manager.is_navigation():
            return

        if (current_time - self.last_gesture_time) < self.GESTURE_COOLDOWN:
            return
        
        self.check_swipe(
            track_x,
            track_y,
            current_time
        )
        