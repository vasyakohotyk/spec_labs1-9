from typing import Generic, TypeVar

T = TypeVar("T")


class DataAccess:
    """
    DataAccess is a generic class designed to store and retrieve data of any type.

    Attributes:
        self.data (T): The data attribute to store an instance of any type.

    Methods:
        __init__():
            Initializes the data attribute to None.

        set(data: T):
            Sets the data attribute with the provided data.

        get() -> T:
            Returns the stored data.
    """

    def __init__(self):
        self.data: T = None

    def set(self, data: T):
        self.data = data

    def get(self) -> T:
        return self.data
