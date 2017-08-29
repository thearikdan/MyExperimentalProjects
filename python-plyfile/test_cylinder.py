import numpy as np
from plyfile import PlyElement, PlyData
from point_cloud import cylinder

point_count = 2048
height = 80
radius = 100

vertex = cylinder.get_cylinder_point_cloud(point_count, height, radius)

el = PlyElement.describe(vertex, 'vertex')

PlyData([el]).write('data/cylinder.ply')
