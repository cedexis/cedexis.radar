
import json

def read_config(config_file_path, default_config):
    try:
        with open(config_file_path) as fp:
            try:
                return json.load(fp)
            except TypeError:
                pass
    except FileNotFoundError:
        pass

    return default_config
