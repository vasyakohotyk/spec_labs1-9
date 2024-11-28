import math


def calculate(num1, operator, num2=None):
    """
    Calculate equation based on the provided operator and numbers.
    :param num1: The first number for the calculation.
    :type num1: float or int
    :param operator: The operator that determines the type of calculation. Supported operators are '+', '-', '*', '/', '^', '√' or 'sqrt', '%'.
    :type operator: str
    :param num2: The second number for the calculation, which is necessary for all operators except '√' or 'sqrt'. Default is None.
    :type num2: float or int, optional
    :return: The result of the calculation based on the provided operator and numbers.
    :rtype: float or int
    :raises ZeroDivisionError: If the operator is '/' or '%' and num2 is zero, this error is raised.
    :raises ValueError: If the operator is '√' or 'sqrt' and num1 is negative, this error is raised.
    """
    if operator == "+":
        return num1 + num2
    elif operator == "-":
        return num1 - num2
    elif operator == "*":
        return num1 * num2
    elif operator == "/":
        if num2 == 0:
            raise ZeroDivisionError("Ділення на нуль")
        return num1 / num2
    elif operator == "^":
        return num1**num2
    elif operator == "√" or operator == "sqrt":
        if num1 < 0:
            raise ValueError(f"Не можна взяти корінь з від'ємного числа {num1}")
        return math.sqrt(num1)
    elif operator == "%":
        if num2 == 0:
            raise ZeroDivisionError("Ділення на нуль")
        return num1 % num2
