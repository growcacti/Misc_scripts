import tkinter as tk
from tkinter import filedialog, messagebox
import json


def process_text_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Parse the key-value pairs and add double quotes around the values
    data = {}
    for line in lines:
        key, value = line.strip().split(":")
        data[key.strip()] = f'"{value.strip()}"'  # Double-quote the value

    return data


def save_as_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def open_file_dialog():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        try:
            data = process_text_file(filename)
            json_filename = filedialog.asksaveasfilename(
                defaultextension=".json", filetypes=[
                    ("JSON files", "*.json")])
            if json_filename:
                save_as_json(data, json_filename)
                messagebox.showinfo(
                    "Success", "Text file processed and saved as JSON successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


# Set up the GUI
root = tk.Tk()
root.title("Convert Text to JSON")
root.geometry("350x120")

label = tk.Label(root, text="Select a text file to convert to JSON")
label.pack(pady=10)

button = tk.Button(root, text="Select File", command=open_file_dialog)
button.pack(pady=10)

root.mainloop()
