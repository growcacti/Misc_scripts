import tkinter as tk
from tkinter import filedialog, ttk
import json
import os

class PathSelector:
    def __init__(self, root):
        self.root = root
        root.title("Path Selector")
        self.paths_file = "paths.json"
        self.path_list = self.load_paths()

        # Entry widget for output
        self.output_entry = tk.Entry(root, width=50)
        self.output_entry.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # Listbox to display paths
        self.path_listbox = tk.Listbox(root)
        self.path_listbox.grid(row=1, column=6, padx=5, pady=5, sticky=tk.NSEW)
        self.path_listbox.bind("<Double-1>", self.select_path)

        # Populate the listbox
        self.update_listbox()

        # Browse button to add new paths
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_path)
        self.browse_button.grid(row=1, column=1, padx=5, pady=5)
        self.open_button = tk.Button(root, text="Open File", command=self.load_paths)
        self.open_button.grid(row=12, column=0, padx=5, pady=5)
        self.save_button = tk.Button(root, text="Save File", command=self.save_paths)
        self.save_button.grid(row=12, column=1, padx=5, pady=5)
    def browse_path(self):
        directory = filedialog.askdirectory()
        if directory and directory not in self.path_list:
            self.path_list.append(directory)
            self.update_listbox()
            self.save_paths()

    def select_path(self, event):
        selection = self.path_listbox.curselection()
        if selection:
            selected_path = self.path_listbox.get(selection[0])
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, selected_path)

    def update_listbox(self):
        self.path_listbox.delete(0, tk.END)
        for path in self.path_list:
            self.path_listbox.insert(tk.END, path)

    def save_paths(self):
         file_path = filedialog.asksaveasfilename(defaultextension=".txt")
         if not file_path:
             print(f"Saved file: {file_path}")  # Example action
         if os.path.exists(self.paths_file):    
             with open(self.paths_file, 'w') as file:
                 json.dump(self.path_list, file)

    def load_paths(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            # Here you can add code to handle the opened file
            print(f"Opened file: {file_path}")  # Example action

        if os.path.exists(self.paths_file):
            with open(self.paths_file, 'r') as file:
                return json.load(file)
        return []

root = tk.Tk()
app = PathSelector(root)
root.mainloop()
