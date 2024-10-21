import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os


class Two_Three_App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Python 2 to 3 Converter")
        self.geometry("400x200")

        # Configure the grid
        self.columnconfigure(0, weight=1)

        # Label
        self.label = tk.Label(self, text="Select Python 2 files or directory to convert")
        self.label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        # Select Files button
        self.select_files_button = tk.Button(self, text="Select Files", command=self.select_files)
        self.select_files_button.grid(row=1, column=0, pady=5, padx=10, sticky="ew")

        # Select Directory button
        self.select_dir_button = tk.Button(self, text="Select Directory", command=self.select_directory)
        self.select_dir_button.grid(row=2, column=0, pady=5, padx=10, sticky="ew")

        # Convert button
        self.convert_button = tk.Button(self, text="Convert", command=self.convert, state=tk.DISABLED)
        self.convert_button.grid(row=3, column=0, pady=20, padx=10, sticky="ew")

        # Initialize filepaths
        self.filepaths = []

    def select_files(self):
        self.filepaths = filedialog.askopenfilenames(filetypes=[("Python Files", "*.py")])
        if self.filepaths:
            self.convert_button.config(state=tk.NORMAL)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.filepaths = self.find_python_files(directory)
            if self.filepaths:
                self.convert_button.config(state=tk.NORMAL)
            else:
                messagebox.showwarning("No Python Files Found", "No Python files found in the selected directory.")

    def find_python_files(self, directory):
        python_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))
        return python_files

    def convert(self):
        if self.filepaths:
            for filepath in self.filepaths:
                try:
                    subprocess.run(["2to3", "--write", "--nobackups", filepath])
                except Exception as e:
                    messagebox.showerror("Error", f"Error while converting {filepath}: {e}")
                    return
            messagebox.showinfo("Success", "All selected files converted successfully!")
        else:
            messagebox.showwarning("No file selected", "Please select Python 2 files first.")


if __name__ == "__main__":
    app = Two_Three_App()
    app.mainloop()
