import os
import shutil

from os import listdir
from os.path import isfile, join

from typing import List


def move_file(current_path: str, new_path: str) -> None:
    shutil.move(current_path, new_path)


def make_directory(folder_path: str) -> None:
    isExist = os.path.exists(folder_path)
    if not isExist:
        os.makedirs(folder_path)


def get_files_from_directory(folder_path: str, file_ext: str) -> List[str]:
    return [f for f in listdir(folder_path) if isfile(join(folder_path, f)) and f.endswith(file_ext)]
