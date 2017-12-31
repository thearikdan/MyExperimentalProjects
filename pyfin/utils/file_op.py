from os import listdir
from os.path import isfile, join
import os
import shutil


def recreate_new_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


def ensure_dir_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def if_file_exists(filename):
    if isfile(filename):
        return true
    else:
        return false


