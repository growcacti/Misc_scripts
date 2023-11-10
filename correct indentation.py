import re
import textwrap


def correct_indentation(code):
    # Remove any common leading whitespace from every line
    code = textwrap.dedent(code)

    # Split the code into lines
    lines = code.split('\n')

    # Stack to keep track of indentation levels
    indent_stack = []

    # Processed lines with correct indentation
    corrected_lines = []

    # Regular expressions for detecting increases and decreases in indentation
    increase_indent_pattern = r':\s*(#.*)?$'
    decrease_indent_patterns = [
        r'^\s*return\b',
        r'^\s*break\b',
        r'^\s*continue\b',
        r'^\s*pass\b',
        r'^\s*raise\b']

    # Process each line
    for line in lines:
        stripped_line = line.strip()

        # If the line is empty or a comment, we don't change the indentation
        if not stripped_line or stripped_line.startswith('#'):
            corrected_lines.append(line)
            continue

        # Check if the line should decrease the indentation
        while indent_stack and any(re.match(pat, line)
                                   for pat in decrease_indent_patterns):
            indent_stack.pop()

        # Correct the indentation
        corrected_line = ('    ' * len(indent_stack)) + stripped_line
        corrected_lines.append(corrected_line)

        # Check if the line should increase the indentation
        if re.search(increase_indent_pattern, stripped_line):
            indent_stack.append(stripped_line)

    # Join the lines back into a single string
    return '\n'.join(corrected_lines)


# Example usage
code_with_incorrect_indentation = '''
def my_function():
print("Hello, World!")
if True:
print("Inside if")
for i in range(5):
print(i)
'''
corrected_code = correct_indentation(code_with_incorrect_indentation)
print(corrected_code)
