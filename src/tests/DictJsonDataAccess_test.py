import json
import unittest

from shared.classes.dict_json import DictJsonDataAccess


class TestDictJsonDataAccess(unittest.TestCase):
    """
    Test suite for the DictJsonDataAccess class to ensure its functionality.

    Methods
    -------
    setUp()
        Set up a JSON file with initial data for testing.
    tearDown()
        Remove the test file after tests are completed.
    test_getitem()
        Test retrieval of an item by key.
    test_setitem()
        Test setting an item by key.
    test_delitem()
        Test deletion of an item by key.
    test_len()
        Test the length of the data structure.
    test_iter()
        Test iteration over keys.
    test_contains()
        Test membership checking.
    test_keys()
        Test retrieval of all keys.
    test_values()
        Test retrieval of all values.
    test_clear()
        Test clearing all items.
    test_update()
        Test updating multiple items.
    test_get()
        Test the get method for retrieving values.
    test_set()
        Test the set method for setting values.
    test_insert()
        Test the insert method for adding values.
    test_different_types()
        Test storing and retrieving various data types.
    """

    def setUp(self):
        # Setting up a json file with initial data for testing
        self.file_path = "assets/test_file.json"
        with open(self.file_path, "w") as f:
            json.dump({"key1": "value1", "key2": "value2"}, f)
        self.data_access = DictJsonDataAccess(path=self.file_path, is_caching=False)

    def tearDown(self):
        # Removing the file after tests
        import os

        os.remove(self.file_path)

    def test_getitem(self):
        self.assertEqual(self.data_access["key1"], "value1")

    def test_setitem(self):
        self.data_access["test_key"] = "value"
        self.assertEqual(self.data_access["test_key"], "value")

    def test_delitem(self):
        del self.data_access["key1"]
        self.assertNotIn("key1", self.data_access)

    def test_len(self):
        self.assertEqual(len(self.data_access), 2)

    def test_iter(self):
        keys = []
        for key in self.data_access:
            keys.append(key)
        self.assertCountEqual(keys, ["key1", "key2"])

    def test_contains(self):
        self.assertIn("key1", self.data_access)

    def test_keys(self):
        self.assertCountEqual(self.data_access.keys(), ["key1", "key2"])

    def test_values(self):
        self.assertCountEqual(self.data_access.values(), ["value1", "value2"])

    def test_clear(self):
        self.data_access.clear()
        self.assertEqual(len(self.data_access), 0)

    def test_update(self):
        self.data_access.update({"key3": "value3"})
        self.assertIn("key3", self.data_access)

    def test_get(self):
        self.assertEqual(self.data_access.get("key1"), "value1")

    def test_set(self):
        self.data_access.set("test_key", "value")
        self.assertEqual(self.data_access["test_key"], "value")

    def test_insert(self):
        self.data_access.insert("test_key", "value")
        self.assertEqual(self.data_access["test_key"], "value")

    def test_different_types(self):
        test_cases = {
            "int_key": 123,
            "float_key": 123.456,
            "bool_key": True,
            "list_key": [1, 2, 3],
            "dict_key": {"nested_key": "nested_value"},
        }
        for key, value in test_cases.items():
            self.data_access[key] = value
            self.assertEqual(self.data_access[key], value)


if __name__ == "__main__":
    unittest.main()
