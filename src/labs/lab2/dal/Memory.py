class Memory:
    """

    This class provides functionality for basic memory operations such as setting a value,
    adding to the current value, retrieving the current value, and clearing the memory.

    class Memory:

    def __init__(self, init_value=0.0) -> None:
        Initializes the Memory instance with an initial value.

        Parameters:
            init_value (float): The initial value to set for memory. Default is 0.0.

    def set(self, value):
        Sets the memory to the given value.

        Parameters:
            value (float): The value to set the memory to.

        Returns:
            float: The current memory value after setting.

    def add(self, value):
        Adds the given value to the current memory value.

        Parameters:
            value (float): The value to add to the current memory.

        Returns:
            float: The current memory value after adding.

    def get(self):
        Retrieves the current memory value.

        Returns:
            float: The current memory value.

    def clear(self):
        Clears the memory by setting its value to 0.0.

        Returns:
            float: The current memory value after clearing.
    """

    def __init__(self, init_value=0.0) -> None:
        self.memory = init_value

    def set(self, value):
        self.memory = value
        return self.memory

    def add(self, value):
        self.memory += value
        return self.memory

    def get(self):
        return self.memory

    def clear(self):
        self.memory = 0.0
        return self.memory
