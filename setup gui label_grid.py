import tkinter as tk
from tkinter import ttk
root = Tk()
   
tk.Label(text="row 0 col 0 ", width=15).grid(row=0, column=0)
tk.Label(text="row0 col1  ", width=15).grid(row=0, column=1)
tk.Label(text=" col2     ", width=30).grid(row=0, column=2)
tk.Label(text=" col3    ", width=30).grid(row=0, column=3)
tk.Label(text=" col4      ", width=30).grid(row=0, column=4)
tk.Label(text=" col5      ", width=30).grid(row=0, column=5)
tk.Label(text="row 0 col 0 ", width=15).grid(row=1, column=0)
tk.Label(text="row0 col1  ", width=15).grid(row=2, column=1)
tk.Label(text=" row 3col2     ", width=30).grid(row=3, column=2)
tk.Label(text=" row4 col3    ", width=30).grid(row=4, column=3)
tk.Label(text=" row 5 col4     ", width=30).grid(row=5, column=4)
tk.Label(text=" row8 col5      ", width=30).grid(row=8, column=5)































root.mainloop()
