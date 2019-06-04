import unittest
from geoleo import cadaster_reader as cadaster
class test_cadaster_reader(unittest.TestCase):
    """"Test class for all methods in cadaster reader
        @author Valentin Hertel
    """
    def setUp(self) -> None:
        pass

    def test_cadaster_reader_get_coordinates_none_points(self):
        """"Test the method get coordinates withe none as points."""
        self.assertEqual(None, cadaster.get_coordinates(None))

    def test_cadaster_reader_get_coordinates_valid_point(self):
        """Test the return Value on normal integer input as String."""
        x = "5"
        y = "3000"
        z = "-3451"
        pointList = []
        pointList.append(x)
        pointList.append(y)
        pointList.append(z)

        self.assertEqual(5.0, cadaster.get_coordinates(pointList)[0]._x)
        self.assertEqual(3000.0, cadaster.get_coordinates(pointList)[0]._y)
        self.assertEqual(-3451.0, cadaster.get_coordinates(pointList)[0]._z)

    def test_cadaster_reader_get_coordinates_not_valid_point(self):
        """Test the method get coordinates without the z value in a Point."""
        x = "4"
        y = "5"
        pointList = []
        pointList.append(x)
        pointList.append(y)
        with self.assertRaises(ValueError):
            cadaster.get_coordinates(pointList)

    def test_cadaster_reader_get_buildings_none_dir(self):
        """Test the get buildings method withe non as building directory."""
        self.assertEqual(None, cadaster.get_buildings(None))


    def test_cadaster_reader_get_xml_element_None_para(self):
        """Test the get xml element method with none as elements and xml_elements."""
        self.assertEqual(None, cadaster.get_xml_element(None, None))

    def tearDown(self) -> None:
        pass