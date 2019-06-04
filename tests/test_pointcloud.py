import unittest
import os
import os.path
from geoleo import pointcloud

class test_pointcloud(unittest.TestCase):
    """Test the method of pointCloud
        @author Valentin Hertel
    """
    def setUp(self):
        pass


    def test_readFile_NoFile(self):
        """Test the readFile method. If the PointCloudFileIO object does not get a valid path
            of a .las/.laz file it should raise an OSError
        """
        with self.assertRaises(OSError):
            pointcloud.PointCloudFileIO("No File")

    def test_writeFileToPath_writefile(self):
        """Test the writeFileTOPath method withe an valide file"""
        pointCloud = pointcloud.PointCloudFileIO("example_data/pointcloud_examples/47078_575411_0011.laz")
        pointCloud.writeFileToPath("example_data/pointcloud_examples/test.las")
        self.assertTrue(os.path.isfile("example_data/pointcloud_examples/test.las"))
        os.remove("example_data/pointcloud_examples/test.las")

    def tearDown(self) -> None:
        pass