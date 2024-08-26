import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import math

class CSVCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Calculator")

        # GUI Components
        self.load_button = tk.Button(root, text="Load CSV", command=self.load_csv)
        self.load_button.grid(row=0, column=0, padx=10, pady=10)

        self.spreadsheet_frame = tk.Frame(root)
        self.spreadsheet_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        self.calculate_button = tk.Button(root, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=2, column=0, padx=10, pady=10)

        self.sum_label = tk.Label(root, text="Sum:")
        self.sum_label.grid(row=3, column=0, sticky='e')

        self.mean_label = tk.Label(root, text="Mean:")
        self.mean_label.grid(row=4, column=0, sticky='e')

        self.stddev_label = tk.Label(root, text="Standard Deviation:")
        self.stddev_label.grid(row=5, column=0, sticky='e')

        self.product_label = tk.Label(root, text="Product:")
        self.product_label.grid(row=6, column=0, sticky='e')

        self.power_label = tk.Label(root, text="Power (2):")
        self.power_label.grid(row=7, column=0, sticky='e')

        self.difference_label = tk.Label(root, text="Differences:")
        self.difference_label.grid(row=8, column=0, sticky='e')

        # Output Labels
        self.sum_value = tk.Label(root, text="")
        self.sum_value.grid(row=3, column=1, sticky='w')

        self.mean_value = tk.Label(root, text="")
        self.mean_value.grid(row=4, column=1, sticky='w')

        self.stddev_value = tk.Label(root, text="")
        self.stddev_value.grid(row=5, column=1, sticky='w')

        self.product_value = tk.Label(root, text="")
        self.product_value.grid(row=6, column=1, sticky='w')

        self.power_value = tk.Label(root, text="")
        self.power_value.grid(row=7, column=1, sticky='w')

        self.difference_value = tk.Label(root, text="")
        self.difference_value.grid(row=8, column=1, sticky='w')

        self.entries = []

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        self.clear_spreadsheet()
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for r_idx, row in enumerate(reader):
                entry_row = []
                for c_idx, value in enumerate(row):
                    entry = tk.Entry(self.spreadsheet_frame, width=10)
                    entry.insert(0, value)
                    entry.grid(row=r_idx, column=c_idx, padx=5, pady=5)
                    entry_row.append(entry)
                self.entries.append(entry_row)

    def clear_spreadsheet(self):
        for widget in self.spreadsheet_frame.winfo_children():
            widget.destroy()
        self.entries = []

    def calculate(self):
        numbers = self.get_numeric_entries()
        if not numbers:
            messagebox.showerror("Error", "No valid numbers found.")
            return

        # Perform calculations
        total_sum = self.calculate_sum(numbers)
        mean_value = self.calculate_mean(numbers)
        std_dev = self.calculate_standard_deviation(numbers)
        product = self.calculate_product(numbers)
        powered_values = self.calculate_power(numbers, 2)  # Example: power of 2
        differences = self.calculate_difference(numbers)

        # Display results
        self.sum_value.config(text=str(total_sum))
        self.mean_value.config(text=str(mean_value))
        self.stddev_value.config(text=str(std_dev))
        self.product_value.config(text=str(product))
        self.power_value.config(text=", ".join(map(str, powered_values)))
        self.difference_value.config(text=", ".join(map(str, differences)))

    def get_numeric_entries(self):
        numbers = []
        for entry_row in self.entries:
            for entry in entry_row:
                try:
                    number = float(entry.get())
                    numbers.append(number)
                except ValueError:
                    continue  # Skip non-numeric values
        return numbers

    def calculate_sum(self, numbers):
        return sum(numbers)

    def calculate_mean(self, numbers):
        return sum(numbers) / len(numbers) if numbers else 0

    def calculate_standard_deviation(self, numbers):
        mean = self.calculate_mean(numbers)
        variance = sum((x - mean) ** 2 for x in numbers) / len(numbers) if numbers else 0
        return math.sqrt(variance)

    def calculate_product(self, numbers):
        product = 1
        for number in numbers:
            product *= number
        return product

    def calculate_power(self, numbers, power):
        return [number ** power for number in numbers]

    def calculate_difference(self, numbers):
        return [numbers[i] - numbers[i-1] for i in range(1, len(numbers))]

if __name__ == '__main__':
    root = tk.Tk()
    app = CSVCalculatorApp(root)
    root.mainloop()
