import logging

from shared.classes.dict_json import DictJsonDataAccess

logger = logging.getLogger(__name__)


class HistoryModel:
    """
    class HistoryModel:
        Represents a history model that manages historical events.

        Methods
        -------
        __init__(path, results_to_save=5)
            Initializes the HistoryModel with a given path and number of results to save.

        get_history()
            Retrieves the historical events stored.

        add(query, regex, regex_field, fields, results)
            Adds a new event to the historical data.

        clear_history()
            Clears all stored historical events.
    """

    def __init__(self, path, results_to_save=5):
        self.__history = DictJsonDataAccess(path)
        self.results_to_save = results_to_save
        if not self.__history.validate(is_can_be_empty=True):
            logger.critical("There no history file")
            raise KeyError("History file doesn't exist")

    def get_history(self):
        return self.__history.get("history")

    def add(self, query, regex, regex_field, fields, results):
        event = {
            "query": query,
            "regex": regex,
            "regex_field": regex_field,
            "fields": fields,
            "results": results,
        }
        history = self.__history.get("history")
        history = history[1 : self.results_to_save - 1]
        history.append(event)
        self.__history.set("history", history)

    def clear_history(self):
        self.__history.set("history", [])
