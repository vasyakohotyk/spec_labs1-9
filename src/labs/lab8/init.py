import logging

import pandas as pd

from config.settings_paths import settings_path_lab8
from labs.lab8.bll.Controller import Controller
from labs.lab8.dal.SettingsModel import SettingsModel
from labs.lab8.ui.UserInterface import UserInterface
from shared.services.relative_to_absolute_path import absolute


def set_up_logging(file_path):
    """
    :param file_path: The file path where the log file will be created.
    :return: None
    """
    # Create a file handler
    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(logging.INFO)

    # Create a stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)

    # Set the logging format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Configure the root logger
    logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, stream_handler])


def main():
    """
    Loads settings, activity data, and sleep data from file paths, initializes the controller, sets up logging, and displays the user interface.

    :return: None
    """
    settings = SettingsModel(settings_path_lab8)
    relative_activity_path = settings.get_activity_file_path()
    relative_sleep_path = settings.get_sleep_file_path()
    activity_path = absolute(relative_activity_path)
    sleep_path = absolute(relative_sleep_path)
    activity = pd.read_csv(activity_path)
    sleep = pd.read_csv(sleep_path)
    controller = Controller(settings, activity, sleep)
    logger_path = controller.get_logger_path()
    set_up_logging(logger_path)
    user_interface = UserInterface(controller)
    user_interface.show()


if __name__ == "__main__":
    main()
