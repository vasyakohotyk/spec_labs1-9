import logging

from shared.classes.dict_json import DictJsonDataAccess
from shared.services.relative_to_absolute_path import absolute

logger = logging.getLogger(__name__)


class UserSettingsModel:
    """
    UserSettingsModel provides methods to interact with user-specific settings stored in a JSON file.

    Attributes:
        __settings (DictJsonDataAccess): Object used to access and manipulate the settings data.

    Methods:
        __init__(path):
            Initializes the UserSettingsModel with a path to the settings file.
            Validates the settings file and raises a KeyError if it doesn't exist.

        get_selected_fields():
            Retrieves the 'selected_fields' from the settings.

        get_table_fields():
            Retrieves the 'table' field from the selected fields in the settings.

        set_table_fields(table_fields):
            Sets the 'table' field in the selected fields of the settings.

        get_list_fields():
            Retrieves the 'list' field from the selected fields in the settings.

        set_list_fields(list_fields):
            Sets the 'list' field in the selected fields of the settings.

        get_is_table_print():
            Retrieves the 'is_table_print' setting.

        set_is_table_print(is_table_print):
            Sets the 'is_table_print' setting.

        get_is_list_print():
            Retrieves the 'is_list_print' setting.

        set_is_list_print(is_list_print):
            Sets the 'is_list_print' setting.

        get_lang():
            Retrieves the 'lang' setting.

        set_lang(lang):
            Sets the 'lang' setting.

        get_items_amount():
            Retrieves the 'items_amount' setting.

        set_items_amount(max_results):
            Sets the 'items_amount' setting.

        get_field_styles():
            Retrieves the 'field_styles' setting.
    """

    def __init__(self, path):
        self.__settings = DictJsonDataAccess(path)
        if not self.__settings.validate(is_can_be_empty=False):
            logger.critical("There no user settings file")
            raise KeyError("Settings doesn't exist")

    def get_selected_fields(self):
        return self.__settings.get("selected_fields")

    def get_table_fields(self):
        selected_fields = self.get_selected_fields()
        return selected_fields.get("table")

    def set_table_fields(self, table_fields):
        selected_fields = self.get_selected_fields()
        selected_fields["table"] = table_fields
        self.__settings.set("selected_fields", selected_fields)

    def get_list_fields(self):
        selected_fields = self.get_selected_fields()
        return selected_fields.get("list")

    def set_list_fields(self, list_fields):
        selected_fields = self.get_selected_fields()
        selected_fields["list"] = list_fields
        self.__settings.set("selected_fields", selected_fields)

    def get_is_table_print(self):
        return self.__settings.get("is_table_print")

    def set_is_table_print(self, is_table_print):
        self.__settings.set("is_table_print", is_table_print)

    def get_is_list_print(self):
        return self.__settings.get("is_list_print")

    def set_is_list_print(self, is_list_print):
        self.__settings.set("is_list_print", is_list_print)

    def get_lang(self):
        return self.__settings.get("lang")

    def set_lang(self, lang):
        self.__settings.set("lang", lang)

    def get_items_amount(self):
        return self.__settings.get("items_amount")

    def set_items_amount(self, max_results):
        self.__settings.set("items_amount", max_results)

    def get_field_styles(self):
        return self.__settings.get("field_styles")
