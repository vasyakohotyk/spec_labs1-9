from colorama import Fore, Style

from shared.interfaces.paint_text_interface import PaintTextInterface


class ColoramaPainter(PaintTextInterface):
    """
    ColoramaPainter is a class that implements the PaintTextInterface. It provides text painting capabilities using color codes from the `colorama` library.

    Attributes:
    -----------
    color_map : dict
        A mapping between color names (as keys) and their corresponding `colorama` color codes (as values).

    Methods:
    --------
    paint(cls, text, color):
        Paints the given text with the specified color if it's supported.

    get_colors(cls):
        Returns a list of all supported colors.
    """

    color_map = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
        "light_gray": "\x1b[37m",
        "dark_gray": "\x1b[90m",
        "black": Fore.BLACK,
        "default": Style.RESET_ALL,
    }

    @classmethod
    def paint(cls, text, color):
        if color in cls.color_map:
            return f"{cls.color_map[color]}{text}{Style.RESET_ALL}"
        else:
            raise ValueError(f"Color '{color}' is not supported.")

    @classmethod
    def get_colors(cls):
        return list(cls.color_map.keys())
