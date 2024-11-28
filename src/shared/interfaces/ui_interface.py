"""
Module docstring for UIInterface
Defines the abstract base class for User Interface (UI).
"""

from abc import ABC, abstractmethod


class UIInterface(ABC):
    """
    UIInterface

    This abstract base class defines the interface for a User Interface (UI).

    Methods
    -------
    show()
        This abstract method should be implemented to display the UI to the user.

    set_controller(controller)
        This abstract method should be implemented to set a controller for the UI.
    """

    @abstractmethod
    def show(self):
        """
        Displays the UI to the user.
        """

    @abstractmethod
    def set_controller(self, controller):
        """
        Sets a controller for the UI.
        """
