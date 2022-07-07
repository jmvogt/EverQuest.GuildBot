from typing import Any

from utils.file import read_yaml

# TODO: Move to configuration file
SECRETS_PATH="secrets.yaml"

def get_secret(secret_key: str) -> Any:
    secret_dict = read_yaml(SECRETS_PATH)
    current_dict = secret_dict
    key_parts = secret_key.split('.')
    for key in key_parts[:-1]:
        current_dict = current_dict[key]
    return current_dict.get(key_parts[-1])
