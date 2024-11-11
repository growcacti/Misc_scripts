import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

class DirectoryNotebookConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Window settings
        self.title("Batch Jupyter Notebook Converter")
        self.geometry("800x500")
        
        # Directory selection label and entry
        tk.Label(self, text="Notebook Directory:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.dir_path_var = tk.StringVar()
        self.dir_entry = tk.Entry(self, textvariable=self.dir_path_var, width=40)
        self.dir_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Browse button for directory selection
        tk.Button(self, text="Browse", command=self.browse_directory).grid(row=0, column=2, padx=10, pady=10)
        
        # Recursive option
        self.recursive_var = tk.BooleanVar(value=True)
        self.recursive_check = tk.Checkbutton(self, text="Include Subdirectories", variable=self.recursive_var)
        self.recursive_check.grid(row=1, column=1, sticky="w", padx=10)
        
        # Output format options
        tk.Label(self, text="Convert to:").grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.format_var = tk.StringVar(value="Python Script (.py)")
        formats = ["Python Script (.py)", "HTML (.html)", "PDF (.pdf)"]
        self.format_menu = tk.OptionMenu(self, self.format_var, *formats)
        self.format_menu.grid(row=2, column=1, sticky="w", padx=10, pady=10)
        
        # Convert button
        tk.Button(self, text="Convert All", command=self.convert_all_notebooks).grid(row=3, column=1, pady=20)
    
    def browse_directory(self):
        """Opens a dialog to select a directory."""
        directory = filedialog.askdirectory()
        self.dir_path_var.set(directory)
    
    def convert_all_notebooks(self):
        """Converts all notebooks in the selected directory (and subdirectories if recursive)."""
        directory = self.dir_path_var.get()
        if not directory or not os.path.isdir(directory):
            messagebox.showerror("Error", "Please select a valid directory.")
            return
        
        output_format = self.format_var.get()
        format_option = ""
        extension = ""
        
        if output_format == "Python Script (.py)":
            format_option = "--to script"
            extension = ".py"
        elif output_format == "HTML (.html)":
            format_option = "--to html"
            extension = ".html"
        elif output_format == "PDF (.pdf)":
            format_option = "--to pdf"
            extension = ".pdf"
        
        # List all .ipynb files in the directory (recursively if needed)
        notebook_files = []
        if self.recursive_var.get():
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith(".ipynb"):
                        notebook_files.append(os.path.join(root, file))
        else:
            notebook_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".ipynb")]
        
        if not notebook_files:
            messagebox.showinfo("No Notebooks Found", "No Jupyter notebooks found in the selected directory.")
            return
        
        converted_files = []
        failed_files = []
        
        # Convert each notebook
        for notebook in notebook_files:
            input_path = notebook
            output_file = os.path.splitext(input_path)[0] + extension
            
            try:
                # Run nbconvert command
                subprocess.run(f"jupyter nbconvert {format_option} \"{input_path}\"", check=True, shell=True)
                converted_files.append(output_file)
            except subprocess.CalledProcessError:
                failed_files.append(input_path)
        
        # Display conversion result
        if converted_files:
            messagebox.showinfo("Conversion Complete", f"Converted {len(converted_files)} notebooks successfully.")
        if failed_files:
            messagebox.showerror("Conversion Failed", f"Failed to convert {len(failed_files)} notebooks.")
        
if __name__ == "__main__":
    app = DirectoryNotebookConverterApp()
    app.mainloop()
