"""
Module for handling various types of user input with validation.

Classes:
--------
VariantsInput:
    A base utility class for handling user input with validation against a set of options.
    
NumberBetweenInput:
    Inherits from VariantsInput and validates whether
    a given value falls within a specified integer range.

BoolInput:
    Inherits from VariantsInput and captures and validates user input as boolean values.

StringInput:
    Inherits from VariantsInput and validates whether a given
    value length falls within a specified integer range.
"""

from typing import Tuple, Union


class VariantsInput:
    """
    A utility class for handling user input with validation against a set of options.
    
    Methods
    -------
    input(cls, message, options=None, warning_message=None, is_finite=False)
        Prompts the user for input and validates the input against a set of options.
    validate(cls, value, options=None)
        Validates the user's input.
    in_wrong(cls, value, message)
        Prints a warning message when the user input is invalid.
    """

    @classmethod
    def input(cls, message, options=None, warning_message=None, is_finite=False):
        """Prompts the user for input and validates the input."""
        while True:
            value = input(message)
            if cls.validate(value, options):
                return value
            cls.in_wrong(warning_message or "Invalid input", value)
            if is_finite:
                break
        return None

    @classmethod
    def validate(cls, value, options=None):
        """Validates the user's input."""
        if not value:
            return False
        if options and value not in options:
            return False
        return True

    @classmethod
    def in_wrong(cls, message, value):
        """Prints a warning message when the user input is invalid."""
        print(f"{message} {value}")


class NumberBetweenInput(VariantsInput):
    """
    Validates whether a given value falls within a specified integer range.
    
    Methods:
        validate(value, options):
            Validates that a value is an integer within a specified range.
    """

    @classmethod
    def validate(cls, value, options=None):
        if not isinstance(options, list) or len(options) != 2:
            raise TypeError("Options should be a list of two elements.")
        if not all(isinstance(x, int) for x in options):
            raise TypeError("Both elements in options should be integers.")
        try:
            value = int(value)
        except ValueError:
            return False

        return options[0] <= value <= options[1]


class BoolInput(VariantsInput):
    """
    BoolInput class for handling boolean input from the user.
    It provides methods to capture and validate user input as boolean values.
    """

    @classmethod
    def default(cls, message=None):
        """Uses default message to prompt user for boolean input."""
        if not message:
            message = "Choose (y/n)"
        true_options = ["y", "yes"]
        false_options = ["n", "no", "not"]
        user_input = cls.input(message, [true_options, false_options])
        return user_input

    @classmethod
    def input(cls, message, options=None, warning_message=None, is_finite=False):
        """Prompts the user for boolean input and validates it."""
        true_options = options[0]
        try:
            false_options = options[1]
        except IndexError:
            false_options = []
        while True:
            value = input(message)
            if cls.validate(value.lower(), true_options):
                return True
            if cls.validate(value.lower(), false_options):
                return False
            cls.in_wrong(warning_message or "Invalid input", value)
            if is_finite:
                return False


class StringInput(VariantsInput):
    """
    Validates whether a given value length falls within a specified integer range.
    
    Methods:
        validate(value, options):
            Validates that a value is an integer within a specified range.
    """

    @classmethod
    def input(
            cls, message, options: Union[None, Tuple[int, int]] = None,
            warning_message=None, is_finite=False,
    ):
        """Prompts the user for input and validates the length of the input."""
        no_limit = False
        try:
            lower_limit = options[0]
            upper_limit = options[1]
        except (TypeError, IndexError):
            no_limit = True
        while True:
            value = input(message)
            if no_limit:
                return value
            value_len = len(value)
            if NumberBetweenInput.validate(value_len, [lower_limit, upper_limit]):
                return value
            cls.in_wrong(warning_message or "Invalid length of value", value)
            if is_finite:
                break
        return None
