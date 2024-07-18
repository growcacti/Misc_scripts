import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import re

def select_files():
    file_paths = filedialog.askopenfilenames()
    entry_filename.delete(0, tk.END)
    entry_filename.insert(0, " ".join(file_paths))
    return file_paths

def perform_operations():
    search_pattern = entry_pattern.get()
    replace_pattern = entry_replace.get()
    file_paths = entry_filename.get().split()

    # Create unique directory for the copied and modified files
    output_dir = create_unique_directory("modified_files")
    if not output_dir:
        messagebox.showerror("Error", "Failed to create output directory.")
        return

    modified_files = []

    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Check if the search pattern exists in the file
            if re.search(search_pattern, content):
                # Define new file path
                new_file_path = os.path.join(output_dir, os.path.basename(file_path))
                
                # Replace text
                modified_content = re.sub(search_pattern, replace_pattern, content)
                
                # Write the modified content to the new file
                with open(new_file_path, 'w', encoding='utf-8') as new_file:
                    new_file.write(modified_content)
                
                modified_files.append(new_file_path)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return

    if modified_files:
        messagebox.showinfo("Success", f"Files processed successfully. Modified files at: {output_dir}")
    else:
        messagebox.showinfo("Info", "No files matched the search pattern.")

def create_unique_directory(prefix):
    base_path = os.getcwd()  # Or any other base path you prefer
    epoch_time = int(time.time())
    directory_name = f"{prefix}_{epoch_time}"
    full_path = os.path.join(base_path, directory_name)
    try:
        os.makedirs(full_path, exist_ok=True)
        return full_path
    except OSError as e:
        print(f"Error creating directory: {e}")
        return None

# Setup the GUI
root = tk.Tk()
root.title("Search, Copy, Replace")

tk.Label(root, text="Files:").pack()
entry_filename = tk.Entry(root, width=80)
entry_filename.pack()
tk.Button(root, text="Select Files", command=select_files).pack()

tk.Label(root, text="Search Pattern:").pack()
entry_pattern = tk.Entry(root)
entry_pattern.pack()

tk.Label(root, text="Replace with:").pack()
entry_replace = tk.Entry(root)
entry_replace.pack()

tk.Button(root, text="Execute", command=perform_operations).pack()

root.mainloop()
