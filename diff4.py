import tkinter as tk
from tkinter import filedialog
import difflib

# Function to load a file
def load_file():
    filepath = filedialog.askopenfilename()
    with open(filepath, 'r') as file:
        return file.readlines()

# Function to show the difference between two files
def show_diff():
    # Clear previous content
    text1.delete(1.0, tk.END)
    text2.delete(1.0, tk.END)

    # Load two files
    file1_lines = load_file()
    file2_lines = load_file()

    # Insert the lines into the text widgets
    text1.insert(tk.END, ''.join(file1_lines))
    text2.insert(tk.END, ''.join(file2_lines))

    # Calculate the differences using difflib
    diff = list(difflib.ndiff(file1_lines, file2_lines))

    # Variables to keep track of line numbers for text widgets
    line_num1, line_num2 = 1, 1

    for line in diff:
        if line.startswith('-'):
            # Line is present in the first file but not in the second (deletion)
            text1.tag_add("delete", f"{line_num1}.0", f"{line_num1}.end")
            line_num1 += 1
        elif line.startswith('+'):
            # Line is present in the second file but not in the first (addition)
            text2.tag_add("add", f"{line_num2}.0", f"{line_num2}.end")
            line_num2 += 1
        elif line.startswith(' '):
            # Line is the same in both files (no change)
            line_num1 += 1
            line_num2 += 1
        elif line.startswith('?'):
            # Line has been modified (change)
            text1.tag_add("change", f"{line_num1 - 1}.0", f"{line_num1 - 1}.end")
            text2.tag_add("change", f"{line_num2 - 1}.0", f"{line_num2 - 1}.end")

# Create the main window
root = tk.Tk()
root.title("Side-by-Side File Difference Viewer")

# Add a label showing "V" at the top
label = tk.Label(root, text="V", font=("Helvetica", 16))
label.pack()

# Define two text widgets side by side
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

text1 = tk.Text(frame, width=60)
text1.pack(side="left", fill="both", expand=True)

text2 = tk.Text(frame, width=60)
text2.pack(side="right", fill="both", expand=True)

# Create tags for different types of changes
text1.tag_config("delete", background="red")
text2.tag_config("add", background="green")
text1.tag_config("change", background="yellow")
text2.tag_config("change", background="yellow")

# Button to load files and show the difference
load_button = tk.Button(root, text="Load Files and Show Difference", command=show_diff)
load_button.pack()

# Run the Tkinter event loop
root.mainloop()
