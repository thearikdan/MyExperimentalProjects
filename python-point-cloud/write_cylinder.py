import numpy as np
from point_cloud import cylinder
from plyfile import plyfile

point_count = 2048
height = 80
radius = 100

vertex = cylinder.get_cylinder_point_cloud(point_count, height, radius)

el = plyfile.PlyElement.describe(vertex, 'vertex')

name = "data/cylinder_" + str(int(height)) + "_" + str(int(radius)) + "_.ply"  

plyfile.PlyData([el]).write(name)
