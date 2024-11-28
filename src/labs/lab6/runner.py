import subprocess
import unittest
from os import path

from config.settings_paths import current_dir
from shared.interfaces.runner_interface import RunnerInterface
from tests.Calculator_lab2_bll_test import CalculatorBllTest

TIMEOUT = 10


def run_in_new_terminal():
    """
    Executes a Python script in a new terminal window, waits for a specified
    timeout period, and then closes the terminal. The specified Python script
    to be executed is 'Calculator_lab2_bll_test.py' located in the 'tests'
    directory.

    :return: None
    """
    test_path = path.join("tests", "Calculator_lab2_bll_test.py")
    parent_dir = path.abspath(path.join(current_dir, '../../'))

    command = f"python {test_path} & timeout /t {TIMEOUT} & exit"
    subprocess.Popen(["start", "cmd", "/C", command], shell=True, cwd=current_dir)


class Runner(RunnerInterface):
    """
    class Runner(RunnerInterface):
    """

    @staticmethod
    def run():
        run_in_new_terminal()
