import tkinter as tk

def sort_lb():
    # Retrieve and sort the lb items
    items = list(lb.get(0, tk.END))
    items.sort()

    # Update the lb with sorted items
    lb.delete(0, tk.END)  # Clear current items
    for item in items:
        lb.insert(tk.END, item)

# Create the main window
root = tk.Tk()
root.title("Sort Listbox")

# Create a Listbox
lb = tk.Listbox(root)
lb.grid(row=3 ,column=5)

# Populate the Listbox with unsorted items
filenames = ["file5.txt", "file3.txt", "file1.txt", "file4.txt", "file2.txt"]
for filename in filenames:
    lb.insert(tk.END, filename)

# Create a Button to sort the lb items
sort_bnt = tk.Button(root, text="Sort", command=sort_lb)
sort_bnt.grid(row=2, column=1)

# Start the GUI event loop
root.mainloop()
