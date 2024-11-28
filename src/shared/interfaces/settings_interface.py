"""
This module defines an abstract base class for settings.

Classes
-------
SettingsInterface : ABC
    An abstract base class that enforces two core methods: `set_default` and `__str__`.
"""
from abc import ABC, abstractmethod


class SettingsInterface(ABC):
    """
    SettingsInterface is an abstract base class that mandates implementations for two core methods.
 
    Methods
    -------
    set_default():
        Abstract method that should be overridden to set default settings.

    __str__():
        Abstract method that should be overridden to provide a string representation of the 
        settings instance.
    """

    @abstractmethod
    def set_default(self):
        """
        Abstract method to set default settings.
        """

    @abstractmethod
    def __str__(self):
        """
        Abstract method to provide string representation of settings instance.
        """
