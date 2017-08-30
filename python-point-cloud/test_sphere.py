import numpy as np
from plyfile import plyfile
from point_cloud import sphere

point_count = 2048

radius = 100.

vertex = sphere.get_sphere_point_cloud(point_count, radius)

el = plyfile.PlyElement.describe(vertex, 'vertex')

plyfile.PlyData([el]).write('data/sphere.ply')
