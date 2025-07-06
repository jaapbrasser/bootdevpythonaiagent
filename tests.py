# tests.py
from functions.get_file_content import get_file_content

print('\nTest: long lorem.txt (should truncate)')
print(get_file_content("calculator", "lorem.txt"))

print('\nTest: main.py')
print(get_file_content("calculator", "main.py"))

print('\nTest: pkg/calculator.py')
print(get_file_content("calculator", "pkg/calculator.py"))

print('\nTest: /bin/cat (should return error)')
print(get_file_content("calculator", "/bin/cat"))