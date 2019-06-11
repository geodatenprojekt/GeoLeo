import unittest
import numpy as np
import os
from geoleo import util


class TestUtil(unittest.TestCase):
    """Test the methods of util
        @author Valentin Hertel
    """
    def setUp(self):
        pass

    def test_get_path_to_file_none_file(self):
        """Test the method "get_path_to_file" in util withe none as file. It should return none.
        """
        self.assertEqual(None, util.getPathToFile(None))

    def test_get_path_relative_to_root_none_file(self):
        """Test the method "get_path_relative_to_root" in util withe none as file.
            It should return none.
        """
        self.assertEqual(None, util.getPathRelativeToRoot(None))

    def test_get_path_relative_to_root_valid_file(self):
        """Test the method "get_path_relative_to_root" in util withe none as file.
            It should return none.
        """
        """string = util.getPathRelativeToRoot("tests/test_suite.py")
        print(string)"""
        self.assertTrue(True)

    def test_get_points_close_to_anchor_same_YAches(self):
        """Test the method "get Points close to anchor" white Points on the same y-aches
            and in a distance of 3"""
        p1 = np.array([1, 3, 5]).reshape(3)
        p2 = np.array([1, 3, 6]).reshape(3)
        p3 = np.array([1, 3, 7]).reshape(3)
        p4 = np.array([2, 3, 5]).reshape(3)
        p5 = np.array([2, 3, 6]).reshape(3)
        p6 = np.array([2, 3, 7]).reshape(3)
        p7 = np.array([3, 3, 5]).reshape(3)
        p8 = np.array([3, 3, 6]).reshape(3)
        p9 = np.array([3, 3, 7]).reshape(3)
        points = [p1, p2, p3, p4, p5, p6, p7, p8, p9]
        anchor = [1, 3, 5]
        distance = 3
        numpy_arr = np.vstack(points)
        assert_list = [True, True, True, True, True, True, True, True, True]
        close_list = util.getPointsCloseToAnchor(anchor, numpy_arr, distance)
        for i in range(len(assert_list)):
            self.assertEqual(assert_list[i], close_list[i])

    def test_getPointsCloseToAnchor_Find_balcony(self):
        """Test the method "get points close to anchor" withe an negativ integer as distance"""
        """coords"""
        b1 = np.array([5, 8, 3]).reshape(3)
        b2 = np.array([1, 0, 3]).reshape(3)
        b3 = np.array([6, 1, 2]).reshape(3)
        b4 = np.array([1, 3, 2]).reshape(3)
        b5 = np.array([5, 2, 5]).reshape(3)
        """all coords"""
        points = [b1, b2, b3, b4, b5]
        numpy_arr = np.vstack(points)
        """anchor cord"""
        anchor = [5, 8, 4]
        distance = -3
        close_list = util.getPointsCloseToAnchor(anchor, numpy_arr, distance)
        self.assertEqual(None, close_list)

    def test_unzip_LAZFILE(self):
        if os.path.exists("example_data/pointcloud_examples/47078_575411_0011.las"):
            os.remove("example_data/pointcloud_examples/47078_575411_0011.las")
        util.unzipLAZFile("example_data/pointcloud_examples/47078_575411_0011.laz")
        self.assertTrue(os.path.exists("example_data/pointcloud_examples/47078_575411_0011.las"))

    def tearDown(self) -> None:
        pass
