import glob
import fnmatch
import os

def search_files(directory, pattern):
    """Search for files matching the pattern in the specified directory."""
    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
        from tkinter import ttk, filedialog    matches.append(os.path.join(root, filename))
    return matches

def rename_files(files, new_name_pattern):
    """Rename files based on a new name pattern."""
    for i, file in enumerate(files):
        directory, filename = os.path.split(file)
        # Example pattern: "document_{}.txt".format(i)
        new_filename = new_name_pattern.format(i)
        new_file_path = os.path.join(directory, new_filename)
        os.rename(file, new_file_path)
        print(f"Renamed {file} to {new_file_path}")

# Usage
directory = '/path/to/search'
pattern = '*.txt'
new_name_pattern = 'document_{}.txt'

files = search_files(directory, pattern)
rename_files(files, new_name_pattern)
def find_and_replace(directory, search_text, replace_text=None):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # Filter for text files or any specific file type
            if filename.endswith('.txt'):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r+', encoding='utf-8') as file:
                    content = file.read()
                    if search_text in content:
                        print(f"Found '{search_text}' in {file_path}")
                        if replace_text is not None:
                            content = content.replace(search_text, replace_text)
                            # Move the pointer at the beginning of the file to overwrite
                            file.seek(0)
                            file.write(content)
                            file.truncate()  # Truncate file to the new content length
                            print(f"Replaced with '{replace_text}' in {file_path}")
