matrix=[]

row=int(input("enter number of rows: "))
cols=int(input("enter number of column: "))

for i in range(row):
    row_input=input(f"enter row{i+1} value with {cols} column values :")
    row=list(map(int, row_input.strip().split()))
    matrix.append(row)

print("\n Matrix ")
for row in matrix :
    for element in row:
        print(element,end="")
    print()