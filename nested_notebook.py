import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.geometry('400x300')

# Create the outer notebook
outer_notebook = ttk.Notebook(root)
outer_notebook.pack(expand=True, fill='both')

# Create a frame for the first tab of the outer notebook
outer_tab1 = ttk.Frame(outer_notebook)
outer_notebook.add(outer_tab1, text='Outer Tab 1')

# Create the inner notebook inside the first tab of the outer notebook
inner_notebook = ttk.Notebook(outer_tab1)
inner_notebook.pack(expand=True, fill='both')

# Create frames for the tabs of the inner notebook
inner_tab1 = ttk.Frame(inner_notebook)
inner_tab2 = ttk.Frame(inner_notebook)

# Add tabs to the inner notebook
inner_notebook.add(inner_tab1, text='Inner Tab 1')
inner_notebook.add(inner_tab2, text='Inner Tab 2')

root.mainloop()
