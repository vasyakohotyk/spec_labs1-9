"""
This module defines an interface for creating runner classes that execute tasks and
 measure execution time.
"""
from time import perf_counter


class RunnerInterface:
    """
    An interface for creating runners.

    This interface should be inherited by any class that aims to implement
    a runner. The inheriting class must provide an implementation for the
    `run` method.

    Methods
    -------
    run():
        Executes the runner. Must be implemented by any subclass.
    """

    @staticmethod
    def run():
        """
        Executes the runner.

        This method should be implemented by subclasses to define
        the specific runner logic.
        """
        raise NotImplementedError("Not implemented runner yet")

    @classmethod
    def run_with_statistic(cls):
        """
        Executes the runner and measures the time taken to complete the execution.

        Returns
        -------
        float
            The time taken to execute the `run` method.
        """
        start = perf_counter()
        cls.run()
        end = perf_counter()
        return end - start

# if __name__ == '__main__':
#     Runner.run()
