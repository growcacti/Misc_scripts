import tkinter as tk
from tkinter import filedialog
import csv
import time
import os

def process_and_load_file():
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
        text_lines = text_file.readlines()[33:]  # Skip the first 33 lines
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
def get_a_column_values(listboxes, column_index):
    column_values = []
    for listbox in listboxes:
        for row_index in range(listbox.size()):
            row_value = listbox.get(row_index)
            if isinstance(row_value, str):
                parts = row_value.split()  # Split the row into parts
                if len(parts) > column_index:  # Check if the column_index is within range
                    try:
                        column_value = parts[column_index]  # Get the value at column_index
                        column_values.append(float(column_value))  # Convert to float
                    except ValueError:
                        # Handle the case where conversion to float fails
                        print(f"ValueError: Cannot convert '{column_value}' to float.")
                else:
                    # Handle the case where there are not enough columns
                    print(f"IndexError: Row {row_index} does not have a column at index {column_index}.")
            else:
                # Handle the case where row_value is not a string
                print(f"TypeError: Row value at index {row_index} is not a string. It's a {type(row_value)}.")
    return column_values
def largest_delta(numbers):
    if len(numbers) < 2:
        return None  # Not enough elements to have a delta
    
    largest_difference = float('-inf')  # Start with the smallest possible number
    for i in range(len(numbers) - 1):
        # Calculate the absolute difference between adjacent numbers
        difference = abs(numbers[i+1] - numbers[i])
        # Update the largest difference if the current one is larger
        if difference > largest_difference:
            largest_difference = difference
    
    return largest_difference




def do_calculation():
    column_values = get_column_values(listboxes, 0)
    delta = largest_delta(column_values)
    print(delta)
    
def set_index():
    column_index = int(entry.get())
    numbers = get_a_column_values(listboxes, column_index)
    results = largest_delta(numbers)
    print(results)

# Main GUI setup
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
calc_button = tk.Button(root,text="do all Deltas", command=do_calculation)
calc_button.grid(row=3, column=1)
tk.Label(root, text="enter index column value for single column calc").grid(row=2, column=3)
entry = tk.Entry(root, bd=7)
entry.grid(row=2, column=4)
ccbutton = tk.Button(root,text="set from entry which column", command=set_index)
ccbutton.grid(row=3, column=4)


root.mainloop()
