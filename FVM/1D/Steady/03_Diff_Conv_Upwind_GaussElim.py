
from sympy import symbols, collect, Matrix
import numpy as np
import matplotlib.pyplot as plt

# Steady state
# 1D
# diffusion + convection
# central differencing applied for diffusion
# upwind differencing applied for convection
#flow direction is from left to right
def gauss_elim(A,B):
    x=np.zeros(B.shape[0])
    if A.shape[0] != A.shape[1]:
        # print("Coefficient matrix is not a square matrix")
        return
    if B.shape[1]!=1 or B.shape[0]!=A.shape[1]:
        # print("Constant matrix is not suitable")
        return
    
    augmented_mat=np.concatenate((A, B), axis=1, dtype=float)
    # print(f"Agumented matrix is \n {augmented_mat} \n")
    n=B.shape[0]
    m=n-1
    for i in range(n-1):
        for j in range(i+1,n):
            ratio=augmented_mat[j][i]/augmented_mat[i][i]
            augmented_mat[j]=augmented_mat[j]-ratio*augmented_mat[i]
    
    
    # print(f"Diagonalized Agumented matrix is \n {augmented_mat} \n")
    x[m]=augmented_mat[m][n]/augmented_mat[m][m]
    for i in range(n-2,-1,-1):
        f=augmented_mat[i][n]
        
        for k in range(i+1,n):
            f=f-augmented_mat[i][k]*x[k]
        x[i]=f/augmented_mat[i][i]
    
        
    return x

N =5 #node number

S = 1000 #source term
a = 1 #surface area
Ly= 4  #length of the bar in y
L = 5 #length of bar in x
k = 100 #conductivity 
T0 = 100
rho=1
cp=1000
U=0.3
exec(f"T{N+1} = 200")
rN=1
cN=5

Lcell = L / N
d = Lcell
V = a * Lcell

Temp = []
coeffMatrix = []
constantMatrix = []


TempList    =   np.zeros((rN,cN+2), dtype="object")
coefficientMatrix =  np.zeros((cN,cN))
constantMatrix   =   np.zeros((cN,rN))


TempList[0][0]=T0
TempList[0][cN+1]=eval(f"T{N+1}")

for c in range(1,cN+1):
    TempList[0][c]=symbols(f'T{c}')
    

     
        
    
for r in range(rN):
    for c in range(1, cN+1):
        if c== 1:
            eqn = (k * a * ((TempList[r][c+ 1] - TempList[r][c]) / d) - k * a * ((TempList[r][c] - T0) / (d / 2))) + S * V +rho*cp*U*a*T0-rho*cp*U*a*(TempList[r][c])


            constantMatrix[c-1][r]=eqn.as_coefficients_dict().get(1,0)
            for m in range(0,cN):
                coefficientMatrix[c-1][m]=-1*eqn.coeff(TempList[r][m+1], 1)
    
                
    
        elif c== cN:
            eqn = (k * a * ((TempList[r][c + 1] - TempList[r][cN]) / (d / 2)) - k * a * ((TempList[r][c] - TempList[r][c - 1]) / d)) + S * V+rho*cp*U*a*TempList[r][c-1] -rho*cp*U*a*TempList[r][c]

            constantMatrix[c-1][r]=eqn.as_coefficients_dict().get(1,0)
            for m in range(0,cN):
                coefficientMatrix[c-1][m]=-1*eqn.coeff(TempList[r][m+1], 1)
                
        else:
            eqn = (k * a * ((TempList[r][c+ 1] - TempList[r][c]) / d) - k * a * ((TempList[r][c] - TempList[r][c- 1]) / d)) + S * V +rho*cp*U*a*TempList[r][c-1]-rho*cp*U*a*TempList[r][c]

            constantMatrix[c-1][r]=eqn.as_coefficients_dict().get(1,0)
            for m in range(0,cN):
                coefficientMatrix[c-1][m]=-1*eqn.coeff(TempList[r][m+1], 1)



resultTemp=gauss_elim(coefficientMatrix, constantMatrix)               


for i in range(1,cN+1):
    TempList[0][i]=resultTemp[i-1]
    

#%% Plotting and Contouring
Y = np.linspace(0,Ly,2)  # Y-axis with two values
X = np.linspace(0, L, cN)  # X-axis from 0 to Lx with cN points
Z = np.tile(resultTemp, (2, 1))  # Replicate TempList to create a shape of (2, 10)

# Create the plot
fig, ax = plt.subplots()

# Plot the temperature distribution with pcolormesh
pc = ax.pcolormesh(X, Y, Z, cmap="coolwarm", vmin=Z.min(), vmax=Z.max())

# Add labels and colorbar
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.colorbar(ax.pcolormesh(X,Y,Z,cmap="coolwarm",vmin=Z.min(),vmax=Z.max()),ax=ax,ticks=np.linspace(Z.min(),Z.max(),N))
ax.set_ylim(0, Ly)
ax.set_aspect("equal")
plt.show()

# Example temperature data points (define your own dataPoints and Temp)
dataPoints = X  # Assuming dataPoints correspond to X
  # Corresponding temperature values

# Plot data points with temperature values

dataPoints=[0]

for i in range(1,cN+2):
    if i==1 or i==cN+1:
        
        dataPoints.append(dataPoints[i-1]+Lcell/2)
        

        

    else:
        
        dataPoints.append(dataPoints[i-1]+Lcell)
plt.plot(dataPoints, TempList[0], "-o")
plt.xlabel("x [m]")
plt.ylabel("T [°C]")
plt.show()

