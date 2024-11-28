import unittest
import sys

print(sys.path)

from labs.lab2.bll.Operation import Operation


class CalculatorBllTest(unittest.TestCase):
    """
    Unit tests for the CalculatorBll operations.

    This test class validates the core mathematical operations
    (addition, subtraction, multiplication, and division) as implemented
    in the Operation class. For each operation, multiple tests are set
    up to ensure the accuracy and correctness of the results.

    Methods:
    - setUp: Initializes a set of pre-defined operations with known results.
    - test_operation_add: Verifies the addition operation is correct.
    - test_operation_subtraction: Verifies the subtraction operation is correct.
    - test_operation_multiply: Verifies the multiplication operation is correct.
    - test_operation_divide: Verifies the division operation is correct.
    - test_operation_divide_by_zero: Ensures division by zero results in an appropriate error.
    """

    def setUp(self):
        self.operation_add = Operation("+", 5, 3, 8)
        self.operation_add_2 = Operation("+", 10, 15, 25)
        self.operation_subtract = Operation("-", 7, 2, 5)
        self.operation_subtract_2 = Operation("-", 20, 5, 15)
        self.operation_multiply = Operation("*", 4, 3, 12)
        self.operation_multiply_2 = Operation("*", 6, 7, 42)
        self.operation_divide = Operation("/", 10, 2, 5)
        self.operation_divide_2 = Operation("/", 20, 4, 5)
        self.operation_divide_by_zero = Operation("/", 10, 0, None)

    def test_operation_add(self):
        self.assertEqual(
            self.operation_add.get_first_number()
            + self.operation_add.get_second_number(),
            self.operation_add.get_result(),
        )
        self.assertEqual(
            self.operation_add_2.get_first_number()
            + self.operation_add_2.get_second_number(),
            self.operation_add_2.get_result(),
        )

    def test_operation_subtraction(self):
        self.assertEqual(
            self.operation_subtract.get_first_number()
            - self.operation_subtract.get_second_number(),
            self.operation_subtract.get_result(),
        )
        self.assertEqual(
            self.operation_subtract_2.get_first_number()
            - self.operation_subtract_2.get_second_number(),
            self.operation_subtract_2.get_result(),
        )

    def test_operation_multiply(self):
        self.assertEqual(
            self.operation_multiply.get_first_number()
            * self.operation_multiply.get_second_number(),
            self.operation_multiply.get_result(),
        )
        self.assertEqual(
            self.operation_multiply_2.get_first_number()
            * self.operation_multiply_2.get_second_number(),
            self.operation_multiply_2.get_result(),
        )

    def test_operation_divide(self):
        self.assertEqual(
            self.operation_divide.get_first_number()
            / self.operation_divide.get_second_number(),
            self.operation_divide.get_result(),
        )
        self.assertEqual(
            self.operation_divide_2.get_first_number()
            / self.operation_divide_2.get_second_number(),
            self.operation_divide_2.get_result(),
        )

    def test_operation_divide_by_zero(self):
        self.assertFalse(self.operation_divide_by_zero.is_complete())
        with self.assertRaises(ZeroDivisionError):
            self.operation_divide_by_zero.get_first_number() / self.operation_divide_by_zero.get_second_number()


if __name__ == "__main__":
    unittest.main()
