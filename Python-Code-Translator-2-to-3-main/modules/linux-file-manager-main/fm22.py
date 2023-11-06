 import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("File Manager")
root.geometry("800x600")

notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, sticky="nsew")

file_tab = ttk.Frame(notebook)
notebook.add(file_tab, text="Files")

listbox = tk.Listbox(file_tab)
listbox.grid(row=0, column=0, sticky="nsew")

# Set grid weights to make the listbox expand with the window
file_tab.grid_rowconfigure(0, weight=1)
file_tab.grid_columnconfigure(0, weight=1)

text_tab = ttk.Frame(notebook)
notebook.add(text_tab, text="Text")

text_widget = tk.Text(text_tab)
text_widget.grid(row=0, column=0, sticky="nsew")

text_tab.grid_rowconfigure(0, weight=1)
text_tab.grid_columnconfigure(0, weight=1)

image_tab = ttk.Frame(notebook)
notebook.add(image_tab, text="Images")

# Add image display widget using grid

image_tab.grid_rowconfigure(0, weight=1)
image_tab.grid_columnconfigure(0, weight=1)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()

