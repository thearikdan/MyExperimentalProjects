from components.primitives import box
from components.primitives import cylinder
from components.assemblies import table

t = table.Table()
print t.getBoxesCount()
print t.getCylindersCount()
print t.getEllipsoidsCount()

t.boxes[0] = box.Box(100, 80, 20)
t.cylinders[0] = cylinder.Cylinder(10, 80)
t.cylinders[1] = cylinder.Cylinder(10, 80)
t.cylinders[2] = cylinder.Cylinder(10, 80)
t.cylinders[3] = cylinder.Cylinder(10, 80)


filename = "data/table.pkl"
t.save(filename)
t.open(filename)

t.boxes[0].printInfo()
t.cylinders[0].printInfo()
t.cylinders[1].printInfo()
t.cylinders[2].printInfo()
t.cylinders[3].printInfo()

