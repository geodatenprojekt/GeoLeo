import unittest
import os
import os.path
from backend import PointCloudReader

class Test_PointCloudReader(unittest.TestCase):
    def setUp(self):
        pass


    """
    If the PointCloudFileIO object do not  get a valid path 
    of a .las/.laz file it should throws an OSError
    """
    def test_readFile_NoFile(self):
        with self.assertRaises(OSError):
            PointCloudReader.PointCloudFileIO("No File")

    def test_writeFileToPath_writefile(self):
        pointCloud = PointCloudReader.PointCloudFileIO("../backend/example_data/47078_575411_0011.laz")
        pointCloud.writeFileToPath("../backend/example_data/test.las")
        self.assertTrue(os.path.isfile("../backend/example_data/test.las"))
        os.remove("../backend/example_data/test.las")

    def tearDown(self) -> None:
        pass