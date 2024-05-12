import json
from dental.constants.filenames import JSON_STORE
from dental.utils.encoder import CustomEncoder

def log_data(data_dict, file_name=JSON_STORE):
    if data_dict:
        with open(file_name, "a") as outfile:
            json.dump(data_dict, outfile, cls=CustomEncoder, indent=4)
    else:
        print("No data to log", file_name)



