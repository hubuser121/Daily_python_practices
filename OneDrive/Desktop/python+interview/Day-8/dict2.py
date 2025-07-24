dictionary = {
    "Karthik": 87,
    "Anu": 92,
    "Ravi": 78
}

# Use max() with key argument
topper = max(dictionary, key=dictionary.get)
print(f"Topper: {topper} with {dictionary[topper]} marks")
