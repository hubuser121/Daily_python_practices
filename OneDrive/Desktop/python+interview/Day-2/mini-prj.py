numbers=[]
even_counter=0
odd_counter=0
even=[]
odd=[]


def is_even_odd(n):
    global even_counter, even, odd, odd_counter

    if n % 2==0:
        even_counter+=1
        even.append(n)
        return "Even"
    else:
        odd_counter+=1
        odd.append(n)
        return "Odd"
    
def finding_even_max():
    return max(even) if even else " No even numbers "

def finding_odd_max():
    return max(odd) if odd else "No odd numbers"


for i in range(10):
    num=int(input(f"enter the number for the {i+1} "))
    numbers.append(num)
    is_even_odd(num)

print("numbers are :", numbers)
print("even numbers :",even )
print("odd numbers :", odd)
print("even number in list :",even_counter)
print("odd number in list",odd_counter)
print("maximum number in even list :",finding_even_max())
print("maximum number in odd list :",finding_odd_max())