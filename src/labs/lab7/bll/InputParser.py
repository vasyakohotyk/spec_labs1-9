import logging
import re

logger = logging.getLogger(__name__)


class InputParser:
    """
    Class for parsing and querying data with support for nested fields and regular expressions.
    """

    @staticmethod
    def is_regex(query_string):
        try:
            re.compile(query_string)
            return True
        except re.error:
            logger.debug("Invalid regex")
            return False

    @staticmethod
    def test_is_regex_invalid_regex(self):
        self.assertFalse(InputParser.is_regex("{[]{"))

    @staticmethod
    def parse_query(data, field, query):
        field_list = field.split(".")
        return [
            item for item in data if InputParser._matches_query(item, field_list, query)
        ]

    @staticmethod
    def _matches_query(item, field_list, query):
        field_value = InputParser._get_nested_value(item, field_list)
        return re.search(query, str(field_value)) is not None

    @staticmethod
    def _get_nested_value(data, fields):
        for field in fields:
            if isinstance(data, dict):
                data = data.get(field)
            else:
                return None
        return data
