dictionary={}
text="karthik loves python  and karthik loves coding "
word=text.lower().split()
for char in word:
    if char in dictionary:
        dictionary[char]+=1
    else:
        dictionary[char]=1
print(dictionary)