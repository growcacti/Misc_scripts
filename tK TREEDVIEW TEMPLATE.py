import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

# create root window
root = tk.Tk()
root.title('TreeView Template')
root.geometry('600x400')

# configure the grid layout
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)


# create a treeview
tree = ttk.Treeview(root)
tree.heading('#0', text='PHatom Column', anchor=tk.W)
# adding data
tree.insert('', tk.END, text='1st Column', iid=0, open=False)
tree.insert('', tk.END, text='2nd', iid=1, open=False)
tree.insert('', tk.END, text='3rd', iid=2, open=False)
tree.insert('', tk.END, text='4th', iid=3, open=False)
tree.insert('', tk.END, text='4TH', iid=4, open=False)

# adding children of first node
tree.insert('', tk.END, text='INFO1', iid=5, open=False)
tree.insert('', tk.END, text='JINFO2', iid=6, open=False)
tree.move(5, 0, 0)
tree.move(6, 0, 1)

# place the Treeview widget on the root window
tree.grid(row=0, column=0, sticky=tk.NSEW)

# run the app
root.mainloop()
