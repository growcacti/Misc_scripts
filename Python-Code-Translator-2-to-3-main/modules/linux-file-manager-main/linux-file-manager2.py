import tkinter as tk
from tkinter import Button, Label, Canvas
import os
import subprocess
from functools import partial
import re

class FileManager:
    def __init__(self):
        self.rootWindow = tk.Tk()
        self.rootWindow.wm_geometry("1000x600+100+100")
        self.photo1 = tk.PhotoImage(file="./icons/directory.png").zoom(1).subsample(3)
        self.photo2 = tk.PhotoImage(file="./icons/file.png").zoom(1).subsample(3)
        
        self.frame = None
        self.path = os.getcwd()
        self.searchBar = None
        
        self.initial_setup()

    def initial_setup(self):
        self.myframe = self.createFrame()
        terminalCommand = "ls -l  " + self.path.strip()
        tempFileContent = subprocess.check_output(terminalCommand, shell=True)

        with open("/home/jh/Desktop/tempFile.txt", "w+") as f:
            f.write(tempFileContent)
        
        noOfIcons = int(subprocess.check_output("wc -l < ~/Desktop/tempFile.txt", shell=True)) - 1
        
        buttonObjects = {}
        iconObjects = {}
        iconNames = {}
        
        with open("/home/jh/Desktop/tempFile.txt", "r+") as file:
            all_lines = file.readlines()
            for i in range(1, noOfIcons+1):
                directoryType = all_lines[i]
                iconNames[i] = directoryType[41:]
                directoryType = directoryType[0]
                
                if directoryType == "d":
                    buttonObjects[i] = tk.Button(
                        self.myframe,
                        image=self.photo1,
                        command=partial(self.appendPath, iconNames[i]),
                        width=50,
                        height=50,
                        compound=tk.TOP,
                        bg="white",
                        bd=0,
                    )
                else:
                    buttonObjects[i] = tk.Button(
                        self.myframe,
                        image=self.photo2,
                        command=partial(self.openFile, iconNames[i]),
                        width=50,
                        height=50,
                        compound=tk.TOP,
                        bg="white",
                        bd=0,
                    )
                iconObjects[i] = Label(
                    self.myframe,
                    text=iconNames[i],
                    width=9,
                    height=3,
                    wraplength=70,
                    bg="white"
                )
                
        self.addIcons(self.myframe, buttonObjects, iconObjects, 1)
        self.rootWindow.mainloop()

def createFrame(self):
    self.frame
    if frame:
        frame.destroy()
    frame = tk.Frame(rootWindow, bg="white")
    frame.pack(expand=True, fill="both")
    canvas = tk.Canvas(frame, bg="white")
    myframe = tk.Frame(canvas, bg="white")

    myscrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=myscrollbar.set)
    myscrollbar.pack(side="right", fill="y")
    canvas.pack(expand=True, fill="both")

    canvas.create_window((0, 0), window=myframe, anchor="nw", height=700, width=1100)
    myframe.bind("<Configure>", myfunction)
    return myframedef createFrame():
    global frame
    if frame:
        frame.destroy()
    frame = tk.Frame(rootWindow, bg="white")
    frame.pack(expand=True, fill="both")
    canvas = tk.Canvas(frame, bg="white")
    myframe = tk.Frame(canvas, bg="white")

    myscrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=myscrollbar.set)
    myscrollbar.pack(side="right", fill="y")
    canvas.pack(expand=True, fill="both")

    canvas.create_window((0, 0), window=myframe, anchor="nw", height=700, width=1100)
    myframe.bind("<Configure>", myfunction)
    return myframe

if __name__ == '__main__':
    app = FileManager()
