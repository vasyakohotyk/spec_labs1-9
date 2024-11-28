from labs.lab2.bll.Operation import Operation


class History:
    """
    Maintains a list of operations performed.

    :param history: A list to store the history of operations.
    :type history: list
    """

    def __init__(self, history):
        self.history = history

    @classmethod
    def empty(self):
        return self([])

    def add(self, operation: Operation):
        if not isinstance(operation, Operation):
            raise ValueError("Can't add operation to history")
        self.history.append(operation)

    def get(self):
        return self.history

    def clear(self):
        self.history = list()

    def to_string(self, decimals) -> str:
        string = "History of calculations:\n"
        if not self.history:
            return string + "History empty.\n"
        for record in self.history:
            if isinstance(record, Operation):
                string += record.to_string(decimals) + "\n"

        return string
