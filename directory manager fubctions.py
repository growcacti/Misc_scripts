import tkinter as tk
from tkinter import filedialog, messagebox

class DirectoryManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Directory Link Manager")
        
        # Frame for Listbox and Scrollbar
        frame = tk.Frame(root)
        frame.pack(padx=10, pady=10)
        
        # Listbox and Scrollbar
        self.scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(frame, width=50, height=15, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(padx=10, pady=10, fill=tk.X)
        
        self.add_button = tk.Button(btn_frame, text="Add Directory", command=self.add_directory)
        self.add_button.pack(side=tk.LEFT, expand=True)
        
        self.remove_button = tk.Button(btn_frame, text="Remove Selected", command=self.remove_directory)
        self.remove_button.pack(side=tk.LEFT, expand=True)
        
        self.save_button = tk.Button(btn_frame, text="Save Directories", command=self.save_directories)
        self.save_button.pack(side=tk.LEFT, expand=True)
        
        self.load_button = tk.Button(btn_frame, text="Load Directories", command=self.load_directories)
        self.load_button.pack(side=tk.LEFT, expand=True)
        
        self.directory_paths = set()

    def add_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            if directory not in self.directory_paths:
                self.directory_paths.add(directory)
                self.listbox.insert(tk.END, directory)
            else:
                messagebox.showinfo("Duplicate Entry", "This directory is already added.")

    def remove_directory(self):
        try:
            index = self.listbox.curselection()[0]
            path = self.listbox.get(index)
            self.directory_paths.remove(path)
            self.listbox.delete(index)
        except IndexError:
            messagebox.showinfo("Selection Error", "Please select a directory to remove.")
    
    def save_directories(self):
        with open("directories.txt", "w") as file:
            for path in self.directory_paths:
                file.write(path + "\n")
        messagebox.showinfo("Save Successful", "Directories have been saved to directories.txt.")
    
    def load_directories(self):
        try:
            with open("directories.txt", "r") as file:
                self.directory_paths = set(file.read().splitlines())
            self.listbox.delete(0, tk.END)
            for path in self.directory_paths:
                self.listbox.insert(tk.END, path)
            messagebox.showinfo("Load Successful", "Directories have been loaded from directories.txt.")
        except FileNotFoundError:
            messagebox.showinfo("File Not Found", "The directories.txt file does not exist.")

root = tk.Tk()
app = DirectoryManager(root)
root.mainloop()
