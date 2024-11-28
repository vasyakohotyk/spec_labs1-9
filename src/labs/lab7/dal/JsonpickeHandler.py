from jsonpickle.handlers import BaseHandler, register

from shared.classes.ordered_set import OrderedSet


class OrderedSetHandler(BaseHandler):
    """
    OrderedSetHandler(BaseHandler)

    A class to handle serialization and deserialization of OrderedSet objects.

    Methods:

    flatten(obj, data)
        Converts the OrderedSet to a list of keys.

        Parameters:
        obj (OrderedSet): The OrderedSet instance to flatten.
        data (dict): Additional data to include in the serialization process.

        Returns:
        list: A list of keys from the OrderedSet.

    restore(data)
        Restores an OrderedSet from a list of keys.

        Parameters:
        data (list): The list of keys to populate the OrderedSet.

        Returns:
        OrderedSet: An OrderedSet instance populated with the provided keys.
    """

    def flatten(self, obj, data):
        return list(obj._data.keys())

    def restore(self, data):
        return OrderedSet(data)


def handle():
    """
    Handles the registration of an OrderedSet with its corresponding handler.

    :return: None
    """
    register(OrderedSet, OrderedSetHandler)
