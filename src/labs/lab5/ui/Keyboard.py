from OpenGL.GLUT import *

from labs.lab5.dal.Keyboard import keys_map


class KeyboardHandler:
    """
    class KeyboardHandler:
        Handles keyboard inputs and interacts with a controller to process key events.

        Methods:

            __init__(self, controller=None):
                Initializes the KeyboardHandler with an optional controller.

            set_controller(self, controller):
                Sets the controller that the KeyboardHandler will use for processing key events.

            special_keyboard_up(self, key, x, y):
                Handles special key up events. Maps the key to a string representation if available, then calls keyboard_up method.

            special_keyboard(self, key, x, y):
                Handles special key down events. Maps the key to a string representation if available, then calls keyboard method.

            keyboard_up(self, key, x, y):
                Processes a key release event. Decodes the key from bytes to a string if necessary and calls the controller's handle_keyboard_up method.

            keyboard(self, key, x, y):
                Processes a key press event. Decodes the key from bytes to a string if necessary, maps the key to a new key if specified, handles key modifiers, and calls the controller's handle_keyboard method.
    """

    def __init__(self, controller=None):
        self.controller = controller

    def set_controller(self, controller):
        self.controller = controller

    def special_keyboard_up(self, key, x, y):
        str_key = keys_map.get(key)
        if str_key:
            self.keyboard_up(str_key, x, y)

    def special_keyboard(self, key, x, y):
        str_key = keys_map.get(key)
        if str_key:
            self.keyboard(str_key, x, y)

    def keyboard_up(self, key, x, y):
        if isinstance(key, bytes):
            try:
                key = key.decode("utf-8")
            except UnicodeDecodeError:
                # can add more languages here
                return
        self.controller.handle_keyboard_up(key)

    def keyboard(self, key, x, y):
        modifiers = glutGetModifiers()
        if isinstance(key, bytes):
            try:
                key = key.decode("utf-8")
            except UnicodeDecodeError:
                # can add more languages here
                return
        key.lower()
        new_key = keys_map.get(key)
        if new_key:
            key = new_key
        if modifiers:
            modifiers = keys_map.get(key)
        self.controller.handle_keyboard(key, modifiers)
