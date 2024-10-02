import re
import os
import shutil
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Define the SearchReplaceApp class
class SearchReplaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Search and Replace Text in Directory - Tkinter Version")

        # Initialize the GUI
        self.create_widgets()

    # Method to create the widgets
    def create_widgets(self):
        # Dropdown for method selection
        method_label = tk.Label(self.root, text="Select Replacement Method:")
        method_label.grid(row=0, column=0, padx=10, pady=5)

        self.method_combo = ttk.Combobox(self.root, values=[
            "Method 1: replace() String Method",
            "Method 2: re.sub() with Regular Expressions",
            "Method 3: str.translate() and str.maketrans()",
            "Method 4: F-strings and replace()",
            "Method 5: Lambda with re.sub()"
        ])
        self.method_combo.grid(row=0, column=1, padx=10, pady=5)
        self.method_combo.current(0)  # Set default selection

        # Text input area
        text_label = tk.Label(self.root, text="Enter Text:")
        text_label.grid(row=1, column=0, padx=10, pady=5)

        self.text_input = tk.Text(self.root, height=5, width=50)
        self.text_input.grid(row=1, column=1, padx=10, pady=5)

        # Search and Replace inputs
        search_label = tk.Label(self.root, text="Search For:")
        search_label.grid(row=2, column=0, padx=10, pady=5)

        self.search_input = tk.Entry(self.root, width=30)
        self.search_input.grid(row=2, column=1, padx=10, pady=5)

        replace_label = tk.Label(self.root, text="Replace With:")
        replace_label.grid(row=3, column=0, padx=10, pady=5)

        self.replace_input = tk.Entry(self.root, width=30)
        self.replace_input.grid(row=3, column=1, padx=10, pady=5)

        # Directory selection
        dir_label = tk.Label(self.root, text="Select Directory:")
        dir_label.grid(row=4, column=0, padx=10, pady=5)

        self.dir_path = tk.Entry(self.root, width=30)
        self.dir_path.grid(row=4, column=1, padx=10, pady=5)

        dir_button = tk.Button(self.root, text="Browse", command=self.browse_directory)
        dir_button.grid(row=4, column=2, padx=5, pady=5)

        # Recursive checkbox
        self.recursive_var = tk.IntVar()
        recursive_check = tk.Checkbutton(self.root, text="Recursive Search", variable=self.recursive_var)
        recursive_check.grid(row=5, column=1, sticky='w', padx=10, pady=5)

        # Output area for the result
        result_label = tk.Label(self.root, text="Result:")
        result_label.grid(row=6, column=0, padx=10, pady=5)

        self.result_output = tk.Text(self.root, height=10, width=50)
        self.result_output.grid(row=6, column=1, padx=10, pady=5)

        # Replace button
        replace_button = tk.Button(self.root, text="Replace in Directory", command=self.perform_replacement)
        replace_button.grid(row=7, column=1, pady=10)

    # Methods for each search and replace option
    def replace_method_1(self, text, search, replace):
        return text.replace(search, replace)

    def replace_method_2(self, text, search, replace):
        return re.sub(search, replace, text)

    def replace_method_3(self, text, search, replace):
        if len(search) != len(replace):
            return "Error: For str.translate, search and replace must have the same length."
        trans = str.maketrans(search, replace)
        return text.translate(trans)

    def replace_method_4(self, text, search, replace):
        return text.replace(search, replace)  # Using F-strings combined with replace.

    def replace_method_5(self, text, search, replace):
        return re.sub(search, lambda match: replace, text)

    # Method to perform the replacement based on user input
    def perform_replacement(self):
        search = self.search_input.get()
        replace = self.replace_input.get()
        method_choice = self.method_combo.get()
        directory = self.dir_path.get()
        recursive = self.recursive_var.get()

        if not directory or not search or not replace:
            messagebox.showwarning("Input Error", "Please provide a directory, search term, and replacement.")
            return

        # Create a new folder with the current epoch time as its name
        new_folder_name = f"modified_files_{int(time.time())}"
        new_folder_path = os.path.join(os.path.dirname(directory), new_folder_name)
        os.makedirs(new_folder_path, exist_ok=True)

        self.result_output.insert(tk.END, f"New folder created: {new_folder_path}\n")

        # Perform search and replace in files
        for root_dir, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root_dir, file)
                # Create a copy of the file in the new folder
                new_file_path = self.copy_to_new_folder(file_path, new_folder_path, root_dir, directory)
                # Process the new file
                self.process_file(new_file_path, search, replace, method_choice)

            if not recursive:
                break  # Stop walking if non-recursive

    # Method to process each file
    def process_file(self, file_path, search, replace, method_choice):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Apply the selected replacement method
            if method_choice == "Method 1: replace() String Method":
                new_content = self.replace_method_1(content, search, replace)
            elif method_choice == "Method 2: re.sub() with Regular Expressions":
                new_content = self.replace_method_2(content, search, replace)
            elif method_choice == "Method 3: str.translate() and str.maketrans()":
                new_content = self.replace_method_3(content, search, replace)
            elif method_choice == "Method 4: F-strings and replace()":
                new_content = self.replace_method_4(content, search, replace)
            elif method_choice == "Method 5: Lambda with re.sub()":
                new_content = self.replace_method_5(content, search, replace)
            else:
                return

            # Save the modified content to the new file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)

            self.result_output.insert(tk.END, f"Processed: {file_path}\n")

        except Exception as e:
            self.result_output.insert(tk.END, f"Error processing {file_path}: {str(e)}\n")

    # Method to copy a file to the new folder
    def copy_to_new_folder(self, file_path, new_folder_path, root_dir, original_directory):
        # Preserve directory structure in the new folder
        relative_path = os.path.relpath(root_dir, original_directory)
        new_dir_path = os.path.join(new_folder_path, relative_path)
        os.makedirs(new_dir_path, exist_ok=True)

        new_file_path = os.path.join(new_dir_path, os.path.basename(file_path))
        shutil.copy2(file_path, new_file_path)
        return new_file_path

    # Method to browse and select a directory
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_path.delete(0, tk.END)
            self.dir_path.insert(0, directory)


# Main program to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SearchReplaceApp(root)
    root.mainloop()
