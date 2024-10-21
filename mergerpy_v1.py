import os
import time
from tkinter import Tk, filedialog, Label, Button, Entry, Checkbutton, IntVar, messagebox

class FileMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Merger")
        
        self.extension = ''
        self.recursive = IntVar()
        
        # GUI Layout
        Label(root, text="Enter File Extension (e.g., 'py')").grid(row=0, column=0, padx=5, pady=5)
        self.extension_entry = Entry(root, width=10)
        self.extension_entry.grid(row=0, column=1, padx=5, pady=5)
        
        Checkbutton(root, text="Recursive Search", variable=self.recursive).grid(row=1, column=0, columnspan=2, pady=5)

        Button(root, text="Select Directory", command=self.select_directory).grid(row=2, column=0, columnspan=2, pady=5)
        Button(root, text="Save As", command=self.save_as).grid(row=3, column=0, columnspan=2, pady=5)
    
    def select_directory(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.merge_files(dir_path)
    
    def merge_files(self, dir_path):
        ext = self.extension_entry.get().strip()
        if not ext:
            messagebox.showerror("Error", "Please enter a file extension.")
            return
        
        ext = f".{ext.lstrip('.')}"  # Ensure the extension starts with a dot
        files_to_merge = []
        
        # Walk through the directory
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith(ext):
                    files_to_merge.append(os.path.join(root, file))
            if not self.recursive.get():
                break
        
        if not files_to_merge:
            messagebox.showinfo("Info", f"No files with extension '{ext}' found.")
            return
        
        self.files_to_merge = files_to_merge
        messagebox.showinfo("Files Found", f"Found {len(files_to_merge)} file(s) to merge.")
    
    def save_as(self):
        if not hasattr(self, 'files_to_merge') or not self.files_to_merge:
            messagebox.showerror("Error", "No files selected for merging.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if save_path:
            self.create_merged_file(save_path)
    
    def create_merged_file(self, save_path):
        try:
            with open(save_path, 'w') as outfile:
                for file_path in self.files_to_merge:
                    with open(file_path, 'r') as infile:
                        outfile.write(infile.read())
                        outfile.write("\n")
            
            messagebox.showinfo("Success", f"Files merged and saved as: {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge files: {e}")

def main():
    root = Tk()
    app = FileMergerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
