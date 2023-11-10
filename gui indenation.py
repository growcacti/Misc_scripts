import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import textwrap
import re


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
# code_with_incorrect_indentation = '''
# def my_function():
# print("Hello, World!")
# if True:
# print("Inside if")
# for i in range(5):
# print(i)
# '''
# corrected_code = correct_indentation(code_with_incorrect_indentation)
# print(corrected_code)


def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Python Files", "*.py")])
    if file_path:
        with open(file_path, 'r') as file:
            code = file.read()
            code_text.delete(1.0, tk.END)
            code_text.insert(1.0, code)
        root.title(f"Python Indentation Corrector - {file_path}")


def save_file_as():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".py", filetypes=[
            ("Python Files", "*.py")])
    if file_path:
        code = code_text.get(1.0, tk.END)
        corrected_code = correct_indentation(code)
        with open(file_path, 'w') as file:
            file.write(corrected_code)
        messagebox.showinfo(
            "Success",
            "File saved with corrected indentation.")


def correct_and_show():
    code = code_text.get(1.0, tk.END)
    corrected_code = correct_indentation(code)
    code_text.delete(1.0, tk.END)
    code_text.insert(1.0, corrected_code)


root = tk.Tk()
root.title("Python Indentation Corrector")

# Create a menu
menu = tk.Menu(root)
root.config(menu=menu)
file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save As...", command=save_file_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Create the text widget for code
code_text = scrolledtext.ScrolledText(root, undo=True)
code_text.pack(expand=True, fill='both')

# Create a 'Correct Indentation' button
correct_button = tk.Button(
    root,
    text="Correct Indentation",
    command=correct_and_show)
correct_button.pack(side='bottom', fill='x')

# Start the GUI loop
root.mainloop()
