"""
choices_menu module

This module provides classes to facilitate the display and selection of menu options with
 various configurations.

Classes
-------
ChooseMenu
    Facilitates the display and selection of menu options with various configurations.

ChooseMenuBuilder
    Provides a builder pattern for creating customized menus with selectable options.
"""

from shared.classes.input import VariantsInput
from shared.classes.ordered_set import OrderedSet


class ChooseMenu:
    """
    ChooseMenu class facilitates the display and selection of menu options with
    various configurations.

    Methods
    -------
    __init__()
        Initializes the ChooseMenu with default settings for options, prompts, flags,
         and other configurations.

    set_selected(options)
        Sets the initially selected options.

    set_choose_prompt(choose_prompt)
        Sets the prompt message shown before the list of options.

    set_input_prompt(input_prompt)
        Sets the prompt message for user input.

    set_warning_prompt(warning_prompt)
        Sets the warning message shown on invalid input.

    set_is_has_order(is_has_order)
        Configures if the menu should display options with ordered numbers.

    add_option(key, option)
        Adds an option to the menu.

    set_leave_option(key, leave_option)
        Sets the option key and message for exiting the menu.

    set_is_multiselect(is_multiselect)
        Configures if multiple selections are allowed.

    set_flags(boolean_selected_flag="[\\*]", numeric_selected_flag="[\\{i}]",
    unselected_flag="[ ]")
        Sets the custom flags for selected and unselected options.

    set_options_format_string(format_string="{key}: {flag} {option}")
        Sets the format string for displaying options.

    set_leave_format_string(format_string="{key}: {message}")
        Sets the format string for displaying the leave option.

    is_valid_option_string(format_string)
        Checks if the provided format string for options is valid.

    is_valid_selected_string(format_string)
        Checks if the provided format string for selected options is valid.

    is_valid_leave_string(format_string)
        Checks if the provided format string for the leave option is valid.

    get_flag(key, value)
        Retrieves the flag for a given option based on its selection state.

    display_menu()
        Displays the current state of the menu and options.

    get_input_and_execute()
        Continuously prompts the user for input until exit or stop is triggered.

    stop()
        Terminates the input loop and stops the menu display.

    show()
        Displays the menu and returns the final selected options.
    """

    def __init__(self):
        """
        Initializes the ChooseMenu with default settings for options, prompts, flags,
        and other configurations.
        """
        self.options = {}
        self.selected_options = OrderedSet()
        self.leave_option = {"key": "exit", "message": "Exit"}
        self.is_multiselect = True
        self.is_has_order = True
        self.numeric_selected_flag = "[{i}]"
        self.boolean_selected_flag = "[*]"
        self.unselected_flag = "[ ]"
        self.choose_prompt = "Choose from the following options:"
        self.input_prompt = "Enter your choice (number):"
        self.warning_prompt = "Invalid choice. Please try again."
        self.is_continue = True
        self.options_format_string = "{flag}—{key}. {option}"
        self.leave_format_string = "{key}: {message}"

    def set_selected(self, options):
        """
        Sets the initially selected options.

        Parameters
        ----------
        options : str or list of str
            The options to be initially selected.
        """
        self.selected_options.clear()
        if isinstance(options, str):
            self.selected_options.add(options)
        else:
            for option in options:
                self.selected_options.add(option)
        return self

    def set_choose_prompt(self, choose_prompt):
        """
        Sets the prompt message shown before the list of options.

        Parameters
        ----------
        choose_prompt : str
            The prompt message to be displayed.
        """
        self.choose_prompt = choose_prompt

    def set_input_prompt(self, input_prompt):
        """
        Sets the prompt message for user input.

        Parameters
        ----------
        input_prompt : str
            The input prompt message to be displayed.
        """
        self.input_prompt = input_prompt

    def set_warning_prompt(self, warning_prompt):
        """
        Sets the warning message shown on invalid input.

        Parameters
        ----------
        warning_prompt : str
            The warning message to be displayed on invalid input.
        """
        self.warning_prompt = warning_prompt

    def set_is_has_order(self, is_has_order):
        """
        Configures if the menu should display options with ordered numbers.

        Parameters
        ----------
        is_has_order : bool
            If True, the menu will display options with ordered numbers.
        """
        self.is_has_order = is_has_order

    def add_option(self, key, option):
        """
        Adds an option to the menu.

        Parameters
        ----------
        key : str
            The key for the option.
        option : str
            The option to be displayed.
        """
        self.options[key] = option

    def set_leave_option(self, key, leave_option):
        """
        Sets the option key and message for exiting the menu.

        Parameters
        ----------
        key : str
            The key for the leave option.
        leave_option : str
            The message to be displayed for the leave option.
        """
        self.leave_option = {"key": key, "message": leave_option}

    def set_is_multiselect(self, is_multiselect):
        """
        Configures if multiple selections are allowed.

        Parameters
        ----------
        is_multiselect : bool
            If True, multiple selections are allowed.
        """
        self.is_multiselect = is_multiselect

    def set_flags(
            self,
            boolean_selected_flag="[*]",
            numeric_selected_flag="[{i}]",
            unselected_flag="[ ]",
    ):
        """
        Sets the custom flags for selected and unselected options.

        Parameters
        ----------
        boolean_selected_flag : str
            The flag for boolean selected options.
        numeric_selected_flag : str
            The flag for numeric selected options.
        unselected_flag : str
            The flag for unselected options.

        Raises
        ------
        ValueError
            If the boolean selected flag is invalid.
        """
        if not self.is_valid_selected_string(boolean_selected_flag):
            raise ValueError("Invalid boolean selected flag")
        self.boolean_selected_flag = boolean_selected_flag
        self.numeric_selected_flag = numeric_selected_flag
        self.unselected_flag = unselected_flag

    def set_options_format_string(self, format_string="{key}: {flag} {option}"):
        """
        Sets the format string for displaying options.

        Parameters
        ----------
        format_string : str
            The format string for options display.

        Raises
        ------
        ValueError
            If the format string is invalid.
        """
        if self.is_valid_option_string(format_string):
            self.options_format_string = format_string
        else:
            raise ValueError("Invalid format string")

    def set_leave_format_string(self, format_string="{key}: {message}"):
        """
        Sets the format string for displaying the leave option.

        Parameters
        ----------
        format_string : str
            The format string for the leave option.

        Raises
        ------
        ValueError
            If the format string is invalid.
        """
        if self.is_valid_leave_string(format_string):
            self.leave_format_string = format_string
        else:
            raise ValueError("Invalid format string")

    @staticmethod
    def is_valid_option_string(format_string):
        """
        Checks if the provided format string for options is valid.

        Parameters
        ----------
        format_string : str
            The format string to be validated.

        Returns
        -------
        bool
            True if the format string is valid, False otherwise.
        """
        try:
            format_string.format(key="", flag="", option="")
            return True
        except KeyError:
            return False

    @staticmethod
    def is_valid_selected_string(format_string):
        """
        Checks if the provided format string for selected options is valid.

        Parameters
        ----------
        format_string : str
            The format string to be validated.

        Returns
        -------
        bool
            True if the format string is valid, False otherwise.
        """
        try:
            format_string.format(i="")
            return True
        except KeyError:
            return False

    @staticmethod
    def is_valid_leave_string(format_string):
        """
        Checks if the provided format string for the leave option is valid.

        Parameters
        ----------
        format_string : str
            The format string to be validated.

        Returns
        -------
        bool
            True if the format string is valid, False otherwise.
        """
        try:
            format_string.format(key="", message="")
            return True
        except KeyError:
            return False

    def get_flag(self, key, value):
        """
        Retrieves the flag for a given option based on its selection state.

        Parameters
        ----------
        key : str
            The key for the option.
        value : str
            The value of the option.

        Returns
        -------
        str
            The flag representing the selection state of the option.

        Raises
        ------
        ValueError
            If the key is invalid.
        """
        if not self.options[key]:
            raise ValueError("Invalid key")
        if value not in self.selected_options:
            return self.unselected_flag
        if self.is_has_order:
            index = self.selected_options.index(value) + 1
            return self.numeric_selected_flag.format(i=index)
        return self.boolean_selected_flag

    def display_menu(self):
        """
        Displays the current state of the menu and options.
        """
        print(self.choose_prompt)
        for key, option in self.options.items():
            flag = self.get_flag(key, option)
            print(self.options_format_string.format(key=key, flag=flag, option=option))
        leave_option_key = self.leave_option["key"]
        leave_option_message = self.leave_option["message"]
        print(
            self.leave_format_string.format(
                key=leave_option_key, message=leave_option_message
            )
        )

    def get_input_and_execute(self):
        """
        Continuously prompts the user for input until exit or stop is triggered.
        """
        while self.is_continue:
            self.display_menu()
            leave_option_key = self.leave_option["key"]
            option_keys = list(self.options.keys()) + [leave_option_key]
            selected_key = VariantsInput().input(
                self.input_prompt,
                option_keys,
                self.warning_prompt,
                not self.is_continue,
            )
            if selected_key in (leave_option_key, None):
                self.stop()
                break
            selected_value = self.options[selected_key]
            if selected_value in self.selected_options:
                self.selected_options.remove(selected_value)
                continue
            if not self.is_multiselect:
                self.selected_options.clear()
            self.selected_options.add(selected_value)

    def stop(self):
        """
        Terminates the input loop and stops the menu display.
        """
        self.is_continue = False

    def show(self):
        """
        Displays the menu and returns the final selected options.

        Returns
        -------
        OrderedSet
            The final set of selected options.
        """
        self.is_continue = True
        self.get_input_and_execute()
        options = self.selected_options
        return options


