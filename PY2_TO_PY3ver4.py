import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import threading

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Python 2 to 3 Converter")
        self.geometry("400x250")
        self.progress_bar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress_bar.pack(pady=10)

        self.label = tk.Label(self, text="Select Python 2 files to convert")
        self.label.pack(pady=20)

        self.select_button = tk.Button(self, text="select files", command=self.select_files)
        self.select_button.pack()
      
        
        self.select_button1 = tk.Button(self,text="Select Directory", command=self.select_directory)
        self.select_button1.pack()
        self.filepaths = []
        self.convert_button = tk.Button(self, text="Convert", command=self.convert, state=tk.DISABLED)
        self.convert_button.pack(pady=30)

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
                messagebox.showwarning("No Python files", "No Python files found in the selected directory.")
    def find_python_files(self, directory):
        python_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        return python_files
    def convert(self):
        if self.filepaths:
            self.progress_bar['maximum'] = len(self.filepaths)
            threading.Thread(target=self.run_conversion, daemon=True).start()

    def run_conversion(self):
        errors = []
        for index, filepath in enumerate(self.filepaths):
            try:
                subprocess.run(["2to3", "--write", "--nobackups", filepath], check=True)
            except subprocess.CalledProcessError as e:
                errors.append((filepath, str(e)))
            finally:
                self.update_progress(index + 1)
        self.finish_conversion(errors)

    def update_progress(self, value):
        self.progress_bar['value'] = value
        self.update_idletasks()

    def finish_conversion(self, errors):
        if errors:
            error_message = "\n".join([f"{filepath}: {error}" for filepath, error in errors])
            messagebox.showerror("Conversion Finished with Errors", error_message)
        else:
            messagebox.showinfo("Success", "All selected files converted successfully!")
if __name__ == "__main__":
    app = App()
    app.mainloop()
