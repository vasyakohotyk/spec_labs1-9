from labs.lab5 import init
from shared.interfaces.runner_interface import RunnerInterface


class Runner(RunnerInterface):
    """
    Class Runner inherits from RunnerInterface to provide functionality for running a process.

    Methods
    -------
    run():
        Static method that calls the main function of the init module to start the process.
    """

    @staticmethod
    def run():
        init.main()


if __name__ == "__main__":
    Runner().run()
