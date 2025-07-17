def title(text):
    words=text.split()
    sentence=[word.capitalize() for word in words]
    return " ".join(sentence)

print(title(" i enjoy coding nowadays"))