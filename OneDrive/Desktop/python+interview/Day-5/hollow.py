n=5
for i in range(1,n+1):
    spaces=" " * (n-i)
    if i==1:
        print(spaces+ "*")
    elif i==n:
        star="*"*(2*i-1)
        print(spaces+star)
    else:
        middle_star=" "*(2*i-3)
        print(spaces+"*"+middle_star+"*")
    
    