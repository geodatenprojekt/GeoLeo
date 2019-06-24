
class Model:

    def __init__(self):
        self.scaleFactor = 0.0
        self.moveX = 0.0
        self.moveY = 0.0

    def moveInXDirection(self, num):
        self.moveX += num

    def moveInYDirection(self, num):
        self.moveY += num

    def scaleSize(self, num):
        self.scaleFactor += num