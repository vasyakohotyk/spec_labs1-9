from labs.lab1.dal.logger import log_error


def get_formatted_float(value, decimals, log_file):
    """
    Round float to the specified number of decimal places.
    :param value: The value to be formatted.
    :param decimals: The number of decimal places to format the value to.
    :param log_file: The file where error logs should be recorded.
    :return: The formatted float as a string, or the original value if a ValueError occurs.
    """
    try:
        value = float(value)
        format = "{0:." + str(decimals) + "f}"
        return format.format(value)
    except ValueError as e:
        log_error(
            f"Неправильний тип значень {value} або {decimals}, повідомлення {e}",
            log_file,
        )
        return value
