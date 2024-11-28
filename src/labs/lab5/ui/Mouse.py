from OpenGL.GLUT import *


class MouseHandler:
    """
    MouseHandler class is responsible for handling mouse events and delegating them to the specified controller.

    Methods:

        __init__(controller=None):
            Initializes the MouseHandler with an optional controller.

        set_controller(controller):
            Sets the controller to delegate mouse events to.

        mouse(button, state, x, y):
            Handles mouse button events, passing the button, state, and coordinates to the controller.

        wheel(wheel, direction, x, y):
            Handles mouse wheel events, passing the wheel, direction, and coordinates to the controller.

        motion(x, y):
            Handles mouse motion events, passing the coordinates to the controller.
    """

    def __init__(self, controller=None):
        self.controller = controller

    def set_controller(self, controller):
        self.controller = controller

    def mouse(self, button, state, x, y):
        self.controller.handle_mouse(button, state, x, y)

    def wheel(self, wheel, direction, x, y):
        self.controller.handle_wheel(wheel, direction, x, y)

    def motion(self, x, y):
        self.controller.handle_motion(x, y)
