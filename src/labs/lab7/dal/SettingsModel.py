import logging

from shared.classes.dict_json import DictJsonDataAccess

logger = logging.getLogger(__name__)


class SettingsModel:
    """
    SettingsModel

    This class provides a model for accessing various user settings stored in a JSON file.
    The settings are accessed through a data access layer, and the class offers multiple
    methods to fetch specific settings.

    Methods
    -------
    __init__(path):
        Initializes the SettingsModel with the given path to the JSON file.
        Raises an exception if the settings file is empty or doesn't exist.

    get_fields():
        Returns the 'fields' setting from the JSON file.

    get_fields_keys():
        Returns a list of keys from the 'fields' setting.

    get_user_settings_path():
        Returns the 'user_settings_path' setting from the JSON file.

    get_history_path():
        Returns the 'history_path' setting from the JSON file.

    get_languages():
        Returns the 'languages' setting from the JSON file.

    get_max_results():
        Returns the 'max_results' setting from the JSON file.

    get_default_save_dir():
        Returns the 'default_save_dir' setting from the JSON file.

    get_default_file_name():
        Returns the 'default_file_name' setting from the JSON file.

    get_results_to_save():
        Returns the 'results_to_save' setting from the JSON file.

    get_colors():
        Returns the 'colors' setting from the JSON file.

    get_attributes():
        Returns the 'attributes' setting from the JSON file.

    get_logger_path():
        Returns the 'logger_path' setting from the JSON file.
    """

    def __init__(self, path):
        self.__settings = DictJsonDataAccess(path)
        if not self.__settings.validate(is_can_be_empty=False):
            logger.critical("There no history file")
            raise KeyError("Settings empty or doesn't exist")

    def get_fields(self):
        return self.__settings.get("fields")

    def get_fields_keys(self):
        keys = list(self.get_fields().keys())
        return keys

    def get_user_settings_path(self):
        return self.__settings.get("user_settings_path")

    def get_history_path(self):
        return self.__settings.get("history_path")

    def get_languages(self):
        return self.__settings.get("languages")

    def get_max_results(self):
        return self.__settings.get("max_results")

    def get_default_save_dir(self):
        return self.__settings.get("default_save_dir")

    def get_default_file_name(self):
        return self.__settings.get("default_file_name")

    def get_results_to_save(self):
        return self.__settings.get("results_to_save")

    def get_colors(self):
        return self.__settings.get("colors")

    def get_attributes(self):
        return self.__settings.get("attributes")

    def get_logger_path(self):
        return self.__settings.get("logger_path")
