import tkinter as tk
from tkinter import ttk, filedialog, messagebox
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
        self.root.title("Multi-File Editor with Treeview")
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

        # Create Treeview widget for displaying data
        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.tree = ttk.Treeview(self.tree_frame, columns=("Key", "Value"), show="headings")
        self.tree.heading("Key", text="Key")
        self.tree.heading("Value", text="Value")
        self.tree.column("Key", width=200)
        self.tree.column("Value", width=400)
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Vertical scrollbar for Treeview
        vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

        # Frame to display Entry or Text widget for editing
        self.input_frame = tk.Frame(self.root)
        self.input_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.entry_widget = tk.Entry(self.input_frame, width=60)
        self.text_widget = tk.Text(self.input_frame, height=5, width=60)

        # Bind selection change in Treeview to display the editable input widget
        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)

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
        """Display the loaded data in the Treeview."""
        # Clear previous data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Display JSON or CSV data in Treeview
        if isinstance(self.file_handler.data, list):
            if isinstance(self.file_handler.data[0], dict):  # JSON list of dictionaries
                for i, entry in enumerate(self.file_handler.data):
                    for key, value in entry.items():
                        self.tree.insert("", "end", values=(key, value))
            else:  # CSV data
                for row in self.file_handler.data:
                    self.tree.insert("", "end", values=(row[0], row[1:] if len(row) > 1 else ""))
        elif isinstance(self.file_handler.data, dict):  # JSON object
            for key, value in self.file_handler.data.items():
                self.tree.insert("", "end", values=(key, value))

    def on_treeview_select(self, event):
        """Handle selection in Treeview and display editable widget."""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            key, value = item["values"]

            self.clear_input_frame()

            if isinstance(value, str) and len(value) > 50:
                self.text_widget.grid(row=0, column=0, padx=5, pady=5)
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, value)
            else:
                self.entry_widget.grid(row=0, column=0, padx=5, pady=5)
                self.entry_widget.delete(0, tk.END)
                self.entry_widget.insert(0, value)

    def clear_input_frame(self):
        """Clear the input frame (remove Entry or Text widget)."""
        self.entry_widget.grid_remove()
        self.text_widget.grid_remove()


# Create the main Tkinter window
root = tk.Tk()

# Run the application
app = MultiFileEditorApp(root)
root.mainloop()
