import unittest
import shutil
from geoleo import file_helper
import os

class Test_file_helper(unittest.TestCase):

    def setUp(self):
        pass



    def test_file_helper_get_all_paths_from_dir_ReadAllFiles(self):
        os.mkdir("test")
        file1 = open("test/test1", "w")
        file2 = open("test/test2", "w")
        file1.close();
        file2.close();
        test_path_list = []
        test_path_list.append("test\\test1")
        test_path_list.append("test\\test2")
        path_list = file_helper.get_all_paths_from_dir("test")
        shutil.rmtree("./test")
        self.assertEqual(test_path_list, path_list)

    def test_file_helper_get_all_paths_from_dir_NoPath(self):
        with self.assertRaises(FileNotFoundError):
            file_helper.get_all_paths_from_dir("test")

    def tearDown(self) -> None:
        pass

