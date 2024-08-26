import tkinter as tk
from tkinter import filedialog
import csv
import time
import os

def process_and_load_file():
    try:
        lines_to_skip = int(skip_lines_entry.get())
    except ValueError:
        print("Invalid number of lines to skip. Please enter an integer.")
        return
    # Ask the user to select a text file
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not file_path:
        return  # No file was selected

    # Create a CSV file with the current epoch time as its name
    epoch_time = int(time.time())
    csv_file_name = f"{epoch_time}_output.csv"
    csv_file_path = os.path.join(os.path.dirname(file_path), csv_file_name)

    # Read the text file, skip the first 33 lines, and write to the CSV file
    with open(file_path, 'r') as text_file, open(csv_file_path, 'w', newline='') as csv_file:
        text_lines = text_file.readlines()[lines_to_skip:]
        writer = csv.writer(csv_file)
        for line in text_lines:
            writer.writerow(line.strip().split())  # Assuming space-separated values

    # Display the CSV file in Listbox widgets
    display_csv_in_listboxes(csv_file_path)

def on_scroll(*args):
    # Update the position of all listboxes' view when the scrollbar is moved
    for lb in listboxes:
        lb.yview(*args)

def display_csv_in_listboxes(csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header_row = next(csv_reader, None)  # Read the header row (if present)
        num_columns = len(header_row) if header_row else max(len(row) for row in csv_reader)

    # Clear previous Listboxes and labels
    for listbox in listboxes:
        listbox.destroy()
    for label in column_labels:
        label.destroy()
    listboxes.clear()
    column_labels.clear()
    scrollbar = tk.Scrollbar(listbox_frame, orient='vertical', command=on_scroll)
    scrollbar.grid(row=1, column=num_columns, sticky='ns')

    # Create Listboxes and labels for each column
    for i in range(num_columns):
        label = tk.Label(listbox_frame, text=f"Column {i+1}")
        label.grid(row=0, column=i, sticky='ew')
        column_labels.append(label)
        listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
        listbox.grid(row=1, column=i, sticky='nsew')
        listboxes.append(listbox)
        listbox_frame.grid_columnconfigure(i, weight=1)

          # Populate Listboxes with data
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            for i, item in enumerate(row):
                listboxes[i].insert(tk.END, item)

# This function assumes that each listbox has the same number of rows.
def get_column_values(listboxes, column_index):
    column_values = []
    for listbox in listboxes:
        for row_index in range(listbox.size()):
            row_value = listbox.get(row_index)
            print("Row value:", row_value)  # Debug print to check the actual row value
            try:
                value = row_value.split()[column_index]  # Assuming values are space-separated
                print("Value to convert:", value)  # Debug print to check the value before conversion
                column_values.append(float(value))  # Convert directly to float
            except IndexError:
                # Break out of the inner loop if there aren't enough columns
                print("IndexError: Not enough columns in the row.")
                break
            except ValueError:
                # Continue to the next iteration if the value can't be converted to a float
                print("ValueError: Cannot convert value to float.")
                continue
    return column_values   




root = tk.Tk()
root.title('CSV Column Display')

# Frame for Listboxes
listbox_frame = tk.Frame(root)
listbox_frame.grid(row=5,column=1)
# Lists to keep track of dynamically created Listboxes and labels
listboxes = []
column_labels = []

# Button to process and load file
load_button = tk.Button(root, text="Load and Process File", command=process_and_load_file)
load_button.grid(row=2, column=1)


entry = tk.Entry(root, bd=7)
entry.grid(row=2, column=2)

tk.Label(root, text="Number of lines to skip:").grid(row=1, column=0)
skip_lines_entry = tk.Entry(root, bd=7)
skip_lines_entry.grid(row=1, column=1)
skip_lines_entry.insert(0, "33")  # Default value of 33 lines to skip


root.mainloop()
