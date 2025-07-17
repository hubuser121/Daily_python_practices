dict={}

text="  karthik naik  "
name=text.strip().lower()
for char in name:

    if char==" ":
        continue
    elif char in dict:
        dict[char]+=1
    else:
        dict[char]=1
print(dict)