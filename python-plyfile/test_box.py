import numpy as np
from plyfile import PlyElement, PlyData
from point_cloud import box

point_count = 2048
length = 100
width = 80
height = 50

vertex = box.get_box_point_cloud(point_count, length, width, height)

el = PlyElement.describe(vertex, 'vertex')

PlyData([el]).write('data/box.ply')
