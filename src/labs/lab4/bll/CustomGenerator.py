from labs.lab4.bll.base_font import base_font
from shared.classes.ascii_generator import AsciiGenerator


class CustomGenerator(AsciiGenerator):
    """
    Class representing a custom ASCII generator.

    class CustomGenerator(AsciiGenerator):

    Attributes:
        name_font (dict): A copy of the base font with some modifications.
        fonts (dict): A dictionary of fonts, including the base font and the modified name font.

    Methods:
        generate(cls, data, font='cap_font', width=80):
            Generates ASCII art from the given data using the specified font.

        string_replace(cls, string, replace_string):
            Replaces all non-space and non-newline characters in the string with characters from the replace_string.

        is_font_break_lines(cls, font):
            Determines if the specified font breaks lines.

        get_fonts(cls):
            Returns a list of available font names.

        get_font(cls, font_name):
            Retrieves the font dictionary for the specified font name. Raises a ValueError if the font is not found.

        get_font_char_height(cls, font_name):
            Retrieves the character height of the specified font.

        get_font_char_width(cls, font_name):
            Retrieves the character width of the specified font.
    """

    name_font = base_font.copy()
    name_font["replace_string"] = "oleh"
    fonts = {"cap": base_font, "oleh_cap": name_font}

    @classmethod
    def generate(cls, data, font="cap_font", width=80):
        char_width = cls.get_font_char_width(font)
        char_height = cls.get_font_char_height(font)
        chars_in_line = width // char_width
        line_result = []
        font_data = cls.get_font(font)

        for i in range(0, len(data), chars_in_line):
            line = data[i : i + chars_in_line].lower()
            for row in range(char_height):
                rows_result = []
                for char in line:
                    if char in font_data["symbols"]:
                        ascii_char = font_data["symbols"][char]
                        rows_result.append(ascii_char[row])
                    else:
                        rows_result.append(" " * char_width)
                line_result.append("".join(rows_result))

        result = "\n".join(line_result)
        if "replace_string" in font_data:
            replace_string = font_data["replace_string"]
            result = cls.string_replace(result, replace_string)
        return result

    @classmethod
    def string_replace(cls, string, replace_string):
        result = []
        replace_len = len(replace_string)
        replace_index = 0
        for char in string:
            if char == " " or char == "\n":
                result.append(char)
            else:
                if replace_index >= replace_len:
                    replace_index = 0
                replace_char = replace_string[replace_index]
                replace_index += 1
                result.append(replace_char)

        return "".join(result)

    @classmethod
    def is_font_break_lines(cls, font):
        font = cls.get_font(font)
        return font.get("is_break_lines", False)

    @classmethod
    def get_fonts(cls):
        return list(cls.fonts.keys())

    @classmethod
    def get_font(cls, font_name):
        if font_name not in cls.fonts:
            raise ValueError(f"Font '{font_name}' not found.")
        return cls.fonts[font_name]

    @classmethod
    def get_font_char_height(cls, font_name):
        font = cls.get_font(font_name)
        return font["height"]

    @classmethod
    def get_font_char_width(cls, font_name):
        font = cls.get_font(font_name)
        return font["width"]
