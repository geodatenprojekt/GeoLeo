import unittest
import os
import os.path
from geoleo import pointcloud

class Test_PointCloudReader(unittest.TestCase):
    def setUp(self):
        pass


    """
    If the PointCloudFileIO object do not  get a valid path 
    of a .las/.laz file it should throws an OSError
    """
    def test_readFile_NoFile(self):
        with self.assertRaises(OSError):
            pointcloud.PointCloudFileIO("No File")

    def test_writeFileToPath_writefile(self):
        pointCloud = pointcloud.PointCloudFileIO("../example_data/pointcloud_examples/47078_575411_0011.laz")
        pointCloud.writeFileToPath("../example_data/pointcloud_examples/test.las")
        self.assertTrue(os.path.isfile("../example_data/pointcloud_examples/test.las"))
        os.remove("../example_data/pointcloud_examples/test.las")

    def tearDown(self) -> None:
        pass