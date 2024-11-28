"""
This module contains the definition of the AsciiGenerator abstract base class 
which defines the interface for generating ASCII art. The module also provides 
static methods for aligning text and replacing characters in a given data string.
"""

from abc import ABC, abstractmethod


class AsciiGenerator(ABC):
    """
    Abstract base class for ASCII art generators.

    Methods:
        generate(data, **kwargs):
            Abstract method to generate ASCII art based on provided data.

        is_font_break_lines(font):
            Abstract method to check if a font breaks lines.

        get_fonts():
            Abstract method to get a list of available fonts.

        get_font_char_height(font):
            Abstract method to get the character height of a given font.

        get_font_char_width(font):
            Abstract method to get the character width of a given font.

        alignment_text(text, alignment, width):
            Aligns the given text to the specified alignment ('left', 'center', 'right')
             within the given width.

        replace(data, bright_symbol, empty_symbol):
            Replaces non-space characters in data with bright_symbol and space
            characters with empty_symbol.
    """

    @staticmethod
    @abstractmethod
    def generate(data, **kwargs):
        """
        Generates ASCII art based on the provided data.
        
        Args:
            data (str): The input data for generating ASCII art.
            **kwargs: Additional keyword arguments for customization.
        
        Returns:
            str: The generated ASCII art.
        """

    @staticmethod
    @abstractmethod
    def is_font_break_lines(font):
        """
        Checks if the given font breaks lines.
        
        Args:
            font (str): The name of the font to check.
        
        Returns:
            bool: True if the font breaks lines, False otherwise.
        """

    @staticmethod
    @abstractmethod
    def get_fonts():
        """
        Gets a list of available fonts.
        
        Returns:
            list: A list of available font names.
        """

    @staticmethod
    @abstractmethod
    def get_font_char_height(font):
        """
        Gets the character height of the given font.
        
        Args:
            font (str): The name of the font.
        
        Returns:
            int: The character height of the font.
        """

    @staticmethod
    @abstractmethod
    def get_font_char_width(font):
        """
        Gets the character width of the given font.
        
        Args:
            font (str): The name of the font.
        
        Returns:
            int: The character width of the font.
        """

    @staticmethod
    def alignment_text(text: str, alignment, width):
        """
        Aligns the given text to the specified alignment within the given width.
        
        Args:
            text (str): The text to align.
            alignment (str): The alignment type ('left', 'center', 'right').
            width (int): The total width for alignment.
        
        Returns:
            str: The aligned text.
        
        Raises:
            ValueError: If the alignment type is invalid.
        """
        lines = text.splitlines()
        aligned_text = []
        if alignment == "right":
            for row in lines:
                aligned_text.append((" " * (width - len(row) - 1)) + row)
        elif alignment == "center":
            for row in lines:
                free_space_amound = int((width - len(row)) / 2)
                free_space = " " * free_space_amound
                aligned_text.append(free_space + row + free_space)
        elif alignment == "left":
            for row in lines:
                aligned_text.append(row + (" " * (width - len(row) - 1)))
        else:
            raise ValueError("Wrong aligned")
        return "\n".join(aligned_text)

    @staticmethod
    def replace(data: str, bright_symbol, empty_symbol):
        """
        Replaces non-space characters in data with bright_symbol and space
        characters with empty_symbol.
        
        Args:
            data (str): The input data string.
            bright_symbol (str): The symbol to replace non-space characters.
            empty_symbol (str): The symbol to replace space characters.
        
        Returns:
            str: The data string after replacements.
        """
        lines = data.splitlines()
        replaced_lines = []

        for line in lines:
            replaced_line = "".join(
                empty_symbol if char.isspace() else bright_symbol for char in line
            )
            replaced_lines.append(replaced_line)
        replaced_data = "\n".join(replaced_lines)
        return replaced_data
