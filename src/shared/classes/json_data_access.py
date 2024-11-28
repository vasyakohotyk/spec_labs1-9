"""
This module provides the class JsonDataAccess for handling JSON data access with optional caching.
"""

from json import JSONDecodeError
from jsonpickle import decode, encode
from shared.classes.file_data_access import FileDataAccess, T


class JsonDataAccess(FileDataAccess):
    """
    Class for handling JSON data access with optional caching.

    :param file_path: The path to the file storing JSON data. Default is
    "config/app_settings/default.txt".
    :param is_caching: Boolean indicating whether caching is enabled. Default is True.
    """

    def __init__(self, file_path="config/app_settings/default.txt", is_caching=True):
        self.cache = None
        self.is_caching = is_caching
        super().__init__(file_path, False)

    def _can_parse_json(self, is_can_be_empty=False):
        """
        Checks if the JSON file can be parsed successfully.

        :param is_can_be_empty: Flag to allow empty JSON.
        :returns: True if the JSON can be parsed, False otherwise.
        """
        try:
            result = self.get()
            if not is_can_be_empty and result == "":
                return False
            return True
        except JSONDecodeError:
            return False

    def validate_json(self, is_can_be_empty=False):
        """
        Validates the JSON by checking if it can be parsed.

        :param is_can_be_empty: Flag to allow empty JSON.
        :returns: True if the JSON is valid, False otherwise.
        """
        return self._can_parse_json(is_can_be_empty)

    def set(self, data: T):
        """
        Sets the data by encoding it into JSON and caching if enabled.

        :param data: The data to be stored.
        """
        if self.is_caching:
            self.cache = data
        json_data = encode(data)
        super().set(json_data)

    def get(self) -> T:
        """
        Gets the data by decoding the JSON, using the cache if enabled.

        :returns: The data read from the JSON file.
        """
        if self.is_caching:
            return self.cache
        json_data = super().get()
        return decode(json_data)
