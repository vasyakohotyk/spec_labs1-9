"""
Menu System Module

This module provides a flexible and customizable menu system for console applications.
It includes two main classes:

Classes:
    - Menu: Represents the main menu system, allowing options to be added, updated,
    and executed based on user input.
    - MenuBuilder: Provides a chainable API for constructing and customizing Menu objects.

Usage:
    Create an instance of Menu or use MenuBuilder to construct and customize your
    Menu before displaying it to the user.
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, Optional


@dataclass
class MenuOptions:
    """
    Contains the options and attributes for the menu.

    Attributes:
        options (Dict[str, Callable]): A dictionary where keys are
        option keys and values are functions to execute.
        attributes (Dict[str, dict]): A dictionary where keys are
        option keys and values are additional attributes for the options.
        end_callback_attributes (Optional[dict]): Attributes for the end callback function.
    """
    options: Dict[str, Callable] = field(default_factory=dict)
    attributes: Dict[str, dict] = field(default_factory=dict)
    end_callback_attributes: Optional[dict] = None


@dataclass
class MenuText:
    """
    Stores various text elements for the menu.

    Attributes:
        title (str): The title to display at the top of the menu.
        dynamic_title (Optional[Callable]): A callable for generating a dynamic title.
        text (Optional[str]): The main text content of the menu.
        bottom (Optional[str]): Text to display at the bottom of the menu.
        input_text (str): The prompt text for user input.
        warning (str): The warning message for invalid input.
    """
    title: str = "Title"
    dynamic_title: Optional[Callable] = None
    text: Optional[str] = None
    bottom: Optional[str] = None
    input_text: str = "Choose:"
    warning: str = "Wrong option!"


class Menu:
    """
    Class representing a menu system for console applications.

    Attributes:
        options (MenuOptions): Stores menu options, their associated methods, and attributes.
        text_elements (MenuText): Stores text elements for the menu.
        is_continue (bool): Flag to control the continuation of the menu loop.
        end_callback (function): Method to call when the menu loop ends.
    """

    def __init__(self):
        """
        Initialize the Menu with default properties, including options, attributes,
        and various text elements.
        """
        self.options = MenuOptions()
        self.text_elements = MenuText()
        self.is_continue = True
        self.end_callback = None

    def set_title(self, title):
        """
        Set a static title for the menu.

        Parameters:
            title (str): The title of the menu.
        """
        self.text_elements.title = title

    def set_dynamic_title(self, method):
        """
        Set a dynamic title method for the menu.

        Parameters:
            method (function): Function to call for generating the dynamic title.
        """
        self.text_elements.dynamic_title = method

    def get_print_text(self):
        """
        Get the concatenated text of the menu, including title, dynamic title,
        and various text sections.

        Returns:
            str: The formatted menu text.
        """
        parts = filter(
            None,
            [
                self.text_elements.title,
                self.text_elements.dynamic_title() if self.text_elements.dynamic_title else None,
                self.text_elements.text,
                self.text_elements.bottom,
            ],
        )
        return "\n".join(parts)

    def set_input_text(self, input_text):
        """
        Set the text prompt for input.

        Parameters:
            input_text (str): The input prompt text.
        """
        self.text_elements.input_text = input_text

    def set_warning(self, warning):
        """
        Set the warning message to display for invalid input.

        Parameters:
            warning (str): The warning message.
        """
        self.text_elements.warning = warning

    def stop(self):
        """
        Stop the menu loop.
        """
        self.is_continue = False

    def update_option(self, key, message, method, **attributes):
        """
        Add or update an option in the menu, including associated message and attributes.

        Parameters:
            key (str): The key for this menu option.
            message (str): The message to display for this option.
            method (function): The function to execute when this option is selected.
            **attributes: Additional attributes for the option.
        """
        if not self.text_elements.text:
            self.text_elements.text = ""
        if message:
            self.text_elements.text += message
        self.options.options[key] = method

        if attributes:
            self.options.attributes[key] = attributes

    def update_end_option(self, key, message, method, **attributes):
        """
        Add or update an end option in the menu, including associated message and attributes.

        Parameters:
            key (str): The key for this end menu option.
            message (str): The message to display for this option.
            method (function): The function to execute when this option is selected.
            **attributes: Additional attributes for the option.
        """
        if not self.text_elements.bottom:
            self.text_elements.bottom = ""
        if message:
            self.text_elements.bottom += message
        self.options.options[key] = method

        if attributes:
            self.options.attributes[key] = attributes

    def update_end_callback(self, method, **attributes):
        """
        Set a callback function to be called when the menu loop ends.

        Parameters:
            method (function): The callback function.
            **attributes: Additional attributes for the callback.

        Raises:
            ValueError: If the provided method is not callable.
        """
        if not callable(method):
            raise ValueError("Wrong end callback")
        self.end_callback = method
        if attributes:
            self.options.end_callback_attributes = attributes

    def show_text(self):
        """
        Display the menu text in the console.
        """
        text = self.get_print_text()
        print(text)

    def get_input_and_execute(self):
        """
        Get user input and execute the associated menu option.
        """
        user_input = input(self.text_elements.input_text)
        if user_input not in self.options.options:
            print(self.text_elements.warning)
            return
        method = self.options.options[user_input]
        if user_input in self.options.attributes:
            method(self.options.attributes[user_input])
        else:
            method()

    def show(self):
        """
        Display the menu and process user input until the menu is stopped.
        """
        self.is_continue = True
        while True:
            self.show_text()
            self.get_input_and_execute()
            if not self.is_continue:
                break
        if self.end_callback:
            if self.options.end_callback_attributes:
                self.end_callback(self.options.end_callback_attributes)
            else:
                self.end_callback()


class MenuBuilder:
    """
    MenuBuilder is a class that facilitates the construction and customization
    of a menu by providing a chainable API.

    Methods
    -------
    __init__()
        Initializes a new instance of MenuBuilder with a default Menu object.

    set_title(title="Settings")
        Sets the title of the menu. Default is "Settings".

    set_dynamic_title(method=lambda: "dynamic title")
        Sets a dynamic title using a callable method. Default method returns "dynamic title".

    set_input_text(input_text="Choose: ")
        Sets the input prompt text for the menu. Default is "Choose: ".

    set_warning(warning="Wrong option!")
        Sets the warning message for invalid menu options. Default is "Wrong option!".

    update_end_callback(end_callback, **attributes)
        Updates the end callback with any specified attributes.

    add_stop_options(keys, message="Exit")
        Adds options to stop the menu based on specified keys. Default message is "Exit".

    add_option(key, message, method, **attributes)
        Adds an option to the menu with a specified key, message, and method.
        Additional attributes can also be provided.

    add_option_without_attributes(key, message, method)
        Adds an option to the menu with a specified key, message, and method without
        additional attributes.

    update_attribute(key, value)
        Updates an attribute of the menu with a specified key and value.

    stop_on_invalid_input()
        Stops the menu execution on invalid input.

    build()
        Constructs and returns the final Menu object.
    """

    def __init__(self):
        """
        Initializes a new instance of MenuBuilder with a default Menu object.
        """
        self._menu = Menu()

    def set_title(self, title="Settings"):
        """
        Sets the title of the menu.

        Parameters:
            title (str): The title of the menu.
        """
        self._menu.set_title(title)
        return self

    def set_dynamic_title(self, method=lambda: "dynamic title"):
        """
        Sets a dynamic title using a callable method.

        Parameters:
            method (function): Function to call for generating the dynamic title.
        """
        if not callable(method):
            raise ValueError("Wrong dynamic title")
        self._menu.set_dynamic_title(method)
        return self

    def set_input_text(self, input_text="Choose: "):
        """
        Sets the input prompt text for the menu.

        Parameters:
            input_text (str): The input prompt text.
        """
        self._menu.set_input_text(input_text)
        return self

    def set_warning(self, warning="Wrong option!"):
        """
        Sets the warning message for invalid menu options.

        Parameters:
            warning (str): The warning message.
        """
        self._menu.set_warning(warning)
        return self

    def update_end_callback(self, end_callback, **attributes):
        """
        Updates the end callback with any specified attributes.

        Parameters:
            end_callback (function): The callback function to be called when the menu loop ends.
            **attributes: Additional attributes for the end callback.
        """
        self._menu.update_end_callback(end_callback, **attributes)
        return self

    def add_stop_options(self, keys, message="Exit"):
        """
        Adds options to stop the menu based on specified keys.

        Parameters:
            keys (list): A list of keys that will stop the menu.
            message (str): The message to display for these options.
        """
        for key in keys:
            self._menu.update_end_option(key, "", self._menu.stop)
        self._menu.text_elements.bottom += message
        return self

    def add_option(self, key, message, method, **attributes):
        """
        Adds an option to the menu with a specified key, message, and method.

        Parameters:
            key (str): The key for this menu option.
            message (str): The message to display for this option.
            method (function): The function to execute when this option is selected.
            **attributes: Additional attributes for the option.
        """
        if not callable(method):
            raise ValueError("Wrong option method")
        self._menu.update_option(key, message, method, **attributes)
        return self

    def add_option_without_attributes(self, key, message, method):
        """
        Adds an option to the menu with a specified key, message, and method without
        additional attributes.

        Parameters:
            key (str): The key for this menu option.
            message (str): The message to display for this option.
            method (function): The function to execute when this option is selected.
        """
        if not callable(method):
            raise ValueError("Wrong option method")
        self._menu.update_option(key, message, method)
        return self

    def update_attribute(self, key, value):
        """
        Updates an attribute of the menu with a specified key and value.

        Parameters:
            key (str): The key for the attribute.
            value (any): The value to set for the attribute.
        """
        self._menu.options.attributes[key] = value
        return self

    def stop_on_invalid_input(self):
        """
        Stops the menu execution on invalid input.
        """
        self._menu.stop()
        return self

    def build(self):
        """
        Constructs and returns the final Menu object.

        Returns:
            Menu: The constructed Menu object.
        """
        return self._menu
