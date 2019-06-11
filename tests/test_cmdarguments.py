import unittest
import sys
from geoleo import cmdargs


class TestCmdArguments(unittest.TestCase):
    """Test all method in cmdarguments
        @author Valentin Hertel
    """
    def setUp(self):
        pass

    def test_parameters_point_cloud_path_short(self):
        """Test the -p argument withe a valid path"""
        sys.argv.append("-p")
        sys.argv.append("example_data")
        para = cmdargs.Parameters()

        self.assertEqual(para.getPointCloudPath(),
                         "example_data")

    def test_parameters_point_cloud_path_long(self):
        """"Test the --pointcload argument withe a valid path"""
        sys.argv.append("--pointcloud")
        sys.argv.append("example_data")
        para = cmdargs.Parameters()

        self.assertEqual(para.getPointCloudPath(),
                         "example_data")

    def test_parameters_cadaster_path_short(self):
        """"Test the -c argument withe a valid path"""
        sys.argv.append("-c")
        sys.argv.append("example_data")
        para = cmdargs.Parameters()

        self.assertEqual("example_data",
                         para.getCadasterPath())

    def test_parameters_cadaster_path_long(self):
        """"Test the --cadaster argument withe a valid path"""
        sys.argv.append("--cadaster")
        sys.argv.append("example_data")
        para = cmdargs.Parameters()

        self.assertEqual("example_data",
                         para.getCadasterPath())

    def test_parameters_output_short(self):
        """"Test the -o argument withe a valid path"""
        sys.argv.append("-o")
        sys.argv.append("example_data")
        para = cmdargs.Parameters()

        self.assertEqual("example_data",
                         para.getOutputPath())

    def test_parameters_output_long(self):
        """"Test the --output argument withe a valid path"""
        sys.argv.append("--output")
        sys.argv.append("example_data")
        para = cmdargs.Parameters()

        self.assertEqual("example_data",
                         para.getOutputPath())

    def test_parameters_x_offset_short(self):
        """"Test the -x argument withe a integer and assert an float"""
        sys.argv.append("-x")
        sys.argv.append("50")
        para = cmdargs.Parameters()

        self.assertEqual(50.0,
                         para.getXOffset())

    def test_parameters_x_offset_long(self):
        """"Test the --xoffset argument withe a integer and assert an float"""
        sys.argv.append("--xoffset")
        sys.argv.append("50")
        para = cmdargs.Parameters()

        self.assertEqual(50.0,
                         para.getXOffset())

    def test_parameters_y_offset_short(self):
        """"Test the -y argument withe a integer and assert an float"""
        sys.argv.append("-y")
        sys.argv.append("50")
        para = cmdargs.Parameters()

        self.assertEqual(50.0,
                         para.getYOffset())

    def test_parameters_y_offset_long(self):
        """"Test the --yoffset argument withe a integer and assert an float"""
        sys.argv.append("--yoffset")
        sys.argv.append("50")
        para = cmdargs.Parameters()

        self.assertEqual(50.0,
                         para.getYOffset())

    def tearDown(self) -> None:
        pass
