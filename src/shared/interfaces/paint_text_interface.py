"""
Module containing the PaintTextInterface for painting text with color.
"""

from abc import ABC, abstractmethod


class PaintTextInterface(ABC):
    """
    Interface for painting text with color.

    This abstract base class defines the methods that any concrete class 
    must implement to provide painting functionality for text.

    Methods:
        paint(text, color):
            Paint the given text with the specified color.

        get_colors():
            Retrieve the list of available colors.
    """

    @staticmethod
    @abstractmethod
    def paint(text, color):
        """
        Paint the given text with the specified color.
        
        Parameters:
        - text (str): The text to be painted.
        - color (str): The color to paint the text.
        """

    @staticmethod
    @abstractmethod
    def get_colors():
        """
        Retrieve the list of available colors.
        
        Returns:
        - list: A list of available color names.
        """
