import tkinter as tk
from tkinter import filedialog, messagebox
import re
import os


class UnifiedListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unified List Application")
        self.setup_ui()
        self.regexpress = r"==\s*\d+(\.\d+)?"  # Example regex pattern
        self.last_directory = os.path.expanduser(
            "~")  # Default to user's home directory

    def setup_ui(self):
        # UI setup code here, ensuring all required widgets are initialized.
        pass

    def load_regex(self):
        """Loads regex patterns from a file into a listbox, with error handling."""
        file_path = filedialog.askopenfilename(
            initialdir=self.last_directory, title="Select file", filetypes=(
                ("Text files", "*.txt"), ("All files", "*.*")))
        if file_path:
            try:
                with open(file_path, "r") as file:
                    self.listbox2.delete(0, tk.END)
                    for line in file:
                        self.listbox2.insert(tk.END, line.strip())
                self.last_directory = os.path.dirname(
                    file_path)  # Update last directory
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def save_list(self):
        """Saves items from the listbox to a file, with improved user experience."""
        items = [self.listbox.get(idx) for idx in range(self.listbox.size())]
        filepath = filedialog.asksaveasfilename(
            initialdir=self.last_directory, defaultextension="txt", filetypes=(
                ("Text files", "*.txt"), ("All files", "*.*")))
        if filepath:
            try:
                with open(filepath, 'w') as file:
                    for item in items:
                        file.write(item + '\n')
                self.last_directory = os.path.dirname(
                    filepath)  # Update last directory
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
