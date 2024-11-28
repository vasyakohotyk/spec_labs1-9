"""
Module for file handling operations including ensuring file existence, writing to a file,
and loading from a file. Provides exception handling to log and raise errors with custom
 messages.
"""

import logging
from os import makedirs
from os.path import dirname, exists

logger = logging.getLogger(__name__)
DEFAULT_MODE = "w"


def handle_exception(custom_message, exception):
    """
    Logs the custom error message and the original exception, then raises a new exception.
    
    :param custom_message: Custom error message to be logged and included in the
    raised exception.
    :param exception: Original exception that triggered the error.
    :return: None
    """
    logger.error("%s: %s", custom_message, exception)
    raise RuntimeError(f"{custom_message}: {exception}")


def ensure_file_exists(file_path):
    """
    Checks if a file exists at the specified path. If not, creates the file and any
    necessary directories.
    
    :param file_path: Path of the file to check and create if it doesn't exist. It should
    be a string representing the file system path.
    :return: None. This function does not return any value. It ensures that the specified
    file exists by creating it and its directories if necessary.
    """
    try:
        if not exists(file_path):
            makedirs(dirname(file_path), exist_ok=True)
            with open(file_path, DEFAULT_MODE, encoding="utf-8"):
                pass
    except PermissionError as e:
        handle_exception("Can't create file, not enough permissions", e)
    except OSError as e:
        handle_exception("Error occurred while creating the file or directories", e)
    except (OSError, IOError) as e:
        handle_exception("Unexpected error occurred while creating the file or directories", e)


def write_to_file(data, file_path):
    """
    Writes the provided data to the specified file path.
    Creates the file if it does not exist.

    :param data: The data to be written to the file.
    :param file_path: The path to the file where data will be written.
    :return: None
    """
    try:
        with open(file_path, DEFAULT_MODE, encoding="utf-8") as file:
            file.write(data)
    except (OSError, IOError) as e:
        handle_exception("Error occurred while writing the file", e)


def load_from_file(file_path):
    """
    Loads and returns the content of the specified file as a string.

    :param file_path: The path to the file that needs to be loaded.
    :return: The content of the file as a string if the file is successfully loaded.
    :raises FileNotFoundError: When the specified file does not exist.
    :raises Exception: For any other exceptions that might occur during file reading.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as e:
        handle_exception("Can't load from file, file not found", e)
    except (OSError, IOError) as e:
        handle_exception("Can't load from file", e)
    return None
