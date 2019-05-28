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

class Building:
    """Building Class

    Attributes:
        coordinates: All Coordinate objects from the building
    """
    coordinates = list()
