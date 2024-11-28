from pyfiglet import FigletFont, figlet_format

from shared.classes.ascii_generator import AsciiGenerator


class PyfigletGenerator(AsciiGenerator):
    """
    PyfigletGenerator class for generating ASCII art using the pyfiglet library.

    Methods
    -------
    generate(data, **kwargs):
        Generate ASCII art for the given data using specified fonts and settings.

    is_font_break_lines(cls, font):
        Determines if a given font will break lines for texts that are too wide.

    get_fonts():
        Retrieves a list of available fonts in the pyfiglet library.

    get_font_char_height(cls, font_name):
        Returns the height of characters for the specified font.

    get_font_char_width(cls, font_name):
        Returns the width of characters for the specified font.
    """

    @staticmethod
    def generate(data, **kwargs):

        return figlet_format(data, **kwargs)

    @classmethod
    def is_font_break_lines(cls, font):
        test_line = "testlineforlinebreakingtomuchtofitinsinglelinethatforshure"
        kwargs = {"font": font, "width": 50}
        art = cls.generate(test_line, **kwargs)
        font_height = cls.get_font_char_height(font)
        rows_amound = len(art.splitlines())
        if rows_amound > font_height:
            return True
        else:
            return False

    @staticmethod
    def get_fonts():
        return FigletFont.getFonts()

    @classmethod
    def get_font_char_height(cls, font_name):
        try:
            font_data = FigletFont.preloadFont(font_name)
            header_line = font_data.splitlines()[0]
            header_parts = header_line.split()
            header_height = int(header_parts[2])
        except Exception as e:
            print(f"Error retrieving font height: {e}")
            return None
        highest_symbols = "ILQWIONCZ"
        kwargs = {"font": font_name}
        max_height = max(
            len(cls.generate(char, **kwargs).splitlines()) for char in highest_symbols
        )
        return max(header_height, max_height)

    @classmethod
    def get_font_char_width(cls, font_name):
        widest_symbols = "mwGMW"
        kwargs = {"font": font_name}
        max_width = max(
            len(cls.generate(char, **kwargs).splitlines()[0]) for char in widest_symbols
        )
        return max_width
