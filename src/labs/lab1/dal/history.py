from labs.lab1.bll.formatting import get_formatted_float


def add_to_history(calculation, history):
    """
    Adds a calculation to the history
    :param calculation: The calculation to be added to the history
    :param history: List containing the history of calculations
    :return: Updated history with the new calculation added
    """
    history.append(calculation)
    return history


def show_history(history, decimals, log_file):
    """
    Format and print the history of calculations.
    :param history: A list of dictionaries where each dictionary contains the details of a calculation record (num1, num2, operator, result).
    :param decimals: An integer specifying the number of decimal places to format the numerical values.
    :param log_file: A file handle used for logging operations and formatting output.
    :return: None
    """
    print("Історія обчислень:")
    if not history:
        print("Історія порожня.")
    else:
        for record in history:
            num1, num2, operator, result = record.values()
            if num2 is not None:
                print(
                    f"{get_formatted_float(num1,decimals, log_file)} {operator} {get_formatted_float(num2,decimals, log_file)} = {get_formatted_float(result,decimals, log_file)}"
                )
            else:
                print(
                    f"{operator}{get_formatted_float(num1,decimals, log_file)} = {get_formatted_float(result,decimals, log_file)}"
                )
