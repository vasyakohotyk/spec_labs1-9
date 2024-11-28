"""
This module provides a Runner class to execute the main process of lab1
using a predefined settings path.
"""

from config.settings_paths import settings_path_lab1
from labs.lab1.ui import menu
from shared.interfaces.runner_interface import RunnerInterface


class Runner(RunnerInterface):
    """
    Runner is a class that implements the RunnerInterface.
    This class contains functionality to execute this lab main process.

    Methods
    -------
    run():
        Static method that triggers the execution of this lab main process using a
        predefined settings path.
    """

    @staticmethod
    def run():
        menu.run(settings_path_lab1)


if __name__ == "__main__":
    Runner.run()
