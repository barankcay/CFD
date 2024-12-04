def createMatrix(r,c,n):
    matrix=[]
    for i in range(r):
        
        row=[]
        for j in range(c):
            row.append(n*3)
        matrix.append(row)
        
    return matrix

    
createMatrix(1, 3, 5)
            