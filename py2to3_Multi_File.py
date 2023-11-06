import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Python 2 to 3 Converter")
        self.geometry("400x150")

        self.label = tk.Label(self, text="Select Python 2 files to convert")
        self.label.pack(pady=20)

        self.select_button = tk.Button(self, text="Select Files", command=self.select_files)
        self.select_button.pack()

        self.convert_button = tk.Button(self, text="Convert", command=self.convert, state=tk.DISABLED)
        self.convert_button.pack(pady=20)

        self.filepaths = []

    def select_files(self):
        self.filepaths = filedialog.askopenfilenames(filetypes=[("Python Files", "*.py")])
        if self.filepaths:
            self.convert_button.config(state=tk.NORMAL)

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
    app = App()
    app.mainloop()
