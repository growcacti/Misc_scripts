import tkinter as tk
from tkinter import filedialog
import os

def open_file_dialog():
    path = filedialog.askopenfilename(initialdir=get_selected_path())
    if path:
        listbox_paths.insert(tk.END, path)

def open_directory_dialog():
    path = filedialog.askdirectory(initialdir=get_selected_path())
    if path:
        listbox_paths.insert(tk.END, path)

def get_selected_path():
    selection = listbox_paths.curselection()
    if selection:
        return listbox_paths.get(selection[0])
    return "/"

def change_directory():
    path = get_selected_path()
    if path and os.path.isdir(path):
        os.chdir(path)
        path_display.insert(0, path)
        print(f"Current working directory changed to: {path}")

def save_paths():
    with open("paths.txt", "w") as file:
        for path in listbox_paths.get(0, tk.END):
            file.write(path + "\n")

def load_paths():
    try:
        with open("paths.txt", "r") as file:
            for path in file:
                listbox_paths.insert(tk.END, path.strip())
    except FileNotFoundError:
        pass

def update_path_display():
    path_display.delete(0, tk.END)
    current = os.getcwd()
    path_display.insert(0, current)
   

def copy_to_clipboard():
    root.clipboard_clear()
    current = os.getcwd()
    root.clipboard_append(current)

# Create the main window
root = tk.Tk()
root.title("File and Directory Dialog Example")

# Create widgets
btn_open_file = tk.Button(root, text="Open File", command=open_file_dialog)
btn_open_directory = tk.Button(root, text="Open Directory", command=open_directory_dialog)
btn_change_dir = tk.Button(root, text="Change Directory", command=change_directory)
btn_save = tk.Button(root, text="Save Paths", command=save_paths)
listbox_paths = tk.Listbox(root, width=50, height=10)
tk.Label(root, text="System Current Directory").grid(row=9, column=0)
path_display = tk.Entry(root, width=50)
btn_copy = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
btn_update = tk.Button(root, text="Update Path", command=update_path_display)



# Place widgets using grid
btn_open_file.grid(row=0, column=0, padx=10, pady=10)
btn_open_directory.grid(row=0, column=1, padx=10, pady=10)
btn_change_dir.grid(row=0, column=2, padx=10, pady=10)
listbox_paths.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
btn_save.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
path_display.grid(row=10, column=0, columnspan=2, padx=10, pady=10)
btn_copy.grid(row=12, column=0, columnspan=2, padx=10, pady=10)
btn_update.grid(row=13,column=0)
# Load the saved paths, if any
load_paths()

# Run the application
root.mainloop()
