import logging

import requests

logger = logging.getLogger(__name__)


class GoogleBooksAPI:
    """
    Class for interacting with the Google Books API.

    Methods
    -------
    __init__(api_key=None)
        Initializes the GoogleBooksAPI class with an optional API key.

    search(query, language='en', start_index=0, max_results_count=40, fields=None)
        Searches for books matching the query with optional parameters for language, start index, maximum results count, and specific fields to include in the response.

    _handle_error(error)
        Handles errors encountered during the request to the Google Books API and logs appropriate error messages.
    """

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/books/v1/volumes"

    def search(
        self, query, language="en", start_index=0, max_results_count=40, fields=None
    ):
        fields = ",".join(fields) if fields else None
        params = {
            "q": query,
            "langRestrict": language,
            "startIndex": start_index,
            "maxResults": max_results_count,
            "fields": fields,
        }
        if self.api_key:
            params["key"] = self.api_key

        response = requests.get(self.base_url, params=params)
        try:
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            return self._handle_error(error)

        return response.json(), response.url

    def _handle_error(self, error):
        if isinstance(error, requests.exceptions.HTTPError):
            logger.error(error)
            return {"error": str(error)}
        elif isinstance(error, requests.exceptions.ConnectionError):
            logger.critical(
                "There is no internet connection or connection error:", error
            )
            return {
                "error": "No internet connection or connection error: " + str(error)
            }
        else:
            logger.critical("Error not related to connection or HTTP:", error)
            return {"error": str(error)}
