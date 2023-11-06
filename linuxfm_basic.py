import os
import subprocess
import tkinter as tk
from functools import partial
import re  # since re is used but wasn't imported

class FileManager:
    
    def __init__(self, rootWindow):
        self.rootWindow = rootWindow
##        self.photo1 = tk.PhotoImage(file="./icons/directory.png").zoom(1).subsample(3)
##        self.photo2 = tk.PhotoImage(file="./icons/file.png").zoom(1).subsample(3)
        self.searchBar = None
        self.frame = None
        self.path = os.getcwd()
        self.initialize_window()

    def initialize_window(self):
        sizex = 1000
        sizey = 600
        posx = 100
        posy = 100
        self.rootWindow.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

    # ... Rest of your functions, converted to class methods ...

    def createFrame(self):
        pass
        # ... contents of createFrame ...

    def addIcons(self, myframe, buttonObjects, iconObjects, back):
        pass
        # ... contents of addIcons ...

    # ... and so on for all other methods ...

# Usage:
rootWindow = tk.Tk()
app = FileManager(rootWindow)
rootWindow.mainloop()
