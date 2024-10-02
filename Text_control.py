import os
import tkinter as tk
from tkinter import filedialog, Text, messagebox
from tkinter import ttk

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_var.set(directory)
        file_list = [f for f in os.listdir(directory) if f.endswith('.txt')]
        file_listbox.delete(0, tk.END)
        for file in file_list:
            file_listbox.insert(tk.END, file)

def extract_text():
    directory = directory_var.get()
    selected_file = file_listbox.get(tk.ACTIVE)
    file_path = os.path.join(directory, selected_file)

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            start_line = int(start_line_spinbox.get())
            end_line = int(end_line_spinbox.get())
            parsed_text = ''.join(lines[start_line - 1:end_line])
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, parsed_text)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def find_and_replace():
    search_text = search_var.get()
    replace_text = replace_var.get()

    content = result_text.get(1.0, tk.END)
    modified_content = content.replace(search_text, replace_text)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, modified_content)

def save_to_file():
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if save_path:
        try:
            with open(save_path, 'w') as file:
                file.write(result_text.get(1.0, tk.END))
            messagebox.showinfo("Success", "File saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Text File Extractor")

directory_var = tk.StringVar()
search_var = tk.StringVar()
replace_var = tk.StringVar()

# Directory selection
tk.Label(root, text="Select Directory:").pack(pady=5)
directory_entry = tk.Entry(root, textvariable=directory_var, width=50)
directory_entry.pack(pady=5)
tk.Button(root, text="Browse", command=browse_directory).pack(pady=5)

# Listbox to display text files in directory
tk.Label(root, text="Text Files:").pack(pady=5)
file_listbox = tk.Listbox(root, width=50, height=5)
file_listbox.pack(pady=5)

# Spinboxes to select line range
tk.Label(root, text="Select Line Range:").pack(pady=5)
start_line_spinbox = ttk.Spinbox(root, from_=1, to=100, width=5)
start_line_spinbox.pack(side=tk.LEFT, padx=(20, 10))
tk.Label(root, text="to").pack(side=tk.LEFT)
end_line_spinbox = ttk.Spinbox(root, from_=1, to=100, width=5)
end_line_spinbox.pack(side=tk.LEFT, padx=(10, 20))

# Extract button
tk.Button(root, text="Extract Text", command=extract_text).pack(pady=5)

# Text widget to display extracted text
tk.Label(root, text="Extracted Text:").pack(pady=5)
result_text = Text(root, width=60, height=10)
result_text.pack(pady=5)

# Find and Replace
tk.Label(root, text="Find:").pack(pady=5)
tk.Entry(root, textvariable=search_var, width=30).pack(pady=5)
tk.Label(root, text="Replace:").pack(pady=5)
tk.Entry(root, textvariable=replace_var, width=30).pack(pady=5)
tk.Button(root, text="Find and Replace", command=find_and_replace).pack(pady=5)

# Save button
tk.Button(root, text="Save to File", command=save_to_file).pack(pady=5)

root.mainloop()
