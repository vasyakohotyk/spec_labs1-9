"""
This module provides an implementation of an OrderedSet,
which is a set that maintains the order of elements.
It is implemented using Python's OrderedDict from the collections module
to keep track of the insertion order.
"""
from collections import OrderedDict


class OrderedSet:
    """
    class OrderedSet:
    An ordered set implementation using OrderedDict to maintain element order.
    """

    def __init__(self, data=None):
        """
        :param data: An optional iterable of items to initialize the OrderedDict. If provided, each
         item from the iterable will be added as a key to the OrderedDict with a value of None.
         If not provided, an empty OrderedDict is initialized.
        """
        self._data = (
            OrderedDict((item, None) for item in data) if data else OrderedDict()
        )

    def clear(self):
        """
        Clears all the items in the internal data structure.

        :return: None
        """
        self._data.clear()

    def add(self, item):
        """
        :param item: The item to be added to the collection.
        :return: None
        """
        if item not in self._data:
            self._data[item] = None

    def discard(self, item):
        """
        :param item: The item to be discarded from the internal data store.
        :return: None. The method removes the item from the data store if it exists.
        """
        if item in self._data:
            del self._data[item]

    def remove(self, item):
        """
        :param item: The item to be removed from the OrderedSet.
        :return: None
        :raises KeyError: If the item is not found in the OrderedSet.
        """
        if item in self._data:
            del self._data[item]
        else:
            raise KeyError(f"Item {item} not found in OrderedSet")

    def __contains__(self, item):
        """
        :param item: The object to check for membership in the collection.
        :return: True if the item exists in the collection, False otherwise.
        """
        return item in self._data

    def __repr__(self):
        """
        :return: A comma-separated string of the keys in the _data dictionary.
        """
        return f"{', '.join(self._data.keys())}"

    def __iter__(self):
        """
        Returns an iterator over the keys of the internal data structure.

        :return: An iterator over the keys
        """
        return iter(self._data.keys())

    def index(self, item):
        """
        :param item: The item to find the index of within the OrderedSet
        :return: The index of the item if it exists within the OrderedSet
        :raises KeyError: If the item is not found in the OrderedSet
        """
        if item in self._data:
            return list(self._data.keys()).index(item)
        raise KeyError(f"Item {item} not found in OrderedSet")

    def __getstate__(self):
        """
        :return: A list containing the keys from the object's _data attribute.
        """
        return list(self._data.keys())

    def __setstate__(self, state):
        """
        :param state: The state input that will be transformed into an OrderedDict.
        :return: None
        """
        self._data = OrderedDict((item, None) for item in state)
