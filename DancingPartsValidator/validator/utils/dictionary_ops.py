import json


dict_file = "../primitives/primitive_labels.json"


def load_dict(dict_file):
    with open(dict_file, 'r') as f:
        try:
            data = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            data = {}
    return data


def save_dict(dict_file, data):
    with open(dict_file, 'w') as f:
        json.dump(data, f)
