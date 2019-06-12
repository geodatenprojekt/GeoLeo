import unittest
from geoleo import cadaster_reader as cadaster


class TestCadasterReader(unittest.TestCase):
    """"Test class for all methods in cadaster reader
        @author Valentin Hertel
    """
    def setUp(self) -> None:
        pass

    def test_get_coordinates_none_points(self):
        """"Test the method get coordinates withe none as points."""
        self.assertEqual(None, cadaster.get_coordinates(None))

    def test_get_coordinates_valid_point(self):
        """Test the return Value on normal integer input as String."""
        x = "5"
        y = "3000"
        z = "-3451"
        point_list = [x, y, z]

        self.assertEqual(5.0, cadaster.get_coordinates(point_list)[0].x)
        self.assertEqual(3000.0, cadaster.get_coordinates(point_list)[0].y)
        self.assertEqual(-3451.0, cadaster.get_coordinates(point_list)[0].z)

    def test_get_coordinates_not_valid_point(self):
        """Test the method get coordinates without the z value in a Point. It should raise
            a ValueError.
        """
        x = "4"
        y = "5"
        point_list = [x, y]

        with self.assertRaises(ValueError):
            cadaster.get_coordinates(point_list)

    def test_get_buildings_none_dir(self):
        """Test the get buildings method withe none as building directory."""
        self.assertEqual(None, cadaster.get_buildings(None))

    def test_get_xml_element_None_para(self):
        """Test the get xml element method with none as elements and xml_elements."""
        self.assertEqual(None, cadaster.get_xml_element(None, None))

    def tearDown(self) -> None:
        pass
