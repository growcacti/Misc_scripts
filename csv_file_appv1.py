import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import csv
from io import StringIO

class CSVEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Editor")
        self.delimiter = ','  # Default delimiter
        self.data = []

        # Create UI components
        self.create_ui()

    def create_ui(self):
        """Create the UI components for the CSV editor."""
        # Frame for buttons
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=0, column=0, padx=10, pady=5)

        # Load CSV button
        self.load_button = tk.Button(button_frame, text="Load CSV", command=self.load_csv)
        self.load_button.grid(row=0, column=0, padx=5, pady=5)

        # Save CSV button
        self.save_button = tk.Button(button_frame, text="Save CSV", command=self.save_csv)
        self.save_button.grid(row=0, column=1, padx=5, pady=5)

        # Create New CSV button
        self.new_button = tk.Button(button_frame, text="New CSV", command=self.create_new_csv)
        self.new_button.grid(row=0, column=2, padx=5, pady=5)

        # Change Delimiter button
        self.delimiter_button = tk.Button(button_frame, text="Change Delimiter", command=self.change_delimiter)
        self.delimiter_button.grid(row=0, column=3, padx=5, pady=5)

        # Frame to display CSV content in a grid
        self.csv_frame = tk.Frame(self.root)
        self.csv_frame.grid(row=1, column=0, padx=10, pady=10)

    def load_csv(self):
        """Load a CSV file and display it in the grid."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=self.delimiter)
                self.data = list(reader)
                self.display_csv_data()

    def save_csv(self):
        """Save the edited CSV data to a file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=self.delimiter)
                for row in self.data:
                    writer.writerow(row)
            messagebox.showinfo("Success", "CSV file saved successfully!")

    def create_new_csv(self):
        """Create a new CSV file."""
        rows = simpledialog.askinteger("Input", "How many rows?", minvalue=1, maxvalue=100)
        cols = simpledialog.askinteger("Input", "How many columns?", minvalue=1, maxvalue=50)
        if rows and cols:
            self.data = [['' for _ in range(cols)] for _ in range(rows)]
            self.display_csv_data()

    def change_delimiter(self):
        """Change the CSV delimiter."""
        delimiter = simpledialog.askstring("Input", "Enter delimiter (e.g., comma, tab, semicolon):")
        if delimiter:
            if delimiter.lower() == "tab":
                self.delimiter = '\t'
            else:
                self.delimiter = delimiter
            self.display_csv_data()  # Re-load the data with the new delimiter

    def display_csv_data(self):
        """Display the CSV data in the grid (editable)."""
        # Clear previous data from the frame
        for widget in self.csv_frame.winfo_children():
            widget.destroy()

        # Display the CSV content in a grid of Entry widgets
        for r, row in enumerate(self.data):
            for c, value in enumerate(row):
                entry = tk.Entry(self.csv_frame, width=15)
                entry.grid(row=r, column=c, padx=5, pady=5)
                entry.insert(0, value)
                entry.bind('<KeyRelease>', lambda event, row=r, col=c: self.update_data(row, col, event.widget.get()))

    def update_data(self, row, col, value):
        """Update the CSV data when the user edits the grid."""
        self.data[row][col] = value


# Create the main Tkinter window
root = tk.Tk()

# Run the application
app = CSVEditorApp(root)
root.mainloop()
