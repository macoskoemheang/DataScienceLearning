"""
Python Basics — Quick Reference
Run this file with: python 01.py
"""

# =============================================================
# 1. VARIABLES
# =============================================================
# A variable is a name that points to a value in memory.
# Python is dynamically typed — no need to declare a type.

name = "Alice"          # string
age = 30                # int
height = 1.68           # float
is_student = False      # bool

# Multiple assignment
x, y, z = 1, 2, 3

# Same value to multiple variables
a = b = c = 0

print("--- Variables ---")
print(name, age, height, is_student)
print(x, y, z, a, b, c)


# =============================================================
# 2. DATA TYPES
# =============================================================
# Basic types: int, float, str, bool, complex
# Collection types: list, tuple, dict, set

whole_number = 10                     # int
decimal_number = 3.14                 # float
text = "Hello, Python"                # str
flag = True                           # bool
complex_num = 2 + 3j                  # complex

my_list = [1, 2, 3, "four"]           # list: ordered, mutable
my_tuple = (1, 2, 3)                  # tuple: ordered, immutable
my_dict = {"key": "value", "n": 1}    # dict: key-value pairs
my_set = {1, 2, 3, 2}                 # set: unordered, unique values

print("\n--- Data Types ---")
print(type(whole_number), type(decimal_number), type(text), type(flag), type(complex_num))
print(my_list, my_tuple, my_dict, my_set)

# Type conversion (casting)
str_num = "42"
converted = int(str_num)
print(converted, type(converted))


# =============================================================
# 3. CONDITIONS
# =============================================================
score = 85

print("\n--- Conditions ---")
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print(f"Score: {score}, Grade: {grade}")

# Ternary (conditional expression)
status = "Pass" if score >= 60 else "Fail"
print(status)

# Logical operators: and, or, not
is_weekend = True
is_holiday = False
if is_weekend or is_holiday:
    print("No work today")


# =============================================================
# 4. LOOPS
# =============================================================
print("\n--- Loops ---")

# for loop
for i in range(5):
    print("for i:", i)

# for loop over a collection
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print("fruit:", fruit)

# while loop
count = 0
while count < 3:
    print("while count:", count)
    count += 1

# break and continue
for i in range(10):
    if i == 3:
        continue   # skip this iteration
    if i == 6:
        break      # stop the loop
    print("loop control i:", i)

# List comprehension (compact loop)
squares = [n ** 2 for n in range(5)]
print("squares:", squares)


# =============================================================
# 5. FUNCTIONS
# =============================================================
print("\n--- Functions ---")

def greet(person_name, greeting="Hello"):
    """Return a greeting message for a person."""
    return f"{greeting}, {person_name}!"

print(greet("Bob"))
print(greet("Carol", greeting="Hi"))

# *args and **kwargs
def add_all(*numbers, **options):
    total = sum(numbers)
    if options.get("double"):
        total *= 2
    return total

print(add_all(1, 2, 3, double=True))

# Lambda (anonymous function)
square = lambda n: n ** 2
print(square(6))


# =============================================================
# 6. OOP BASICS
# =============================================================
print("\n--- OOP Basics ---")

class Animal:
    species_count = 0  # class attribute (shared by all instances)

    def __init__(self, name, sound):
        self.name = name        # instance attribute
        self.sound = sound
        Animal.species_count += 1

    def make_sound(self):
        return f"{self.name} says {self.sound}"

    def __str__(self):
        return f"Animal({self.name})"


class Dog(Animal):              # inheritance
    def __init__(self, name):
        super().__init__(name, sound="Woof")

    def fetch(self):            # method unique to Dog
        return f"{self.name} fetches the ball"


generic_animal = Animal("Cat", "Meow")
dog = Dog("Rex")

print(generic_animal.make_sound())
print(dog.make_sound())   # inherited method
print(dog.fetch())        # subclass-specific method
print(f"Total animals created: {Animal.species_count}")
print(generic_animal)     # uses __str__


# =============================================================
# 7. EXCEPTION HANDLING
# =============================================================
print("\n--- Exception Handling ---")

def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: cannot divide by zero")
        return None
    except TypeError:
        print("Error: invalid types for division")
        return None
    else:
        print("Division succeeded")
        return result
    finally:
        print("safe_divide() finished")

print(safe_divide(10, 2))
print(safe_divide(10, 0))

# Raising custom exceptions
class InsufficientFundsError(Exception):
    pass

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError("Not enough balance")
    return balance - amount

try:
    withdraw(100, 150)
except InsufficientFundsError as e:
    print(f"Caught custom exception: {e}")


# =============================================================
# 8. FILE HANDLING
# =============================================================
print("\n--- File Handling ---")

file_path = "sample.txt"

# Writing to a file ("with" auto-closes the file)
with open(file_path, "w") as f:
    f.write("Hello, file!\n")
    f.write("Second line.\n")

# Reading a whole file
with open(file_path, "r") as f:
    content = f.read()
print("File content:\n" + content)

# Reading line by line
with open(file_path, "r") as f:
    for line in f:
        print("line:", line.strip())

# Appending to a file
with open(file_path, "a") as f:
    f.write("Appended line.\n")

# Clean up the demo file
import os
os.remove(file_path)


# =============================================================
# 9. VIRTUAL ENVIRONMENTS
# =============================================================
# A virtual environment is an isolated Python installation so each
# project can have its own dependencies without conflicts.
#
# Create:      python -m venv venv
# Activate:
#   macOS/Linux:  source venv/bin/activate
#   Windows:      venv\Scripts\activate
# Install a package:  pip install requests
# Save dependencies:  pip freeze > requirements.txt
# Install from file:  pip install -r requirements.txt
# Deactivate:         deactivate


# =============================================================
# 10. JUPYTER NOTEBOOK
# =============================================================
# Jupyter Notebook lets you run Python in interactive "cells"
# mixed with text, plots, and outputs — great for data science.
#
# Install:  pip install notebook
# Launch:   jupyter notebook
# Or use JupyterLab:  pip install jupyterlab && jupyter lab
#
# Cell types: Code cells (run with Shift+Enter) and Markdown cells (notes/docs)
# Common magic commands:
#   %timeit some_function()   -> measure execution time
#   %matplotlib inline        -> show plots inside the notebook
#   !pip install pandas       -> run shell commands from a cell


# =============================================================
# 11. GIT + GITHUB BASICS
# =============================================================
# Git tracks changes to your code locally; GitHub hosts remote
# repositories so you can back up and collaborate on that code.
#
# git init                     -> start a new repo
# git status                   -> see changed/untracked files
# git add <file>                -> stage a file for commit
# git add .                     -> stage all changes
# git commit -m "message"      -> save a snapshot with a message
# git log                      -> view commit history
# git branch <name>            -> create a new branch
# git checkout <branch>        -> switch branches
# git checkout -b <branch>     -> create + switch in one step
# git merge <branch>           -> merge a branch into current one
#
# Working with GitHub (remote repo):
# git remote add origin <url>  -> link local repo to GitHub
# git push -u origin main      -> upload commits (first time)
# git push                     -> upload commits (subsequent)
# git pull                     -> download + merge latest changes
# git clone <url>              -> copy a remote repo locally
