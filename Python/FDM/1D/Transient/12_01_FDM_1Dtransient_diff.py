import numpy as np
import sys
import matplotlib.pyplot as plt
import time
start_time=time.time()
rN=1 #number of nodes in y axis
cN=8 #number of nodes in x axis
diffusivity=0.2

Lx   =   10  #length of the bar
Ly   = 2
dx  =   Lx/cN #length between each node in x axis

totalTime=1000
dt = 3   #time step size
numberOfTimeSteps=int(totalTime/dt)
T1=[]
d=diffusivity*dt/(dx**2)

if d <= 0.5:
    print(f"d is equal to {d}")
    print("soluton is stable")
else:
    print(f"d is equal to {d}")
    print("soluton is unstable")
    sys.exit(0)

#%% Initial Conditions
TempList    =   np.full((rN,cN),30.)

#%% Boundary Conditions
Twall   =   300
Ttip    =   50 
TempList[0][0] =   Twall
TempList[0][cN-1]   =   Ttip 


#%% FTCS (Forward in time-central in space) 

for m in range(numberOfTimeSteps):
    previousTempList   =   TempList.copy()
    for r in range(rN):
        for c in range(1,cN-1):
            # TempList[-1]=TempList[N-2] #this section is for BC
            
            TempList[r][c]     =   TempList[r][c]+diffusivity*(dt/(dx**2))*(TempList[r][c+1]-2*TempList[r][c]+TempList[r][c-1])
            if c==1:
                T1.append(TempList[r][c])
            
    #%% Plotting and Contouring
    # Y = np.linspace(0, Ly, 3)  # Y-axis with two values
    # X = np.linspace(0, Lx, cN+1)  # X-axis from 0 to Lx with cN points
    # Z = np.tile(TempList, (2, 1))  # Replicate TempList to create a shape of (2, 10)

    # # Create the plot
    # fig, ax = plt.subplots()

    # # Plot the temperature distribution with pcolormesh
    # pc = ax.pcolormesh(X, Y, Z, cmap="coolwarm", vmin=Z.min(), vmax=Z.max())
    # plt.xticks(np.arange(0, Lx + 1, 1))

    # # Add labels and colorbar
    # plt.xlabel("x [m]")
    # plt.ylabel("y [m]")
    # plt.colorbar(pc, ax=ax, ticks=np.linspace(Z.min(), Z.max(), cN))
    # ax.set_aspect("equal")
    # plt.show()

# %% Residual Check             
    # residual    =   np.ones((rN,cN))        
    # for r in range(rN):
    #     for c in range(cN):
    #         residual[r][c] =   abs(TempList[r][c]-previousTempList[r][c])
            

        
        
    # # plt.plot(np.linspace(1, cN,cN),TempList,"-")
    # e=residual.max()
    # # print(TempList)
    # if e<0.25:
    #     print(f"solution is converged at second {m}, max residual is {e} \n")
    #     # print(residual, "\n")
    #     print(TempList)
    #     break
    # else:
    #     print(f"max residual is {e}, solution is not converged")
        
    #     continue

    




# # Example temperature data points (define your own dataPoints and Temp)
# dataPoints = np.linspace(0, Lx, cN)  # Assuming dataPoints correspond to X
# Temp = TempList[0]  # Corresponding temperature values

# # Plot data points with temperature values
# plt.plot(dataPoints, Temp, "-o")
# plt.xlabel("x [m]")
# plt.ylabel("T [°C]")
# plt.show()


print(TempList)
end_time=time.time()
elapsed_time = end_time - start_time
print(f"Elapsed Time: {elapsed_time} seconds")

# f=np.linspace(0,m+1,m+1)            
# plt.plot(f,T1,"-")
# plt.show()