import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Define the SearchReplaceApp class
class SearchReplaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Search and Replace Text - Tkinter Version")

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

        # Output area for the result
        result_label = tk.Label(self.root, text="Result:")
        result_label.grid(row=4, column=0, padx=10, pady=5)

        self.result_output = tk.Text(self.root, height=5, width=50)
        self.result_output.grid(row=4, column=1, padx=10, pady=5)

        # Replace button
        replace_button = tk.Button(self.root, text="Replace", command=self.perform_replacement)
        replace_button.grid(row=5, column=1, pady=10)

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
        text = self.text_input.get("1.0", tk.END).strip()
        search = self.search_input.get()
        replace = self.replace_input.get()
        method_choice = self.method_combo.get()

        if not text or not search or not replace:
            messagebox.showwarning("Input Error", "Please provide all inputs.")
            return

        result = ""
        if method_choice == "Method 1: replace() String Method":
            result = self.replace_method_1(text, search, replace)
        elif method_choice == "Method 2: re.sub() with Regular Expressions":
            result = self.replace_method_2(text, search, replace)
        elif method_choice == "Method 3: str.translate() and str.maketrans()":
            result = self.replace_method_3(text, search, replace)
        elif method_choice == "Method 4: F-strings and replace()":
            result = self.replace_method_4(text, search, replace)
        elif method_choice == "Method 5: Lambda with re.sub()":
            result = self.replace_method_5(text, search, replace)
        else:
            result = "Please select a valid method."

        # Display the result in the output text box
        self.result_output.delete("1.0", tk.END)
        self.result_output.insert(tk.END, result)

# Main program to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SearchReplaceApp(root)
    root.mainloop()
