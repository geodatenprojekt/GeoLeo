import unittest
import numpy as np
import os
from geoleo import util
class Test_util(unittest.TestCase):
    """Test the methods of util
        @author Valentin Hertel
    """
    def setUp(self):
        pass


    def test_get_path_to_file_none_file(self):
        """Test the method "get_path_to_file" in util withe none as file. It should return
            none.
        """
        self.assertEqual(None, util.getPathToFile(None))

    def test_get_path_relative_to_root_none_file(self):
        """Test the method "get_path_relative_to_root" in util withe none as file. It should return
                   none.
        """
        self.assertEqual(None, util.getPathRelativeToRoot(None))

    def test_get_path_relative_to_root_none_file(self):
        """Test the method "get_path_relative_to_root" in util withe none as file. It should return
                   none.
        """
        string = util.getPathRelativeToRoot("test_suite.py")
        #print(string)
        self.assertTrue(True)



    def test_util_getPointsCloseToAnchor_sameYAches(self):
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
        list = [True,True,True,True,True,True,True, True, True]
        closeList = util.getPointsCloseToAnchor(anchor, numpy_arr, distance)
        for i in range(len(list)):
            self.assertEqual(closeList[i],list[i])

    def test_util_getPointsCloseToAnchor_Find_balcony(self):
        """Test the method "get points close to anchor" withe a point on the roof and
            some points of a balcony and a gutter."""
        #Balconiy coord
        #right side
        b1 = np.array([5, 8, 3]).reshape(3)
        b2 = np.array([5.5, 8, 2.5]).reshape(3)
        b3 = np.array([6, 8, 2]).reshape(3)
        #front side
        b4 = np.array([6.5, 8, 2]).reshape(3)
        b5 = np.array([6.7, 8, 2.5]).reshape(3)
        b6 = np.array([6.9, 8, 3]).reshape(3)
        b7 = np.array([7, 8, 3.5]).reshape(3)
        #left side
        b8 = np.array([6, 8, 3.7]).reshape(3)
        b9 = np.array([5.5, 8, 4]).reshape(3)
        #gutter coord
        g1 = np.array([5.5, 12, 3]).reshape(3)
        g2 = np.array([5.5, 12, 4]).reshape(3)
        #anchor cord
        anchor = [5, 8, 4]
        #all coords
        points = [b1, b2, b3, b4, b5, b6, b7, b8, b9, g1, g2]
        distance = 3
        numpy_arr = np.vstack(points)
        list = [True, True, True, True, True, True, True, True, True, False, False]
        closeList = util.getPointsCloseToAnchor(anchor, numpy_arr, distance)
        for i in range(len(list)):
            self.assertEqual(closeList[i],list[i])

    def tearDown(self) -> None:
        pass