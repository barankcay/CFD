from sympy import symbols
import numpy as np
import matplotlib.pyplot as plt
import time

start_time = time.time()
def gauss_elim(A,B):
    x=np.zeros(B.shape[0])
    if A.shape[0] != A.shape[1]:
        print("Coefficient matrix is not a square matrix")
        return
    if B.shape[1]!=1 or B.shape[0]!=A.shape[1]:
        print("Constant matrix is not suitable")
        return
    
    augmented_mat=np.concatenate((A, B), axis=1, dtype=float)
    print(f"Agumented matrix is \n {augmented_mat} \n")
    n=B.shape[0]
    m=n-1
    for i in range(n-1):
        for j in range(i+1,n):
            ratio=augmented_mat[j][i]/augmented_mat[i][i]
            augmented_mat[j]=augmented_mat[j]-ratio*augmented_mat[i]
    
    
    print(f"Diagonalized Agumented matrix is \n {augmented_mat} \n")
    x[m]=augmented_mat[m][n]/augmented_mat[m][m]
    for i in range(n-2,-1,-1):
        f=augmented_mat[i][n]
        
        for k in range(i+1,n):
            f=f-augmented_mat[i][k]*x[k]
        x[i]=f/augmented_mat[i][i]
    
        
    return x


rN=20 #number of nodes in y axis
cN=20 #number of nodes in x axis

Lx   =   20  #length of the bar
Ly   =   20   
dx  =   Lx/(cN-1) #length between each node in x axis
dy= Ly/(rN-1)

beta=dx/dy

x= np.linspace(0,Lx,cN+2)
y= np.linspace(0,Ly,rN+2)
Twall_n   =   50.
Twall_w   =   80.
Twall_s   =   100.
Twall_e   =   20.

TempList    =   np.full((rN+2,cN+2),120., dtype="object")

coefficientMatrix =  np.zeros((cN*rN,cN*rN))
constantMatrix   =   np.zeros((cN*rN,1))


TempList[0]=Twall_n
TempList[-1]=Twall_s
for r in range(rN+2):
    TempList[r][0]=Twall_w
    TempList[r][-1]=Twall_e

for r in range(1,rN+1):
    for c in range(1,cN+1):
        TempList[r][c]=symbols(f'T{r}_{c}')
        


# residual    =   np.ones((rN,cN))

i=0
for r in range(1,rN+1):
    
    for c in range(1,cN+1):
        
        # TempList[-1]=TempList[N-2] #this section is for BC
        
        eqn= TempList[r][c]- 0.5*(1/(1+beta**2))*(TempList[r+1][c]+TempList[r-1][c]+TempList[r][c+1]*(beta**2)+TempList[r][c-1]*(beta**2))
                                           
                                                   
        # print(TempList[r][c])
        constantMatrix[i][0]=eqn.as_coefficients_dict().get(1,0) 
                                                                           
        # for m in range(0,cN):
        #     coeff.append(-1*eqn.coeff(TempList[r][m+1], 1))
        # coefficientMatrix[i]=coeff
            # for l in range(0,cN*rN):
        coeff=[]
        for f in range(1,rN+1):
            
            for g in range(1,cN+1):
                                                                           
                coeff.append(-1*eqn.coeff(TempList[f][g], 1))

                    # print(m)
                    # print(coefficientMatrix[r-1][m])
                # x=x+1
                # print(-1*eqn.coeff(TempList[r][m+1], 1))
        # print(coeff)

        coefficientMatrix[i]=coeff
        i+=1 
            
    
resultTemp=gauss_elim(coefficientMatrix, constantMatrix)                                                                                          
p=0
for r in range(1,rN+1):                                                                           
    for c in range(1,cN+1):                                                                           
        TempList[r][c]=resultTemp[p]
        p+=1                                                                           
       

      

print(TempList)             
#%% Residual Check             
    # for r in range(rN):
    #     for c in range(cN):
    #         residual[r][c] =   abs(TempList[r][c]-previousTempList[r][c])
            

        
        
    # # plt.plot(np.arange(0,L,dx),TempList[0],"-")
    # e=residual.max()
    # # print(TempList)
    # if e<1E-4:
    #     print(f"solution is converged at iteration {m}, max residual is {e} \n")
    #     # print(residual, "\n")
    #     # print(TempList)
    #     break
    # else:
    #     print(f"max residual is {e}, solution is not converged")
        
    #     continue






#%% Plotting and Contouring
contourTempList=TempList.copy()
for r in range(0,rN+2):
    contourTempList[r-1]=TempList[-r]    
Z=np.array(contourTempList,dtype=float)
X, Y = np.meshgrid(x, y)

# Create the contour plot
plt.figure(figsize=(10, 6))
contour = plt.contourf(X, Y, Z, levels=50, cmap='viridis')  #coolwarm or jet or turbo or viridis Adjust levels and colormap as needed
plt.colorbar(contour)  # Add a colorbar to indicate values
plt.title('Temperature Contour Plot')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.grid()

# Show the plot
plt.show()
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed Time: {elapsed_time} seconds")