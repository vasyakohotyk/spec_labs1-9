from shared.classes.json_data_access import JsonDataAccess
from shared.classes.key_data_access import KeyDataAccess


class DictJsonDataAccess(KeyDataAccess):
    """
    DictJsonDataAccess is a class for managing JSON data with dictionary-like access patterns.
    It wraps around JsonDataAccess to support caching and CRUD operations with key-based access.

    :param path: The path to the JSON file.
    :param is_caching: Flag to indicate whether caching is enabled.
    """

    def __init__(self, path=None, is_caching=True):
        self._data_access = JsonDataAccess(path, is_caching)

    def validate(self, is_can_be_empty=False):
        return self._data_access.validate_json(is_can_be_empty)

    def set_is_caching(self, is_caching):
        self._data_access.set_is_caching(is_caching)

    def __getitem__(self, key):
        data = self._data_access.get()
        return data.get(key)

    def __setitem__(self, key, value):
        data = self._data_access.get()
        data[key] = value
        self._data_access.set(data)

    def __delitem__(self, key):
        data = self._data_access.get()
        if key in data:
            del data[key]
            self._data_access.set(data)

    def __len__(self):
        data = self._data_access.get()
        return len(data)

    def __iter__(self):
        data = self._data_access.get()
        return iter(data)

    def __contains__(self, key):
        data = self._data_access.get()
        return key in data

    def keys(self):
        data = self._data_access.get()
        return list(data.keys())

    def values(self):
        data = self._data_access.get()
        return list(data.values())

    def items(self):
        data = self._data_access.get()
        return list(data.items())

    def clear(self):
        self._data_access.set({})

    def update(self, other):
        data = self._data_access.get()
        data.update(other)
        self._data_access.set(data)

    def get(self, key):
        data = self._data_access.get()
        return data.get(key, None)

    def set(self, key, value):
        data = self._data_access.get()
        data[key] = value
        self._data_access.set(data)

    def insert(self, key, value):
        data = self._data_access.get()
        data[key] = value
        self._data_access.set(data)
