import numpy as np
from plyfile import PlyElement, PlyData
from point_cloud import circle

point_count = 2048

radius = 100.
shift = 0

vertex = circle.get_circle_point_cloud(point_count, radius, shift)

el = PlyElement.describe(vertex, 'vertex')

PlyData([el]).write('data/circle.ply')
