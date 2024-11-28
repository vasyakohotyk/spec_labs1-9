from labs.lab3.bll.AsciiController import AsciiController
from shared.classes.input import StringInput
from shared.classes.menu_builder import MenuBuilder
from shared.interfaces.ui_interface import UIInterface


class AsciiMenu(UIInterface):
    """
    AsciiMenu class inheriting from UIInterface, responsible for displaying and interacting with the ASCII art generation menu.

    Attributes:
        __controller (AsciiController): The controller handling ASCII art creation and storage.
        __settings_ui (UIInterface): Interface for the settings menu.
        __arts_folder (str): Directory where art files are stored.

    Methods:
        __init__(settings_ui, arts_folder=None, controller=None):
            Initializes the AsciiMenu instance with settings UI, arts folder, and controller.

        set_controller(controller):
            Sets the controller for ASCII art generation and rebuilds the menu.

        show():
            Displays the ASCII art menu.

        __menu_build():
            Constructs and returns the complete menu for the ASCII art generator.

        show_settings():
            Displays the settings UI.

        make_art():
            Handles the creation of ASCII art based on user input.

        save_art():
            Saves the generated ASCII art to a text file.

        get_art():
            Retrieves and returns the currently generated ASCII art, if any.
    """

    def __init__(
        self,
        settings_ui: UIInterface,
        arts_folder=None,
        controller: AsciiController = None,
    ):
        self.__controller = controller
        self.__settings_ui = settings_ui
        self.__arts_folder = arts_folder

    def set_controller(self, controller: AsciiController):
        self.__controller = controller
        self.__menu = self.__menu_build()

    def show(self):
        self.__menu.show()

    def __menu_build(self):
        return (
            MenuBuilder()
            .set_title("Ascii generator")
            .set_warning("Wrong input!")
            .set_input_text("Choose: ")
            .set_dynamic_title(self.get_art)
            .add_option("1", "1. Make art\n", self.make_art)
            .add_option("2", "2. Save art\n", self.save_art)
            .add_option("3", "3. Settings", self.show_settings)
            .add_stop_options(["0", "Exit", "exit"], "0. Exit")
            .build()
        )

    def show_settings(self):
        self.__settings_ui.show()

    def make_art(self):
        is_font_correct = self.__controller.is_font_correct()
        if not is_font_correct:
            print("Can't generate example, no such font\n CHANGE FONT TO AVAILABLE")
            return
        char_width = self.__controller.get_char_limit()
        if char_width == 0:
            print("Limits too low, can't create even 1 symbol, change settings")
            return
        message = (
            f"Make art up to {char_width} chars"
            + "\nIf want more change width, height, font or line breaking in settings"
            + "\n Input text : "
        )
        input = StringInput().input(message, [1, char_width], "Too long")
        art = self.__controller.generate(input)
        if len(art) < 1:
            try:
                int(input)
                print("Art empty, problem might be with numbers")
            except:
                print("Art empty, problem might be with punctuation marks")
            return
        if not art:
            print("Art can't created")
            return
        art = self.__controller.create_art(input)

    def save_art(self):
        art = self.__controller.get_art()
        if not art:
            return
        print(art)
        message = "Write name: "
        limit = 30  # hardcode variable of key lenght
        input = StringInput().input(message, [1, limit], "Too long")
        self.__controller.save_art(input)
        print(f"Save your art in {self.__arts_folder}/{input}.txt")

    def get_art(self):
        if self.__controller.is_art_exist():
            return "Current art \n" + self.__controller.get_art()
        else:
            return "No current art"
