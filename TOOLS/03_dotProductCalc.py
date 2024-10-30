def DotProduct(M1,M2):
    r=len(M1)
    if not r==1:
        print("dot product is not applicable")
        
    c=len(M2[0])
    if not c==3:
        print("dot product is not applicable")
    for i in range(r):
        result=0
        for j in range(c):
            result+=M1[i][j]*M2[i][j]
    
    return result

MAT1=createMatrix(1, 3, 7)
MAT2=createMatrix(1, 3, 2)
print(DotProduct(MAT1, MAT2))