def reverse(word):
    text=word.strip().split()
    reversed_word=text[::-1]
    return " ".join(reversed_word)
print(reverse("hello karthik"))