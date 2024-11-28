"""
This module provides the `GlobalUI` class which serves as the main interface
for initializing, displaying, and managing a menu-driven user interface.
The user interface allows users to select and run various laboratory exercises.

Classes:
--------
GlobalUI:
    Provides methods to construct a menu, display the menu to the user,
    and run the selected laboratory exercise.

Functions:
----------
__init__(self):
    Initializes the GlobalUI instance and, if specified, starts a particular lab.

menu(self):
    Displays the main menu to the user.

build_menu(self):
    Constructs the menu with various lab options and controls using the MenuBuilder.

__run_lab(self, lab=None):
    Dynamically imports and runs the specified lab by calling its 'run' method.
"""

from importlib import import_module

from shared.classes.menu_builder import MenuBuilder

# for try specific lab, otherwise set to None
USE_LAB = None


class GlobalUI:
    """
    Class GlobalUI handles the graphical user interface for navigating different
    specialized programming language labs.

    Methods:
    - __init__: Initializes the GlobalUI instance,
    optionally runs a specific lab,
    and builds the main menu.
    - menu: Displays the main menu.
    - build_menu: Constructs the menu using the MenuBuilder, setting various options
     and descriptions.
    - __run_lab: Executes a specified lab by dynamically importing and
    running its `run` method.
    """

    def __init__(self):
        """

        Initializes the instance of the class.
        If 'use_lab' is True, continuously runs the lab until stopped.
        Otherwise, builds the menu by calling 'self.build_menu()' method.

        :param use_lab: A boolean flag determining if the lab environment should be used.
        :type use_lab: bool
        """
        if USE_LAB:
            while True:
                self.__run_lab(USE_LAB)
        self.build_menu()

    def menu(self):
        """
        Builds and displays the menu.

        :return: None
        """
        self.build_menu()
        self._menu.show()

    def build_menu(self):
        """
        :return: Build and configure a menu with various options such as
        calculators, ASCII arts, tests, API program, and data visualization.
        The menu also includes stop options to exit.
        """
        self._menu = (
            MenuBuilder()
            .set_title("\nWelcome to specialized programming languages!")
            .set_warning("Wrong input!")
            .set_input_text("Choose lab:")
            .add_option("1", "1. Function calculator\n", self.__run_lab, number=1)
            .add_option("2", "2. OOP calculator\n", self.__run_lab, number=2)
            .add_option("3", "3. ASCII pyfiglet arts\n", self.__run_lab, number=3)
            .add_option("4", "4. ASCII custom arts\n", self.__run_lab, number=4)
            .add_option("5", "5. ASCII 3d\n", self.__run_lab, number=5)
            .add_option("6", "6. Run tests\n", self.__run_lab, number=6)
            .add_option("7", "7. Run API program\n", self.__run_lab, number=7)
            .add_option("8", "8. Data visualization\n", self.__run_lab, number=8)
            .add_option("9", "9. Docs/Help\n", self.__run_lab, number=9)
            .add_stop_options(["e", "0", "exit", "Exit"], "0.Exit(e)")
            .build()
        )

    def __run_lab(self, lab=None):
        """
        :param lab: Dictionary containing lab details or a numeric identifier
        for the lab. If None, the function returns without doing anything.
        :return: None
        """
        if lab is None:
            return
        try:
            numeric = lab["number"]
        except (TypeError, KeyError):
            numeric = lab
        module_name = f"labs.lab{numeric}.runner"
        try:
            runner = import_module(module_name)
        except ImportError:
            print(f"Error: Can't import {module_name}. Please try again.")
            return
        if hasattr(runner.Runner, "run") and callable(runner.Runner.run):
            runner.Runner.run()
        else:
            print(f"Error: 'run' function not found in {module_name}.")
