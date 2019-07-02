
class Model:

    def __init__(self, lasp, gmlp):
        self.lasPath = lasp
        self.gmlPath = gmlp
        self.moveX = 0.0
        self.moveY = 0.0

    def moveInXDirection(self, num):
        self.moveX += num

    def moveInYDirection(self, num):
        self.moveY += num