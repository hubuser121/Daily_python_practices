matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Print main diagonal: 1, 5, 9
# Print secondary diagonal: 3, 5, 7
main=[]
second=[]
for i in range(len(matrix[0])):
    main.append(matrix[i][i])
    second.append(matrix[i][len(matrix)-1-i])
print("first diagonal :",main)
print("second diagonal :",second)