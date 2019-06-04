import unittest
import shutil
from geoleo import file_helper
import os

class Test_file_helper(unittest.TestCase):

    def setUp(self):
        pass


    def test_file_helper_get_all_paths_from_dir_none__path(self):
        """Test the method get all paths from dir withe None as path.
            It should return None."""
        self.assertEqual(None, file_helper.get_all_paths_from_dir(None))

    def test_file_helper_get_all_paths_from_dir_ReadAllFiles(self):
        """"Test the method get all paths from dir withe a valid direction and two files in it.
            The return value should be equals withe the file path list.
        """
        os.mkdir("test")
        file_path_list = ["test\\test1", "test\\test2"]
        file1 = open(file_path_list[0], "w")
        file1.close();
        file2 = open(file_path_list[1], "w")
        file2.close();

        path_list = file_helper.get_all_paths_from_dir("test")
        shutil.rmtree("./test")
        self.assertEqual(file_path_list, path_list)

    def test_file_helper_get_all_paths_from_dir_not_valid_path(self):
        """Test the method get all paths from dir withe an not existing direction.
            It should return none"""
        self.assertEqual(None, file_helper.get_all_paths_from_dir(None))

    def tearDown(self) -> None:
        pass

