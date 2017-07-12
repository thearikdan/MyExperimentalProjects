from cylinder import generate_XYZ
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
origin = np.array([0, 0, 0])
#axis and radius
#p0 = np.array([1, 3, 2])
#p1 = np.array([8, 5, 9])
p0 = np.array([0, 0, 0])
p1 = np.array([0, 0, 10])

R = 1
X, Y, Z = generate_XYZ(p0, p1, R)
ax.plot_surface(X, Y, Z)
ax.plot_surface(X + 5, Y, Z)
ax.plot_surface(X, Y + 5, Z)
ax.plot_surface(X + 5, Y + 5, Z)
#plot axis
ax.plot(*zip(p0, p1), color = 'red')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_zlim(0, 10)
plt.show()

