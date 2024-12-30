#%% 3D Plot of gradient

import numpy as np
import matplotlib.pyplot as plt
from math import e
from sympy import symbols, diff, lambdify

# Define symbolic variables
X_sym, Y_sym = symbols("X Y")

# Define the symbolic function Z
Z = X_sym * e**(-X_sym**2 - Y_sym**2)

# Compute the symbolic derivatives
u = diff(Z, X_sym)  # Gradient with respect to X
v = diff(Z, Y_sym)  # Gradient with respect to Y

# Convert symbolic expressions to numerical functions
u_func = lambdify([X_sym, Y_sym], u, 'numpy')
v_func = lambdify([X_sym, Y_sym], v, 'numpy')

# Create a grid for X and Y
x = np.linspace(-2, 2, 50)
y = np.linspace(-2, 2, 50)
X, Y = np.meshgrid(x, y)

# Evaluate the gradient functions on the grid
u_vals = u_func(X, Y)
v_vals = v_func(X, Y)

# Create the quiver plot
plt.quiver(X, Y, u_vals, v_vals)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Gradient of Z = X * exp(-X^2 - Y^2)')
plt.show()