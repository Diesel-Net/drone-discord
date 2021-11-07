import os
from ruamel import yaml

_config_path = os.path.expanduser("~") + "/api/config.yaml"

# load config file
with open(_config_path, "r") as file:
    # Round Trip Loader maintains the ordering, but requires more parse cycles
    _config = yaml.load(file, Loader=yaml.RoundTripLoader)
