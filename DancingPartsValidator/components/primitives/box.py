import json
from primitive import Primitive

class Box(Primitive):

    def __init__(self, w = 0, l = 0, h = 0):
        self.w = w
        self.l = l
        self.h = h

    @property
    def width(self):
        return self.w

    @property
    def length(self):
        return self.l

    @property
    def height(self):
        return self.h

    def getVolume(self):
        return self.w * self.l * self.h

    def getSignature(self):
        return self.getVolume() * 1000 + self.h * 100 + self.w * 10 + self.l

    def getName(self):
        return "Box"

    def printInfo(self):
        print self.w
        print self.l
        print self.h

