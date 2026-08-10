import pyautogui
from config.config_manager import ConfigManager
from modules.gesture.calibration_manager import CalibrationManager
class CursorController:

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        
        self.prev_x = 0
        self.prev_y = 0

        self.smoothing = 0.2
        self.margin_ratio = 0.25

        # -------- Cursor Calibration --------
        self.calibrated = False

        self.min_x = None
        self.max_x = None

        self.min_y = None
        self.max_y = None

        self.config = ConfigManager()
        self.calibration = CalibrationManager()

        self.load_calibration()

    def load_calibration(self):

        data = self.calibration.calibration_data

        if not data.get("calibrated", False):
            return

        self.calibrated = True

        self.min_x = data["min_x"]
        self.max_x = data["max_x"]

        self.min_y = data["min_y"]
        self.max_y = data["max_y"]

        print("Cursor calibration loaded")
        print(
            f"X: {self.min_x} -> {self.max_x}"
        )
        print(
            f"Y: {self.min_y} -> {self.max_y}"
        )

        
    def move_cursor(self, landmarks, frame):

        if self.calibration.is_active():
            return

        frame_height, frame_width = frame.shape[:2]

        index_tip = landmarks[8]

        camera_x = index_tip[1]
        camera_y = index_tip[2]

        # Mirror X because webcam is mirrored
        camera_x = frame_width - camera_x

        print(
            f"Raw: ({camera_x}, {camera_y})",
            end="\r"
        )

        # --------------------------------
        # CALIBRATED CURSOR MAPPING
        # --------------------------------

        if self.calibrated:

            left_x = min(self.min_x, self.max_x)
            right_x = max(self.min_x, self.max_x)

            top_y = min(self.min_y, self.max_y)
            bottom_y = max(self.min_y, self.max_y)

            # Keep finger inside calibrated region
            camera_x = max(
                left_x,
                min(camera_x, right_x)
            )

            camera_y = max(
                top_y,
                min(camera_y, bottom_y)
            )

            # Map calibrated camera coordinates
            # to the complete screen
            screen_x = int(
                (camera_x - left_x)
                * self.screen_width
                / (right_x - left_x)
            )

            screen_y = int(
                (camera_y - top_y)
                * self.screen_height
                / (bottom_y - top_y)
            )

        # --------------------------------
        # OLD FALLBACK MAPPING
        # --------------------------------

        else:

            margin_x, margin_y, _, _ = self.get_active_region(frame)

            camera_x = max(
                margin_x,
                min(camera_x, frame_width - margin_x)
            )

            camera_y = max(
                margin_y,
                min(camera_y, frame_height - margin_y)
            )

            screen_x = int(
                (camera_x - margin_x)
                * self.screen_width
                / (frame_width - 2 * margin_x)
            )

            screen_y = int(
                (camera_y - margin_y)
                * self.screen_height
                / (frame_height - 2 * margin_y)
            )

        # --------------------------------
        # SCREEN BOUNDS
        # --------------------------------

        screen_x = max(
            0,
            min(screen_x, self.screen_width - 1)
        )

        screen_y = max(
            0,
            min(screen_y, self.screen_height - 1)
        )

        # --------------------------------
        # SMOOTHING
        # --------------------------------

        smooth_x = (
            self.prev_x
            + (screen_x - self.prev_x)
            * self.smoothing
        )

        smooth_y = (
            self.prev_y
            + (screen_y - self.prev_y)
            * self.smoothing
        )

        self.prev_x = smooth_x
        self.prev_y = smooth_y

        pyautogui.moveTo(
            int(smooth_x),
            int(smooth_y)
        )

    def get_active_region(self, frame):

        frame_height, frame_width = frame.shape[:2]

        margin_x = int(frame_width * self.margin_ratio)
        margin_y = int(frame_height * self.margin_ratio)

        return (
            margin_x,
            margin_y,
            frame_width,
            frame_height
        )