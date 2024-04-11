import tkinter as tk
from tkinter import filedialog
import re

def search_for_pattern():
    pattern = entry_pattern.get()
    filename = entry_filename.get()
    text_area.delete('1.0', tk.END)  # Clear the text area for new output
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                if re.search(pattern, line):
                    text_area.insert(tk.END, line)
    except FileNotFoundError:
        text_area.insert(tk.END, "File not found. Please check the filename and try again.")

def open_file_dialog():
    filename = filedialog.askopenfilename()
    entry_filename.delete(0, tk.END)  # Clear the entry field
    entry_filename.insert(0, filename)  # Insert the selected filename

# Setup the GUI
root = tk.Tk()
root.title("Python Grep Simulation")

tk.Label(root, text="Pattern:").pack()
entry_pattern = tk.Entry(root)
entry_pattern.pack()

tk.Label(root, text="Filename:").pack()
entry_filename = tk.Entry(root)
entry_filename.pack()

tk.Button(root, text="Browse", command=open_file_dialog).pack()
tk.Button(root, text="Search", command=search_for_pattern).pack()

text_area = tk.Text(root, height=10, width=50)
text_area.pack()

root.mainloop()

