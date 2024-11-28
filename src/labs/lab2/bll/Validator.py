from builtins import float

from labs.lab2.bll.Operation import Operation


class Validator:
    """
    Validator class is responsible for validating various operators and equations.
    It checks for the type of operator (unary or double), verifies numerical values,
    and determines if an equation is complete or incomplete based on the provided
    operators and numbers.
    """

    def __init__(self, unary_operations, double_operations):
        self.unary_operations = unary_operations
        self.double_operations = double_operations

    def is_operator(self, operator):
        if operator in self.unary_operations:
            return True
        elif operator in self.double_operations:
            return True
        else:
            return False

    def is_unary(self, operator):
        return operator in self.unary_operations

    def is_double(self, operator):
        return operator in self.double_operations

    def available_operators(self):
        return self.unary_operations + self.double_operations

    def available_operators_str(self):
        return ", ".join(self.available_operators())

    @staticmethod
    def is_numeric(var):
        try:
            float(var)
            return True
        except:
            return False

    @staticmethod
    def to_float(var):
        return float(var)

    def is_nums(self, nums):
        for num in nums:
            if not self.is_numeric(num):
                return False
        return True

    def is_equation_incomplete_args(self, operator, num1, num2):
        if operator in self.unary_operations:
            return self.is_nums([num1])
        elif operator in self.double_operations:
            return self.is_nums([num1, num2])
        else:
            return False

    def is_equation_complete_args(self, operator, num1, num2, result):
        if operator in self.unary_operations:
            return self.is_nums([num1, result])
        elif operator in self.double_operations:
            return self.is_nums([num1, num2, result])
        else:
            return False

    def is_equation_incomplete(self, operation_object: Operation):
        try:
            operator, num1, num2, result = operation_object.to_components()
            is_equation = self.is_equation_incomplete_args(operator, num1, num2)
            return is_equation
        except Exception as e:
            print("Can't use method from Operation. {e}")
            return False

    def is_equation_complete(self, operation_object: Operation):
        try:
            operator, num1, num2, result = operation_object.to_components()
            return self.is_equation_complete_args(operator, num1, num2, result)
        except Exception as e:
            print("Can't use method from Operation. {e}")

    def is_operator_in_object(self, operation_object: Operation):
        try:
            operator = operation_object.operation()
            return self.is_operator(operator)
        except Exception as e:
            print(f"Can't use menthod from Operation. {e}")
