a=int(input("enter first number "))
b=int(input("enter second number "))
c=int(input("enter third number "))

if a>=b and a>=c:
    print(" first number is greater ",a)
elif b>=a and b>=c:
    print("Second number is greater ",b)
else :
    print("third number is greater ",c)