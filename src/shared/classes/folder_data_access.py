from pathlib import Path

from shared.classes.key_data_access import KeyDataAccess
from shared.services.file_operations import *


class FolderDataAccess(KeyDataAccess):
    """
    Initializes the FolderDataAccess object with specified folder path,
    whether files should be saved without an extension, and the default
    extension for files.

    Args:
        folder_path (str): The path to the folder where files reside.
        is_without_extension (bool): Whether to save files without extensions.
        extensions (str): Default extension for files if not saving without extension.
    """

    def __init__(
        self, folder_path="assets/", is_without_extension=False, extensions=".txt"
    ):
        self.folder_path = Path(folder_path)
        self.is_without_extension = is_without_extension
        self.extensions = extensions

    def set(self, key, data):
        write_to_file(data, self.full_path(key))

    def get(self, key):
        return load_from_file(self.full_path(key))

    def full_path(self, file_name):
        if self.is_without_extension:
            file_name += self.extensions
        return Path(self.folder_path, file_name)
