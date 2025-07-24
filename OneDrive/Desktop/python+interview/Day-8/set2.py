set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}

set=[]

for num1 in set1:
    for num2 in set2:
        if num1==num2:
            set.append(num1)
print(f"the elements that are repeated in both sets are :{set}")
print()