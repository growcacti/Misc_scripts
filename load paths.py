import json
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to load saved paths from JSON file
def load_paths(file_name="paths.json"):
    try:
        with open(file_name, "r") as f:
            paths = json.load(f)
        if not paths:
            paths = ["No paths saved"]
    except FileNotFoundError:
        paths = ["No paths saved"]
    return paths

# Function to save paths to JSON file
def save_paths(paths, file_name="paths.json"):
    with open(file_name, "w") as f:
        json.dump(paths, f)

# Function to add a new path
def add_new_path(file_name="paths.json"):
    new_path = filedialog.askdirectory()
    if new_path:
        paths = load_paths(file_name)
        if "No paths saved" in paths:
            paths.remove("No paths saved")
        paths.append(new_path)
        save_paths(paths, file_name)
        messagebox.showinfo("Path Added", f"Path '{new_path}' has been added.")
    return new_path

# Function to use saved paths in filedialog
def open_file_with_saved_path(initial_path="paths.json"):
    paths = load_paths(initial_path)
    initial_dir = paths[0] if paths[0] != "No paths saved" else "/"
    file_path = filedialog.askopenfilename(initialdir=initial_dir)
    if file_path:
        messagebox.showinfo("File Selected", f"Selected file: {file_path}")
    return file_path

# Example Tkinter GUI for managing paths (can be standalone)
class PathManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Path Manager")
        self.paths_file = "paths.json"
        self.saved_paths = load_paths(self.paths_file)

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

        self.save_button = tk.Button(root, text="Save", command=self.save_paths)
        self.save_button.grid(row=0, column=3, padx=5)

        self.open_file_button = tk.Button(root, text="Open File", command=self.open_file_dialog)
        self.open_file_button.grid(row=1, column=0, columnspan=4, pady=10)

    def save_paths(self):
        save_paths(self.saved_paths, self.paths_file)
        messagebox.showinfo("Paths Saved", "Paths have been successfully saved.")

    def add_path(self):
        new_path = add_new_path(self.paths_file)
        if new_path:
            self.update_dropdown()

    def remove_path(self):
        current_path = self.path_var.get()
        if current_path in self.saved_paths:
            self.saved_paths.remove(current_path)
            save_paths(self.saved_paths, self.paths_file)
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
        open_file_with_saved_path(self.paths_file)

if __name__ == "__main__":
    root = tk.Tk()
    app = PathManagerApp(root)
    root.mainloop()
