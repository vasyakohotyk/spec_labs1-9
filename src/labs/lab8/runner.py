from labs.lab8.init import main
from shared.interfaces.runner_interface import RunnerInterface


class Runner(RunnerInterface):
    """
    Class Runner inherits from RunnerInterface to implement
    a specific way to execute tasks by calling the main function.

    Methods:
    @staticmethod
    def run():
        Calls the main function to execute the primary logic of this runner.
    """

    @staticmethod
    def run():
        main()


if __name__ == "__main__":
    Runner.run()
