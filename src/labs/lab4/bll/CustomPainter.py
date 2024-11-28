from shared.interfaces.paint_text_interface import PaintTextInterface


class CustomPainter(PaintTextInterface):
    """
    CustomPainter class inheriting from PaintTextInterface

    This class provides methods to paint text with different colors and to retrieve the list of supported colors.

    color_map:
        A dictionary mapping color names to their respective ANSI escape codes.

    Methods:
        paint(cls, text, color):
            Paints the given text with the specified color using ANSI escape codes.

            Parameters:
                text (str): The text to be painted.
                color (str): The color in which to paint the text. Must be one of the keys in the color_map dictionary.

            Returns:
                str: The painted text with ANSI escape codes.

            Raises:
                ValueError: If the specified color is not supported.

        get_colors(cls):
            Retrieves the list of supported colors.

            Returns:
                list: A list of color names supported by the CustomPainter class.
    """

    color_map = {
        "red": "\x1b[31m",
        "green": "\x1b[32m",
        "yellow": "\x1b[33m",
        "blue": "\x1b[34m",
        "magenta": "\x1b[35m",
        "cyan": "\x1b[36m",
        "white": "\x1b[97m",
        "light_gray": "\x1b[37m",
        "dark_gray": "\x1b[90m",
        "black": "\x1b[30m",
        "default": "\x1b[0m",
    }

    @classmethod
    def paint(cls, text, color):
        if color in cls.color_map:
            start_color = cls.color_map[color]
            end_color = cls.color_map["default"]
            return f"{start_color}{text}{end_color}"
        else:
            raise ValueError(f"Color '{color}' is not supported.")

    @classmethod
    def get_colors(cls):
        return list(cls.color_map.keys())
