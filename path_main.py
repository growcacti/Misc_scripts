import tkinter as tk
from tkinter import filedialog, messagebox
import path_manager  # Import the module

def main_app():
    root = tk.Tk()
    root.title("Main App with Path Manager")

    # Use the path manager to open a file dialog
    open_file_button = tk.Button(
        root, text="Open File with Saved Path", command=path_manager.open_file_with_saved_path
    )
    open_file_button.pack(pady=10)

    add_path_button = tk.Button(
        root, text="Add New Path", command=path_manager.add_new_path
    )
    add_path_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main_app()
