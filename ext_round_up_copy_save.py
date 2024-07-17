import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

class FileSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drive File Search and Copy")

        self.recursive = tk.BooleanVar()
        self.create_widgets()

    def create_widgets(self):
        self.usb_label = tk.Label(self.root, text="Drive Path:")
        self.usb_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.usb_entry = tk.Entry(self.root, width=50)
        self.usb_entry.grid(row=0, column=1, padx=10, pady=10)
        
        self.usb_browse_button = tk.Button(self.root, text="Browse", command=self.browse_usb)
        self.usb_browse_button.grid(row=0, column=2, padx=10, pady=10)
        
        self.ext_label = tk.Label(self.root, text="File Extension:")
        self.ext_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.ext_entry = tk.Entry(self.root, width=50)
        self.ext_entry.grid(row=1, column=1, padx=10, pady=10)
        
        self.dest_label = tk.Label(self.root, text="Destination Path:")
        self.dest_label.grid(row=2, column=0, padx=10, pady=10)
        
        self.dest_entry = tk.Entry(self.root, width=50)
        self.dest_entry.grid(row=2, column=1, padx=10, pady=10)
        
        self.dest_browse_button = tk.Button(self.root, text="Browse", command=self.browse_dest)
        self.dest_browse_button.grid(row=2, column=2, padx=10, pady=10)
        
        self.recursive_checkbutton = tk.Checkbutton(self.root, text="Recursive Search", variable=self.recursive)
        self.recursive_checkbutton.grid(row=3, column=1, padx=10, pady=10)

        self.search_button = tk.Button(self.root, text="Search and Copy", command=self.search_and_copy)
        self.search_button.grid(row=4, column=1, padx=10, pady=10)

    def browse_usb(self):
        usb_path = filedialog.askdirectory()
        self.usb_entry.insert(0, usb_path)

    def browse_dest(self):
        dest_path = filedialog.askdirectory()
        self.dest_entry.insert(0, dest_path)

    def search_and_copy(self):
        usb_path = self.usb_entry.get()
        file_ext = self.ext_entry.get()
        dest_path = self.dest_entry.get()
        is_recursive = self.recursive.get()
        
        if not usb_path or not file_ext or not dest_path:
            messagebox.showerror("Error", "All fields are required")
            return
        
        if not os.path.exists(usb_path):
            messagebox.showerror("Error", "USB Path does not exist")
            return
        
        if not os.path.exists(dest_path):
            messagebox.showerror("Error", "Destination Path does not exist")
            return

        if is_recursive:
            files_copied = self.recursive_search_and_copy(usb_path, file_ext, dest_path)
        else:
            files_copied = self.non_recursive_search_and_copy(usb_path, file_ext, dest_path)

        messagebox.showinfo("Success", f"Copied {files_copied} files to {dest_path}")

    def recursive_search_and_copy(self, search_path, file_ext, dest_path):
        files_copied = 0
        for root, _, files in os.walk(search_path):
            for file in files:
                if file.endswith(file_ext):
                    full_file_path = os.path.join(root, file)
                    shutil.copy(full_file_path, dest_path)
                    files_copied += 1
        return files_copied

    def non_recursive_search_and_copy(self, search_path, file_ext, dest_path):
        files_copied = 0
        for file in os.listdir(search_path):
            full_file_path = os.path.join(search_path, file)
            if os.path.isfile(full_file_path) and file.endswith(file_ext):
                shutil.copy(full_file_path, dest_path)
                files_copied += 1
        return files_copied

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSearchApp(root)
    root.mainloop()
