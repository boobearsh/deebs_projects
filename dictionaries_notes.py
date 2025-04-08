# A dictionary is a collection of key-value pairs that are unordered, changeable, and indexed

# 1. Creating dictionaries
# Method 1: Using curly braces
student = {
    "name": "John",
    "age": 20,
    "grades": [85, 90, 88]
}

# Method 2: Using dict() constructor
student2 = dict(name="Alice", age=19, grades=[92, 88, 95])

# Method 3: Creating an empty dictionary
empty_dict = {}

# 2. Accessing dictionary values
print(student["name"])  # Output: John
print(student.get("age"))  # Output: 20
# Using get() is safer as it returns None if key doesn't exist
print(student.get("address", "Not found"))  # Output: Not found

# 3. Modifying dictionaries
# Adding new key-value pairs
student["email"] = "john@example.com"

# Updating existing values
student["age"] = 21

# 4. Dictionary methods
# keys() - returns all keys
print(student.keys())  # Output: dict_keys(['name', 'age', 'grades', 'email'])

# values() - returns all values
# Output: dict_values(['John', 21, [85, 90, 88], 'john@example.com'])
print(student.values())

# items() - returns all key-value pairs
# Output: dict_items([('name', 'John'), ('age', 21), ...])
print(student.items())

# 5. Checking if key exists
if "name" in student:
    print("Name exists in dictionary")

# 6. Removing items
# Using del
del student["email"]

# Using pop()
age = student.pop("age")  # Removes and returns the value
print(age)  # Output: 21

# Using popitem() - removes the last inserted item
last_item = student.popitem()
print(last_item)  # Output: ('grades', [85, 90, 88])

# 7. Nested dictionaries
school = {
    "students": {
        "john": {"age": 20, "grade": "A"},
        "alice": {"age": 19, "grade": "B"}
    },
    "teachers": {
        "math": "Mr. Smith",
        "science": "Mrs. Johnson"
    }
}

# Accessing nested dictionary values
print(school["students"]["john"]["grade"])  # Output: A
print(school["teachers"]["math"])  # Output: Mr. Smith

# 8. Dictionary comprehension
squares = {x: x**2 for x in range(5)}
print(squares)  # Output: {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 9. Merging dictionaries
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}

# Method 1: Using update()
dict1.update(dict2)
print(dict1)  # Output: {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# Method 2: Using | operator (Python 3.9+)
dict3 = {"e": 5, "f": 6}
merged = dict1 | dict3
print(merged)  # Output: {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}

# 10. Common use cases
# Counting occurrences
text = "hello world hello python"
word_count = {}
for word in text.split():
    word_count[word] = word_count.get(word, 0) + 1
print(word_count)  # Output: {'hello': 2, 'world': 1, 'python': 1}

# Grouping items
fruits = ["apple", "banana", "cherry", "date", "elderberry"]
fruit_lengths = {}
for fruit in fruits:
    length = len(fruit)
    if length not in fruit_lengths:
        fruit_lengths[length] = []
    fruit_lengths[length].append(fruit)
# Output: {5: ['apple'], 6: ['banana', 'cherry'], 4: ['date'], 10: ['elderberry']}
print(fruit_lengths)
