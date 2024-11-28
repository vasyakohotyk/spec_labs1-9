import logging
from dataclasses import field

from requests import HTTPError

from labs.lab7.bll.GoogleBooksAPI import GoogleBooksAPI
from labs.lab7.bll.InputParser import InputParser
from labs.lab7.bll.ItemExtraction import extract_data_items
from labs.lab7.dal.FileHandler import FileHandler
from labs.lab7.dal.HistoryModel import HistoryModel
from labs.lab7.dal.SettingsModel import SettingsModel
from labs.lab7.dal.UserSettingsModel import UserSettingsModel
from shared.services.relative_to_absolute_path import absolute

logger = logging.getLogger(__name__)


class Controller:
    """
    Controller

    PUBLISHING_DATE_FIELD
        A constant string representing the initial publishing date field.

    REGEX_FOR_DATE
        A initial regular expression pattern for matching dates ranging from 2017 to 2029.

    LAST_QUERY
        A initial constant string representing the last query made by the user.

    __init__(self, settings, history, user_settings, api)
        Initializes the Controller with settings, history, user settings, and API models.

    set_last_query(self, query)
        Sets the last search query.

    set_last_regex(self, regex)
        Sets the regular expression for filtering results.

    set_regex_field_name(self, field)
        Sets the field name for applying the regular expression.

    clear_regex_field_name(self)
        Clears the field name and regular expression for filtering results.

    is_regex(query)
        Static method to check if the given query is a regular expression.

    parse_query(data, field, query)
        Static method to parse data based on the field and query.

    search_for_table(self)
        Executes a search configured for table format.

    search_for_list(self)
        Executes a search configured for list format.

    _search_generic(self, check_func, fields_func, search_type)
        Executes a generic search based on the provided checking function, fields, and search type.

    search(self, fields_names=None)
        Executes a search with the specified field names.

    add_to_history(self, query, regex, regex_field_name, fields_names, results)
        Adds the given search parameters and results to the history.

    _fetch_additional_results(self, query, lang, start_index, max_results, fields, is_total_items=False)
        Fetches additional search results using the API and applies regex if needed.

    _apply_regex_if_needed(self, data)
        Applies regular expression on the data if regex and field name are set.

    name_to_field(self, field_name, fields_dict=None)
        Converts a field name to its corresponding field value using the fields dictionary.

    names_to_fields(self, fields_names)
        Converts a list of field names to their corresponding field values.

    do_regex(self, data)
        Applies regex filtering on the data.

    get_regex_field_name(self)
        Returns the field name associated with the regex.

    get_regex(self)
        Returns the last used regex pattern.

    get_query(self)
        Returns the last used query.

    get_selected_fields(self, mode)
        Returns the selected fields based on the given mode (List or Table).

    set_selected(self, chosen_fields, mode="List")
        Sets the selected fields for the given mode (List or Table).

    set_is_list(self, is_list)
        Sets whether the data is in list format.

    set_is_table(self, is_table)
        Sets whether the data is in table format.

    get_is_list(self)
        Returns whether the data is in list format.

    get_is_table(self)
        Returns whether the data is in table format.

    get_fields(self)
        Returns the available fields from settings.

    get_fields_keys(self)
        Returns the keys of available fields from settings.

    get_history(self)
        Returns the search history.

    clear_history(self)
        Clears the search history.

    get_languages(self)
        Returns the supported languages from settings.

    get_max_results(self)
        Returns the maximum number of results per search.

    _get_default_save_dir(self)
        Returns the default save directory from settings.

    get_default_save_dir"""

    PUBLISHING_DATE_FIELD = "Publishing date"
    REGEX_FOR_DATE = "^201[7-9]|^202"
    LAST_QUERY = "Python"

    def __init__(
        self,
        settings: SettingsModel,
        history: HistoryModel,
        user_settings: UserSettingsModel,
        api: GoogleBooksAPI,
    ):
        self.settings = settings
        self.history = history
        self.user_settings = user_settings
        self.api = api
        self.last_query = self.LAST_QUERY
        self.last_regex = self.REGEX_FOR_DATE
        self.regex_field_name = self.PUBLISHING_DATE_FIELD

    def set_last_query(self, query):
        self.last_query = query

    def set_last_regex(self, regex):
        self.last_regex = regex

    def set_regex_field_name(self, field):
        self.regex_field_name = field

    def clear_regex_field_name(self):
        self.last_regex = None
        self.regex_field_name = None

    @staticmethod
    def is_regex(query):
        return InputParser.is_regex(query)

    @staticmethod
    def parse_query(data, field, query):
        is_wrapped = hasattr(data, "items") and field.startswith("items.")
        if is_wrapped:
            data = data["items"]
            field = field.replace("items.", "", 1)
        new_data = InputParser.parse_query(data, field, query)
        if is_wrapped:
            new_data = {"items": new_data}
        return new_data

    def search_for_table(self):
        return self._search_generic(
            self.get_is_table, self.user_settings.get_table_fields, "table"
        )

    def search_for_list(self):
        return self._search_generic(
            self.get_is_list, self.user_settings.get_list_fields, "list"
        )

    def _search_generic(self, check_func, fields_func, search_type):
        if not check_func():
            return None
        fields = fields_func()
        try:
            return self.search(fields), fields
        except Exception as e:
            logger.error(f"Get error in {search_type} search!", exc_info=e)
            raise

    def search(self, fields_names=None):
        query = self.last_query
        if not query:
            return None
        if self.regex_field_name:
            fields_names.append(self.regex_field_name)
        lang = self.user_settings.get_lang()
        max_results = self.settings.get_max_results()
        items_amount = self.user_settings.get_items_amount()
        fields = self.names_to_fields(fields_names)
        items = []
        start_index = 0
        total_items = None
        while len(items) < items_amount and (
            total_items is None or start_index < total_items
        ):
            is_total_items = total_items is None
            try:
                response, total_items = self._fetch_additional_results(
                    query, lang, start_index, max_results, fields, is_total_items
                )
            except Exception as e:
                logger.error("Get error in general search!", exc_info=e)
                raise
            if not response:
                break
            items.extend(response)
            start_index += max_results
        result = {"items": items[:items_amount]}
        self.add_to_history(
            query, self.last_regex, self.regex_field_name, fields_names, result
        )
        return result

    def add_to_history(self, query, regex, regex_field_name, fields_names, results):
        self.history.add(query, regex, regex_field_name, fields_names, results)

    def _fetch_additional_results(
        self, query, lang, start_index, max_results, fields, is_total_items=False
    ):
        try:
            temp_result, url = self.api.search(
                query, lang, start_index, max_results, fields
            )
            temp_result = self._apply_regex_if_needed(temp_result)
            if not temp_result["items"]:
                return [], None
            total_items = temp_result.get("totalItems") if is_total_items else None
            return temp_result["items"], total_items
        except HTTPError as e:
            logger.error("Get HTTP error when fetching results", exc_info=e)
            raise Exception(f"Bad API response: {e}") from e
        except Exception as e:
            logger.error("Get non-HTTP error", exc_info=e)
            raise Exception(str(e)) from e

    def _apply_regex_if_needed(self, data):
        return (
            self.do_regex(data) if self.last_regex and self.regex_field_name else data
        )

    def name_to_field(self, field_name, fields_dict=None):
        if fields_dict is None:
            fields_dict = self.settings.get_fields()
        field_name = str(field_name)
        return fields_dict.get(field_name)

    def names_to_fields(self, fields_names):
        fields = []
        fields_dict = self.settings.get_fields()
        for name in fields_names or []:
            field = self.name_to_field(name, fields_dict)
            if field:
                fields.append(field)
        return fields

    def do_regex(self, data):
        if not self.last_regex or not self.regex_field_name:
            logger.critical("Wrong using of function do_regex, not checked data before")
            raise ValueError("No regex and field to do regex")
        field = self.name_to_field(self.regex_field_name)
        return self.parse_query(data, field, self.last_regex)

    def get_regex_field_name(self):
        return self.regex_field_name

    def get_regex(self):
        return self.last_regex

    def get_query(self):
        return self.last_query

    def get_selected_fields(self, mode):
        if mode == "List":
            return self.user_settings.get_list_fields()
        if mode == "Table":
            return self.user_settings.get_table_fields()
        raise ValueError("Wrong mode")

    def set_selected(self, chosen_fields, mode="List"):
        if mode == "List":
            self.user_settings.set_list_fields(chosen_fields)
        elif mode == "Table":
            self.user_settings.set_table_fields(chosen_fields)
        else:
            raise ValueError("Wrong mode")

    def set_is_list(self, is_list):
        self.user_settings.set_is_list_print(is_list)

    def set_is_table(self, is_table):
        self.user_settings.set_is_table_print(is_table)

    def get_is_list(self):
        return self.user_settings.get_is_list_print()

    def get_is_table(self):
        return self.user_settings.get_is_table_print()

    def get_fields(self):
        return self.settings.get_fields()

    def get_fields_keys(self):
        return self.settings.get_fields_keys()

    def get_history(self):
        return self.history.get_history()

    def clear_history(self):
        self.history.clear_history()

    def get_languages(self):
        return self.settings.get_languages()

    def get_max_results(self):
        return self.settings.get_max_results()

    def _get_default_save_dir(self):
        return self.settings.get_default_save_dir()

    def get_default_save_dir(self):
        return absolute(self._get_default_save_dir())

    def get_logger_path(self):
        path = self.settings.get_logger_path()
        if not path:
            raise KeyError("There no logger path provided!")

        absolute_path = absolute(path)
        return absolute_path

    def get_default_file_name(self):
        return self.settings.get_default_file_name()

    def get_field_styles(self):
        return self.user_settings.get_field_styles()

    def flat_search(self, mode="List"):
        data, selected_fields = (
            self.search_for_list() if mode == "List" else self.search_for_table()
        )
        fields_dict = self.settings.get_fields()
        extracted_items = extract_data_items(data, selected_fields, fields_dict)
        return extracted_items, selected_fields

    def save(self, file_path, data=None):
        if file_path.endswith(".json"):
            self.save_to_json(file_path)
        elif file_path.endswith(".csv"):
            self.save_to_csv(file_path)
        else:
            FileHandler.save_to_text(data, file_path)

    def save_to_json(self, file_path):
        result = {}
        if self.get_is_table():
            data = self.search_for_table()
            result["table"] = data
        if self.get_is_list():
            data = self.search_for_list()
            result["list"] = data
        FileHandler.save_to_json(result, file_path)

    def save_to_csv(self, file_path):
        if self.get_is_table():
            data, data_fields = self.flat_search("Table")
            table_path = file_path.replace(".csv", "_table.csv")
            FileHandler.save_to_csv(data, data_fields, table_path)
        if self.get_is_list():
            data, data_fields = self.flat_search("List")
            list_path = file_path.replace(".csv", "_list.csv")
            FileHandler.save_to_csv(data, data_fields, list_path)
