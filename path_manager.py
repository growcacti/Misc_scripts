import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

class PathManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Path Manager")
        self.saved_paths = self.load_paths()
        
        # Ensure at least one default option
        if not self.saved_paths:
            self.saved_paths = ["No paths saved"]

        # GUI Components
        self.path_var = tk.StringVar(value=self.saved_paths[0])
        self.path_dropdown = tk.OptionMenu(root, self.path_var, *self.saved_paths)
        self.path_dropdown.grid(row=0, column=0, padx=10, pady=10)

        self.add_path_button = tk.Button(root, text="Add Path", command=self.add_path)
        self.add_path_button.grid(row=0, column=1, padx=5)

        self.remove_path_button = tk.Button(root, text="Remove Path", command=self.remove_path)
        self.remove_path_button.grid(row=0, column=2, padx=5)

        self.open_file_button = tk.Button(root, text="Open File", command=self.open_file_dialog)
        self.open_file_button.grid(row=1, column=0, columnspan=3, pady=10)

    def load_paths(self):
        try:
            with open("paths.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_paths(self):
        with open("paths.json", "w") as f:
            json.dump(self.saved_paths, f)

    def add_path(self):
        new_path = filedialog.askdirectory()
        if new_path:
            if "No paths saved" in self.saved_paths:
                self.saved_paths.remove("No paths saved")
            self.saved_paths.append(new_path)
            self.save_paths()
            self.update_dropdown()
            messagebox.showinfo("Path Added", f"Path '{new_path}' has been added.")

    def remove_path(self):
        current_path = self.path_var.get()
        if current_path in self.saved_paths:
            self.saved_paths.remove(current_path)
            self.save_paths()
            self.update_dropdown()
            messagebox.showinfo("Path Removed", f"Path '{current_path}' has been removed.")
        else:
            messagebox.showwarning("No Path Selected", "Please select a path to remove.")

    def update_dropdown(self):
        menu = self.path_dropdown["menu"]
        menu.delete(0, "end")
        
        if not self.saved_paths:
            self.saved_paths = ["No paths saved"]
        
        for path in self.saved_paths:
            menu.add_command(label=path, command=lambda value=path: self.path_var.set(value))

        self.path_var.set(self.saved_paths[0])  # Set the first option as default

    def open_file_dialog(self):
        initial_dir = self.path_var.get() if self.path_var.get() != "No paths saved" else "/"
        file_path = filedialog.askopenfilename(initialdir=initial_dir)
        if file_path:
            messagebox.showinfo("File Selected", f"Selected file: {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PathManagerApp(root)
    root.mainloop()
