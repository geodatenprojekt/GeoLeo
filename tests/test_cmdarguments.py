import unittest
import sys
from geoleo import cmdargs
class Test_cmdarguments(unittest.TestCase):
    def setUp(self):
        pass

    def test_Parameters_PointCloudPath(self):
        sys.argv.append("-p")
        sys.argv.append("../example_data")
        para = cmdargs.Parameters()

        self.assertEqual(para.getPointCloudPath(),
                         "../example_data")
    """
    def test_Parameters_PointCloudNotAPath(self):
        sys.argv.append("-p")
        sys.argv.append("NoPath")
        with self.assertRaises(argparse.ArgumentTypeError):
            para = cmdargs.Parameters()
    """
    def test_Parameters_CadasterPath(self):
        sys.argv.append("-c")
        sys.argv.append("../example_data")
        para = cmdargs.Parameters()

        self.assertEqual("../example_data",
                         para.getCadasterPath())

    def test_Parameters_Output(self):
        sys.argv.append("-o")
        sys.argv.append("../")
        para = cmdargs.Parameters()

        self.assertEqual("../",
                         para.getOutputPath())

    def test_Parameters_XOffset(self):
        sys.argv.append("-x")
        sys.argv.append("50")
        para = cmdargs.Parameters()

        self.assertEqual(50.0,
                         para.getXOffset())

    def test_Parameters_YOffset(self):
        sys.argv.append("-y")
        sys.argv.append("50")
        para = cmdargs.Parameters()

        self.assertEqual(50.0,
                         para.getYOffset())

    def tearDown(self) -> None:
        pass