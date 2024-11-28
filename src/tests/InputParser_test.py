import unittest

from labs.lab7.bll.InputParser import InputParser


class TestInputParser(unittest.TestCase):
    """
    Unit tests for InputParser class focusing on various scenarios for the _matches_query method.
    """

    def test_matches_query_success(self):

        item = {"name": "test", "value": "query_example"}
        field_list = ["value"]
        query = (
            r"query_\w+"  # Correct regex to match 'query_' followed by word characters
        )
        result = InputParser._matches_query(item, field_list, query)
        self.assertTrue(result, "Query should match item for these values.")

    def test_matches_query_fail(self):
        item = {"name": "test", "value": "wrong_value"}
        field_list = ["value"]
        query = r"query_example"
        result = InputParser._matches_query(item, field_list, query)
        self.assertFalse(result, "Query should not match item for these values.")

    def test_matches_query_wrong_field(self):
        item = {"name": "test"}
        field_list = ["value"]
        query = r"any_value"
        result = InputParser._matches_query(item, field_list, query)
        self.assertFalse(result, "Query should not match item with no matching field.")

    def test_matches_query_missing_value_field(self):
        item = {"name": "test", "value": None}
        field_list = ["value"]
        query = r"query_example"
        result = InputParser._matches_query(item, field_list, query)
        self.assertFalse(result, "Query should not match item with None value.")

    def test_matches_query_complex_nested_field(self):
        item = {"name": "test", "detail": {"name": "query_example"}}
        field_list = ["detail", "name"]
        query = r"query_example"
        result = InputParser._matches_query(item, field_list, query)
        self.assertTrue(result, "Query should match nested field value in the item.")


if __name__ == "__main__":
    unittest.main()
