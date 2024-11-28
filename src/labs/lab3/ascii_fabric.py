from config.settings_paths import settings_path_lab3
from labs.lab3.bll.AsciiController import AsciiController
from labs.lab3.bll.ColoramaPainter import ColoramaPainter
from labs.lab3.bll.PyfigletGenerator import PyfigletGenerator
from labs.lab3.ui.AsciiMenu import AsciiMenu
from labs.lab3.ui.AsciiSettings import AsciiSettingsUI
from labs.lab4.bll.CustomGenerator import CustomGenerator
from labs.lab4.bll.CustomPainter import CustomPainter
from shared.classes.dict_json import DictJsonDataAccess
from shared.classes.folder_data_access import FolderDataAccess
from shared.interfaces.ui_interface import UIInterface


class AsciiFabric:
    """
    AsciiFabric class is a facade for generating ASCII art and managing user interface.

    Attributes:
        __ascii_ui (UIInterface): Interface to interact with ASCII art generation menu.

    Methods:
        __init__(generator, coloring): Initializes the AsciiFabric with a specific generator and coloring tool.
        show(): Displays the ASCII art generation menu.
        pyfiglet(): Class method to instantiate AsciiFabric with PyfigletGenerator and ColoramaPainter.
        custom(): Class method to instantiate AsciiFabric with CustomGenerator and CustomPainter.
    """

    def __init__(self, generator=PyfigletGenerator(), coloring=ColoramaPainter()):
        settings_access = DictJsonDataAccess(settings_path_lab3)
        __arts_folder = settings_access.get("__arts_folder")
        settings_ui: UIInterface = AsciiSettingsUI()
        ascii_ui: UIInterface = AsciiMenu(settings_ui, arts_folder=__arts_folder)
        arts_access = FolderDataAccess(__arts_folder, True, ".txt")
        controller = AsciiController(
            generator,
            coloring,
            arts_access,
            settings_access,
        )
        settings_ui.set_controller(controller)
        ascii_ui.set_controller(controller)
        self.__ascii_ui = ascii_ui

    def show(self):
        self.__ascii_ui.show()

    @classmethod
    def pyfiglet(cls):
        generator = PyfigletGenerator()
        coloring = ColoramaPainter()
        return cls(generator, coloring)

    @classmethod
    def custom(cls):
        generator = CustomGenerator()
        coloring = CustomPainter()
        return cls(generator, coloring)
