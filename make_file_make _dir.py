import os
from tkinter import Tk, Label, Entry, Button, Text, END

def create_resources():
    # Clear the feedback text area at the start of the operation
    feedback_text.delete('1.0', END)
    
    filenames = file_entry.get().split(',')
    dirnames = dir_entry.get().split(',')

    for name in filenames:
        if name.strip():  # Ensure the name is not empty
            try:
                with open(name.strip(), 'w') as f:
                    pass  # Just create the file if it doesn't exist
                feedback_text.insert(END, f"File created: {name.strip()}\n")
            except Exception as e:
                feedback_text.insert(END, f"Failed to create file {name.strip()}: {e}\n")

    for name in dirnames:
        if name.strip():  # Ensure the name is not empty
            try:
                os.makedirs(name.strip(), exist_ok=True)
                feedback_text.insert(END, f"Directory created: {name.strip()}\n")
            except Exception as e:
                feedback_text.insert(END, f"Failed to create directory {name.strip()}: {e}\n")

# Set up the GUI
root = Tk()
root.title("File and Directory Creator")

Label(root, text="Enter file names (comma separated):").grid(row=0, column=0, sticky="w")
file_entry = Entry(root, width=50)
file_entry.grid(row=0, column=1)

Label(root, text="Enter directory names (comma separated):").grid(row=1, column=0, sticky="w")
dir_entry = Entry(root, width=50)
dir_entry.grid(row=1, column=1)

Button(root, text="Create", command=create_resources).grid(row=2, column=0, columnspan=2)

feedback_text = Text(root, height=10, width=50)
feedback_text.grid(row=3, column=0, columnspan=2, sticky="nsew")

# Adjust row and column configurations for better layout
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
