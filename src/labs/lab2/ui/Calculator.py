from math import sqrt

from colorama.ansi import set_title
from pygments import highlight

from labs.lab2.bll.Operation import Operation
from labs.lab2.bll.Validator import Validator
from labs.lab2.dal.History import History
from labs.lab2.dal.Logger import Logger
from labs.lab2.dal.Memory import Memory
from shared.classes.dict_json import DictJsonDataAccess
from shared.classes.menu_builder import MenuBuilder


class Calculator:
    """
    Calculator class that handles various arithmetic operations and manages operation history, memory, and settings.

    Attributes:
        settings_path (str): Path to settings file.
        settings (DictJsonDataAccess): Data access object for handling settings stored in a JSON file.
        unary_operations (dict): Dictionary of unary operations supported.
        double_operations (dict): Dictionary of double operations supported.
        decimals (int): Number of decimal places to display in results.
        history (History): Object to manage history of operations.
        memory (Memory): Object representing calculator's memory.
        operation (Operation): The current operation being processed.
        validator (Validator): Object responsible for validating input and operations.
        logger (Logger): Logger object for error and info logging.

    Methods:
        is_setted_operator_valid():
            Checks if the currently set operator is valid.

        set_decimals():
            Sets the number of decimal places to display in results.

        set_operation():
            Sets the current operation based on user input, including numbers and operator.

        _calculate():
            Performs the arithmetic calculation based on set operation.

        _add_last_to_history():
            Adds the last performed operation to the history if it is valid and complete.

        _last_result_to_str():
            Returns the last result as a formatted string.

        get_formatted_float(value):
            Returns a formatted string representing the given value with the specified number of decimals.

        get_memory_title():
            Returns a formatted string representing the current memory value with the specified number of decimals.

        _perform_calculation():
            Sets up, performs, and logs the result of the current operation.

        _write_result_in_memory():
            Writes the last calculation result into the calculator memory.

        _add_result_to_memory():
            Adds the last calculation result to the current memory value.

        _show_calculation_history():
            Displays the history of calculations.

        _clear_calculation_history():
            Clears the history of calculations.

        _set_decimals_option():
            Prompts user to set the number of decimal places to display.

        menu():
            Displays and manages the menu for user interaction with various calculator operations.
    """

    def __init__(self, settings_path):
        self.settings = DictJsonDataAccess(settings_path)
        self.unary_operations = self.settings.get("unary_operations")
        self.double_operations = self.settings.get("double_operations")
        self.decimals = self.settings.get("decimals")
        self.history = History(self.settings.get("history"))
        self.memory = Memory(self.settings.get("memory"))
        self.operation = Operation.empty()
        self.validator = Validator(self.unary_operations, self.double_operations)
        try:
            self.logger = Logger.console_and_file(self.settings.get("log_file"))
        except Exception as e:
            print(f"{e} \nErrors only in console now")
            self.logger = Logger.console_only()

    def is_setted_operator_valid(self):
        return self.validator.is_operator(self.operator)

    def set_decimals(self):
        try:
            print(f"Decimals now: {self.decimals}")
            decimals = int(input("Input new amound of decimals: "))
            self.decimals = decimals
        except ValueError:
            print("It's not a integer, try again")
            self.set_decimals()

    def set_operation(self):
        try:
            num1_input = input("Enter first number or 'mr' for take from memory: ")
            if num1_input == "mr":
                num1 = self.memory.get()
            else:
                num1 = self.validator.to_float(num1_input)

            if not self.validator.is_numeric(num1):
                raise ValueError(f"Wrong first number {num1}")
            operator = input(
                f"Input operator ({self.validator.available_operators_str()}): "
            )
            if not self.validator.is_operator(operator):
                raise ValueError("Wrong operator")
            if self.validator.is_double(operator):
                num2_input = input("Enter second number or 'mr' for take from memory: ")
                if num2_input == "mr":
                    num2 = self.memory.get()
                else:
                    num2 = self.validator.to_float(num2_input)
                if not self.validator.to_float(
                    num2
                ) != 0.0 or not self.validator.to_float(num2):
                    raise ValueError(f"Wrong second number {num2}")
            else:
                num2 = None
            operation = Operation(operator, num1, num2)
            self.operation = operation
        except ValueError as e:
            print(f"Wrong input. {e}")
            return self.set_operation()

    def _calculate(self):
        try:
            operation = self.operation
            operator = operation.get_operator()
            num1 = operation.get_first_number()
            num2 = operation.get_second_number()
            if not self.validator.is_equation_incomplete(operation):
                raise ValueError(
                    f"Wrong equasion, can't _calculate num1:{num1} num2: {num2} operator: {operator}"
                )
            match operator:
                case "+":
                    operation.set_result(num1 + num2)
                case "-":
                    operation.set_result(num1 - num2)
                case "*":
                    operation.set_result(num1 * num2)
                case "/":
                    if operation.num2 == 0:
                        raise ZeroDivisionError("Division by zero")
                    operation.set_result(num1 / num2)
                case "^":
                    operation.set_result(num1**num2)
                case "√" | "sqrt":
                    if num1 < 0:
                        raise ValueError(f"Can't take square root from {num1}")
                    else:
                        operation.set_result(sqrt(num1))
                case "%":
                    if num2 == 0:
                        raise ZeroDivisionError("Division by zero")
                    else:
                        operation.set_result(num1 % num2)
                case _:
                    raise ValueError(f"Wrong operator{operator}")
        except Exception as e:
            self.logger.log_error(e)
            raise e

    def _add_last_to_history(self):
        operation = self.operation
        if not self.validator.is_equation_complete(operation):
            self.logger.log_error(f"Can't add to history {operation}, wrong")
        if not self.operation.is_complete():
            self.logger.log_error(f"Can't add to history {operation}, incomplete")
        self.history.add(operation)

    def _last_result_to_str(self):
        return self.operation.to_string(self.decimals)

    def get_formatted_float(self, value):
        try:
            format_template = "{0:." + str(self.decimals) + "f}"
            return format_template.format(value)
        except ValueError as e:
            self.logger.log_error(f"Can't format {value} into float, {e}")
            return value

    def get_memory_title(self):
        formatted_memory = self.get_formatted_float(self.memory.get())
        return f"M: {formatted_memory}"

    def _perform_calculation(self):
        try:
            self.set_operation()
            self._calculate()
            self._add_last_to_history()
            print(self._last_result_to_str())
        except Exception as e:
            self.logger.log_error(e)
            return

    def _write_result_in_memory(self):
        last_result = self.operation.get_result()
        if last_result is None:
            print("No available results")
            return
        self.memory.set(last_result)

    def _add_result_to_memory(self):
        last_result = self.operation.get_result()
        if last_result is None:
            print("No available results")
            return
        self.memory.add(last_result)

    def _show_calculation_history(self):
        print(self.history.to_string(self.decimals))

    def _clear_calculation_history(self):
        self.history.clear()

    def _set_decimals_option(self):
        self.set_decimals()

    def menu(self):
        menu = (
            MenuBuilder()
            .set_title("=== Console calculator ===")
            .set_dynamic_title(self.get_memory_title)
            .add_option("1", "1. Calculation", self._perform_calculation)
            .add_option(
                "2", "\n2. Wrote result in memory MS", self._write_result_in_memory
            )
            .add_option("3", "\n3. Add result to memory M+", self._add_result_to_memory)
            .add_option("4", "\n4. Set memory to 0 MC", self.memory.clear)
            .add_option(
                "5", "\n5. Show calculation history", self._show_calculation_history
            )
            .add_option(
                "6", "\n6. Clear calculation history", self._clear_calculation_history
            )
            .add_option(
                "7", "\n7. Set how many decimals to show", self._set_decimals_option
            )
            .add_stop_options("\n0", "0. Exit")
            .update_end_callback(self.save)
            .set_input_text("Choose (0-6):")
            .set_warning("Wrong input!")
            .build()
        )
        menu.show()

    # def menu(self):
    #     menu = (MenuBuilder()
    #             .set_title("\n=== Console calculator ===")
    #             .set_dynamic_title(self.get_memory_title)
    #             .add_option("1", "1. Calculation", )
    #             .add_option("2", "2. Wrote result in memory MS")
    #             .add_option("3", "3. Add result to memory M+")
    #             .add_option("4", "4. Set memory to 0 MC")
    #             .add_option("5", "5. Show calculation history")
    #             .add_option("6", "6. Set how much decimals to show")
    #             .add_option("0", "0. Exit")
    #             .build())
    #     while True:
    #         print("\n=== Console calculator ===")
    #         print("1. Calculation")
    #         print("2. Wrote result in memory MS")
    #         print("3. Add result to memory M+")
    #         print("4. Set memory to 0 MC")
    #         print("5. Show calculation history")
    #         print("6. Set how much decimals to show")
    #         print("0. Exit")
    #         choice = input("Choose (0-6): ")
    #         match choice:
    #             case "1":
    #                 try:
    #                     self.set_operation()
    #                     self._calculate()
    #                     self._add_last_to_history()
    #                     print(self._last_result_to_str())
    #                 except Exception as e:
    #                     self.logger.log_error(e)
    #                     continue
    #             case "2":
    #                 last_result = self.operation.get_result()
    #                 if last_result == None:
    #                     print("No available results")
    #                     continue
    #                 self.memory.set(last_result)
    #             case "3":
    #                 last_result = self.operation.get_result()
    #                 if last_result == None:
    #                     print("No available results")
    #                     continue
    #                 self.memory.add(last_result)
    #             case "4":
    #                 self.memory.clear()
    #             case "5":
    #                 print(self.history.to_string(self.decimals))
    #             case "6":
    #                 self.set_decimals()
    #             case "0":
    #                 print("Exit.")
    #                 break
    #             case _:
    #                 print("Wrong choise, try again.")
    #     self.save()

    def save(self):
        memory = self.memory.get()
        history = self.history.get()
        self.settings.set("memory", memory)
        self.settings.set("history", history)
        self.settings.set("decimals", self.decimals)
