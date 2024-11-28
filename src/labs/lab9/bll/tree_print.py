def folder_tree(
    array: list[str],
    nest_divider=".",
    indent=" ",
    nest_indent="└-",
    flag_format="\x1b[1m{}\x1b[22m",
):
    """
    :param array: A list of strings where each string represents a nested item using the specified nest_divider.
    :param nest_divider: A string that separates different levels of nesting within an item. Defaults to ".".
    :param indent: A string used to indent nested items. Defaults to a space " ".
    :param nest_indent: A string used as a prefix for nested items. Defaults to "└-".
    :param flag_format: A string format used to apply styling to items. Defaults to bold formatting using ANSI escape codes.
    :return: A formatted tree structure as a string where each item's nesting is visually represented.
    """
    divided = [string.split(nest_divider) for string in array]
    return list_to_tree("", divided, 0, indent, nest_indent, flag_format)


def list_to_tree(
    string,
    lists: list[list[str]],
    level,
    indent=" ",
    nest_indent="└-",
    flag_format="\x1b[1m{}\x1b[1m",
):
    """
    :param string: Initial string to which the tree structure will be appended.
    :param lists: A list of lists, where each inner list represents a path in the tree.
    :param level: Current level of depth in the tree structure.
    :param indent: String used for indentation (default is a single space).
    :param nest_indent: String used for nesting levels (default is "└-").
    :param flag_format: Format string used to highlight certain nodes (default wraps the node in ANSI bold codes).
    :return: Updated string with the constructed tree structure.
    """
    first_elements = {element[0] for element in lists if element}  # use set for unique elements
    for element in first_elements:
        lists_with_first_element = [
            sublist[1:] for sublist in lists if sublist and sublist[0] == element
        ]
        if [] in lists_with_first_element:
            string_element = flag_format.format(element)
        else:
            string_element = element
        string += f"{level * indent}{nest_indent if level>0 else ""}{string_element}\n"

        if lists_with_first_element:
            string = list_to_tree(
                string,
                lists_with_first_element,
                level + 1,
                indent,
                nest_indent,
                flag_format,
            )

    return string
