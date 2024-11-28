import logging
import os
from importlib.util import find_spec

from Cython.Shadow import returns
from pyautogui import mouseUp
from docs.generator import generate_docs
from labs.lab9.bll.Controller import Controller
from labs.lab9.bll.tree_print import folder_tree
from shared.classes.input import BoolInput, StringInput
from shared.classes.menu_builder import MenuBuilder

logger = logging.getLogger(__name__)


class UserInterface:
    """
    Class representing the user interface for interacting with documentation.

    Attributes:
        controller (Controller): The controller providing the necessary functionality.
        main_menu (Menu): The main menu of the user interface.
    """

    def __init__(self, controller: Controller):
        self.controller = controller
        self.main_menu = self.build_main()

    def show(self):
        self.main_menu.show()

    def build_main(self):
        menu = (
            MenuBuilder()
            .set_title("Docs")
            .add_option("1", "\n1. Docs in browser", self.browser_docs)
            .add_option("2", "\n2. Docs in console", self.console_docs)
            .add_option("3", "\n3. Generate all HTML docs", self.generate_docs)
            .add_option(
                "4", "\n4. List all available modules", self.list_available_modules
            )
            .add_stop_options(["0", "Exit", "exit", "e", "q"], "0. Exit")
            .build()
        )
        logger.debug("Build main menu")
        return menu

    def generate_docs(self):
        self.controller.generate_docs()

    def browser_docs(self):
        module_name = self.get_module_name()
        self.controller.open_pydoc_browser(module_name)

    def console_docs(self):
        module_name = self.get_module_name()
        help(module_name)

    def get_module_name(self):
        message = "Write module name:"
        string_len_range = [3, 30]
        is_exist = False
        module_name = ""
        while not is_exist:
            module_name = StringInput.input(message, string_len_range)
            is_exist = self.module_exists(module_name)
            if not is_exist:
                print("Module does not exist, try again.")
        return module_name

    def module_exists(self, module_name):
        is_exist = find_spec(module_name) is not None
        return is_exist

    def list_available_modules(self):
        root_path = self.controller.get_root_path()
        modules = []
        for root, _, files in os.walk(root_path):
            for f in files:
                if f.endswith(".py") and f != "__init__.py":
                    relative_path = os.path.relpath(root, root_path)
                    module = (
                        os.path.join(relative_path, f)
                        .replace(".py", "")
                        .replace(os.sep, ".")
                    )
                    if module.startswith(".."):
                        module = module[2:]
                    modules.append(module)
        str_modules = folder_tree(modules)
        print(f"Available modules:\n{str_modules}")
        if not modules:
            logger.warning("No available modules found.")
            print("No available modules found.")
