import logging

from docs.generator import *
from labs.lab9.dal.SettingsModel import SettingsModel
from shared.services.relative_to_absolute_path import absolute, root_dir

logger = logging.getLogger(__name__)
import logging
import pydoc
import webbrowser

logger = logging.getLogger(__name__)


class Controller:
    """
    Controller class handles document directory paths and logging paths,
    generating documents and rendering module documentation.

    Methods
    -------
    __init__(settings: SettingsModel)
        Initializes the Controller with given settings.

    get_docs_dir()
        Returns the absolute path of the documents directory.

    get_logger_path()
        Returns the absolute path of the logger path.

    generate_docs()
        Generates documentation in the documents directory.

    get_module_docs_text(module_name)
        Returns the documentation text for a given module.

    open_pydoc_browser(module_name)
        Opens the documentation for a given module in a web browser.

    get_root_path()
        Returns the root directory path.
    """

    def __init__(self, settings: SettingsModel):
        self.settings = settings

    def get_docs_dir(self):
        path = absolute(self.settings.get_docs_dir())
        return path

    def get_logger_path(self):
        path = absolute(self.settings.get_logger_path())
        return path

    def generate_docs(self):
        generate_docs(self.get_docs_dir())


    @staticmethod
    def get_module_docs_text(module_name):
        doc_text = pydoc.render_doc(module_name)
        return doc_text

    @staticmethod
    def open_pydoc_browser(module_name):
        absolute_path = absolute(["docs", f"{module_name}.html"])
        webbrowser.open(absolute_path)

    @staticmethod
    def get_root_path():
        path = root_dir()
        return path
