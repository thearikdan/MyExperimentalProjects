import numpy as np
from point_cloud import cone
from plyfile import plyfile
import math

point_count = 2048
angle = 60
radius = 100

rad = math.radians(angle)

vertex = cone.get_cone_point_cloud(point_count, rad, radius)

el = plyfile.PlyElement.describe(vertex, 'vertex')

name = "data/cone_" + str(int(angle)) + "_" + str(int(radius)) + ".ply"  

plyfile.PlyData([el]).write(name)
