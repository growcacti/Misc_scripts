import tkinter as tk
from tkinter import messagebox

def add_entry():
    # Get the values from the entry widgets
    key = entry_key.get()
    value = entry_value.get()
    
    # Check if either entry is empty
    if not key or not value:
        messagebox.showwarning("Warning", "Both fields must be filled out.")
        return
    
    # Add the dictionary as a string to the list box
    list_box.insert(tk.END, str({key: value}))
    
    # Clear the entry widgets
    entry_key.delete(0, tk.END)
    entry_value.delete(0, tk.END)

def save_entries():
    # Save list box contents to a file
    with open("entries.txt", "w") as file:
        for entry in list_box.get(0, tk.END):
            file.write(entry + "\n")
    messagebox.showinfo("Success", "Entries saved to entries.txt")

root = tk.Tk()
root.title("Entry to Dictionary")

# Create a frame
frame = tk.Frame(root, width =1200 , height =800)
frame.grid(row=0, column=0)
savnac = tk.Canvas(frame, bg="aquamarine2")
savnac.grid(row=1, column=1)

# Entry widgets
entry_key = tk.Entry(savnac)
entry_key.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
entry_value = tk.Entry(savnac)
entry_value.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Button to add entry
btn_add = tk.Button(savnac, text="Add", command=add_entry)
btn_add.grid(row=1, column=0, columnspan=2, sticky="ew")

# List box to display entries
list_box = tk.Listbox(savnac)
list_box.grid(row=2, column=0, columnspan=2, sticky="nsew")

# Button to save entries
btn_save = tk.Button(savnac, text="Save", command=save_entries)
btn_save.grid(row=3, column=0, columnspan=2, sticky="ew")

# Configure grid to expand
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.rowconfigure(2, weight=1)

root.mainloop()
