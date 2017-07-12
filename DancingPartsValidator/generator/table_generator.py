import sys 
import numpy.random
sys.path.append('..')

from components.primitives import box
from components.primitives import cylinder
from components.assemblies import table


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def generate_normal_random (mean, deviation, minimum, maximum):
    r = numpy.random.normal(mean, deviation)
    r = clamp(r, minimum, maximum)
    return r


def get_surface_width(sl):
    sw = generate_normal_random(0.8 * sl, 0.1 * sl, 0.3 * sl, sl)
    return sw
 

def get_surface_height(sl):
    sh = generate_normal_random(0.2 * sl, 0.05 * sl, 0.1 * sl, 0.3 * sl)
    return sh


def get_leg_radius(sl):
    lr = generate_normal_random(0.2 * sl, 0.1 * sl, 0.1 * sl, 0.4 * sl)
    return lr


def get_leg_height(sl):
    lh = generate_normal_random(0.7 * sl, 0.3 * sl, 0.4 * sl, 1.1 * sl)
    return lh


#Generates a table given a surface length
def generate_table(sl):
    sw = get_surface_width(sl)
    sh = get_surface_height(sl)
    lr = get_leg_radius(sl)
    lh = get_leg_height(sl)

    t = table.Table()

    t.boxes[0] = box.Box(sw, sl, sh)
    t.cylinders[0] = cylinder.Cylinder(lr, lh)
    t.cylinders[1] = cylinder.Cylinder(lr, lh)
    t.cylinders[2] = cylinder.Cylinder(lr, lh)
    t.cylinders[3] = cylinder.Cylinder(lr, lh)

    return t


for i in range(100):
    asl = 100 #average surface length
    surface_length = generate_normal_random(asl, 0.3 * asl, 0.3 * asl, 1.7 * asl)
    t = generate_table(surface_length)
    t.id = i

    t.boxes[0].printInfo()
    t.cylinders[0].printInfo()
    t.cylinders[1].printInfo()
    t.cylinders[2].printInfo()
    t.cylinders[3].printInfo()
    print "----------------------------"

    filename = "../data/table_" + str(t.id) + ".pkl"
    t.save(filename)

    t1 = table.Table()
    t1 = t1.open(filename)

    t1.boxes[0].printInfo()
    t1.cylinders[0].printInfo()
    t1.cylinders[1].printInfo()
    t1.cylinders[2].printInfo()
    t1.cylinders[3].printInfo()
    print "----------------------------"

'''
t = table.Table()
print t.getBoxesCount()
print t.getCylindersCount()
print t.getEllipsoidsCount()

t.boxes[0] = box.Box(100, 80, 20)
t.cylinders[0] = cylinder.Cylinder(10, 80)
t.cylinders[1] = cylinder.Cylinder(10, 80)
t.cylinders[2] = cylinder.Cylinder(10, 80)
t.cylinders[3] = cylinder.Cylinder(10, 80)


filename = "../data/table.pkl"
t.save(filename)
t.open(filename)

t.boxes[0].printInfo()
t.cylinders[0].printInfo()
t.cylinders[1].printInfo()
t.cylinders[2].printInfo()
t.cylinders[3].printInfo()
'''
