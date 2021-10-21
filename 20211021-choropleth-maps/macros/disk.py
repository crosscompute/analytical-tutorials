from os import listdir, makedirs, remove
from os.path import join
from shutil import rmtree


def make_folder(folder):
    try:
        makedirs(folder)
    except FileExistsError:
        pass
    return folder


def clean_folder(folder):
    'Remove folder contents but keep folder'
    for x_name in listdir(make_folder(folder)):
        x_path = join(folder, x_name)
        remove_safely(x_path)
    return folder


def remove_safely(folder_or_path):
    'Make sure a path or folder does not exist without raising an exception'
    try:
        rmtree(folder_or_path)
    except OSError:
        try:
            remove(folder_or_path)
        except OSError:
            pass
    return folder_or_path


def remove_folder(folder):
    try:
        rmtree(folder)
    except FileNotFoundError:
        pass
    return folder


def remove_path(path):
    try:
        remove(path)
    except FileNotFoundError:
        pass
    return path