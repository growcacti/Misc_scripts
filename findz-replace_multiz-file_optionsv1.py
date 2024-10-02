import re
import os
import shutil
import time
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class SearchReplaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Search and Replace Text in Directory - Enhanced Version")

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
        self.method_combo.current(0)

        # Search and Replace inputs
        search_label = tk.Label(self.root, text="Search For:")
        search_label.grid(row=1, column=0, padx=10, pady=5)
        self.search_input = tk.Entry(self.root, width=30)
        self.search_input.grid(row=1, column=1, padx=10, pady=5)

        replace_label = tk.Label(self.root, text="Replace With:")
        replace_label.grid(row=2, column=0, padx=10, pady=5)
        self.replace_input = tk.Entry(self.root, width=30)
        self.replace_input.grid(row=2, column=1, padx=10, pady=5)

        # Directory selection
        dir_label = tk.Label(self.root, text="Select Directory:")
        dir_label.grid(row=3, column=0, padx=10, pady=5)
        self.dir_path = tk.Entry(self.root, width=30)
        self.dir_path.grid(row=3, column=1, padx=10, pady=5)
        dir_button = tk.Button(self.root, text="Browse", command=self.browse_directory)
        dir_button.grid(row=3, column=2, padx=5, pady=5)

        # File type filtering
        file_type_label = tk.Label(self.root, text="File Types (e.g., *.txt, *.csv):")
        file_type_label.grid(row=4, column=0, padx=10, pady=5)
        self.file_types = tk.Entry(self.root, width=30)
        self.file_types.grid(row=4, column=1, padx=10, pady=5)

        # Backup checkbox
        self.backup_var = tk.IntVar()
        backup_check = tk.Checkbutton(self.root, text="Create Backup of Original Files", variable=self.backup_var)
        backup_check.grid(row=5, column=1, sticky='w', padx=10, pady=5)

        # Recursive checkbox
        self.recursive_var = tk.IntVar()
        recursive_check = tk.Checkbutton(self.root, text="Recursive Search", variable=self.recursive_var)
        recursive_check.grid(row=6, column=1, sticky='w', padx=10, pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=7, column=1, pady=10)

        # Output area for the result
        result_label = tk.Label(self.root, text="Result Log:")
        result_label.grid(row=8, column=0, padx=10, pady=5)
        self.log_output = tk.Text(self.root, height=10, width=50)
        self.log_output.grid(row=8, column=1, padx=10, pady=5)

        # Replace button
        replace_button = tk.Button(self.root, text="Replace in Directory", command=self.perform_replacement)
        replace_button.grid(row=9, column=1, pady=10)

        # Preview button
        preview_button = tk.Button(self.root, text="Preview Changes", command=self.preview_changes)
        preview_button.grid(row=9, column=2, pady=10)

        # Save and Load config buttons
        save_button = tk.Button(self.root, text="Save Config", command=self.save_config)
        save_button.grid(row=10, column=0, pady=10)
        load_button = tk.Button(self.root, text="Load Config", command=self.load_config)
        load_button.grid(row=10, column=1, pady=10)

        # Help button
        help_button = tk.Button(self.root, text="Help", command=self.show_help)
        help_button.grid(row=9, column=0, padx=10, pady=5)

        # Regex pattern dropdown
        regex_patterns = {
            "Email Address": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "Phone Number": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
            "URL": r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+",
            "IPv4 Address": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
            "File Path": r"[A-Za-z]:\\(?:[A-Za-z0-9]+\\)*[A-Za-z0-9]+\.[A-Za-z]{2,4}",
            "Credit Card": r"\b(?:\d{4}[ -]?){3}\d{4}\b",
        }
        regex_combo = ttk.Combobox(self.root, values=list(regex_patterns.keys()))
        regex_combo.grid(row=11, column=1, padx=10, pady=5)
        regex_button = tk.Button(self.root, text="Use Pattern", command=lambda: self.use_pattern(regex_combo, regex_patterns))
        regex_button.grid(row=11, column=2, pady=5)
        # Regex Tester Section
        tester_label = tk.Label(self.root, text="Test Your Regex:")
        tester_label.grid(row=12, column=0, padx=10, pady=5)

        # Regex Tester Inputs
        self.tester_pattern = tk.Entry(self.root, width=30)
        self.tester_pattern.grid(row=12, column=1, padx=10, pady=5)
        self.tester_text = tk.Text(self.root, height=5, width=50)
        self.tester_text.grid(row=13, column=1, padx=10, pady=5)

        # Test Button
        test_button = tk.Button(self.root, text="Test Regex", command=self.test_regex)
        test_button.grid(row=13, column=2, pady=5)

        # Test Results Output
        self.test_results = tk.Text(self.root, height=5, width=50)
        self.test_results.grid(row=14, column=1, padx=10, pady=5)


    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_path.delete(0, tk.END)
            self.dir_path.insert(0, directory)

    def perform_replacement(self):
        search = self.search_input.get()
        replace = self.replace_input.get()
        method_choice = self.method_combo.get()
        directory = self.dir_path.get()
        file_types = self.file_types.get().split(',')

        if not directory or not search or not replace:
            messagebox.showwarning("Input Error", "Please provide a directory, search term, and replacement.")
            return

        # Create a new folder with the current epoch time as its name
        new_folder_name = f"modified_files_{int(time.time())}"
        new_folder_path = os.path.join(os.path.dirname(directory), new_folder_name)
        os.makedirs(new_folder_path, exist_ok=True)
        self.log_output.insert(tk.END, f"New folder created: {new_folder_path}\n")

        total_files = sum(len(files) for _, _, files in os.walk(directory))
        self.progress["maximum"] = total_files
        processed_files = 0
        start_time = time.time()

        # Perform search and replace in files
        for root_dir, dirs, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ft.strip()) for ft in file_types):
                    file_path = os.path.join(root_dir, file)
                    if self.backup_var.get():
                        self.create_backup(file_path)

                    new_file_path = self.copy_to_new_folder(file_path, new_folder_path, root_dir, directory)
                    self.process_file(new_file_path, search, replace, method_choice)

                    # Log the file that was processed
                    self.log_output.insert(tk.END, f"Processed: {file_path}\n")
                    processed_files += 1
                    elapsed_time = time.time() - start_time
                    est_total_time = (elapsed_time / processed_files) * total_files
                    remaining_time = est_total_time - elapsed_time
                    self.log_output.insert(tk.END, f"Estimated time left: {int(remaining_time)}s\n")
                    self.progress.step(1)
                    self.root.update_idletasks()

            if not self.recursive_var.get():
                break

        self.log_output.insert(tk.END, f"Finished processing {processed_files} files.\n")

    def create_backup(self, file_path):
        backup_folder = os.path.join(os.path.dirname(file_path), "backup")
        os.makedirs(backup_folder, exist_ok=True)
        backup_file_path = os.path.join(backup_folder, os.path.basename(file_path))
        shutil.copy2(file_path, backup_file_path)

    def copy_to_new_folder(self, file_path, new_folder_path, root_dir, original_directory):
        relative_path = os.path.relpath(root_dir, original_directory)
        new_dir_path = os.path.join(new_folder_path, relative_path)
        os.makedirs(new_dir_path, exist_ok=True)
        new_file_path = os.path.join(new_dir_path, os.path.basename(file_path))
        shutil.copy2(file_path, new_file_path)
        return new_file_path

    def process_file(self, file_path, search, replace, method_choice):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            if method_choice == "Method 1: replace() String Method":
                new_content = content.replace(search, replace)
            elif method_choice == "Method 2: re.sub() with Regular Expressions":
                new_content = re.sub(search, replace, content)
            elif method_choice == "Method 3: str.translate() and str.maketrans()":
                new_content = content.translate(str.maketrans(search, replace))
            elif method_choice == "Method 4: F-strings and replace()":
                new_content = content.replace(search, replace)
            elif method_choice == "Method 5: Lambda with re.sub()":
                new_content = re.sub(search, lambda _: replace, content)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
        except Exception as e:
            self.log_output.insert(tk.END, f"Error processing {file_path}: {str(e)}\n")

    def preview_changes(self):
        search = self.search_input.get()
        replace = self.replace_input.get()
        method_choice = self.method_combo.get()
        directory = self.dir_path.get()

        preview_window = tk.Toplevel(self.root)
        preview_window.title("Preview Changes")

        for root_dir, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root_dir, file)
                if file.endswith('.txt'):
                    with open(file_path, 'r', encoding='utf-8') as file:
                        original_content = file.read()

                    modified_content = self.process_preview(original_content, search, replace, method_choice)
                    tk.Label(preview_window, text="Original Content:").pack()
                    original_text = tk.Text(preview_window, height=10, width=50)
                    original_text.insert(tk.END, original_content)
                    original_text.pack()
                    tk.Label(preview_window, text="Modified Content:").pack()
                    modified_text = tk.Text(preview_window, height=10, width=50)
                    modified_text.insert(tk.END, modified_content)
                    modified_text.pack()
                    break
            break

    def process_preview(self, text, search, replace, method_choice):
        if method_choice == "Method 1: replace() String Method":
            return text.replace(search, replace)
        elif method_choice == "Method 2: re.sub() with Regular Expressions":
            return re.sub(search, replace, text)

    def save_config(self):
        config = {
            "method": self.method_combo.get(),
            "search": self.search_input.get(),
            "replace": self.replace_input.get(),
            "directory": self.dir_path.get(),
            "file_types": self.file_types.get(),
            "recursive": self.recursive_var.get(),
            "backup": self.backup_var.get(),
        }
        with open("config.json", "w") as f:
            json.dump(config, f)
        messagebox.showinfo("Success", "Configuration saved!")

    def load_config(self):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
            self.method_combo.set(config["method"])
            self.search_input.delete(0, tk.END)
            self.search_input.insert(0, config["search"])
            self.replace_input.delete(0, tk.END)
            self.replace_input.insert(0, config["replace"])
            self.dir_path.delete(0, tk.END)
            self.dir_path.insert(0, config["directory"])
            self.file_types.delete(0, tk.END)
            self.file_types.insert(0, config["file_types"])
            self.recursive_var.set(config["recursive"])
            self.backup_var.set(config["backup"])
            messagebox.showinfo("Success", "Configuration loaded!")
        except FileNotFoundError:
            messagebox.showerror("Error", "No configuration found.")
    def show_help(self):
            help_window = tk.Toplevel(self.root)
            help_window.title("Help - Search and Replace Text in Directory & Regex Cheat Sheet")

            help_message = (
                "This program allows you to search and replace text in multiple files within a directory.\n\n"
                "Instructions:\n"
                "1. Select the replacement method from the dropdown:\n"
                "   - Method 1: Simple string replacement using the replace() method.\n"
                "   - Method 2: Regular expression replacement using re.sub().\n"
                "   - Method 3: Character-level replacement using str.translate() and str.maketrans().\n"
                "   - Method 4: String interpolation (F-strings) and replace().\n"
                "   - Method 5: Lambda function with re.sub() for dynamic replacements.\n\n"
                "2. Enter the text you want to search for in the 'Search For' field.\n"
                "3. Enter the text you want to replace with in the 'Replace With' field.\n"
                "4. Select the directory where the files are located using the 'Browse' button.\n"
                "5. Specify the file types you want to process (e.g., *.txt).\n"
                "6. Choose whether to create backups and whether to search recursively.\n"
                "7. Click 'Replace in Directory' to begin the search and replace operation. The program will create a new folder and copy modified files into it.\n"
                "8. The results of the operation will be displayed in the log.\n\n"
                "Regex Cheat Sheet:\n\n"
                "Basic Character Classes:\n"
                " - \d : Matches any digit (0-9).\n"
                " - \w : Matches any word character (letters, digits, underscores).\n"
                " - \s : Matches any whitespace character (spaces, tabs, line breaks).\n"
                " - \W : Matches any non-word character.\n"
                " - \D : Matches any non-digit character.\n"
                " - \S : Matches any non-whitespace character.\n"
                "\n"
                "Quantifiers:\n"
                " - * : Matches 0 or more of the preceding element.\n"
                " - + : Matches 1 or more of the preceding element.\n"
                " - ? : Matches 0 or 1 of the preceding element (making it optional).\n"
                " - {n} : Matches exactly 'n' occurrences of the preceding element.\n"
                " - {n,m} : Matches between 'n' and 'm' occurrences of the preceding element.\n"
                "\n"
                "Anchors:\n"
                " - ^ : Anchors the match to the start of a string.\n"
                " - $ : Anchors the match to the end of a string.\n"
                " - \\b : Matches a word boundary (space, punctuation, etc.).\n"
                "\n"
                "Special Sequences:\n"
                " - \\d : Matches any digit.\n"
                " - \\D : Matches any non-digit.\n"
                " - \\s : Matches any whitespace character.\n"
                " - \\S : Matches any non-whitespace character.\n"
                " - \\w : Matches any word character (letters, digits, underscores).\n"
                " - \\W : Matches any non-word character.\n"
                "\n"
                "Advanced Patterns:\n"
                " - \\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b : Matches an email address.\n"
                " - \\d{4}-\\d{2}-\\d{2} : Matches a date in the format YYYY-MM-DD.\n"
                " - \\b\\d{3}[-.]\\d{3}[-.]\\d{4}\\b : Matches a phone number (e.g., 123-456-7890 or 123.456.7890).\n"
                " - https?://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+ : Matches a URL.\n"
                " - \\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b : Matches an IPv4 address.\n"
                " - [A-Za-z]:\\\\(?:[A-Za-z0-9]+\\\\)*[A-Za-z0-9]+\\.[A-Za-z]{2,4} : Matches a file path (e.g., C:\\path\\file.txt).\n"
                " - \\b(?:\\d{4}[ -]?){3}\\d{4}\\b : Matches a credit card number.\n\n"
                "For more regex details, visit: https://regex101.com/"
            )

            help_label = tk.Label(help_window, text=help_message, justify=tk.LEFT)
            help_label.pack(padx=10, pady=10)
    def use_pattern(self, regex_combo, regex_patterns):
        selected_pattern = regex_combo.get()
        if selected_pattern in regex_patterns:
            self.search_input.delete(0, tk.END)
            self.search_input.insert(0, regex_patterns[selected_pattern])

    def test_regex(self):
            """Method to test a custom regex against sample text."""
            pattern = self.tester_pattern.get()
            test_text = self.tester_text.get("1.0", tk.END)
            try:
                compiled_pattern = re.compile(pattern)
                matches = compiled_pattern.findall(test_text)
                if matches:
                    self.test_results.delete("1.0", tk.END)
                    self.test_results.insert(tk.END, f"Matches Found:\n{matches}")
                else:
                    self.test_results.delete("1.0", tk.END)
                    self.test_results.insert(tk.END, "No matches found.")
            except re.error as e:
                self.test_results.delete("1.0", tk.END)
                self.test_results.insert(tk.END, f"Invalid Regex: {e}")

      

# Main program to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SearchReplaceApp(root)
    root.mainloop()
