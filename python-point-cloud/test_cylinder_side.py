import numpy as np
from plyfile import PlyElement, PlyData
from point_cloud import cylinder_side

point_count = 2048

radius = 100.
height = 80.

vertex = cylinder_side.get_cylinder_side_point_cloud(point_count, height, radius)

el = PlyElement.describe(vertex, 'vertex')

PlyData([el]).write('data/cylinder_side.ply')
