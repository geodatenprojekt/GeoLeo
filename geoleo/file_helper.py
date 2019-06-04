"""file helper module that contains functions to get file informations

"""
from os import listdir
from os.path import isfile, join

def get_all_paths_from_dir(path_to_dir):
    """Returns a list with all file paths in a given directory path

    Keyword arguments:
    path_to_dir -- the path to the directoy, which do you want all file paths
    """
    list_file_paths = []
    for file_name in listdir(path_to_dir):
        file_path = join(path_to_dir, file_name)
        if isfile(file_path):
            list_file_paths.append(file_path)
    return list_file_paths
