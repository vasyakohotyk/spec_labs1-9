from datetime import datetime


def log_error(message, log_file):
    """
    Writes to file error message and to console.
    :param message: The error message to be logged.
    :param log_file: The file where the error message will be logged.
    :return: None
    """
    error_message = f"{str(datetime.now())} - {message}"
    print(f"Помилка: {message}")
    write_to_file(error_message, log_file)


def write_to_file(message, filepath):
    """
    Function that write to file message.
    :param message: The message string to be written to the file.
    :param filepath: The path to the file where the message will be written.
    :return: None
    """
    try:
        with open(filepath, "a", encoding="utf-8") as file:
            file.write(f"{message}\n")
    except Exception as e:
        print(f"Проблема запису у файл: {e}")
