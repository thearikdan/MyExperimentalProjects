import numpy as np
from point_cloud import cylinder
from plyfile import plyfile

point_count = 2048
height = 80
radius = 100

vertex = cylinder.get_cylinder_point_cloud(point_count, height, radius)

el = plyfile.PlyElement.describe(vertex, 'vertex')

plyfile.PlyData([el]).write('data/cylinder.ply')
