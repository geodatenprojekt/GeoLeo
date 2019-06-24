"""Cadaster classes implementation"""
from geoleo import cadaster_reader as cad_reader

class Cadaster:
    """Cadaster Class

    Attributes:
        buildings: All Building objects from the cadaster
    """
    buildings = list()

    #def Resize(self, scale):
    #    self.scale = scale

    #def Move(self, x, y):
    #    self.offsetX = x
    #    self.offsetY = y

    def __init__(self, directory):
        """Set buildings"""
        self.buildings = cad_reader.get_buildings(directory)

class Coordinate:
    """Cordinate Class

    Attributes:
        x: X Coordinate
        y: Y Coordinate
        z: Z Coordinate
    """
    _x = 0
    _y = 0
    _z = 0

    def __init__(self, x, y, z):
        """Set x, y and z"""
        self._x = x
        self._y = y
        self._z = z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return self.x.__hash__() + 7 * self.y.__hash__()

    def __str__(self):
        return "({:.3f}, {:.3f}, {:.3f})".format(self.x, self.y, self.z)

class Building:
    """Building Class

    Attributes:
        coordinates: All Coordinate objects from the building
    """

    def __init__(self):
        self.coordinates = list()
