import numpy as np
from plyfile import plyfile

point_count = 2048
x_low = 0.
x_high = 100.

y_low = 0.
y_high = 0.

z_low = 0.
z_high = 100.

vertex = np.zeros((2048,),
                      dtype=[('x', 'f4'), ('y', 'f4'),
                             ('z', 'f4')])

for i in range (point_count):
    vertex[i] = (np.random.uniform(x_low, x_high), np.random.uniform(y_low, y_high), np.random.uniform(z_low, z_high))

print vertex


el = plyfile.PlyElement.describe(vertex, 'vertex')

plyfile.PlyData([el]).write('data/square.ply')
