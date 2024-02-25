import os
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog

def select_directory(title):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    directory = filedialog.askdirectory(title=title)
    root.destroy()
    return directory

def ask_for_extension(title):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    extension = simpledialog.askstring("Input", title, parent=root)
    root.destroy()
    return extension

def gather_files_with_extension(src_dir, extension):
    matched_files = []
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(extension):
                full_path = os.path.join(root, file)
                matched_files.append(full_path)
    return matched_files

def copy_files(matched_files, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for file in matched_files:
        shutil.copy(file, dest_dir)

if __name__ == "__main__":
    src_dir = select_directory("Select Source Directory for Searching Files")
    if src_dir:
        extension = ask_for_extension("Enter the file extension (e.g., .mp3)")
        if extension:
            matched_files = gather_files_with_extension(src_dir, extension)
            if matched_files:
                dest_dir = select_directory("Select Destination Directory for Files")
                if dest_dir:
                    copy_files(matched_files, dest_dir)
                    print(f"Files with extension '{extension}' have been copied successfully to {dest_dir}")
                else:
                    print("No destination directory selected.")
            else:
                print(f"No files with extension '{extension}' found in the selected source directory.")
        else:
            print("No file extension entered.")
    else:
        print("No source directory selected.")
