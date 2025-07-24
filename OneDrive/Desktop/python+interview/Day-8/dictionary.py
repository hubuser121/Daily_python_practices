s="banana"
elements={}
for letter in s:
    if letter in elements:
        elements[letter] +=1
    else:
        elements[letter] =1

for letter, count in elements.items():
    print(f"letter {letter} is repeated {count} times")