"""
This module defines the AsciiGeneratorInterface, an interface for generating ASCII art 
from given data. It includes methods for generating ASCII representations, determining 
font capabilities, retrieving available fonts, and aligning text within a specified width.
"""

from abc import ABC, abstractmethod


class AsciiGeneratorInterface(ABC):
    """
    An interface for generating ASCII art from given data.

    Methods:
        generate(data, **kwargs):
            Generates an ASCII representation from the provided data.

        is_font_break_lines(font):
            Determines if the given font supports line breaks.

        get_fonts():
            Retrieves a list of available fonts.

        get_font_char_height(font):
            Returns the character height for the specified font.

        get_font_char_width(font):
            Returns the character width for the specified font.

        replace(data, bright_symbol, empty_symbol):
            Replaces characters in the data with the specified symbols.

        alignment_text(data, alignment, width):
            Aligns the given text to the specified alignment within the given width.
    """

    @staticmethod
    @abstractmethod
    def generate(data, **kwargs):
        """Generates an ASCII representation from the provided data."""

    @staticmethod
    @abstractmethod
    def is_font_break_lines(font):
        """Determines if the given font supports line breaks."""

    @staticmethod
    @abstractmethod
    def get_fonts():
        """Retrieves a list of available fonts."""

    @staticmethod
    @abstractmethod
    def get_font_char_height(font):
        """Returns the character height for the specified font."""

    @staticmethod
    @abstractmethod
    def get_font_char_width(font):
        """Returns the character width for the specified font."""

    @staticmethod
    @abstractmethod
    def replace(data, bright_symbol, empty_symbol):
        """Replaces characters in the data with the specified symbols."""

    @staticmethod
    @abstractmethod
    def alignment_text(data, alignment, width):
        """Aligns the given text to the specified alignment within the given width."""
