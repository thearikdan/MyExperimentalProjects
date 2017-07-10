from primitive import Primitive

class Box(Primitive):
    def __init__(self, w, l, h):
        self.w = w
        self.l = l
        self.h = h

    @property
    def width(self):
        return self.w

    @property
    def length(self):
        return self.w

    @property
    def height(self):
        return self.h

    def getVolume(self):
        return self.w * self.l * self.h

    def getSignature(self):
        return self.getVolume() * 1000 + self.h * 100 + self.w * 10 + self.l

    def getName(self):
        return "Box"

