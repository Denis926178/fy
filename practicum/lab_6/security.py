import os
import json

CONFIG_FILE = "config/config.json"

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"working_directory": os.getcwd()}, f)

with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

WORKING_DIR = os.path.abspath(config.get("working_directory", os.getcwd()))

class SecurityManager:
    @staticmethod
    def __is_safe_path(path):
        abs_path = os.path.abspath(path)
        return abs_path.startswith(WORKING_DIR)

    @staticmethod
    def get_absolute_path(path):
        if (SecurityManager.__is_safe_path(path)):
            return os.path.abspath(path)
        else:
            raise ValueError("Попытка выйти за пределы рабочей директории!")

    @staticmethod
    def start_path():
        return WORKING_DIR
