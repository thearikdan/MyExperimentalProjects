import numpy
from plyfile import PlyElement, PlyData

vertex = numpy.array([(0, 0, 0),
                       (0, 1, 1),
                       (1, 0, 1),
                       (1, 1, 0)],
                      dtype=[('x', 'f4'), ('y', 'f4'),
                             ('z', 'f4')])

face = numpy.array([([0, 1, 2], 255, 255, 255),
                     ([0, 2, 3], 255,   0,   0),
                     ([0, 1, 3],   0, 255,   0),
                     ([1, 2, 3],   0,   0, 255)],
                    dtype=[('vertex_indices', 'i4', (3,)),
                           ('red', 'u1'), ('green', 'u1'),
                           ('blue', 'u1')])

el = PlyElement.describe(vertex, 'vertex')

PlyData([el]).write('some_binary.ply')
