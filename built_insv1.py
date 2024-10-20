import tkinter as tk

class BuiltInApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Built-ins with Tkinter")
        
        # Label for Instruction
        self.label = tk.Label(root, text="Enter a comma-separated list of numbers:")
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        # Entry for User Input
        self.input_entry = tk.Entry(root, width=30)
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        # Sort Button
        self.sort_button = tk.Button(root, text="Sort", command=self.sort_numbers)
        self.sort_button.grid(row=2, column=0, padx=10, pady=5)

        # Filter Even Button
        self.filter_button = tk.Button(root, text="Filter Evens", command=self.filter_even)
        self.filter_button.grid(row=2, column=1, padx=10, pady=5)

        # Result Label
        self.result_label = tk.Label(root, text="Result:")
        self.result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Result Display
        self.result_display = tk.Label(root, text="", fg="blue")
        self.result_display.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    def sort_numbers(self):
        # Get the input from the Entry widget
        input_text = self.input_entry.get()
        # Convert to a list of integers
        try:
            numbers = list(map(int, input_text.split(',')))
            sorted_numbers = sorted(numbers)  # Sort the numbers
            self.result_display.config(text=f"Sorted: {sorted_numbers}")
        except ValueError:
            self.result_display.config(text="Invalid input! Please enter numbers only.")

    def filter_even(self):
        # Get the input from the Entry widget
        input_text = self.input_entry.get()
        # Convert to a list of integers
        try:
            numbers = list(map(int, input_text.split(',')))
            evens = list(filter(lambda x: x % 2 == 0, numbers))  # Filter even numbers
            self.result_display.config(text=f"Evens: {evens}")
        except ValueError:
            self.result_display.config(text="Invalid input! Please enter numbers only.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BuiltInApp(root)
    root.mainloop()
