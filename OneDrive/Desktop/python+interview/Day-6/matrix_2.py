matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

for i in range(len(matrix[0])):
    for row in matrix:
        print(f"{row[i]}",end=" ")
    print()

