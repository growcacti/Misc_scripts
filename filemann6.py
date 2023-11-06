import os
import tkinter as tk
from tkinter import messagebox

class FileManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Listbox File Manager')
        self.geometry('600x400')

        self.current_path = os.path.expanduser('~')  # Start at user's home directory
        self.listbox = tk.Listbox(self)
        self.listbox.pack(side='left', fill='both', expand=True)

        self.populate_listbox(self.current_path)

        self.listbox.bind('<Double-1>', self.on_double_click)  # Bind double click event

    def populate_listbox(self, path):
        self.listbox.delete(0, tk.END)  # Clear the current listbox contents
        self.listbox.insert(tk.END, '..')  # Add a 'Go Up' option to the listbox

        # Prepare lists for directories and files
        dirs = []
        files = []

        # List the contents of the directory and sort them
        try:
            for entry in os.listdir(path):
                full_path = os.path.join(path, entry)
                if os.path.isdir(full_path):
                    dirs.append(entry)
                else:
                    files.append(entry)

            # Sort directories and files
            dirs.sort(key=lambda s: s.lower())
            files.sort(key=lambda s: s.lower())

            # Insert the sorted directories and files into the listbox
            for entry in dirs:
                self.listbox.insert(tk.END, entry)
            for entry in files:
                self.listbox.insert(tk.END, entry)

        except PermissionError:
            messagebox.showerror('Permission Denied', f'Cannot open directory: {path}')
            return

    def on_double_click(self, event):
        # Get the listbox selection
        selection = self.listbox.curselection()
        if not selection:
            return

        entry = self.listbox.get(selection[0])
        path = os.path.join(self.current_path, entry)

        if os.path.isdir(path):
            if entry == '..':
                # Go up to the parent directory
                self.current_path = os.path.dirname(self.current_path)
            else:
                # Navigate into the selected directory
                self.current_path = path
            self.populate_listbox(self.current_path)
        else:
            # You can put file-opening logic here
            messagebox.showinfo('Selected File', f'You selected the file: {entry}')

if __name__ == '__main__':
    app = FileManager()
    app.mainloop()
