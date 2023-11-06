import autopep8

# Read the content of your Python file
with open('example.py', 'r') as file:
    code = file.read()

# Use autopep8 to format the code
formatted_code = autopep8.fix_code(code, options={'aggressive': 1})

# Write the formatted code back to the file or a new file
with open('example_fixed.py', 'w') as file:
    file.write(formatted_code)
