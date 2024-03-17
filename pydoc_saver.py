import os
import tkinter as tk
from tkinter import filedialog
import importlib.util
import contextlib
import io

def save_module_docs(directory="module_docs"):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    for item in os.listdir(directory):
        module_name, ext = os.path.splitext(item)
        if ext != '.py':  # Skip non-Python files
            continue

        # Construct module path
        module_path = os.path.join(directory, item)
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)

        try:
            spec.loader.exec_module(module)
        except ImportError as e:
            print(f"Could not import {module_name} due to {e}, skipping.")
            continue

        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            try:
                help(module)
                doc = buf.getvalue()
            except Exception as e:
                print(f"Could not get help for {module_name} due to {e}, skipping.")
                continue

            # Save the documentation to a file
            pathway ="/home/jh/Desktop/module_docs"
            filepath = os.path.join(pathway, f"{module_name}_doc.txt")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(doc)
            print(f"Saved documentation for {module_name}")

def gui():
    root = tk.Tk()
    root.title("Module Documentation Saver")

    def browse_directory():
        directory = filedialog.askdirectory()
        if directory:  # Directory selected
            directory_label.config(text=directory)
            save_module_docs(directory)

    directory_label = tk.Label(root, text="No directory selected")
    directory_label.pack()

    browse_button = tk.Button(root, text="Browse Directory", command=browse_directory)
    browse_button.pack()

    root.mainloop()

if __name__ == "__main__":
    gui()
