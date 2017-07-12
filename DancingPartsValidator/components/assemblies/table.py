from ..primitives import box
from ..primitives import cylinder
from assembly import Assembly


class Table(Assembly):
    def __init__(self):
        self.id = 0
        self.boxes = [box.Box() for _ in range(1)]
        self.cylinders = [cylinder.Cylinder() for _ in range(4)]
        self.ellipsoids = []

    def getClass(self):
        return "table"

