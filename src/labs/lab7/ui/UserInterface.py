import logging

logger = logging.getLogger(__name__)

from tkinter import Tk, filedialog

import pyautogui
from scipy.optimize import brent

from labs.lab7.bll.Controller import Controller
from labs.lab7.bll.DataStyler import DataStyler
from shared.classes.choose_menu_builder import ChooseMenuBuilder
from shared.classes.input import StringInput
from shared.classes.menu_builder import MenuBuilder


class UserInterface:
    """
    UserInterface

    Attributes:
        TITLE (str): Title string for the main menu.
        REGEX_MENU_TITLE (str): Title string for the regex menu.
        SETTINGS_TITLE (str): Title string for the settings menu.
        SAVE_TITLE (str): Title string for the save menu, describes available file types.
        FILE_EXTENSIONS (list): List of tuples describing acceptable file extensions for saving.

        MIN_QUERY_LEN (int): Minimum length for a query string.
        MAX_QUERY_LEN (int): Maximum length for a query string.
        MIN_REGEX_LEN (int): Minimum length for a regex string.
        MAX_REGEX_LEN (int): Maximum length for a regex string.

    Methods:
        __init__: Initializes the UserInterface instance.

        show: Displays the main menu.

        _build_main_menu: Constructs and returns the main menu.

        _build_choose_mode: Constructs and returns the choose mode menu.

        _build_settings_menu: Constructs and returns the settings menu.

        _build_choose_fields_menu: Constructs and returns the choose fields menu.

        _build_field_selection_menu: Constructs and returns the field selection menu.

        _build_regex_menu: Constructs and returns the regex menu.

        save: Saves the queried data to a file; supports .txt, .json, and .csv formats.

        _save_file_dialog: Opens a file save dialog and returns the selected file path.

        _dynamic_regex_title: Constructs and returns the dynamic title string for the regex menu.

        get_regex: Returns the current regex string from the controller.

        get_regex_field: Returns the current regex field name from the controller.

        get_results: Retrieves and returns the results based on the current query and settings.

        _get_results_string: Constructs and returns the formatted results string based on query and settings.

        set_query: Prompts the user to input a search query and sets it in the controller.

        set_regex: Prompts the user to input a regular expression and sets it in the controller.

        set_regex_field: Prompts the user to select a regex field and sets it in the controller.

        choose_fields: Prompts the user to select fields based on the given mode and sets them in the controller.

        choose_visualization_method: Prompts the user to choose visualization methods and sets them in the controller.
    """

    TITLE = "Google Books API\n"
    REGEX_MENU_TITLE = "Regex string"
    SETTINGS_TITLE = "Settings"
    SAVE_TITLE = "Save. You can choose .txt, .csv or .json file types. For csv it will create _list.csv or/and _table.csv file if needed"
    FILE_EXTENSIONS = [
        ("Text files", "*.txt"),
        ("CSV files", "*.csv"),
        ("JSON files", "*.json"),
        ("All files", "*.*"),
    ]

    MIN_QUERY_LEN = 3
    MAX_QUERY_LEN = 30
    MIN_REGEX_LEN = 2
    MAX_REGEX_LEN = 100

    def __init__(self, controller: Controller):
        self.controller = controller
        self.styler = DataStyler.default()
        self.regex_menu = self._build_regex_menu()
        self.field_selection_menu = self._build_field_selection_menu()
        self.settings_menu = self._build_settings_menu()
        self.choose_mode_menu = self._build_choose_mode()
        self.choose_fields_menu = self._build_choose_fields_menu()
        self.main_menu = self._build_main_menu()

    def show(self):
        self.main_menu.show()

    def _build_main_menu(self):
        return (
            MenuBuilder()
            .set_title(self.TITLE)
            .set_dynamic_title(self.get_results)
            .add_option("1", "\n1. Input search query", self.set_query)
            .add_option("2", "\n2. Input regular expression", self.regex_menu.show)
            .add_option(
                "3",
                "\n3. Choose visualization methods",
                self.choose_visualization_method,
            )
            .add_option("4", "\n4. Settings", self.settings_menu.show)
            .add_option("5", "\n5. Save", self.save)
            .add_stop_options(["0", "Exit", "exit", "e", "q"], "0. Exit")
            .build()
        )

    def _build_choose_mode(self):
        return (
            ChooseMenuBuilder.unordered()
            .add_option("1", "List")
            .add_option("2", "Table")
            .set_leave_option("0", "Exit")
            .build()
        )

    def _build_settings_menu(self):
        return (
            MenuBuilder()
            .set_title(self.SETTINGS_TITLE)
            .add_option("1", "\n1. List fields", self.choose_fields, mode="List")
            .add_option("2", "\n2. Table fields", self.choose_fields, mode="Table")
            .add_stop_options(["0", "Exit", "exit", "e", "q"], "0. Exit")
            .build()
        )

    def _build_choose_fields_menu(self):
        keys = self.controller.get_fields_keys()
        choose_fields_menu = ChooseMenuBuilder.ordered().set_leave_option("0", "Exit")

        for i, field in enumerate(keys):
            choose_fields_menu.add_option(f"{i + 1}", field)

        return choose_fields_menu.build()

    def _build_field_selection_menu(self):
        fields_keys = self.controller.get_fields_keys()
        menu = (
            ChooseMenuBuilder.unordered()
            .set_leave_option("0", "Exit")
            .set_is_multiselect(False)
        )

        for index, field in enumerate(fields_keys):
            menu.add_option(f"{index + 1}", str(field))

        return menu.build()

    def _build_regex_menu(self):
        return (
            MenuBuilder()
            .set_title(self.REGEX_MENU_TITLE)
            .set_dynamic_title(self._dynamic_regex_title)
            .add_option("1", "\n1. Regular expression", self.set_regex)
            .add_option("2", "\n2. Field", self.set_regex_field)
            .add_stop_options(["0", "Exit", "exit", "e", "q"], "0. Exit")
            .build()
        )

    def save(self):
        query = self.controller.get_query()
        if not query:
            return "No query yet"
        file_path = self._save_file_dialog()
        if not file_path:
            print("Empty filepath!")
            return
        if not file_path.endswith(tuple(ext := [".txt", ".json", ".csv"])):
            print("Invalid file extension!")
            return

        data = None
        if file_path.endswith(".txt"):
            styled_data = self.get_results()
            data = self.styler.remove_styles(styled_data)

        self.controller.save(file_path, data)

    def _save_file_dialog(self):
        root = Tk()
        root.withdraw()
        default_name = self.controller.get_default_file_name()
        default_path = self.controller.get_default_save_dir()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=self.FILE_EXTENSIONS,
            initialfile=default_name,
            initialdir=default_path,
            title=self.SAVE_TITLE,
        )
        root.destroy()
        return file_path or ""

    def _dynamic_regex_title(self):
        return f"{self.get_regex()} regex string on {self.get_regex_field()} field"

    def get_regex(self):
        return self.controller.get_regex()

    def get_regex_field(self):
        return self.controller.get_regex_field_name()

    def get_results(self):
        query = self.controller.get_query()
        if not query:
            return "No query yet"
        fields = self.controller.get_fields()
        field_styles = self.controller.get_field_styles()
        is_table = self.controller.get_is_table()
        is_list = self.controller.get_is_list()
        return self._get_results_string(query, fields, field_styles, is_table, is_list)

    def _get_results_string(self, query, fields, field_styles, is_table, is_list):
        str_results = ""
        if is_table:
            try:
                table = self.controller.search_for_table()
            except Exception as e:
                logger.error(e)
                return "Error"
            if not table[0]["items"]:
                str_results += (
                    "No table results for such query, regex and field, change them\n"
                )
            else:
                styled_table = self.styler.as_table(*table, field_styles, fields)
                str_results += f"\n{styled_table}"
        if is_list:
            try:
                lst = self.controller.search_for_list()
            except Exception as e:
                logger.error(e)
                return "Error"
            if not lst[0]["items"]:
                str_results += (
                    "No list results for such query, regex and field, change them\n"
                )
            else:
                styled_list = self.styler.as_list(*lst, field_styles, fields)
                str_results += f"\n{styled_list}"
        regex_string = self._dynamic_regex_title()
        str_results += f"Query: {query}\n{regex_string}\n"
        return str_results

    def set_query(self):
        query = StringInput().input(
            f"Enter query {self.MIN_QUERY_LEN}-{self.MAX_QUERY_LEN}:",
            [self.MIN_QUERY_LEN, self.MAX_QUERY_LEN],
            "Not in range",
        )
        self.controller.set_last_query(query)

    def set_regex(self):
        while True:
            regex = StringInput().input(
                f"Enter regex {self.MIN_REGEX_LEN}-{self.MAX_REGEX_LEN}:",
                [self.MIN_REGEX_LEN, self.MAX_REGEX_LEN],
                "Not in range",
            )
            if self.controller.is_regex(regex):
                break
            else:
                print("Wrong regex, try again")
        self.controller.set_last_regex(regex)

    def set_regex_field(self):
        selected_now = self.controller.get_regex_field_name()
        selected_field = self.field_selection_menu.set_selected(selected_now).show()
        self.controller.set_regex_field_name(str(selected_field))

    def choose_fields(self, attributes):
        mode = attributes.get("mode")
        selected_fields = self.controller.get_selected_fields(mode)
        chosen_fields = self.choose_fields_menu.set_selected(selected_fields).show()
        self.controller.set_selected(chosen_fields, mode)

    def choose_visualization_method(self):
        selected = []
        if self.controller.get_is_list():
            selected.append("List")
        if self.controller.get_is_table():
            selected.append("Table")
        choose = self.choose_mode_menu.set_selected(selected).show()
        self.controller.set_is_list("List" in choose)
        self.controller.set_is_table("Table" in choose)
