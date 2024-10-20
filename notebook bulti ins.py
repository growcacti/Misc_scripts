import tkinter as tk
from tkinter import ttk

class BuiltInAppWithNotebook:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Built-ins with Tkinter")
        
        # Create a Notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Tab 1 for Sorting
        self.tab_sort = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_sort, text="Sort Numbers")
        self.create_sort_tab()

        # Tab 2 for Filtering
        self.tab_filter = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_filter, text="Filter Evens")
        self.create_filter_tab()

    def create_sort_tab(self):
        # Label for Instruction
        self.sort_label = tk.Label(self.tab_sort, text="Enter a comma-separated list of numbers:")
        self.sort_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        # Entry for User Input
        self.sort_entry = tk.Entry(self.tab_sort, width=30)
        self.sort_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        # Sort Button
        self.sort_button = tk.Button(self.tab_sort, text="Sort", command=self.sort_numbers)
        self.sort_button.grid(row=2, column=0, padx=10, pady=5)

        # Result Label
        self.sort_result_label = tk.Label(self.tab_sort, text="Result:")
        self.sort_result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Result Display
        self.sort_result_display = tk.Label(self.tab_sort, text="", fg="blue")
        self.sort_result_display.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    def create_filter_tab(self):
        # Label for Instruction
        self.filter_label = tk.Label(self.tab_filter, text="Enter a comma-separated list of numbers:")
        self.filter_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        # Entry for User Input
        self.filter_entry = tk.Entry(self.tab_filter, width=30)
        self.filter_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        # Filter Button
        self.filter_button = tk.Button(self.tab_filter, text="Filter Evens", command=self.filter_even)
        self.filter_button.grid(row=2, column=0, padx=10, pady=5)

        # Result Label
        self.filter_result_label = tk.Label(self.tab_filter, text="Result:")
        self.filter_result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Result Display
        self.filter_result_display = tk.Label(self.tab_filter, text="", fg="blue")
        self.filter_result_display.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    def sort_numbers(self):
        input_text = self.sort_entry.get()
        try:
            numbers = list(map(int, input_text.split(',')))
            sorted_numbers = sorted(numbers)
            self.sort_result_display.config(text=f"Sorted: {sorted_numbers}")
        except ValueError:
            self.sort_result_display.config(text="Invalid input! Please enter numbers only.")

    def filter_even(self):
        input_text = self.filter_entry.get()
        try:
            numbers = list(map(int, input_text.split(',')))
            evens = list(filter(lambda x: x % 2 == 0, numbers))
            self.filter_result_display.config(text=f"Evens: {evens}")
        except ValueError:
            self.filter_result_display.config(text="Invalid input! Please enter numbers only.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BuiltInAppWithNotebook(root)
    root.mainloop()
