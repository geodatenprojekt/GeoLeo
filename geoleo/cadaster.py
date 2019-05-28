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
        self.buildings = cad_reader.getBuildings(directory)

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
        """Set x, y and z"""
        self.x = _x
        self.y = _y
        self.z = _z

class Building:
    """Building Class

    Attributes:
        coordinates: All Coordinate objects from the building
    """
    coordinates = list()

    def __init__(self, _coordinates):
        """Set coordinates"""
        self.coordinates = _coordinates
