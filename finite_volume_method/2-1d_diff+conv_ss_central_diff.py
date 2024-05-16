
from sympy import symbols, collect, Matrix
import numpy as np
import matplotlib.pyplot as plt

# Steady state
# 1D
# diffusion + convection
# central differencing applied for diffusion
# central differencing applied for convection




N =5

S = 1000
a = 0.5
L = 5
k = 100
T0 = 100
rho=1
cp=1000
U=0.1
exec(f"T{N+1} = 200")

Lcell = L / N
d = Lcell
V = a * Lcell

Temp = []
coeffMatrix = []
constantMatrix = []

for i in range(N + 2):
    if i==0:
        Temp.append(eval(f'T{i}'))
    elif i==N+1:
        Temp.append(eval(f'T{i}'))        
    else:
        Temp.append(symbols(f'T{i}'))        
        
    

for i in range(1, N + 1):
    if i == 1:
        eqn = (k * a * ((Temp[i + 1] - Temp[i]) / d) - k * a * ((Temp[i] - T0) / (d / 2))) + S * V +rho*cp*U*a*T0-rho*cp*U*a*(Temp[i]+Temp[i+1])/2
        coefficients = collect(eqn, Temp[1:N+1], evaluate=False)
        constantMatrix.append(coefficients[1])
        # print(constantMatrix)
        for j in range(1, N + 1):
            coeffMatrix.append(-1*coefficients.get(Temp[j], 0))
            

    elif i == N:
        eqn = (k * a * ((Temp[N + 1] - Temp[N]) / (d / 2)) - k * a * ((Temp[N] - Temp[N - 1]) / d)) + S * V+rho*cp*U*a*(Temp[i]+Temp[i-1])/2 -rho*cp*U*a*Temp[N+1]
        coefficients = collect(eqn, Temp[1:N+1], evaluate=False)
        constantMatrix.append(coefficients[1])
        # print(constantMatrix)

        for j in range(1, N + 1):
            coeffMatrix.append(-1*coefficients.get(Temp[j], 0))
            
    else:
        eqn = (k * a * ((Temp[i + 1] - Temp[i]) / d) - k * a * ((Temp[i] - Temp[i - 1]) / d)) + S * V +rho*cp*U*a*(Temp[i]+Temp[i-1])/2-rho*cp*U*a*(Temp[i]+Temp[i+1])/2
        coefficients = collect(eqn, Temp[1:N+1], evaluate=False)
        constantMatrix.append(coefficients[1])
        # print(constantMatrix)

        for j in range(1, N + 1):
            coeffMatrix.append(-1*coefficients.get(Temp[j], 0))
            

# Define variables

coeffFinalMatrix = Matrix(N, N, coeffMatrix)
constantFinalMatrix = Matrix(constantMatrix)

solution = coeffFinalMatrix.inv() * constantFinalMatrix
#print(solution)


for u in range(1,N+1):
    Temp[u]=solution[u-1]


#Comparison with analytical solution

dataPoints=[0]

for i in range(1,N+2):
    if i==1 or i==N+1:
        
        dataPoints.append(dataPoints[i-1]+Lcell/2)
        

        

    else:
        
        dataPoints.append(dataPoints[i-1]+Lcell)

newData=[]

for i in range(0,N+1):
    newData.append(i*Lcell)

newTemp=[]
for i in range(0,len(solution)):
    newTemp.append(solution[i])
Nrows=1
Ncols=len(solution)

Y=np.arange(0,2*a,a)
X=np.array(newData)
Z=np.array(newTemp).astype(float).reshape(Nrows,Ncols)


fig, ax=plt.subplots()

ax.pcolormesh(newData,Y,Z,cmap="coolwarm",vmin=Z.min(),vmax=Z.max())


plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.colorbar(ax.pcolormesh(newData,Y,Z,cmap="coolwarm",vmin=Z.min(),vmax=Z.max()),ax=ax,ticks=np.linspace(Z.min(),Z.max(),N))
ax.set_aspect("equal")
plt.show()



plt.plot(dataPoints,Temp,"-o")

plt.xlabel("x [m]")
plt.ylabel("T [C]")


plt.show()

print(f"Peclet number = {rho*cp*a*U*d/(k*a)}")
