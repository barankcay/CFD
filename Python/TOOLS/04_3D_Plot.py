#%% 3D Plot
# importing mplot3d toolkits, numpy and matplotlib
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from math import e 
from sympy import symbols, diff

x,y=symbols("x y")

fig = plt.figure(figsize = (12,10))
ax = plt.axes(projection='3d')

x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)

X, Y = np.meshgrid(x, y)
Z = X*e**(-X**2-(Y**2))

surf = ax.plot_surface(X, Y, Z, cmap = plt.cm.cividis)

# Set axes label
ax.set_xlabel('x', labelpad=20)
ax.set_ylabel('y', labelpad=20)
ax.set_zlabel('z', labelpad=20)

fig.colorbar(surf, shrink=0.5, aspect=8)
plt.xlabel("x")
plt.ylabel("y")

plt.title('Z = X * exp(-X^2 - Y^2)')
plt.show()