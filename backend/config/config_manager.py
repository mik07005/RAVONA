import json
import os


class ConfigManager:

    def __init__(self):

        self.config_dir = "config"

        self.create_config_directory()


    def create_config_directory(self):

        if not os.path.exists(self.config_dir):

            os.makedirs(self.config_dir)


    def get_file_path(self, filename):

        return os.path.join(
            self.config_dir,
            filename
        )

    def save_json(self, filename, data):

        file_path = self.get_file_path(filename)

        with open(file_path, "w") as file:

            json.dump(data, file, indent=4)

    def load_json(self, filename, default_data):

        file_path = self.get_file_path(filename)

        if not os.path.exists(file_path):

            self.save_json(
                filename,
                default_data
            )

            return default_data

        with open(file_path, "r") as file:

            return json.load(file)