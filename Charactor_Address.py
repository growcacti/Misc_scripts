import tkinter as tk
from tkinter import ttk

def display_string():
    # Clear Listbox and Text widget
    listbox.delete(0, tk.END)
    text_widget.delete('1.0', tk.END)

    # Get the string from the Entry widget
    input_str = entry.get()

    # Process the string and update Listbox and Text widget
    for char in input_str:
        listbox.insert(tk.END, f"ch: {char} codepoint: {hex(ord(char))}")
    text_widget.insert('1.0', input_str)

# Create the main window
root = tk.Tk()
root.title("String Viewer")

# Create widgets
entry = ttk.Entry(root, width=50)
entry.grid(row=0, column=0, padx=10, pady=10)

button = ttk.Button(root, text="Show String", command=display_string)
button.grid(row=0, column=1, padx=10, pady=10)

listbox = tk.Listbox(root, width=30, height=10)
listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

text_widget = tk.Text(root, height=5, width=50)
text_widget.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Start the main loop
root.mainloop()
