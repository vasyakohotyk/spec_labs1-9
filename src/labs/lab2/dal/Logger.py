from datetime import datetime
from os import makedirs
from os.path import dirname, exists


class Logger:
    """
    Logger class

    Provides logging functionality to either a file, console, or both.

    Methods:

        __init__(file_path=None, is_write_to_console=True)
            Initializes Logger. Optionally sets file path and console logging.

        console_only()
            Class method. Initializes Logger to log only to the console.

        file_only(file_path)
            Class method. Initializes Logger to log only to a specified file.

        console_and_file(file_path)
            Class method. Initializes Logger to log to both console and file.

        log_error(message, error_level="ERROR")
            Logs an error message with specified error level. Logs to console and/or file based on Logger settings.

        _ensure_file_exists(file_path)
            Ensures the specified file exists, creating it if necessary. Handles potential file creation errors.

        _write_to_file(message)
            Writes a message to the configured log file. Handles potential file writing errors.
    """

    def __init__(self, file_path=None, is_write_to_console=True):

        if not file_path is None:
            self._ensure_file_exists(file_path)
            self.is_write_to_file = False
        else:
            self.file_path = file_path
            self.is_write_to_file = True
        self.is_write_to_console = is_write_to_console

    @classmethod
    def console_only(cls):
        return cls()

    @classmethod
    def file_only(self, file_path):
        return self(file_path, False)

    @classmethod
    def console_and_file(self, file_path):
        return self(file_path)

    def log_error(self, message, error_level="ERROR"):
        error_message = f"{str(datetime.now())} - {message}"
        if self.is_write_to_console:
            print(f"{error_level}: {message}")
        if self.is_write_to_file:
            self._write_to_file(error_message)

    def _ensure_file_exists(self, file_path):
        try:
            if exists(file_path):
                return
            makedirs(dirname(file_path), exist_ok=True)
            with open(file_path, "w") as file:
                return
        except (OSError, PermissionError) as e:
            raise f"Error occurred while creating the file or directories: {e}"

    def _write_to_file(self, message):
        try:
            with open(self.file_path, "a", encoding="utf-8") as file:
                file.write(f"{message}\n")
        except Exception as e:
            print(f"Problem writing to file: {e}")
