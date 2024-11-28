def memory_set(memory, calculation):
    """
    Change memory based on calculation result.
    :param memory: The current memory value that might be overwritten.
    :param calculation: A dictionary containing calculation results.
    :return: The updated memory value with the new calculation result.
    """
    memory = calculation["result"]
    print("Значення збережено в пам'яті.")
    return memory


def memory_save(memory, calculation):
    """
    Adding to memory calculation result.
    :param memory: The current value stored in memory.
    :param calculation: A dictionary containing at least a "result" key with the calculated result to be added to memory.
    :return: The updated memory value after adding the calculation result.
    """
    memory += calculation["result"]
    print("Значення збережено в пам'яті.")
    return memory


def memory_retrieve(memory):
    """
    Format and print the value stored in memory.
    :param memory: The value to be retrieved from memory. It can be any data type.
    :return: The value stored in memory if it exists, otherwise returns 0.
    """
    if memory:
        print(f"Значення з пам'яті: {memory}")
        return memory
    else:
        print("Пам'ять порожня.")
        return 0


def memory_clean():
    """
    Cleans the memory and prints confirmation message.

    :return: 0 indicating successful memory clean operation.
    """
    print("Пам'ять очищена.")
    return 0
