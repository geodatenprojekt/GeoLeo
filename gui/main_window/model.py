
class Model:

    def __init__(self):
        self.cadaster = None
        self.pointcloud = None
        self.scaleFactor = 0.0
        self.moveX = 0.0
        self.moveY = 0.0

    def loadCadaster(self, path):
        pass


    def loadPointcloud(self, path):
        pass

    def moveInXDirection(self, num):
        self.moveX += num

    def moveInYDirection(self, num):
        self.moveY += num

    def scaleSize(self, num):
        self.scaleFactor += num