from shared.classes.data_access import DataAccess, T
from shared.services.file_operations import (
    ensure_file_exists,
    load_from_file,
    write_to_file,
)


class FileDataAccess(DataAccess):
    """
    FileDataAccess class provides file-based data access with optional caching.
    Inherits from DataAccess.

    Constructor:
    :param file_path: The path to the file. Default is "assets/2d ascii texts/default.txt".
    :param is_caching: Flag to enable/disable caching. Default is False.
    :raises: Exception if the file does not exist.

    set_file_path:
    Sets the file path for file operations.
    :param file_path: The new path to the file.

    set:
    Writes data to the file and optionally caches it.
    :param data: The data to write.
    :raises: Exception if writing to the file fails.

    get:
    Reads data from the file, using cached data if caching is enabled.
    :returns: Data read from the file.
    :raises: Exception if reading from the file fails.

    set_is_caching:
    Enables or disables caching, and updates the cache if enabling.
    :param is_caching: The new caching state.
    """

    def __init__(self, file_path="assets/2d ascii texts/default.txt", is_caching=False):
        try:
            ensure_file_exists(file_path)
        except Exception as e:
            raise e
        self.__file_path = file_path
        self.is_caching = is_caching
        self.cache = None

    def set_file_path(self, file_path):
        self.__file_path = file_path

    def set(self, data: T):
        if self.is_caching:
            self.cache = data
        try:
            write_to_file(data, self.__file_path)
        except Exception as e:
            raise e

    def get(self) -> T:
        if self.is_caching:
            return self.cache
        try:
            return load_from_file(self.__file_path)
        except Exception as e:
            raise e

    def set_is_caching(self, is_caching):
        if not is_caching:
            self.cache = None
        elif not self.is_caching:
            self.cache = self.get()
        self.is_caching = is_caching
