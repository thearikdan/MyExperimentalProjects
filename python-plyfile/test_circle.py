import numpy as np
from plyfile import PlyElement, PlyData

point_count = 2048

radius = 100.


vertex = np.zeros((2048,),
                      dtype=[('x', 'f4'), ('y', 'f4'),
                             ('z', 'f4')])

for i in range (point_count):
    x = np.random.uniform(-radius, radius)
    y = 0.0
    z_ = np.sqrt(radius * radius - x * x)
    z = np.random.uniform(-z_, z_)
    vertex[i] = (x, y, z)

print vertex


el = PlyElement.describe(vertex, 'vertex')

PlyData([el]).write('data/circle.ply')
