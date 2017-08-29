import numpy as np
from plyfile import PlyElement, PlyData
from point_cloud import sphere

point_count = 2048

radius = 100.

vertex = sphere.get_sphere_point_cloud(point_count, radius)

el = PlyElement.describe(vertex, 'vertex')

PlyData([el]).write('data/sphere.ply')
