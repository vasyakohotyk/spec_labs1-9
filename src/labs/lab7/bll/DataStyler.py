import re

from colorama import Fore, Style, init
from tabulate import tabulate

from labs.lab7.bll.ItemExtraction import extract_data_items

init(autoreset=True)

COLORAMA_FORE_COLORS = {
    "red": Fore.RED,
    "blue": Fore.BLUE,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "white": Fore.WHITE,
    "magenta": Fore.MAGENTA,
    "cyan": Fore.CYAN,
    "black": Fore.BLACK,
}

TEXT_ATTRIBUTES = {
    "bold": Style.BRIGHT,
    "dim": Style.DIM,
    "normal": Style.NORMAL,
}


class DataStyler:
    """
    DataStyler Class

    This class is responsible for styling textual data with various foreground colors
    and text attributes such as font styles. It provides methods to apply these styles
    and format data into list or table representations.

    Methods:

    __init__(self, fore_colors, text_attributes):
        Initializes the DataStyler with provided color and text attribute mappings.

    default(cls):
        Class method that returns an instance of DataStyler with default color and
        text attribute mappings.

    remove_styles(styled_text):
        Static method that removes any ANSI escape sequences from the given styled text,
        resulting in plain text.

    get_available_fore_colors(self):
        Returns a list of available foreground color names based on the initialized
        fore_colors dictionary.

    get_available_text_attributes(self):
        Returns a list of available text attribute names based on the initialized
        text_attributes dictionary.

    apply_styles(self, field, fields_looks):
        Applies the appropriate styles to the given field based on the fields_looks
        dictionary and returns the styled text.

    as_list(self, data, selected_fields, fields_looks, fields_dict):
        Formats the given data into a list representation with styled field names
        and corresponding values.

    as_table(self, data, selected_fields, fields_looks, fields_dict):
        Formats the given data into a table representation with styled headers and
        corresponding values, utilizing the 'tabulate' module for table formatting.
    """

    def __init__(self, fore_colors, text_attributes):
        self.fore_colors = fore_colors
        self.text_attributes = text_attributes

    @classmethod
    def default(cls):
        return cls(COLORAMA_FORE_COLORS, TEXT_ATTRIBUTES)

    @staticmethod
    def remove_styles(styled_text):
        ansi_escape_pattern = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
        return ansi_escape_pattern.sub("", styled_text)

    def get_available_fore_colors(self):
        return list(self.fore_colors.keys())

    def get_available_text_attributes(self):
        return list(self.text_attributes.keys())

    def apply_styles(self, field, fields_looks):
        style = fields_looks.get(field, {})

        fore_color = self.fore_colors.get(style.get("color", "white"), Fore.WHITE)
        font_style = self.text_attributes.get(style.get("font", "normal"), Style.NORMAL)

        return f"{font_style}{fore_color}{field}{Style.RESET_ALL}"

    def as_list(self, data, selected_fields, fields_looks, fields_dict):
        extracted_items = extract_data_items(data, selected_fields, fields_dict)
        result = ""

        for item in extracted_items:
            for i, field in enumerate(selected_fields):
                title = self.apply_styles(field, fields_looks)
                value = item[i]
                if isinstance(value, list):
                    value = ", ".join(value)
                result += f"{title}: {value}\n"
            result += "\n"
        return result

    def as_table(self, data, selected_fields, fields_looks, fields_dict):
        extracted_items = extract_data_items(data, selected_fields, fields_dict)

        headers = [self.apply_styles(field, fields_looks) for field in selected_fields]
        formatted_items = []
        for item in extracted_items:
            formatted_row = []
            for value in item:
                if isinstance(value, list):
                    formatted_row.append(", ".join(value))
                else:
                    formatted_row.append(value)
            formatted_items.append(formatted_row)
        return tabulate(formatted_items, headers, tablefmt="grid")
