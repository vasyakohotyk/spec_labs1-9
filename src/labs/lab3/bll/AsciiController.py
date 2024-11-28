from shared.classes.ascii_generator import AsciiGenerator
from shared.classes.key_data_access import KeyDataAccess
from shared.interfaces.paint_text_interface import PaintTextInterface


class AsciiController:
    """
    AsciiController is responsible for managing ASCII art generation settings and processes.
    It interacts with the ASCII art generator, coloring interface, and settings storage.

    :param generator: Object responsible for generating ASCII art.
    :type generator: AsciiGenerator
    :param coloring: Interface for coloring ASCII art text.
    :type coloring: PaintTextInterface
    :param arts_access: Access interface for art storage.
    :type arts_access: KeyDataAccess
    :param settings_access: Access interface for settings storage.
    :type settings_access: KeyDataAccess
    """

    def __init__(
        self,
        generator: AsciiGenerator,
        coloring: PaintTextInterface,
        arts_access: KeyDataAccess,
        settings_access: KeyDataAccess,
    ):
        self._generator = generator
        self._coloring = coloring
        self._arts_access = arts_access
        self._settings = settings_access
        self.art = None

    def get_fonts(self):
        return self._generator.get_fonts()

    def get_font(self):
        return self._settings.get("font")

    def is_font_correct(self):
        current_font = self.get_font()
        fonts = self.get_fonts()
        if current_font in fonts:
            return True
        else:
            return False

    def set_font(self, font):
        if not font in self.get_fonts():
            raise ValueError("Font not in fonts list")
        self._settings.set("font", font)

    def get_bright_symbol(self):
        return self._settings.get("bright_symbol")

    def get_empty_symbol(self):
        return self._settings.get("empty_symbol")

    def set_bright_symbol(self, bright_symbol):
        if len(bright_symbol) != 1:
            raise ValueError("String with wrong lenghts, can't set symbol")
        self._settings.set("bright_symbol", bright_symbol)

    def set_empty_symbol(self, empty_symbol):
        if len(empty_symbol) != 1:
            raise ValueError("String with wrong lenghts, can't set symbol")
        self._settings.set("empty_symbol", empty_symbol)

    def set_is_symbols_replace(self, is_symbols_replace):
        if is_symbols_replace not in [True, False]:
            raise ValueError("Try set non-bool value to using symbols")
        self._settings.set("is_symbols_replace", is_symbols_replace)

    def get_is_symbols_replace(self):
        return self._settings.get("is_symbols_replace")

    def get_colors(self):
        return self._coloring.get_colors()

    def get_color(self):
        return self._settings.get("color")

    def set_color(self, color):
        if not color in self.get_colors():
            raise ValueError("Color not in colors list")
        self._settings.set("color", color)

    def get_min_width(self):
        font = self.get_font()
        return self._generator.get_font_char_width(font)

    def get_min_height(self):
        font = self.get_font()
        return self._generator.get_font_char_height(font)

    def is_font_support_line_break(self):
        font = self.get_font()
        return self._generator.is_font_break_lines(font)

    def get_char_limit(self):
        font_height = self.get_min_height()
        font_width = self.get_min_width()
        height_limit = self.get_height()
        width_limit = self.get_width()
        if font_height > height_limit:
            return 0
        if font_width > width_limit:
            return 0
        symbols_in_row = int(width_limit / font_width)
        is_line_breaks = self.get_is_line_breaks()
        is_font_breaks_line = self.is_font_support_line_break()
        if not is_line_breaks or not is_font_breaks_line:
            return symbols_in_row
        cols = int(height_limit / font_height)
        return symbols_in_row * cols

    def get_max_possible_width(self):
        return self._settings.get("max_width")

    def get_max_possible_height(self):
        return self._settings.get("max_height")

    def get_width(self):
        return self._settings.get("width")

    def get_height(self):
        return self._settings.get("height")

    def set_height(self, height):
        try:
            height = int(height)
        except:
            raise TypeError("Wrong type of width")

        max_height = self.get_max_possible_height()
        min_height = self.get_min_height()
        if not min_height <= height <= max_height:
            raise ValueError("Height not in diapason")
        self._settings.set("height", height)

    def set_width(self, width):
        try:
            width = int(width)
        except:
            raise TypeError("Wrong type of width")

        max_width = self.get_max_possible_width()
        min_width = self.get_min_width()
        if not min_width <= width <= max_width:
            raise ValueError("Width not in diapason")
        self._settings.set("width", width)

    def get_alignment(self):
        return self._settings.get("alignment")

    def set_alignment(self, alignment):
        options = ["left", "right", "center"]
        if alignment not in options:
            raise ValueError("Wrong alignment")
        self._settings.set("alignment", alignment)

    def get_is_line_breaks(self):
        return self._settings.get("is_line_breaks")

    def set_is_line_breaks(self, is_line_breaks):
        if is_line_breaks not in [True, False]:
            raise ValueError("Try set non-bool value to line breaking")
        self._settings.set("is_line_breaks", is_line_breaks)

    def is_line_broken(self, art: str):
        is_symbol_replace = self.get_is_symbols_replace()
        bright_symbol = self.get_bright_symbol() if is_symbol_replace else None
        is_symbol_detected = False
        is_gap_detected = False

        for line in art.splitlines():
            line_has_content = (
                bright_symbol in line if is_symbol_replace else line.strip()
            )

            if line_has_content:
                is_symbol_detected = True
                if is_gap_detected:
                    return True
            else:
                if is_symbol_detected:
                    is_gap_detected = True

        return False

    def is_art_exist(self):
        return bool(self.art)

    def get_art(self):
        return self.art

    def set_art(self, art):
        if not art:
            raise ValueError("No art to set")
        self.art = art

    def save_art(self, name):
        art = self.get_art()
        if not art:
            raise ValueError("No art to save")
        if not self.is_art_allowed(art):
            raise ValueError("Too wide")
        self._arts_access.set(name, art)

    def remove_color(string):
        result = []
        in_ansi_sequence = False
        for char in string:
            if char == "\x1b":
                in_ansi_sequence = True
            elif in_ansi_sequence and char == "m":
                in_ansi_sequence = False
            elif not in_ansi_sequence:
                result.append(char)
        return "".join(result)

    def is_art_allowed(self, art: str):
        lines = art.splitlines()
        if not lines:
            return False
        art_height = len(lines)
        art_weight = len(lines[1])
        height_limit = self.get_height()
        width_limit = self.get_width()
        if art_height > height_limit:
            return False

        if art_weight > width_limit:
            return False
        is_line_breaks = self.get_is_line_breaks()
        if not is_line_breaks:
            is_line_broken = self.is_line_broken(art)
            if is_line_broken:
                return False
        return True

    def generate(self, text, width=None):
        font = self.get_font()
        if width is None:
            width = self.get_width()
        kwargs = {"font": font, "width": width}

        art = self._generator.generate(text, **kwargs)
        return art

    def replace(self, art):
        bright = self.get_bright_symbol()
        empty = self.get_empty_symbol()
        return self._generator.replace(art, bright, empty)

    def paint(self, art):
        color = self.get_color()
        return self._coloring.paint(art, color)

    def cut(self, text, width, height):
        lines = text.split("\n")
        lines = lines[0 : height - 1]
        lines_to_return = []
        for line in lines:
            lines_to_return.append(line[0 : width - 1])
        return "\n".join(lines_to_return)

    def justify(self, text):
        alignment = self.get_alignment()
        width = self.get_width()
        justified_text = self._generator.alignment_text(text, alignment, width)
        return justified_text

    def create_art(self, text):
        art = self.generate(text)
        is_allowed = self.is_art_allowed(art)
        if not is_allowed:
            raise ValueError("Art breaks the rules")
        justified_art = self.justify(art)
        is_replace = self.get_is_symbols_replace()
        if is_replace:
            justified_art = self.replace(justified_art)
        self.set_art(justified_art)
        painted_art = self.paint(justified_art)
        return painted_art

    def create_cut_art(self, text):
        is_line_breaks = self.get_is_line_breaks()
        if not is_line_breaks:
            art = self.generate(text, 999)
        else:
            art = self.generate(text)
        width = self.get_width()
        height = self.get_height()
        cutted_art = self.cut(art, width, height)
        justified_art = self.justify(cutted_art)
        is_replace = self.get_is_symbols_replace()
        if is_replace:
            justified_art = self.replace(justified_art)
        painted_art = self.paint(justified_art)
        return painted_art

    def get_settings_info(self):
        return self._settings.__str__()
