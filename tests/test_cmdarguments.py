import unittest
import sys
from geoleo import cmdargs
class Test_cmdarguments(unittest.TestCase):
    def setUp(self):
        pass

    def test_Parameters_PointCloudPath_short(self):
        sys.argv.append("-p")
        sys.argv.append("example_data")
        para = cmdargs.Parameters()

        self.assertEqual(para.getPointCloudPath(),
                         "example_data")

    def test_Parameters_PointCloudPath_long(self):
        sys.argv.append("--pointcloud")
        sys.argv.append("example_data")
        para = cmdargs.Parameters()

        self.assertEqual(para.getPointCloudPath(),
                         "example_data")

    def test_Parameters_CadasterPath_short(self):
        sys.argv.append("-c")
        sys.argv.append("example_data")
        para = cmdargs.Parameters()

        self.assertEqual("example_data",
                         para.getCadasterPath())

    def test_Parameters_CadasterPath_long(self):
        sys.argv.append("--cadaster")
        sys.argv.append("example_data")
        para = cmdargs.Parameters()

        self.assertEqual("example_data",
                         para.getCadasterPath())

    def test_Parameters_Output_short(self):
        sys.argv.append("-o")
        sys.argv.append("example_data")
        para = cmdargs.Parameters()

        self.assertEqual("example_data",
                         para.getOutputPath())

    def test_Parameters_Output_long(self):
        sys.argv.append("--output")
        sys.argv.append("example_data")
        para = cmdargs.Parameters()

        self.assertEqual("example_data",
                         para.getOutputPath())

    def test_Parameters_XOffset_short(self):
        sys.argv.append("-x")
        sys.argv.append("50")
        para = cmdargs.Parameters()

        self.assertEqual(50.0,
                         para.getXOffset())

    def test_Parameters_XOffset_long(self):
        sys.argv.append("--xoffset")
        sys.argv.append("50")
        para = cmdargs.Parameters()

        self.assertEqual(50.0,
                         para.getXOffset())

    def test_Parameters_YOffset_short(self):
        sys.argv.append("-y")
        sys.argv.append("50")
        para = cmdargs.Parameters()

        self.assertEqual(50.0,
                         para.getYOffset())

    def test_Parameters_YOffset_long(self):
        sys.argv.append("--yoffset")
        sys.argv.append("50")
        para = cmdargs.Parameters()

        self.assertEqual(50.0,
                         para.getYOffset())

    def tearDown(self) -> None:
        pass