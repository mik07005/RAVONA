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


    def process(self, frame, hands):

        current_time = time.time()

        for hand in hands:

            landmarks = hand["landmarks"]

            fingers = self.detector.fingers_up(hand)

            self.handle_open_palm(fingers)
            self.handle_cursor_mode(fingers)

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