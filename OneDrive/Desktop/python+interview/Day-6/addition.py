matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

for i in range(len(matrix[0])):
    total=sum(matrix[i])
    print(f"the total of row {i+1} = {total}" )