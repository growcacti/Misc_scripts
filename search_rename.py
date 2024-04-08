import glob
import fnmatch
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox

class FileSearchAndRenameApp:
    def __init__(self, root):
        self.root = root
        self.root.title('File Search and Rename Tool')
        
        # Set up the GUI layout
        self.setup_gui()

    def setup_gui(self):
        # Button for selecting search directory
        self.btn_select_dir = tk.Button(self.root, text='Select Search Directory', command=self.select_search_directory)
        self.btn_select_dir.pack(pady=10)
        
        # Button for starting the search (and rename) process
        self.btn_start_search = tk.Button(self.root, text='Start Search', state='disabled', command=self.start_search_and_rename)
        self.btn_start_search.pack(pady=5)

    def select_search_directory(self):
        self.search_dir = filedialog.askdirectory(title='Select Search Directory')
        if self.search_dir:
            self.btn_start_search['state'] = 'normal'
            messagebox.showinfo('Directory Selected', f'Search Directory: {self.search_dir}')
    
    def start_search_and_rename(self):
        search_pattern = simpledialog.askstring('Input', 'Enter search pattern (e.g., *.txt):')
        if search_pattern:
            rename = messagebox.askyesno('Rename Files', 'Do you want to rename the matching files?')
            new_name_pattern = None
            if rename:
                new_name_pattern = simpledialog.askstring('Input', 'Enter new name pattern (include {} for numbering, e.g., document_{}):')
            self.search_and_rename_files(self.search_dir, search_pattern, rename, new_name_pattern)
            messagebox.showinfo('Operation Complete', 'Search (and rename) operation completed.')
    
    def search_and_rename_files(self, search_dir, search_pattern, rename=False, new_name_pattern=None):
        files = glob.glob(f"{search_dir}/{search_pattern}")
        
        for i, file_path in enumerate(files):
            if fnmatch.fnmatch(os.path.basename(file_path), search_pattern):
                print(f"Found: {file_path}")
                if rename and new_name_pattern is not None:
                    new_name = new_name_pattern.format(i) + os.path.splitext(file_path)[1]
                    new_path = os.path.join(search_dir, new_name)
                    os.rename(file_path, new_path)
                    print(f"Renamed: {file_path} -> {new_path}")

# Create the main window
root = tk.Tk()
app = FileSearchAndRenameApp(root)

# Start the GUI event loop
root.mainloop()
