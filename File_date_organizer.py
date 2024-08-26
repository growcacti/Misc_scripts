import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk
from datetime import datetime

# Function to organize files
def organize_files(source_dir, dest_dir, prefix, extension, recursive):
    files = []
    if recursive:
        # Recursively search for files with the specified extension
        for root, _, filenames in os.walk(source_dir):
            files.extend([os.path.join(root, f) for f in filenames if f.endswith(extension)])
    else:
        # Non-recursively search for files with the specified extension
        files = [os.path.join(source_dir, f) for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f)) and f.endswith(extension)]
    
    date_folders = {}
    
    for file_path in files:
        # Get the file's modified date
        modified_time = os.path.getmtime(file_path)
        date_str = datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d')
        
        # Create the folder name with the prefix and date
        if date_str not in date_folders:
            date_folders[date_str] = 0
        date_folders[date_str] += 1
        folder_name = f"{prefix}_{date_str}_{date_folders[date_str]}"
        
        # Create the directory if it doesn't exist
        date_folder_path = os.path.join(dest_dir, folder_name)
        os.makedirs(date_folder_path, exist_ok=True)
        
        # Copy the file to the new directory
        shutil.copy(file_path, os.path.join(date_folder_path, os.path.basename(file_path)))
    
    return date_folders

# Function to update the Treeview with the folder hierarchy
def update_treeview(tree, dest_dir):
    for item in tree.get_children():
        tree.delete(item)
    
    for root, dirs, files in os.walk(dest_dir):
        parent = ''
        for dir_name in dirs:
            tree.insert(parent, 'end', text=dir_name, values=[os.path.join(root, dir_name)])

# Main GUI setup
def main():
    root = tk.Tk()
    root.title("File Organizer by Date")
    
    # Frame for source directory selection
    frame_source = tk.Frame(root)
    frame_source.pack(fill='x')
    
    tk.Label(frame_source, text="Source Directory:").pack(side='left')
    source_dir_entry = tk.Entry(frame_source)
    source_dir_entry.pack(side='left', fill='x', expand=True)
    tk.Button(frame_source, text="Browse", command=lambda: source_dir_entry.insert(0, filedialog.askdirectory())).pack(side='left')
    
    # Frame for destination directory selection
    frame_dest = tk.Frame(root)
    frame_dest.pack(fill='x')
    
    tk.Label(frame_dest, text="Destination Directory:").pack(side='left')
    dest_dir_entry = tk.Entry(frame_dest)
    dest_dir_entry.pack(side='left', fill='x', expand=True)
    tk.Button(frame_dest, text="Browse", command=lambda: dest_dir_entry.insert(0, filedialog.askdirectory())).pack(side='left')
    
    # Frame for prefix
    frame_prefix = tk.Frame(root)
    frame_prefix.pack(fill='x')
    
    tk.Label(frame_prefix, text="Folder Prefix:").pack(side='left')
    prefix_entry = tk.Entry(frame_prefix)
    prefix_entry.pack(side='left', fill='x', expand=True)
    
    # Frame for file extension
    frame_extension = tk.Frame(root)
    frame_extension.pack(fill='x')
    
    tk.Label(frame_extension, text="File Extension:").pack(side='left')
    extension_entry = tk.Entry(frame_extension)
    extension_entry.insert(0, ".txt")  # Default to .txt files
    extension_entry.pack(side='left', fill='x', expand=True)
    
    # Checkbox for recursive option
    recursive_var = tk.BooleanVar()
    recursive_checkbox = tk.Checkbutton(root, text="Recursive Search", variable=recursive_var)
    recursive_checkbox.pack()
    
    # Treeview for folder hierarchy
    tree = ttk.Treeview(root)
    tree.pack(fill='both', expand=True)
    
    # Button to organize files
    tk.Button(root, text="Organize Files", command=lambda: organize_and_update(tree, source_dir_entry.get(), dest_dir_entry.get(), prefix_entry.get(), extension_entry.get(), recursive_var.get())).pack()
    
    root.mainloop()

def organize_and_update(tree, source_dir, dest_dir, prefix, extension, recursive):
    if not source_dir or not dest_dir:
        return
    organize_files(source_dir, dest_dir, prefix, extension, recursive)
    update_treeview(tree, dest_dir)

if __name__ == "__main__":
    main()
