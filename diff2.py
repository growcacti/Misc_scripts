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

    # Highlight differences
    for i, line in enumerate(diff):
        if line.startswith('-'):
            text1.tag_add("delete", f"{i+1}.0", f"{i+1}.end")
        elif line.startswith('+'):
            text2.tag_add("add", f"{i+1}.0", f"{i+1}.end")
        elif line.startswith('?'):
            text1.tag_add("change", f"{i+1}.0", f"{i+1}.end")
            text2.tag_add("change", f"{i+1}.0", f"{i+1}.end")

# Create the main window
root = tk.Tk()
root.title("Side-by-Side File Difference Viewer")

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
