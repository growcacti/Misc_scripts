import tkinter as tk
from tkinter import Listbox

# Create the main window
root = tk.Tk()
root.geometry("200x200")

# Create a Listbox
listbox = Listbox(root)
listbox.pack(pady=15)

# Initial list of strings
strings = ["First Item", "Second Item", "Delete This", "Another Item", "delete me too"]

# Function to process and update the listbox
def update_listbox():
    listbox.delete(0, tk.END)  # Clear the listbox
    processed_strings = [s.lower() + " - processed" for s in strings if "delete" not in s.lower()]
    for item in processed_strings:
        listbox.insert(tk.END, item)

# Initially populate the listbox
update_listbox()

root.mainloop()
# Initial list of strings
strings = ["First Item", "Second Item", "Delete This", "Another Item", "delete me too"]

# Convert to lowercase, remove strings containing "delete", and append " - processed"
processed_strings = [s.lower() + " - processed" for s in strings if "delete" not in s.lower()]

print(processed_strings)
