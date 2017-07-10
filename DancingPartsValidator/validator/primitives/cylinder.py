from primitive import Primitive
import math

class Cylinder(Primitive):
    def __init__(self, r = 0, h = 0):
        self.r = r
        self.h = h

    @property
    def radius(self):
        return self.r

    @property
    def height(self):
        return self.h

    def getVolume(self):
        return self.h * math.pi * self.r * self.r

    def getSignature(self):
        return self.getVolume() * 100 + self.h * 10 + self.r

    def getName(self):
        return "Cylinder"

