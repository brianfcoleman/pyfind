from os import walk
from os.path import join
from scanner.path import normalize_path


def scan(root_path):
    for dir_path, dir_names, file_names in walk(root_path):
        for file_name in file_names:
            yield normalize_path(join(dir_path, file_name))
