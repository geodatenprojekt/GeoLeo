import unittest
import sys
import argparse
from cmdarguments import cmdargs
class Test_cmdarguments(unittest.TestCase):
    def setUp(self):
        pass

    def test_Parameters_PointCloudPath(self):
        sys.argv.append("-p")
        sys.argv.append("../backend/example_data")
        para = cmdargs.Parameters()

        self.assertEqual(para.getPointCloudPath(),
                         "../backend/example_data")
"""
    def test_Parameters_PointCloudNotAPath(self):
        sys.argv.append("-p")
        sys.argv.append("NoPath")
        with self.assertRaises(argparse.ArgumentTypeError):
            para = cmdargs.Parameters()
"""
    def test_Parameters_CadasterPath(self):
        sys.argv.append("-c")
        sys.argv.append("../backend/CadasterReader/ExampleData")
        para = cmdargs.Parameters()

        self.assertEqual("../backend/CadasterReader/ExampleData",
                         para.getCadasterPath())

    def test_Parameters_Output(self):
        sys.argv.append("-o")
        sys.argv.append("../backend")
        para = cmdargs.Parameters()

        self.assertEqual("../backend",
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