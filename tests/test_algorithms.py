import unittest
from geoleo import algorithms
from geoleo import cadaster_reader as cadasta


class TestAlgorithms (unittest.TestCase):
    """Test the algorithms of util
        @author Valentin Hertel
    """

    def test_algorithms_shift_cadaster_coordinates_first_and_last_coordinates(self):
        """Test the method "shift cadaster coordinates" withe the first coordinate
            of the first building and the last coordinate od the last building.
        """
        buildings = cadasta.get_buildings("example_data/cadaster_examples")
        firstx = buildings[0].coordinates[0].x
        lastx = buildings[len(buildings)-1].coordinates[len(buildings[len(buildings)-1].coordinates)-1].x
        firsty = buildings[0].coordinates[0].y
        lasty = buildings[len(buildings)-1].coordinates[len(buildings[len(buildings)-1].coordinates)-1].y
        offset = [5, 10]

        algorithms.shiftCadasterCoordinates(buildings, offset)
        self.assertEqual(firstx+offset[0], buildings[0].coordinates[0].x)
        self.assertEqual(lastx+offset[0], buildings[len(buildings)-1]
                         .coordinates[len(buildings[len(buildings)-1].coordinates)-1].x)
        self.assertEqual(firsty+offset[1], buildings[0].coordinates[0].y)
        self.assertEqual(lasty+offset[1], buildings[len(buildings)-1]
                         .coordinates[len(buildings[len(buildings)-1].coordinates)-1].y)
