import logging

from shared.classes.dict_json import DictJsonDataAccess

logger = logging.getLogger(__name__)


class SettingsModel:
    """
    SettingsModel class manages application settings stored in a JSON file.

    Methods:

        __init__(path)
            Initializes the SettingsModel with the path to the JSON file.
            Validates if the settings file is not empty or non-existent.

        get_docs_dir()
            Retrieves the directory path where documents are saved.

        get_logger_path()
            Retrieves the path of the logger configuration file.
    """

    def __init__(self, path):
        self.__settings = DictJsonDataAccess(path)
        if not self.__settings.validate(is_can_be_empty=False):
            raise KeyError("Settings empty or doesn't exist")

    def get_docs_dir(self):
        return self.__settings.get("docs_save_dir")

    def get_logger_path(self):
        return self.__settings.get("logger_path")
