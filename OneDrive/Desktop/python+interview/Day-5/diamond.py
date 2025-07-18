n=5
for i in range(1,n+1):
    spaces=" " * (n-i)
    star="*" * (2*i-1)
    print(spaces+star)
for i in range(n-1,0,-1):
    spaces=" " * (n-i)
    star="*" * (2*i-1)
    print(spaces+star)