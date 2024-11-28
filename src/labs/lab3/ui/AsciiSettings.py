from labs.lab3.bll.AsciiController import AsciiController
from shared.classes.input import (
    BoolInput,
    NumberBetweenInput,
    StringInput,
    VariantsInput,
)
from shared.classes.menu_builder import MenuBuilder


class AsciiSettingsUI:
    """
    AsciiSettingsUI

    This class represents the user interface for ASCII art settings. It is responsible for displaying various settings menus and options to the user and obtaining their input to configure the ASCII art generation.

    Methods
    -------
    __init__(self, controller: AsciiController = None)
        Initializes the AsciiSettingsUI instance with an optional AsciiController instance.

    set_controller(self, controller: AsciiController)
        Sets the AsciiController instance for this UI and rebuilds the main menu.

    show(self)
        Displays the main menu to the user.

    __menu_build(self)
        Builds and configures the main settings menu.

    set_symbols(self)
        Displays the menu for configuring symbol replacements used in ASCII art.

    get_symbols_replacement_info(self)
        Retrieves current symbol replacement settings from the controller.

    set_alignment(self)
        Allows the user to set text alignment for the ASCII art.

    set_bright_symbol(self)
        Allows the user to set the symbol used for bright areas in the ASCII art.

    set_empty_symbol(self)
        Allows the user to set the symbol used for empty areas in the ASCII art.

    set_is_replace_symbols(self)
        Allows the user to enable or disable symbol replacement.

    set_color(self)
        Allows the user to set the color for the ASCII art.

    set_font(self)
        Allows the user to set the font used in the ASCII art.

    set_width(self)
        Allows the user to set the width of the ASCII art.

    set_height(self)
        Allows the user to set the height of the ASCII art.

    set_line_breaking(self)
        Allows the user to enable or disable line breaking (word wrapping) during ASCII art generation.

    see_example(self)
        Provides an example of the current settings applied to a sample text.
    """

    def __init__(self, controller: AsciiController = None):
        self.__controller = controller

    def set_controller(self, controller: AsciiController):
        self.__controller = controller
        self.__menu = self.__menu_build()

    def show(self):
        self.__menu.show()

    def __menu_build(self):
        return (
            MenuBuilder()
            .set_title("Setting for ascii")
            .set_input_text("Choose: ")
            .set_warning("No such setting")
            .set_dynamic_title(self.see_example)
            .add_option("1", "1. Replacing symbols\n", self.set_symbols)
            .add_option("2", "2. Change font\n", self.set_font)
            .add_option("3", "3. Change color\n", self.set_color)
            .add_option("4", "4. Change width\n", self.set_width)
            .add_option("5", "5. Change height\n", self.set_height)
            .add_option("6", "6. Change alignment\n", self.set_alignment)
            .add_option(
                "7", "7. Change line breaking (word wrapping)\n", self.set_line_breaking
            )
            .add_stop_options(["0", "Exit", "exit"], "0. Exit")
            .build()
        )

    def set_symbols(self):
        symbols_menu = (
            MenuBuilder()
            .set_title("Replacing symbols")
            .set_input_text("Choose: ")
            .set_warning("No such setting")
            .set_dynamic_title(self.get_symbols_replacement_info)
            .add_option_without_attributes(
                "1", "1. Set using this symbols\n", self.set_is_replace_symbols
            )
            .add_option_without_attributes(
                "2", "2. Set bright symbols\n", self.set_bright_symbol
            )
            .add_option_without_attributes(
                "3", "3. Set empty symbol\n", self.set_empty_symbol
            )
            .add_stop_options(["0", "Exit", "exit"], "0. Exit")
            .build()
        )
        symbols_menu.show()

    def get_symbols_replacement_info(self):
        bright = self.__controller.get_bright_symbol()
        empty = self.__controller.get_empty_symbol()
        is_replace_symbols = self.__controller.get_is_symbols_replace()
        return (
            "Current symbols:"
            + f"\n bright: {bright}"
            + f"\n empty: {empty}"
            + f"\n replacing: {is_replace_symbols}"
        )

    def set_alignment(self):
        options = ["left", "right", "center"]
        options_str = "/".join(options)
        message = f"Choose alignment ({options_str}): "
        result = VariantsInput().input(message, options, "Wrong alignment")
        self.__controller.set_alignment(result)

    def set_bright_symbol(self):
        message = "Bright symbol:  "
        result = StringInput.input(message, [1, 1])
        self.__controller.set_bright_symbol(result)

    def set_empty_symbol(self):
        message = "Empty symbol:  "
        result = StringInput.input(message, [1, 1])
        self.__controller.set_empty_symbol(result)

    def set_is_replace_symbols(self):
        message = "Replace (y/n)? "
        result = BoolInput.default(message)
        self.__controller.set_is_symbols_replace(result)

    def set_color(self):
        colors = self.__controller.get_colors()
        colors_str = " ,".join(colors)
        color = VariantsInput().input(
            f"Colors: {colors_str}\n Choose color:", colors, "Wrong color!"
        )
        self.__controller.set_color(color)

    def set_font(self):
        fonts = self.__controller.get_fonts()
        fonts_str = ""
        in_row = 5
        last = 0
        for index in range(0, len(fonts), in_row):
            row = ", ".join(fonts[index : index + in_row])
            fonts_str += "\n" + row

        font = VariantsInput.input(fonts_str + "\nChoose font: ", fonts)
        self.__controller.set_font(font)

    def set_width(self):
        min_width = self.__controller.get_min_width()
        max_width = self.__controller.get_max_possible_width()
        cur_width = self.__controller.get_width()

        message = (
            f"Current width: {cur_width}. Range: {min_width}-{max_width}\n Set width: "
        )
        width = NumberBetweenInput().input(
            message, [min_width, max_width], "Wrong width"
        )
        self.__controller.set_width(width)

    def set_height(self):
        min_height = self.__controller.get_min_height()
        max_height = self.__controller.get_max_possible_height()
        cur_height = self.__controller.get_height()

        message = f"Current height: {cur_height}. Range: {min_height}-{max_height}\n Set height: "
        height = NumberBetweenInput().input(
            message, [min_height, max_height], "Wrong height"
        )
        self.__controller.set_height(height)

    def set_line_breaking(self):
        is_font_support = self.__controller.is_font_support_line_break()
        if is_font_support:
            supporting = "current font support"
        else:
            supporting = "current font not support"
        message = f"Break line/wrap word ({supporting}) (y/n)? "
        result = BoolInput.default(message)
        self.__controller.set_is_line_breaks(result)

    def see_example(self):
        is_font_correct = self.__controller.is_font_correct()
        if not is_font_correct:
            return "Can't generate example, no such font\n CHANGE FONT TO AVAILABLE"
        example_text = "Settings for art"
        settings_info = self.__controller.get_settings_info()
        art = self.__controller.create_cut_art(example_text)
        return settings_info + f"\n '{example_text}' string example\n" + art
