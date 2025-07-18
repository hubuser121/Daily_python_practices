n=5
for i in range(1,n+1):
    space=" "* (n-i)
    number= " ".join(str(j) for j in range(1,i+1))
    print(space+number)