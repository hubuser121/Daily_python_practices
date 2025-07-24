t=(1,2,2,3,3,4,4,4,4,4,6,9)
count=0
num1=[]
for num in t:
    if num not in num1:
        num1.append(num)
        count+=1
        print(f"the number {num} repeated {(t.count(num))} times")
print(f"the unique values are :",num1)