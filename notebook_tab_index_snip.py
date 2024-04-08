import tkinter as tk
from tkinter import ttk
from tkinter import Menu

def on_tab_changed(event):
    # Determine the index of the current tab
    current_tab_index = notebook.index(notebook.select())
    # Fetch the menu associated with the current tab from the dictionary
    current_menu = tab_menus.get(current_tab_index, default_menu)
    # Update the application's menu based on the selected tab
    root.config(menu=current_menu)

# Initialize the main window
root = tk.Tk()
root.title("Tab-Dependent Menus Example")

# Create a notebook widget
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Create sample tabs
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
notebook.add(tab1, text='Tab 1')
notebook.add(tab2, text='Tab 2')

# Create menus for each tab
menu_for_tab1 = Menu(root)
menu_for_tab1.add_command(label="Tab 1 Action", command=lambda: print("Tab 1 Action"))

menu_for_tab2 = Menu(root)
menu_for_tab2.add_command(label="Tab 2 Action", command=lambda: print("Tab 2 Action"))

default_menu = Menu(root)  # A default menu if needed

# Dictionary to associate tabs with their corresponding menus
tab_menus = {
    0: menu_for_tab1,  # Index 0 for Tab 1
    1: menu_for_tab2,  # Index 1 for Tab 2
}

# Bind the tab changed event to the on_tab_changed function
notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

root.mainloop()
