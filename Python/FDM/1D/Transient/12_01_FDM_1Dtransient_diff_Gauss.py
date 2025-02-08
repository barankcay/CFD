from sympy import symbols
import numpy as np
import matplotlib.pyplot as plt
import time

start_time = time.time()
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



rN=1 #number of nodes in y axis
cN=10 #number of nodes in x axis

diffusivity=0.002
Lx   =   10  #length of the bar
Ly   = 2
dx  =   Lx/cN #length between each node in x axis

totalTime=12
dt = 0.1   #time step size
numberOfTimeSteps=int(totalTime/dt)
T1=[]

#%% Initial Conditions
TempList    =   np.full((rN,cN+2),20., dtype="object")
coefficientMatrix =  np.zeros((cN,cN))
constantMatrix   =   np.zeros((cN,1))

#%% Boundary Conditions
Twall   =   200
Ttip    =   20 
TempList[0][0] =   Twall
TempList[0][-1]   =   Ttip 
T1=[]
for c in range(1,cN+1):
    TempList[0][c]=symbols(f'T{c}')
print(TempList)

#%% Central Differencing (2nd Order) FDM  

for n in range(numberOfTimeSteps): 
    for r in range(rN):
        for c in range(1, cN+1):
            
                
            eqn=TempList[r][c] - TempList[r][c]-diffusivity*(dt/(dx**2))*(TempList[r][c+1]-2*TempList[r][c]+TempList[r][c-1])
            constantMatrix[c-1][r]=eqn.as_coefficients_dict().get(1,0)
            for m in range(0,cN):
                coefficientMatrix[c-1][m]=-1*eqn.coeff(TempList[r][m+1], 1)
                # print(TempList[r][m+1])
                # print(coefficientMatrix[c-1][m])
    
                  
    resultTemp=gauss_elim(coefficientMatrix, constantMatrix)               
    T1.append(resultTemp[0])
    
    
    
    
for i in range(1,cN+1):
    TempList[0][i]=resultTemp[i-1]  

print(TempList)
              
#%% Residual Check             
    # residual    =   np.ones((rN,cN))        
    # for r in range(rN):
    #     for c in range(cN):
    #         residual[r][c] =   abs(TempList[r][c]-previousTempList[r][c])
            

        
        
    # # plt.plot(np.linspace(1, cN,cN),TempList,"-")
    # e=residual.max()
    # # print(TempList)
    # if e<1E-4:
    #     print(f"solution is converged at iteration {m}, max residual is {e} \n")
    #     # print(residual, "\n")
    #     print(TempList)
    #     break
    # else:
    #     print(f"max residual is {e}, solution is not converged")
        
    #     continue
    
#%% Plotting and Contouring
Y = np.linspace(0, Ly, 3)  # Y-axis with two values
X = np.linspace(0, Lx, cN+3)  # X-axis from 0 to Lx with cN points
Z = np.tile(TempList, (2, 1))  # Replicate TempList to create a shape of (2, cN)
Z = Z.astype(float)

# Create the plot
fig, ax = plt.subplots()

# Plot the temperature distribution with pcolormesh
pc = ax.pcolormesh(X, Y, Z, cmap="coolwarm", vmin=Z.min(), vmax=Z.max())

# Add labels and colorbar
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.colorbar(pc, ax=ax, ticks=np.linspace(Z.min(), Z.max(), cN+2))
plt.xticks(np.arange(0, Lx + 1, 1))
ax.set_aspect("equal")
plt.show()

# Example temperature data points
dataPoints = np.linspace(0,Lx,cN+2)  # X-axis values (you can adjust these if needed)
Temp = TempList[0]  # Corresponding temperature values from TempList

# Plot data points with temperature values
plt.plot(dataPoints, Temp, "-o")
plt.xlabel("x [m]")
plt.ylabel("T [°C]")
plt.show()

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed Time: {elapsed_time} seconds")