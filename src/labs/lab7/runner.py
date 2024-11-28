from labs.lab7.init import main
from shared.interfaces.runner_interface import RunnerInterface


class Runner(RunnerInterface):
    """
    Represents a Runner that implements RunnerInterface

    Method:
        run:
            Executes the main function. This method serves as
            the entry point for the Runner's functionality.
    """

    @staticmethod
    def run():
        main()


if __name__ == "__main__":
    Runner.run()
