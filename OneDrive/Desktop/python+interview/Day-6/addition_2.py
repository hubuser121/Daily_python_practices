matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

for i in range(len(matrix[0])):
    total = 0
    for row in matrix:
        total+=row[i]
    print(f"sum of column {i+1} :",total)
