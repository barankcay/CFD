def MatrixTranspose(M):
    r=len(M)
    c=len(M[0])
    transposeMatrix=[]
    for x in range(c):
        
        row=[]
        for y in range(r):
            
            row.append(M[y][x])
        transposeMatrix.append(row)
    print(transposeMatrix)

M=[[15, 29, 26], [-1, 49,59]] 
MatrixTranspose(M)
        