"""
This module provides a generic in-memory key-value storage system.

Classes:
    KeyDataAccess(T): A generic class for in-memory key-value storage.

The KeyDataAccess class allows for storing and retrieving values associated with string keys.
"""
from typing import Dict, Generic, TypeVar

T = TypeVar("T")


class KeyDataAccess(Generic[T]):
    """
    KeyDataAccess is a generic class that acts as a simple in-memory
    storage with string keys and generic type values.

    Methods:
        __init__:
            Initializes an empty dictionary to store key-value pairs.

        set:
            Stores a value with the given key in the dictionary.

        get:
            Retrieves the value associated with the given key from the dictionary.
    """

    def __init__(self):
        """
        Initializes an empty dictionary to store key-value pairs.
        """
        self.list: Dict[str, T] = {}

    def set(self, key: str, data: T):
        """
        Stores a value with the given key in the dictionary.

        :param key: The key for the data to be stored.
        :param data: The data to be stored.
        """
        self.list[key] = data

    def get(self, key: str) -> T:
        """
        Retrieves the value associated with the given key from the dictionary.

        :param key: The key for the data to be retrieved.
        :return: The data associated with the given key.
        """
        return self.list[key]
