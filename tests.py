# tests.py
from functions.run_python import run_python_file

print('\nTest: run main.py')
print(run_python_file("calculator", "main.py"))

print('\nTest: run tests.py')
print(run_python_file("calculator", "tests.py"))

print('\nTest: run ../main.py (outside working dir)')
print(run_python_file("calculator", "../main.py"))

print('\nTest: run nonexistent.py')
print(run_python_file("calculator", "nonexistent.py"))
