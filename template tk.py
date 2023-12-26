import tkinter as tk
from tkinter import filedialog

def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        label.config(text=f"Selected file: {file_path}")

# Create the main root
root = tk.Tk()
root.title("File Dialog Example")

# Button to open file dialog
button = tk.Button(root, text="Open File", command=open_file_dialog)
button.grid(row=3,column=1)

# Label to display the selected file name
label = tk.Label(root, text="Selected file: ")
label.grid(row=1,column=1)

# Start the main event loop
root.mainloop()
