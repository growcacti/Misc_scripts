import os
import fnmatch
import re
import tkinter as tk
from tkinter import filedialog, messagebox

# Basic knowledge base for standard Python library functions
KNOWLEDGE_BASE = {
    "print": "Outputs text to the console.",
    "len": "Returns the number of items in a container.",
    "sum": "Returns the sum of all items in an iterable.",
    "max": "Returns the largest item in an iterable or two or more arguments.",
    "min": "Returns the smallest item in an iterable or two or more arguments.",
    "range": "Generates a sequence of numbers from start to stop (exclusive).",
    "sorted": "Returns a new sorted list from the items in an iterable.",
    "open": "Opens a file and returns a file object.",
    "input": "Reads a line of input from the user.",
    "map": "Applies a function to all items in an input list.",
    "filter": "Constructs an iterator from items in iterable for which function returns true.",
    # Add more functions as needed
}

# List of file extensions to ignore
EXCLUDED_EXTENSIONS = {'.pyc', '.log', '.txt','.png','.jpg','.mp3','.bmp'}

class CodeSnippetExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Code Snippet Extractor")
        
        # Label for directory selection
        self.dir_label = tk.Label(root, text="Directory:")
        self.dir_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Entry to display selected directory
        self.dir_entry = tk.Entry(root, width=40)
        self.dir_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Button to browse directory
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_directory)
        self.browse_button.grid(row=0, column=2, padx=10, pady=10)
        
        # Recursive option checkbox
        self.recursive_var = tk.BooleanVar(value=True)
        self.recursive_check = tk.Checkbutton(root, text="Recursive", variable=self.recursive_var)
        self.recursive_check.grid(row=1, column=0, columnspan=3, pady=5)
        
        # Button to start extraction
        self.extract_button = tk.Button(root, text="Extract Snippets", command=self.extract_snippets)
        self.extract_button.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Text box to display snippets
        self.snippets_text = tk.Text(root, wrap="word", height=20, width=80)
        self.snippets_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        
        # Save button to save snippets to file
        self.save_button = tk.Button(root, text="Save Snippets", command=self.save_snippets)
        self.save_button.grid(row=4, column=0, columnspan=3, pady=10)
        
    def browse_directory(self):
        # Open a directory selection dialog
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)

    def extract_snippets(self):
        directory = self.dir_entry.get()
        if not directory:
            messagebox.showwarning("No Directory Selected", "Please select a directory first.")
            return

        snippets = self.get_code_snippets(directory, self.recursive_var.get())
        self.snippets_text.delete("1.0", tk.END)
        self.snippets_text.insert(tk.END, "\n".join(snippets))

    def get_code_snippets(self, directory, recursive):
        snippets = []
        
        if recursive:
            file_paths = [
                os.path.join(root, filename)
                for root, _, files in os.walk(directory)
                for filename in fnmatch.filter(files, "*.py")
                if not filename.endswith(tuple(EXCLUDED_EXTENSIONS))
            ]
        else:
            file_paths = [
                os.path.join(directory, filename)
                for filename in os.listdir(directory)
                if fnmatch.fnmatch(filename, "*.py") and not filename.endswith(tuple(EXCLUDED_EXTENSIONS))
            ]

        for filepath in file_paths:
            try:
                # Try to open the file with UTF-8 encoding, ignoring errors
                with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                    
                    # Adjust regex to capture functions with multiple lines, including return statements
                    functions = re.findall(
                        r"(?:#.*\n)?def\s+(\w+)\(.*?\):\n((?: {4}.*\n)+)",
                        content
                    )
                    
                    for func_name, code_block in functions:
                        # Check for docstring in code block
                        docstring = re.search(r'""".*?"""', code_block, re.DOTALL)
                        if docstring:
                            description = docstring.group(0)
                        elif func_name in KNOWLEDGE_BASE:
                            description = KNOWLEDGE_BASE[func_name]
                        else:
                            description = "No description available"
                        
                        snippet_text = (
                            f"File: {filepath}\n"
                            f"Function: {func_name}\n"
                            f"Description: {description}\n"
                            f"Code:\n{code_block.strip()}\n{'-'*40}\n"
                        )
                        snippets.append(snippet_text)
            except FileNotFoundError:
                print(f"File not found or inaccessible: {filepath}")
            except PermissionError:
                print(f"Permission denied: {filepath}")
        
        if not snippets:
            messagebox.showinfo("No Snippets Found", "No functions found in the selected directory.")
        
        return snippets
    
    def save_snippets(self):
        snippets = self.snippets_text.get("1.0", tk.END).strip()
        if not snippets:
            messagebox.showwarning("No Snippets", "No snippets to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(snippets)
            messagebox.showinfo("Saved", f"Snippets saved to {file_path}")

# Main application
root = tk.Tk()
app = CodeSnippetExtractorApp(root)
root.mainloop()
