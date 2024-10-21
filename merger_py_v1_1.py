import os
import tkinter as tk
from tkinter import filedialog, messagebox
import time

class FileMergerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Merger")
        self.geometry("400x300")

        self.directory = None
        self.extension = tk.StringVar()
        self.is_recursive = tk.BooleanVar()

        # UI Setup
        self.setup_ui()

    def setup_ui(self):
        # Directory Selection
        tk.Label(self, text="Select Directory:").grid(row=0, column=0, padx=10, pady=10)
        tk.Button(self, text="Browse", command=self.browse_directory).grid(row=0, column=1, padx=10, pady=10)

        # Recursive or Flat Search
        tk.Label(self, text="Search Type:").grid(row=1, column=0, padx=10, pady=10)
        tk.Radiobutton(self, text="Recursive", variable=self.is_recursive, value=True).grid(row=1, column=1, sticky='w')
        tk.Radiobutton(self, text="Flat", variable=self.is_recursive, value=False).grid(row=2, column=1, sticky='w')

        # File Extension
        tk.Label(self, text="File Extension (e.g., py):").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(self, textvariable=self.extension).grid(row=3, column=1, padx=10, pady=10)

        # Merge Button
        tk.Button(self, text="Merge Files", command=self.merge_files).grid(row=4, column=0, columnspan=2, pady=20)

    def browse_directory(self):
        self.directory = filedialog.askdirectory()
        if self.directory:
            messagebox.showinfo("Selected Directory", f"Directory: {self.directory}")

    def merge_files(self):
        if not self.directory or not self.extension.get():
            messagebox.showwarning("Error", "Please select a directory and enter a file extension.")
            return
        
        # Find files and merge
        file_list = self.find_files(self.directory, self.extension.get(), self.is_recursive.get())
        if not file_list:
            messagebox.showwarning("No Files Found", "No files found with the given extension.")
            return

        merged_content = self.read_and_merge_files(file_list)
        if merged_content:
            self.save_merged_file(merged_content)

    def find_files(self, directory, ext, recursive):
        file_list = []
        if recursive:
            for root, _, files in os.walk(directory):
                file_list.extend([os.path.join(root, f) for f in files if f.endswith(f".{ext}")])
        else:
            file_list = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(f".{ext}")]
        return file_list

    def read_and_merge_files(self, file_list):
        content = []
        for file in file_list:
            try:
                with open(file, 'r') as f:
                    content.append(f.read())
            except Exception as e:
                messagebox.showerror("Error", f"Could not read file {file}: {e}")
                return None
        return "\n".join(content)

    def save_merged_file(self, content):
        timestamp = int(time.time())
        default_filename = f"merged_{timestamp}.txt"
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=default_filename)

        if save_path:
            try:
                with open(save_path, 'w') as f:
                    f.write(content)
                messagebox.showinfo("Success", f"Files merged and saved as {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

if __name__ == "__main__":
    app = FileMergerApp()
    app.mainloop()
