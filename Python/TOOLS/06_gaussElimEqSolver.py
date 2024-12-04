import numpy as np

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
A=np.array([
    [2,2,-1,1],
    [4,3,-1,2],
    [8,5,-3,4],
    [3,3,-2,2]
    ])
B=np.array([[4],
            [6],
            [12],
            [6]])

print(f"Roots are \n {gauss_elim(A, B)}")  


realSol=np.linalg.inv(A).dot(B)
print(f"Real roots are \n {realSol}") 
     