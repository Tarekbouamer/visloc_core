
from os import path, makedirs


def get_root():
    return path.dirname(path.dirname(path.abspath(__file__)))


def create_folder(folder):
    if not path.exists(folder):
        makedirs(folder)



