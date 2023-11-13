import os
import tkinter as tk
from tkinter import filedialog, messagebox

def set_permissions_recursive(path, mode):
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            os.chmod(os.path.join(root, dir), mode)
        for file in files:
            os.chmod(os.path.join(root, file), mode)

def choose_directory():
    directory = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, directory)

def change_permissions():
    directory = directory_entry.get()
    if directory:
        try:
            set_permissions_recursive(directory, 0o777)
            messagebox.showinfo("Success", "Permissions changed successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Warning", "Please choose a directory.")

app = tk.Tk()
app.title("Change Directory Permissions")

directory_entry = tk.Entry(app, width=50)
directory_entry.pack()

choose_button = tk.Button(app, text="Choose Directory", command=choose_directory)
choose_button.pack()

change_button = tk.Button(app, text="Change Permissions to 777", command=change_permissions)
change_button.pack()

app.mainloop()
