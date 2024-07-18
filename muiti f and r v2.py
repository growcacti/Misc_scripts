import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import shutil
import re
import time

def select_files():
    file_paths = filedialog.askopenfilenames()
    listbox_files.delete(0, tk.END)  # Clear the listbox before adding new items
    for file_path in file_paths:
        listbox_files.insert(tk.END, file_path)

def perform_operations():
    search_pattern = entry_pattern.get()
    replace_pattern = entry_replace.get()
    file_paths = [listbox_files.get(idx) for idx in range(listbox_files.size())]

    output_dir = create_unique_directory("modified_files")
    if not output_dir:
        messagebox.showerror("Error", "Failed to create output directory.")
        return

    modified_files = []

    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            if re.search(search_pattern, content):
                new_file_path = os.path.join(output_dir, os.path.basename(file_path))
                modified_content = re.sub(search_pattern, replace_pattern, content)
                
                with open(new_file_path, 'w', encoding='utf-8') as new_file:
                    new_file.write(modified_content)
                
                modified_files.append(new_file_path)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            continue

    if modified_files:
        messagebox.showinfo("Success", f"Files processed successfully. Modified files at: {output_dir}")
    else:
        messagebox.showinfo("Info", "No files matched the search pattern.")

def create_unique_directory(prefix):
    base_path = os.getcwd()
    epoch_time = int(time.time())
    directory_name = f"{prefix}_{epoch_time}"
    full_path = os.path.join(base_path, directory_name)
    try:
        os.makedirs(full_path, exist_ok=True)
        return full_path
    except OSError as e:
        return None

root = tk.Tk()
root.title("Multi-File Search and Replace")

frame_top = tk.Frame(root)
frame_top.pack(fill=tk.X)

tk.Label(frame_top, text="Files:").pack(side=tk.LEFT)
btn_select_files = tk.Button(frame_top, text="Select Files", command=select_files)
btn_select_files.pack(side=tk.RIGHT)

listbox_files = tk.Listbox(root, height=6)
listbox_files.pack(fill=tk.BOTH, expand=True)

frame_middle = tk.Frame(root)
frame_middle.pack(fill=tk.X)

tk.Label(frame_middle, text="Search Pattern:").pack(side=tk.LEFT)
entry_pattern = tk.Entry(frame_middle)
entry_pattern.pack(fill=tk.X, expand=True, side=tk.LEFT)

tk.Label(frame_middle, text="Replace with:").pack(side=tk.LEFT)
entry_replace = tk.Entry(frame_middle)
entry_replace.pack(fill=tk.X, expand=True, side=tk.RIGHT)

btn_execute = tk.Button(root, text="Execute", command=perform_operations)
btn_execute.pack(fill=tk.X)

root.mainloop()
