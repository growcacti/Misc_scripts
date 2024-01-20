import tkinter as tk
from tkinter import ttk

# Define your string functions here
# ...

# Function dictionary
# ...

# Event handler for the execute button
# ...

# Create the main root
root = tk.Tk()
root.title("String Functions Demonstrator")

# ... (Menu code remains the same)

# Dropdown for selecting the function
function_name_var = tk.StringVar()
function_selector = ttk.Combobox(root, textvariable=function_name_var, width=50)
function_selector['values'] = list(function_dict.keys())
function_selector.grid(row=0, column=1, padx=10, pady=10)

# Label for the dropdown
function_label = tk.Label(root, text="Select Function:")
function_label.grid(row=0, column=0, padx=10, pady=10)

# Input area
input_label = tk.Label(root, text="Enter String:")
input_label.grid(row=1, column=0, padx=10, pady=10)

input_entry = tk.Entry(root, width=53)
input_entry.grid(row=1, column=1, padx=10, pady=10)

# Execute button
execute_button = tk.Button(root, text="Execute", command=run_selected_function)
execute_button.grid(row=2, column=1, sticky="w", padx=10, pady=10)

# Output area
output_label = tk.Label(root, text="Output:")
output_label.grid(row=3, column=0, padx=10, pady=10)

output_text = tk.Text(root, height=10, width=40)
output_text.grid(row=3, column=1, padx=10, pady=10)

# Run the application
root.mainloop()
