import tkinter as tk
from tkinter import filedialog, messagebox
import re

def search_for_pattern():
    pattern = entry_pattern.get()
    filename = entry_filename.get()
    text_area.delete('1.0', tk.END)  # Clear the text area for new output
    
    try:
        re_pattern = re.compile(pattern, re.IGNORECASE if var_case_insensitive.get() else 0)
    except re.error:
        messagebox.showerror("Invalid Pattern", "The entered pattern is not a valid regular expression.")
        return

    try:
        with open(filename, 'r') as file:
            line_number = 1
            for line in file:
                if re_pattern.search(line):
                    text_area.insert(tk.END, f"{line_number}: {line}")
                line_number += 1
    except FileNotFoundError:
        text_area.insert(tk.END, "File not found. Please check the filename and try again.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def open_file_dialog():
    filename = filedialog.askopenfilename()
    entry_filename.delete(0, tk.END)  # Clear the entry field
    entry_filename.insert(0, filename)  # Insert the selected filename

# Setup the GUI
root = tk.Tk()
root.title("Python Grep Simulation")

frame_options = tk.Frame(root)
frame_options.pack(pady=5)

tk.Label(frame_options, text="Pattern:").pack(side=tk.LEFT)
entry_pattern = tk.Entry(frame_options)
entry_pattern.pack(side=tk.LEFT, padx=5)

var_case_insensitive = tk.BooleanVar()
check_case_insensitive = tk.Checkbutton(frame_options, text="Case Insensitive", variable=var_case_insensitive)
check_case_insensitive.pack(side=tk.LEFT)

frame_file = tk.Frame(root)
frame_file.pack(pady=5)

tk.Label(frame_file, text="Filename:").pack(side=tk.LEFT)
entry_filename = tk.Entry(frame_file)
entry_filename.pack(side=tk.LEFT, padx=5)

tk.Button(frame_file, text="Browse", command=open_file_dialog).pack(side=tk.LEFT)

tk.Button(root, text="Search", command=search_for_pattern).pack(pady=5)

text_area = tk.Text(root, height=15, width=80)
text_area.pack(padx=10, pady=5)

root.mainloop()
