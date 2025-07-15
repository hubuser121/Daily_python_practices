def vowel_counter(text):
    count=0
    vowels=["a","e","i","o","u","A","E","I","O","U"]
    for char in text:
        if char in vowels:
            count+=1
    return count
print(vowel_counter("karthik benki"))