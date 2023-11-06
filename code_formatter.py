import tkinter as tk
from tkinter import filedialog
import os
import subprocess


class CodeFormatter:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Formatter")

        # Menu bar for opening files
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.file_menu = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.load_directory)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

    def load_directory(self):
        selected_directory = filedialog.askdirectory(title="Please select a directory")
        if selected_directory:
            self.reformat_code(selected_directory)

    def reformat_code(self, directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)

                    result = subprocess.run(
                        ["python", "-m", "black", filepath],
                        capture_output=True,
                        text=True,
                    )

            if result.returncode == 0:
                print(f"Successfully formatted: {filepath}")
                print(result.stdout)
            else:
                print(f"Error formatting {filepath}")
                print(result.stderr)


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeFormatter(root)
    root.mainloop()
