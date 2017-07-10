from ..primitives import box
from ..primitives import cylinder


class Table:
    def __init__(self):
        self.id = 0
        self.surface = box.Box()
        self.legs = [cylinder.Cylinder() for _ in range(4)]

    @property
    def id(self):
        return self.id

    @property
    def surface(self):
        return self.surface

    @property
    def legs(self):
        return self.legs

    def getClass(self):
        return "table"

