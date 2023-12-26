import os
import tkinter as tk
from tkinter import simpledialog

def create_directories():
    base_dir_name = simpledialog.askstring("Input", "Enter base directory name:",
                                   parent=root)
    num_dirs = simpledialog.askinteger("Input", "How many directories?",
                                       parent=root)
    
    if base_dir_name and num_dirs:
        for i in range(num_dirs):
            dir_name = f"{base_dir_name}{i+1}"
            try:
                os.makedirs(dir_name)
                print(f"Directory created: {dir_name}")
            except FileExistsError:
                print(f"Directory already exists: {dir_name}")
            except OSError as e:
                print(f"Error: {e}")

root = tk.Tk()
root.geometry("300x200")

create_button = tk.Button(root, text="Create Directories", command=create_directories)
create_button.grid(row=1,column=2)

root.mainloop()
