from config.settings_paths import settings_path_lab2
from labs.lab2.ui.Calculator import Calculator
from shared.interfaces.runner_interface import RunnerInterface


class Runner(RunnerInterface):
    """
    Runner class implementing the RunnerInterface.

    This class provides a static method to initialize and run the Calculator.

    Methods
    -------
    run():
        Initializes the Calculator with a given settings path and starts the menu.
    """

    @staticmethod
    def run():
        calculator = Calculator(settings_path_lab2)
        calculator.menu()


if __name__ == "__main__":
    Runner.run()
