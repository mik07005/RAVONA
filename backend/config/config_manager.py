import json
import os


class ConfigManager:

    def __init__(self):

        self.config_dir = "config"

        self.cursor_file = os.path.join(
            self.config_dir,
            "cursor_calibration.json"
        )

        self.create_config_directory()
        self.create_cursor_config()


    def create_config_directory(self):

        if not os.path.exists(self.config_dir):

            os.makedirs(self.config_dir)



    def create_cursor_config(self):

        if os.path.exists(self.cursor_file):
            return

        default_data = {
            "calibrated": False,
            "min_x": None,
            "max_x": None,
            "min_y": None,
            "max_y": None
        }

        with open(self.cursor_file, "w") as file:

            json.dump(default_data, file, indent=4)