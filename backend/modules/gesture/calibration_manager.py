class CalibrationManager:

    def __init__(self):

        self.is_calibrating = False

        self.step = 0

        self.calibration_data = {
            "calibrated": False,
            "min_x": None,
            "max_x": None,
            "min_y": None,
            "max_y": None
        }

    def start(self):

        self.is_calibrating = True
        self.step = 1


    def stop(self):

        self.is_calibrating = False
        self.step = 0


    def is_active(self):

        return self.is_calibrating