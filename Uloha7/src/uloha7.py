import numpy as np
import re

# 1. priklad
matrix = np.loadtxt("matrix.txt", dtype='i', delimiter=' ')
det = np.linalg.det(matrix)
inv = np.linalg.inv(matrix)

print(det)
print(inv)

# 2. priklad
matrix2 = np.loadtxt("matrix2.txt", dtype='i', delimiter=' ')
x = np.linalg.solve(matrix, matrix2)

print(x)

# 3. priklad
def solution(file_txt):
    results = []
    matrix = []
    equation = []
    x = []
    y = []
    f = open(file_txt, 'r')
    for line in f:
        equation = re.split(('[=]'), line.strip().replace(" ", ""))
        results.append(int(equation[-1]))
        equation = re.split(('[x-y]'), equation[0])
        matrix.append(equation[:-1])
    
    for i in range(len(matrix)):
        for j in range(2):
            if '+' in matrix[i][j]:
                matrix[i][j] = matrix[i][j].replace("+", "")
            if not matrix[i][j]:
                matrix[i][j] = matrix[i][j].replace("", "1")
            if '-' == matrix[i][j]:
                matrix[i][j] = matrix[i][j].replace("-", "-1")
        
    matrix = np.array(matrix, dtype='i')
    results = np.array(results, dtype='i')
    solution = np.linalg.solve(matrix, results)
    output = "solution: x = %.2f, y = %.2f" % (solution[0], solution[1])
    print(output)

solution('equation.txt')
