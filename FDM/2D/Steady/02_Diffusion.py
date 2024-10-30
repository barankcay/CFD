import numpy as np
import sys
import matplotlib.pyplot as plt
rN=10 #number of nodes in y axis
cN=10 #number of nodes in x axis

Lx   =   10  #length of the bar
Ly   =   10   
dx  =   Lx/(cN-1) #length between each node in x axis
dy= Ly/(rN-1)

beta=dx/dy
#%% Initial Conditions
TempList    =   np.full((rN,cN),50.)

#%% Boundary Conditions
Twall_n   =   50.
Twall_w   =   80.
Twall_s   =   100.
Twall_e   =   20.

for c in range(cN):
    TempList[0][c]=Twall_n
    TempList[rN-1][c]=Twall_s
for r in range(rN):
    TempList[r][0]=Twall_w
    TempList[r][cN-1]=Twall_e
    
    
#%% Central Differencing (2nd Order) FDM  
iteration   =   100000 #number of iterations


for m in range(iteration):
    previousTempList   =   TempList.copy()
    for r in range(1,rN-1):
        for c in range(1,cN-1):
            # TempList[-1]=TempList[N-2] #this section is for BC
            
            TempList[r][c]     =  0.5*(1/(1+beta**2))*(TempList[r+1][c]+
                                                       TempList[r-1][c]+
                                                       TempList[r][c+1]*beta**2+
                                                       TempList[r][c-1]*beta**2)
#%% Residual Check
    residual    =   np.ones((rN,cN))      
    for r in range(rN):
        for c in range(cN):
            residual[r][c] =   abs(TempList[r][c]-previousTempList[r][c])

        
    # plt.plot(np.arange(0,L,dx),TempList[0],"-")
    e=residual.max()
    # print(TempList)
    if e<1E-4:
        print(f"solution is converged at iteration {m}, max residual is {e} \n")
        # print(residual, "\n")
        # print(TempList)
        break
    else:
        print(f"max residual is {e}, solution is not converged")
        
        continue

#%% Plotting and Contouring

contourTempList=TempList.copy()
for r in range(1,rN+1):
    contourTempList[r-1]=TempList[-r]   #contourTempList yerine np.flipud(TempList) de işe yarar 
    

x= np.linspace(0,Lx,cN)
y= np.linspace(0,Ly,rN)
# Create the contour plot
plt.figure(figsize=(10, 6))
contour = plt.contourf(x, y, contourTempList, levels=50, cmap='viridis')  #coolwarm or jet or turbo or viridis 
plt.colorbar(contour)  # Add a colorbar to indicate values
# plt.gca().invert_yaxis()
plt.title('Temperature Contour Plot')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.grid()

# Show the plot
plt.show()



