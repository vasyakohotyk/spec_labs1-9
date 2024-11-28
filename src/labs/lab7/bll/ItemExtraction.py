def extract_data_items(
    data, selected_fields, fields_dict, is_to_dict=False, is_to_string=False
):
    """
    From tree like structure and id get flat representation of data.
    :param data: A dictionary object containing the data from which items will be extracted.
    :param selected_fields: A list of field names to be extracted from each item in the data.
    :param fields_dict: A dictionary mapping field names to their respective paths within the item data.
    :param is_to_dict: A boolean flag indicating if the extracted data should be returned as a list of dictionaries. Defaults to False.
    :param is_to_string: A boolean flag indicating if the field values should be converted to strings. Defaults to False.
    :return: A list containing the extracted items, each either as a list or a dictionary based on the is_to_dict flag.
    """
    items = data.get("items", [])
    extracted_items = []

    for item in items:
        if is_to_dict:
            row = {}
        else:
            row = []
        for field in selected_fields:
            field_path = fields_dict.get(field)
            if field_path:
                value = item
                keys = field_path.split(".")
                if keys[0] == "items":
                    keys = keys[1:]
                for key in keys:
                    value = value.get(key, "")
                if is_to_string:
                    value = str(value)
                if is_to_dict:
                    row[field] = value
                else:
                    row.append(value)
        extracted_items.append(row)
    return extracted_items
