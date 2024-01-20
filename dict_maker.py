import tkinter as tk

def create_dict_from_lists():
    key_list = keys_entry.get().split()
    value_list = values_entry.get().split()
    if len(key_list) == len(value_list):
        dictionary = dict(zip(key_list, value_list))
        output_label['text'] = str(dictionary)
    else:
        output_label['text'] = "Error: Key and value lists are not the same length"

def add_key_value_pair():
    key = key_entry.get()
    value = value_entry.get()
    if key and value:
        dictionary[key] = value
        dict_display.configure(state='normal')
        dict_display.insert(tk.END, f"{key}: {value}\n")
        dict_display.configure(state='disabled')

# Create the main window
root = tk.Tk()
root.title("Dictionary Creator")

# For creating dictionary from two lists
tk.Label(root, text="Enter keys:").grid(row=0, column=0)
keys_entry = tk.Entry(root)
keys_entry.grid(row=0, column=1)

tk.Label(root, text="Enter values:").grid(row=1, column=0)
values_entry = tk.Entry(root)
values_entry.grid(row=1, column=1)

create_button = tk.Button(root, text="Create Dictionary", command=create_dict_from_lists)
create_button.grid(row=2, columnspan=2)

output_label = tk.Label(root, text="")
output_label.grid(row=3, columnspan=2)

# Separator
tk.Label(root, text="").grid(row=4)  # Just to add a space

# For adding key-value pairs one by one
dictionary = {}

tk.Label(root, text="Enter key:").grid(row=5, column=0)
key_entry = tk.Entry(root)
key_entry.grid(row=5, column=1)

tk.Label(root, text="Enter value:").grid(row=6, column=0)
value_entry = tk.Entry(root)
value_entry.grid(row=6, column=1)

add_button = tk.Button(root, text="Add to Dictionary", command=add_key_value_pair)
add_button.grid(row=7, columnspan=2)

dict_display = tk.Text(root, height=5, state='disabled')
dict_display.grid(row=8, columnspan=2)

# Run the application
root.mainloop()