class ChooseMenuBuilder:
    """
    ChooseMenuBuilder class provides a builder pattern for creating customized menus
    with selectable options.

    Methods
    -------
    ordered()
        Initiates a builder for an ordered menu.

    unordered()
        Initiates a builder for an unordered menu.

    set_selected(options)
        Sets the initially selected options.

    set_choose_prompt(choose_prompt)
        Sets the prompt message shown before the list of options.

    set_input_prompt(input_prompt)
        Sets the prompt message for user input.

    set_warning_prompt(warning_prompt)
        Sets the warning message shown on invalid input.

    set_is_has_order(is_has_order)
        Configures if the menu should display options with ordered numbers.

    add_option(key, option)
        Adds an option to the menu.

    set_leave_option(key, leave_option)
        Sets the option key and message for exiting the menu.

    set_is_multiselect(is_multiselect)
        Configures if multiple selections are allowed.

    set_flags(boolean_selected_flag="[\\*]", numeric_selected_flag="[\\{i}]",
    unselected_flag="[ ]")
        Sets the custom flags for selected and unselected options.

    set_options_format_string(format_string="{key}: {flag} {option}")
        Sets the format string for displaying options.

    set_leave_format_string(format_string="{key}: {message}")
        Sets the format string for displaying the leave option.

    build()
        Builds and returns the customized ChooseMenu instance.
    """

    def __init__(self):
        self.menu = ChooseMenu()

    @classmethod
    def ordered(cls):
        """
        Initiates a builder for an ordered menu.

        Returns
        -------
        ChooseMenuBuilder
            A builder instance with default settings for an ordered menu.
        """
        return (
            cls()
            .set_choose_prompt("Select:")
            .set_is_multiselect(True)
            .set_is_has_order(True)
            .set_flags(numeric_selected_flag="[{i}]", unselected_flag="[ ]")
            .set_input_prompt("Enter number:")
            .set_options_format_string("{key}: {flag} {option}")
            .set_warning_prompt("not in variants, please select a valid number.")
            .set_leave_option("0", "Finish selection")
            .set_leave_format_string("{key}: {message}")
        )

    @classmethod
    def unordered(cls):
        """
        Initiates a builder for an unordered menu.

        Returns
        -------
        ChooseMenuBuilder
            A builder instance with default settings for an unordered menu.
        """
        return (
            cls()
            .set_choose_prompt("Select:")
            .set_is_multiselect(True)
            .set_is_has_order(False)
            .set_flags(boolean_selected_flag="[*]", unselected_flag="[ ]")
            .set_input_prompt("Choose:")
            .set_options_format_string("{key}: {flag} {option}")
            .set_warning_prompt(" — wrong input.")
            .set_leave_option("Exit", "Finish selection")
            .set_leave_format_string("{key}: {message}")
        )

    def set_selected(self, options):
        """
        Sets the initially selected options.

        Parameters
        ----------
        options : str or list of str
            The options to be initially selected.
        """
        self.menu.set_selected(options)

    def set_choose_prompt(self, choose_prompt):
        """
        Sets the prompt message shown before the list of options.

        Parameters
        ----------
        choose_prompt : str
            The prompt message to be displayed.
        """
        self.menu.set_choose_prompt(choose_prompt)
        return self

    def set_input_prompt(self, input_prompt):
        """
        Sets the prompt message for user input.

        Parameters
        ----------
        input_prompt : str
            The input prompt message to be displayed.
        """
        self.menu.set_input_prompt(input_prompt)
        return self

    def set_warning_prompt(self, warning_prompt):
        """
        Sets the warning message shown on invalid input.

        Parameters
        ----------
        warning_prompt : str
            The warning message to be displayed on invalid input.
        """
        self.menu.set_warning_prompt(warning_prompt)
        return self

    def set_is_has_order(self, is_has_order):
        """
        Configures if the menu should display options with ordered numbers.

        Parameters
        ----------
        is_has_order : bool
            If True, the menu will display options with ordered numbers.
        """
        self.menu.set_is_has_order(is_has_order)
        return self

    def add_option(self, key, option):
        """
        Adds an option to the menu.

        Parameters
        ----------
        key : str
            The key for the option.
        option : str
            The option to be displayed.
        """
        self.menu.add_option(key, option)
        return self

    def set_leave_option(self, key, leave_option):
        """
        Sets the option key and message for exiting the menu.

        Parameters
        ----------
        key : str
            The key for the leave option.
        leave_option : str
            The message to be displayed for the leave option.
        """
        self.menu.set_leave_option(key, leave_option)
        return self

    def set_is_multiselect(self, is_multiselect):
        """
        Configures if multiple selections are allowed.

        Parameters
        ----------
        is_multiselect : bool
            If True, multiple selections are allowed.
        """
        self.menu.set_is_multiselect(is_multiselect)
        return self

    def set_flags(
            self,
            boolean_selected_flag="[*]",
            numeric_selected_flag="[{i}]",
            unselected_flag="[ ]",
    ):
        """
        Sets the custom flags for selected and unselected options.

        Parameters
        ----------
        boolean_selected_flag : str
            The flag for boolean selected options.
        numeric_selected_flag : str
            The flag for numeric selected options.
        unselected_flag : str
            The flag for unselected options.
        """
        self.menu.set_flags(
            boolean_selected_flag, numeric_selected_flag, unselected_flag
        )
        return self

    def set_options_format_string(self, format_string="{key}: {flag} {option}"):
        """
        Sets the format string for displaying options.

        Parameters
        ----------
        format_string : str
            The format string for options display.
        """
        self.menu.set_options_format_string(format_string)
        return self

    def set_leave_format_string(self, format_string="{key}: {message}"):
        """
        Sets the format string for displaying the leave option.

        Parameters
        ----------
        format_string : str
            The format string for the leave option.
        """
        self.menu.set_leave_format_string(format_string)
        return self

    def build(self):
        """
        Builds and returns the customized ChooseMenu instance.

        Returns
        -------
        ChooseMenu
            The customized ChooseMenu instance.

        Raises
        ------
        ValueError
            If a selected option is not part of the menu options.
        """
        for selected in self.menu.selected_options:
            if selected not in self.menu.options:
                raise ValueError(
                    f"Select {selected}, but not in variants({self.menu.options})"
                )
        return self.menu
