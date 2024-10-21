import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import json
import csv
import xml.etree.ElementTree as ET


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
        elif file_type == 'xml':
            self.file_type = 'xml'
            self.load_xml(file_path)

    def save_file(self):
        """Save the data to a file based on the current file type."""
        if not self.file_type:
            messagebox.showerror("Error", "No file type selected for saving.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=f".{self.file_type}", filetypes=[(f"{self.file_type.upper()} files", f"*.{self.file_type}")])
        if not file_path:
            return

        if self.file_type == 'csv':
            self.save_csv(file_path)
        elif self.file_type == 'json':
            self.save_json(file_path)
        elif self.file_type == 'xml':
            self.save_xml(file_path)

    def load_csv(self, file_path):
        """Load CSV file and store its data."""
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter)
            self.data = list(reader)

    def save_csv(self, file_path):
        """Save CSV data to file."""
        with open(file_path, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=self.delimiter)
            for row in self.data:
                writer.writerow(row)
        messagebox.showinfo("Success", "CSV file saved successfully!")

    def load_json(self, file_path):
        """Load JSON file and store its data."""
        with open(file_path, "r") as json_file:
            self.data = json.load(json_file)
            self.data = self.flatten_json(self.data)

    def save_json(self, file_path):
        """Save JSON data to file."""
        # Unflatten the JSON structure before saving
        unflattened_data = self.unflatten_json(self.data)
        with open(file_path, "w") as json_file:
            json.dump(unflattened_data, json_file, indent=4)
        messagebox.showinfo("Success", "JSON file saved successfully!")

    def load_xml(self, file_path):
        """Load XML file and store its data."""
        tree = ET.parse(file_path)
        root = tree.getroot()
        self.data = self.xml_to_dict(root)
        self.data = self.flatten_json(self.data)

    def save_xml(self, file_path):
        """Save data as XML file."""
        unflattened_data = self.unflatten_json(self.data)
        root = self.dict_to_xml("root", unflattened_data)
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)
        messagebox.showinfo("Success", "XML file saved successfully!")

    def flatten_json(self, json_obj, parent_key='', sep='_'):
        """Flatten nested JSON objects into a dictionary."""
        items = {}
        for k, v in json_obj.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(self.flatten_json(v, new_key, sep=sep))
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    items.update(self.flatten_json({f"{k}_{i}": item}, parent_key, sep=sep))
            else:
                items[new_key] = v
        return items

    def unflatten_json(self, flat_json, sep='_'):
        """Unflatten a dictionary to restore nested JSON objects."""
        unflattened = {}
        for k, v in flat_json.items():
            keys = k.split(sep)
            d = unflattened
            for key in keys[:-1]:
                d = d.setdefault(key, {})
            d[keys[-1]] = v
        return unflattened

    def xml_to_dict(self, element):
        """Convert an XML element and its children into a dictionary."""
        d = {element.tag: {} if element.attrib else None}
        children = list(element)
        if children:
            dd = {}
            for dc in map(self.xml_to_dict, children):
                for k, v in dc.items():
                    if k in dd:
                        if not isinstance(dd[k], list):
                            dd[k] = [dd[k]]
                        dd[k].append(v)
                    else:
                        dd[k] = v
            d = {element.tag: dd}
        if element.attrib:
            d[element.tag].update(('@' + k, v) for k, v in element.attrib.items())
        if element.text:
            text = element.text.strip()
            if children or element.attrib:
                if text:
                    d[element.tag]['#text'] = text
            else:
                d[element.tag] = text
        return d

    def dict_to_xml(self, tag, d):
        """Convert a dictionary back to an XML element."""
        element = ET.Element(tag)
        for k, v in d.items():
            if isinstance(v, dict):
                child = self.dict_to_xml(k, v)
                element.append(child)
            else:
                child = ET.SubElement(element, k)
                child.text = str(v)
        return element


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

        # Load XML button
        self.load_xml_button = tk.Button(button_frame, text="Load XML", command=lambda: self.load_file('xml'))
        self.load_xml_button.grid(row=0, column=2, padx=5, pady=5)

        # Save button
        self.save_button = tk.Button(button_frame, text="Save", command=self.save_file)
        self.save_button.grid(row=0, column=3, padx=5, pady=5)

        # Change Delimiter button
        self.delimiter_button = tk.Button(button_frame, text="Change Delimiter", command=self.change_delimiter)
        self.delimiter_button.grid(row=0, column=4, padx=5, pady=5)

        # Frame to display file content in a grid
        self.file_frame = tk.Frame(self.root)
        self.file_frame.grid(row=1, column=0, padx=10, pady=10)

    def load_file(self, file_type):
        """Load a file and display its content."""
        self.file_handler.load_file(file_type)
        self.display_data()

    def save_file(self):
        """Save the file."""
        self.file_handler.save_file()

    def change_delimiter(self):
        """Change the CSV delimiter."""
        delimiter = tk.simpledialog.askstring("Input", "Enter delimiter (e.g., comma, tab, semicolon):")
        if delimiter:
            self.file_handler.change_delimiter(delimiter)

    def display_data(self):
        """Display the loaded data in the grid."""
        # Clear the current grid
        for widget in self.file_frame.winfo_children():
            widget.destroy()

        # Display data in a grid of Entry widgets
        for r, (key, value) in enumerate(self.file_handler.data.items()):
            key_entry = tk.Entry(self.file_frame, width=30)
            key_entry.grid(row=r, column=0, padx=5, pady=5)
            key_entry.insert(0, key)
            value_entry = tk.Entry(self.file_frame, width=30)
            value_entry.grid(row=r, column=1, padx=5, pady=5)
            value_entry.insert(0, value)
            value_entry.bind('<KeyRelease>', lambda event, k=key: self.file_handler.update_data(k, event.widget.get()))


# Create the main Tkinter window
root = tk.Tk()

# Run the application
app = MultiFileEditorApp(root)
root.mainloop()
