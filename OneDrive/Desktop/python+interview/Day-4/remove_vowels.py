def remove_vowels(sentences):
    sentence=sentences.strip()
    result=[]
    vowels="aeiouAEIOU"
    for char in sentence:
        if char not in vowels:
            result.append(char)
    return " ".join(result)
print(remove_vowels("    kaRTHIK loves PyThon   "))