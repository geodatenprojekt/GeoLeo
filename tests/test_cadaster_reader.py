import unittest
from geoleo import cadaster_reader as cadaster
class test_cadaster_reader(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_get_coordinates_Prosetiv_int_Numbers(self):
        """Test the return Value on normal integer input as String"""
        x = "5"
        y = "3"
        z = "1"
        pointList = []
        pointList.append(x)
        pointList.append(y)
        pointList.append(z)

        self.assertEqual(5.0, cadaster.get_coordinates(pointList)[0]._x)
        self.assertEqual(300.0, cadaster.get_coordinates(pointList)[0]._y)
        self.assertEqual(-50.0, cadaster.get_coordinates(pointList)[0]._z)

    def tearDown(self) -> None:
        pass