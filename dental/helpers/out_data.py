import json
from dental.constants.filenames import JSON_STORE
import os

def get_data_from_store(filename=JSON_STORE):
    if os.path.getsize(filename)==0: # Handling empty file
        return []
    with open(filename, 'r') as json_file:
        products_data = json.load(json_file)
    return products_data


def delete_products():
    if os.path.exists(JSON_STORE):
        os.remove(JSON_STORE)
        return True
    return False

    