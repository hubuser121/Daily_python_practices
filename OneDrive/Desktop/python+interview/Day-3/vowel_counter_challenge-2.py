def vowel_counter(name):
    counter=0
    vowels="aeiouAEIOU"
    for char in name:
        if char in vowels:
            counter+=1  
    print("no of vowels are :", counter)
vowel_counter(" karthik naik ")