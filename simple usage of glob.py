import glob
import fnmatch
import os
import tkinter as tk
from tkinter import ttk, filedialog

def search_and_rename_files(search_dir, search_pattern, rename=False, new_name_pattern=None):
    """
    Search for files matching a given pattern and optionally rename them.
    
    :param search_dir: Directory to search in.
    :param search_pattern: Pattern to match filenames against (glob-style).
    :param rename: Whether to rename the matching files.
    :param new_name_pattern: New name pattern for renaming files. Must include `{}` for numbering.
    """
    # Search files using glob
    files = glob.glob(f"{search_dir}/{search_pattern}")
    
    for i, file_path in enumerate(files):
        # Optionally, check again with fnmatch for more complex matching
        if fnmatch.fnmatch(os.path.basename(file_path), search_pattern):
            print(f"Found: {file_path}")
            if rename and new_name_pattern is not None:
                # Construct new filename
                new_name = new_name_pattern.format(i) + os.path.splitext(file_path)[1]
                new_path = os.path.join(search_dir, new_name)
                # Rename file
                os.rename(file_path, new_path)
                print(f"Renamed: {file_path} -> {new_path}")



def set_dir():
    source_dir = filedialog.askdirecory()
    search_pattern = "*.txt"
    rename = True
    new_name_pattern = "document_{}"  # Example: document_0.txt, document_1.txt, etc.

    search_and_rename_files(source_dir, search_pattern, rename, new_name_pattern)


root = tk.Tk()
set_dir()

root.mainloop-()
