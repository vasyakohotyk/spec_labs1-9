from labs.lab1.bll.calculator import calculate
from labs.lab1.bll.formatting import get_formatted_float
from labs.lab1.dal.history import add_to_history, show_history
from labs.lab1.dal.logger import log_error
from labs.lab1.dal.memory import *
from shared.classes.dict_json import DictJsonDataAccess


def set_decimals(decimals, log_file):
    """
    Function to let user change decimal settings
    :param decimals: The current number of decimal places to be used.
    :param log_file: The file where errors will be logged.
    :return: The new number of decimal places entered by the user or the old value in case of an error.
    """
    try:
        print(f"Кількість знаків після коми: {decimals}")
        decimals = int(input("Введіть нову кількість знаків після коми: "))
        return decimals
    except ValueError:
        log_error("Невірне введення кількості десяткових знаків", log_file)
        return decimals


def is_valid_operator(operator, available_operations, log_file):
    """
    Check is operator is valid
    :param operator: The operator to be validated
    :param available_operations: A list of valid operations
    :param log_file: The file where errors should be logged
    :return: True if the operator is valid, otherwise False
    """
    if operator in available_operations:
        return True
    else:
        log_error(f"Невірний оператор: {operator}", log_file)
        return False


def calculation_menu(memory, available_operations, decimals, log_file, history):
    """
    Perform a calculation on parameters entered by the user previously.
    :param memory: Stores previous calculations or results that can be reused in subsequent operations.
    :param available_operations: A list of arithmetic operations that are supported (e.g., '+', '-', '*', '/').
    :param decimals: Number of decimal places to format the result.
    :param log_file: File path or buffer where error logs and information will be recorded.
    :param history: A list that records all previous calculations including operators, operands, and results.
    :return: Updated memory and calculation history after performing the operation and managing errors.
    """
    num1, operator, num2 = get_input(memory, available_operations, log_file)
    if is_valid_operator(operator, available_operations, log_file):
        try:
            result = calculate(num1, operator, num2)
            calculation = {
                "num1": num1,
                "num2": num2,
                "operator": operator,
                "result": result,
            }
            history = add_to_history(calculation, history)
            print(f"Результат: {get_formatted_float(result,decimals, log_file)}")
            return memory, history
        except ZeroDivisionError as e:
            log_error(str(e), log_file)
        except ValueError as e:
            log_error(str(e), log_file)
    else:
        log_error(
            f"Неправильний оператор, доступні {', '.join(available_operations)}",
            log_file,
        )
    return memory, history


def get_input(memory, available_operations, log_file):
    """
    Function to get valid user input
    :param memory: Value stored in memory, can be reused by inputting 'mr'.
    :param available_operations: List of valid operations (e.g., '+', '-', '√', 'sqrt') that the user can choose from.
    :param log_file: Path to the log file where errors should be logged.
    :return: A tuple containing the first number, the operator, and the second number (or None if not applicable).
    """
    try:
        num1_input = input("Введіть перше число або 'mr' для пам'яті: ")
        if num1_input == "mr":
            num1 = memory
        else:
            num1 = float(num1_input)

        operator = input(f"Введіть оператор ({', '.join(available_operations)}): ")

        num2 = None
        if operator != "√" and operator != "sqrt":
            num2_input = input("Введіть друге число або 'mr' для пам'яті: ")
            if num2_input == "mr":
                num2 = memory
            else:
                num2 = float(num2_input)
        return num1, operator, num2
    except ValueError:
        log_error("Неправильне введення", log_file)
        return get_input(memory, available_operations, log_file)


def menu(settings, memory, available_operations, decimals, log_file, history):
    """
    Function to navigate the user interface.
    :param settings: Application settings object for storing and retrieving configurations.
    :param memory: Current value stored in memory.
    :param available_operations: List of operations that the calculator can perform.
    :param decimals: Number of decimal places to display in the results.
    :param log_file: File path for saving logs.
    :param history: List of past calculation results.
    :return: None
    """
    while True:
        print("\n=== Консольний калькулятор ===")
        print(f"M: {get_formatted_float(memory, decimals, log_file)}")
        print("1. Обчислення")
        print("2. Записати результат у пам'ять MS")
        print("3. Додати результат у пам'ять M+")
        print("4. Очистити пам'ять MC")
        print("5. Показати історію обчислень")
        print("6. Налаштувати кількість десяткових знаків")
        print("0. Вийти")
        choice = input("Виберіть опцію (0-6): ")
        match choice:
            case "1":
                memory, history = calculation_menu(
                    memory, available_operations, decimals, log_file, history
                )
            case "2":
                memory = memory_set(memory, history[-1])
            case "3":
                if not history:
                    print("Немає результатів для збереження.")
                    continue
                memory = memory_save(memory, history[-1])

            case "4":
                memory = memory_clean()
            case "5":
                show_history(history, decimals, log_file)
            case "6":
                decimals = set_decimals(decimals, log_file)
            case "0":
                print("Вихід з програми.")
                break
            case _:
                print("Неправильний вибір. Спробуйте ще раз.")
    settings.set("memory", memory)
    settings.set("history", history)
    settings.set("decimals", decimals)


def run(settings_path):
    """
    Function set up parameters and run the menu.
    :param settings_path: Path to the settings JSON file
    :return: None
    """
    settings = DictJsonDataAccess(settings_path)
    memory = settings.get("memory")
    available_operations = settings.get("available_operations")
    decimals = settings.get("decimals")
    log_file = settings.get("log_file")
    history = settings.get("history")
    menu(settings, memory, available_operations, decimals, log_file, history)
