from primitive import Primitive
import math

class Ellipsoid(Primitive):
    def __init__(self, r1, r2, r3):
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3

    @property
    def radius1(self):
        return self.r1

    @property
    def radius2(self):
        return self.r2

    @property
    def radius3(self):
        return self.r3

    def getVolume(self):
        return 4.0 / 3.0 * math.pi * self.r1 * self.r2 * self.r3

    def getSignature(self):
        arr = [self.r1, self.r2, self.r3]
        arr.sort()
        return self.getVolume() * 1000 + arr[2] * 100 + arr[1] * 10 + arr[0]

    def getName(self):
        return "Ellipsoid"

