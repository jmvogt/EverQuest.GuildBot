from typing import Any

from utils.file import read_yaml

# TODO: Move to configuration file
SECRETS_PATH="secrets.yaml"
CONFIG_PATH="config.yaml"


def get_from_yaml(yaml_input, path):
    current_dict = yaml_input
    key_parts = path.split('.')
    for key in key_parts[:-1]:
        if key not in current_dict:
            return
        current_dict = current_dict[key]
    return current_dict.get(key_parts[-1])


def get_secret(secret_path: str) -> Any:
    return get_from_yaml(read_yaml(SECRETS_PATH), secret_path)


def get_config(config_path: str, default_value=None) -> Any:
    value = get_from_yaml(read_yaml(CONFIG_PATH), config_path)
    if value is None and default_value is not None:
        return default_value
    return value
