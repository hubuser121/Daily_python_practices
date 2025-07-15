num=int(input("enter a number "))
fact=1
if num <0:
    print("factorial of negative number cant be done ")
elif num==0:
    print("factorial of 0 is 1")
else:
    for i in range(1,num+1):
        fact*=i
    print(f"factorial of the {num} is: {fact} ")