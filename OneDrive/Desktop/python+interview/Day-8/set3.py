set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}
numbers=[]
for num1 in set1:
    if num1 not in set2:
        numbers.append(num1)
print("the number not in the other set are :",numbers)