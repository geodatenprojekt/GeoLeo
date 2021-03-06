"""file helper module that contains functions to get file informations

"""
from os import listdir
from os.path import isfile, join

def get_all_paths_from_dir(path_to_dir, file_ending=None):
    """Returns a list with all file paths in a given directory path

    Keyword arguments:
    path_to_dir -- the path to the directoy, which do you want all file paths
    """
    if path_to_dir is None:
        return None
    try:
        list_file_paths = []
        for file_name in listdir(path_to_dir):
            file_path = ""
            if file_ending is not None:
                if file_name.endswith(file_ending):
                    file_path = join(path_to_dir, file_name)
            if isfile(file_path):
                list_file_paths.append(file_path)
    except FileNotFoundError:
        return None
    return list_file_paths
