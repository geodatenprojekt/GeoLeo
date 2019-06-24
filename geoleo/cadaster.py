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
    
    def get_buildings(self, file_name):
        blds = cad_reader.get_buildings(file_name)
        for bld in blds:
          self.buildings.append(bld)

class Coordinate:
    """Cordinate Class

    Attributes:
        x: X Coordinate
        y: Y Coordinate
        z: Z Coordinate
    """
    x = 0
    y = 0
    z = 0

    def __init__(self, x, y, z):
        """Set x, y and z"""
        self.x = x
        self.y = y
        self.z = z

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
    coordinates = list()
    
    def __init__(self, coordinates=None):
        """Set coordinates"""
        if coordinates is not None:
          self.coordinates = coordinates
