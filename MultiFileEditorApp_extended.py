import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Entry, Text
import json
import csv


class FileHandler:
    def __init__(self):
        self.data = []
        self.file_type = None
        self.delimiter = ','  # Default delimiter for CSV

    def load_file(self, file_type):
        """Load a file based on the file type."""
        file_path = filedialog.askopenfilename(filetypes=[(f"{file_type.upper()} files", f"*.{file_type}")])
        if not file_path:
            return

        if file_type == 'csv':
            self.file_type = 'csv'
            self.load_csv(file_path)
        elif file_type == 'json':
            self.file_type = 'json'
            self.load_json(file_path)

    def load_csv(self, file_path):
        """Load CSV file and store its data."""
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter)
            self.data = list(reader)

    def load_json(self, file_path):
        """Load JSON file and store its data."""
        with open(file_path, "r") as json_file:
            self.data = json.load(json_file)

    def save_file(self, file_path):
        """Save the data to a file based on the current file type."""
        if self.file_type == 'csv':
            self.save_csv(file_path)
        elif self.file_type == 'json':
            self.save_json(file_path)

    def save_csv(self, file_path):
        """Save CSV data to file."""
        with open(file_path, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=self.delimiter)
            for row in self.data:
                writer.writerow(row)
        messagebox.showinfo("Success", "CSV file saved successfully!")

    def save_json(self, file_path):
        """Save JSON data to file."""
        with open(file_path, "w") as json_file:
            json.dump(self.data, json_file, indent=4)
        messagebox.showinfo("Success", "JSON file saved successfully!")


class MultiFileEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-File Editor")
        self.file_handler = FileHandler()

        # Create UI components
        self.create_ui()

    def create_ui(self):
        """Create the UI components."""
        # Frame for buttons
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=0, column=0, padx=10, pady=5)

        # Load CSV button
        self.load_csv_button = tk.Button(button_frame, text="Load CSV", command=lambda: self.load_file('csv'))
        self.load_csv_button.grid(row=0, column=0, padx=5, pady=5)

        # Load JSON button
        self.load_json_button = tk.Button(button_frame, text="Load JSON", command=lambda: self.load_file('json'))
        self.load_json_button.grid(row=0, column=1, padx=5, pady=5)

        # Save button
        self.save_button = tk.Button(button_frame, text="Save", command=self.save_file)
        self.save_button.grid(row=0, column=2, padx=5, pady=5)

        # Create listboxes and dynamic input areas
        self.listbox_frame = tk.Frame(self.root)
        self.listbox_frame.grid(row=1, column=0, padx=10, pady=10)

        self.listbox_keys = Listbox(self.listbox_frame, height=20, width=30)
        self.listbox_keys.grid(row=0, column=0, padx=5, pady=5)
        self.listbox_keys.bind("<<ListboxSelect>>", self.on_listbox_select)

        self.input_frame = tk.Frame(self.listbox_frame)
        self.input_frame.grid(row=0, column=1, padx=5, pady=5)

    def load_file(self, file_type):
        """Load a file and display its content."""
        self.file_handler.load_file(file_type)
        self.display_data()

    def save_file(self):
        """Save the file."""
        file_path = filedialog.asksaveasfilename(defaultextension=f".{self.file_handler.file_type}", filetypes=[(f"{self.file_handler.file_type.upper()} files", f"*.{self.file_handler.file_type}")])
        if file_path:
            self.file_handler.save_file(file_path)

    def display_data(self):
        """Display the loaded data in a listbox (for JSON/CSV) and show entry or text widget dynamically."""
        self.listbox_keys.delete(0, tk.END)
        self.clear_input_frame()

        if isinstance(self.file_handler.data, list):
            if isinstance(self.file_handler.data[0], dict):  # For JSON list of dictionaries
                for i, entry in enumerate(self.file_handler.data):
                    self.listbox_keys.insert(tk.END, f"Item {i+1}")
            else:  # For CSV data
                for i, row in enumerate(self.file_handler.data):
                    self.listbox_keys.insert(tk.END, f"Row {i+1}")
        elif isinstance(self.file_handler.data, dict):  # For JSON object
            for key in self.file_handler.data.keys():
                self.listbox_keys.insert(tk.END, key)

    def clear_input_frame(self):
        """Clear the dynamic input frame (Entry or Text widget)."""
        for widget in self.input_frame.winfo_children():
            widget.destroy()

    def on_listbox_select(self, event):
        """Handle listbox selection and show corresponding data in Entry or Text."""
        selection = event.widget.curselection()
        if not selection:
            return

        index = selection[0]
        self.clear_input_frame()

        if isinstance(self.file_handler.data, list):
            if isinstance(self.file_handler.data[0], dict):  # For JSON list of dictionaries
                selected_data = self.file_handler.data[index]
                self.populate_input_widgets(selected_data)
            else:  # For CSV data
                selected_data = self.file_handler.data[index]
                for i, value in enumerate(selected_data):
                    self.create_input_widget(value, row=i)
        elif isinstance(self.file_handler.data, dict):  # For JSON object
            key = self.listbox_keys.get(index)
            value = self.file_handler.data[key]
            self.create_input_widget(value)

    def populate_input_widgets(self, data_dict):
        """Create input widgets for each key-value pair in a dictionary."""
        for row, (key, value) in enumerate(data_dict.items()):
            tk.Label(self.input_frame, text=key).grid(row=row, column=0, padx=5, pady=5)
            self.create_input_widget(value, row=row, column=1)

    def create_input_widget(self, value, row=0, column=1):
        """Create either an Entry or Text widget depending on the data type or length."""
        if isinstance(value, str) and len(value) > 50:
            text_widget = Text(self.input_frame, height=5, width=30)
            text_widget.grid(row=row, column=column, padx=5, pady=5)
            text_widget.insert(tk.END, value)
        else:
            entry_widget = Entry(self.input_frame, width=30)
            entry_widget.grid(row=row, column=column, padx=5, pady=5)
            entry_widget.insert(0, value)


# Create the main Tkinter window
root = tk.Tk()

# Run the application
app = MultiFileEditorApp(root)
root.mainloop()
