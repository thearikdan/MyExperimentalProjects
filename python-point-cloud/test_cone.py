import numpy as np
from point_cloud import cone
from plyfile import plyfile

point_count = 2048
angle = np.pi / 3
radius = 100

vertex = cone.get_cone_point_cloud(point_count, angle, radius)

el = plyfile.PlyElement.describe(vertex, 'vertex')

plyfile.PlyData([el]).write('data/cone.ply')
