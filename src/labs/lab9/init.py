import logging

from config.settings_paths import settings_path_lab9
from labs.lab9.bll.Controller import Controller
from labs.lab9.dal.SettingsModel import SettingsModel
from labs.lab9.ui.UserInterface import UserInterface
from shared.services.relative_to_absolute_path import absolute


def set_up_logging(file_path):
    """
    :param file_path: The path to the log file where log messages will be recorded.
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
    Initializes the main application components, including settings, controller, logger, and user interface.

    :return: None
    """
    settings = SettingsModel(settings_path_lab9)
    controller = Controller(settings)
    logger_path = controller.get_logger_path()
    set_up_logging(logger_path)
    user_interface = UserInterface(controller)
    user_interface.show()


if __name__ == "__main__":
    main()
