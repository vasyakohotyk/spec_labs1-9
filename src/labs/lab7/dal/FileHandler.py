import csv
import json


class FileHandler:
    """
    Utils to save data to json, csv or text files.
    """

    @staticmethod
    def save_to_json(data, filename="data.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def save_to_csv(data, header, filename="data.csv"):
        if not data:
            return
        data_dicts = [{header[i]: row[i] for i in range(len(header))} for row in data]
        with open(filename, "w", newline="", encoding="utf-8") as f:
            dict_writer = csv.DictWriter(f, fieldnames=header)
            dict_writer.writeheader()
            dict_writer.writerows(data_dicts)

    @staticmethod
    def save_to_text(data, filename="data.txt"):
        if not isinstance(data, str):
            data = str(data)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(data)
