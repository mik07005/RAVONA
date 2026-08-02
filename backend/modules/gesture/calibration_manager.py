from config.config_manager import ConfigManager
class CalibrationManager:

    def __init__(self):

        self.is_calibrating = False

        self.step = 0

        self.config = ConfigManager()

        self.current_x = None
        self.current_y = None

        self.default_data = {
            "calibrated": False,
            "min_x": None,
            "max_x": None,
            "min_y": None,
            "max_y": None
        }

        self.calibration_data = self.config.load_json(
            "cursor_calibration.json",
            self.default_data
        )

        self.current_corner = 0

        self.corner_names = [
            "TOP LEFT",
            "TOP RIGHT",
            "BOTTOM LEFT",
            "BOTTOM RIGHT"
        ]

        self.corner_keys = [
            ("min_x", "min_y"),
            ("max_x", "min_y"),
            ("min_x", "max_y"),
            ("max_x", "max_y")
        ]
        
    def start(self):

        self.is_calibrating = True

        self.step = 1

        self.calibration_data = self.default_data.copy()

        print("Calibration Started")


    def save_current_point(self, x, y):

        key_x, key_y = self.corner_keys[self.current_corner]

        self.calibration_data[key_x] = x
        self.calibration_data[key_y] = y

        print(
            f"Saved {self.corner_names[self.current_corner]} : ({x}, {y})"
        )

        self.current_corner += 1
    
    def stop(self):

        self.is_calibrating = False
        self.step = 0


    def is_active(self):

        return self.is_calibrating