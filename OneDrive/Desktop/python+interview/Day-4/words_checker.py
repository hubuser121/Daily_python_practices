def repeated_words(text):
    seen=set()
    result=""

    word=text.strip().lower()
    for char in word:
        if char not in seen:
            result+=char
            seen.add(char)

    return result

print(repeated_words("  karthikkkk   "))