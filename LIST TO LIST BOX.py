import tkinter as tk

# Your Python list
python_list = ['Item 1', 'Item 2', 'Item 3', 'Item 4']

# Create the main window
root = tk.Tk()
root.title('List to Listbox')

# Create a Listbox widget
listbox = tk.Listbox(root)
listbox.pack()

# Iterate through the Python list and add items to the Listbox
for item in python_list:
    listbox.insert(tk.END, item)

# Start the Tkinter event loop
root.mainloop()
