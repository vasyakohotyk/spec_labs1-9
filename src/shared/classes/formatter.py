from builtins import float


class Formatter:
    """
    Class to handle various formatting operations.
    """

    @staticmethod
    def get_formatted_float(value, decimals):
        try:
            value = float(value)
            format = "{0:." + str(decimals) + "f}"
            return format.format(value)
        except ValueError as e:
            return value
