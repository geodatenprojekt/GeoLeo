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

    def __init__(self, _x, _y, _z):
        """Get and write the attributes of the class in the object"""
        self.x = _x
        self.y = _y
        self.z = _z

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
