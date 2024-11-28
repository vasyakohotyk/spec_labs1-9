import logging

from shared.classes.dict_json import DictJsonDataAccess

logger = logging.getLogger(__name__)


class SettingsModel:
    """
    Class SettingsModel provides access to application settings stored in a JSON file.

    Methods
    -------
    __init__(path)
        Initializes the SettingsModel with the path to the settings file.
        Raises a KeyError if the settings file is empty or doesn't exist.

    get_assets_save_dir()
        Returns the directory path where assets should be saved.

    get_activity_file_path()
        Returns the file path for activity data.

    get_sleep_file_path()
        Returns the file path for sleep data.

    get_default_file_name()
        Returns the default file name used in the application.

    get_logger_path()
        Returns the file path for the application logger.
    """

    def __init__(self, path):
        self.__settings = DictJsonDataAccess(path)
        if not self.__settings.validate(is_can_be_empty=False):
            raise KeyError("Settings empty or doesn't exist")

    def get_assets_save_dir(self):
        return self.__settings.get("assets_save_dir")

    def get_activity_file_path(self):
        return self.__settings.get("activity_file_path")

    def get_sleep_file_path(self):
        return self.__settings.get("sleep_file_path")

    def get_default_file_name(self):
        return self.__settings.get("default_file_name")

    def get_logger_path(self):
        return self.__settings.get("logger_path")
