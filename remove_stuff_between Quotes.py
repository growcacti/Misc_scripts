import os
import re
import time
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def remove_content_between_quotes(text, single_replace, double_replace):
    # Replace content between single quotes with specified replacement
    text = re.sub(r"'[^']*'", single_replace, text)
    # Replace content between double quotes with specified replacement
    text = re.sub(r'"[^"]*"', double_replace, text)
    return text

def create_backup_folder(directory):
    # Create a unique backup folder with epoch timestamp
    timestamp = str(int(time.time()))
    backup_folder = os.path.join(directory, f"backup_{timestamp}")
    os.makedirs(backup_folder, exist_ok=True)
    return backup_folder

def process_single_file(file_path, backup_folder, single_replace, double_replace):
    # Copy the file to the backup folder
    filename = os.path.basename(file_path)
    backup_file_path = os.path.join(backup_folder, filename)
    shutil.copy2(file_path, backup_file_path)

    # Modify the copied file
    with open(backup_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    updated_content = remove_content_between_quotes(content, single_replace, double_replace)

    with open(backup_file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"Processed file: {backup_file_path}")

def process_directory(directory, backup_folder, single_replace, double_replace):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                process_single_file(file_path, backup_folder, single_replace, double_replace)

def browse_path():
    if file_or_directory.get() == "directory":
        path = filedialog.askdirectory()
    else:
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"),("Python Scripts", "*.py"),("All Files", "*.*")])
    
    if path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, path)

def apply_changes():
    path = path_entry.get()
    single_replace = single_quote_entry.get() or "''"
    double_replace = double_quote_entry.get() or '""'

    if not path:
        messagebox.showwarning("Path Required", "Please select a file or directory.")
        return

    # Determine backup folder location
    parent_dir = os.path.dirname(path) if file_or_directory.get() == "file" else path
    backup_folder = create_backup_folder(parent_dir)

    # Process files based on selection
    if file_or_directory.get() == "directory":
        process_directory(path, backup_folder, single_replace, double_replace)
    else:
        process_single_file(path, backup_folder, single_replace, double_replace)

    messagebox.showinfo("Process Complete", f"Text processing complete. Modified files are saved in {backup_folder}.")

# GUI setup
root = tk.Tk()
root.title("Find and Replace Text Between Quotes")
root.geometry("500x250")
root.grid_columnconfigure(1, weight=1)

file_or_directory = tk.StringVar(value="directory")

# File or Directory selection
tk.Label(root, text="Process:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
directory_radio = tk.Radiobutton(root, text="Directory", variable=file_or_directory, value="directory")
directory_radio.grid(row=0, column=1, sticky="w")
file_radio = tk.Radiobutton(root, text="Single File", variable=file_or_directory, value="file")
file_radio.grid(row=0, column=2, sticky="w")

# Path selection
tk.Label(root, text="Path:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
path_entry = tk.Entry(root, width=40)
path_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
browse_button = tk.Button(root, text="Browse", command=browse_path)
browse_button.grid(row=1, column=2, padx=10, pady=10)

# Replacement for single quotes
tk.Label(root, text="Replace in single quotes with:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
single_quote_entry = tk.Entry(root, width=20)
single_quote_entry.insert(0, "''")  # Default replacement
single_quote_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

# Replacement for double quotes
tk.Label(root, text="Replace in double quotes with:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
double_quote_entry = tk.Entry(root, width=20)
double_quote_entry.insert(0, '""')  # Default replacement
double_quote_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

# Apply button
apply_button = tk.Button(root, text="Apply Changes", command=apply_changes)
apply_button.grid(row=4, column=1, padx=10, pady=20)

root.mainloop()
