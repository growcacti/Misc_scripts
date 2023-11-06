import tkinter as tk
from tkinter import Canvas, Frame,Scrollbar
import PIL

import os
import subprocess
from tkinter import *
from functools import partial

rootWindow = tk.Tk()

sizex = 1000
sizey = 600
posx = 100
posy = 100

rootWindow.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

photo1 = PhotoImage(file="./icons/directory.png")  # Pic of directory
photo1 = photo1.zoom(1)
photo1 = photo1.subsample(3)

photo2 = PhotoImage(file="./icons/file.png")  # Pic of file
photo2 = photo2.zoom(1)
photo2 = photo2.subsample(3)


global searchBar
global frame
frame = None
global path
path = os.getcwd()


def createFrame():
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


def addIcons(myframe, buttonObjects, iconObjects, back):
    global searchBar
    global path
    # global iconNames

    if path != "/home/jh" or back:
        back = Button(
            frame, text="BACK", command=partial(reverseBack, "none"), width=7, height=3
        )
        back.place(x=10, y=10)
    else:
        searchBar = tk.Text(frame, height=1)
        sb = tk.Button(
            frame, height=1, width=10, text="Read", command=partial(search, "none")
        )
        searchBar.place(x=200, y=20)
        sb.place(x=850, y=20)

    i = 1
    X = 1
    Y = 1
    c = 12
    myframe.grid_rowconfigure(0, minsize=100)
    myframe.grid_columnconfigure(0, minsize=100)
    while i <= int(noOfIcons):
        buttonObjects[i].grid(row=Y, column=X)
        yl = Y + 1
        xl = X
        iconObjects[i].grid(row=yl, column=xl)
        X += 1
        i += 1
        if i > c:
            Y += 2
            c += 12
            X = 1


def openFileFromSearch(loc, dire):
    fil_op = "gedit " + loc.strip() + "/" + dire.strip()
    os.system(fil_op)


def openFile(name_add):
    fil_op = "gedit " + path.strip() + "/" + name_add.strip() + " &"
    os.system(fil_op)


def myfunction(event):
    canvas.configure(
        scrollregion=canvas.bbox("all"),
        height=canvas.winfo_height(),
        width=canvas.winfo_width(),
    )


def openDirectory(loc, dire):
    print("openDirectory")
    global path
    path = path.strip() + "/" + dire.strip()

    myframe = createFrame()
    terminalCommand = "ls -l  " + path.strip()

    # getting files to display
    tempFileContent = subprocess.check_output(terminalCommand, shell=True)

    # writing the list of files in a temp txt file
    f = open("/home/jh/Desktop/tempFile.txt", "w+")
    f.write(tempFileContent)
    f.close()

    # Getting no of files or directories to display from txt file
    noOfIcons = subprocess.check_output("wc -l < ~/Desktop/tempFile.txt", shell=True)

    noOfIcons = int(noOfIcons) - 1

    buttonObjects = {}
    iconObjects = {}
    iconNames = {}
    i = 1

    # assigning data and functions to tkinter buttons to display
    while i <= noOfIcons:
        file = open("/home/jh/Desktop/tempFile.txt", "r+")
        all_lines = file.readlines()
        directoryType = all_lines[i]

        iconNames[i] = directoryType.rsplit(None, 1)[-1]
        directoryType = directoryType[0]
        resNum = i
        if directoryType == "d":
            buttonObjects[i] = tk.Button(
                myframe,
                image=photo1,
                command=partial(appendPath, iconNames[i]),
                width=50,
                height=50,
                compound=TOP,
                bg="white",
                bd=0,
            )
            iconObjects[i] = Label(
                myframe, text=iconNames[i], width=9, height=3, wraplength=70, bg="white"
            )

        elif directoryType == "-":
            buttonObjects[i] = tk.Button(
                myframe,
                image=photo2,
                command=partial(openFile, iconNames[i]),
                width=50,
                height=50,
                compound=TOP,
                bg="white",
                bd=0,
            )
            iconObjects[i] = Label(
                myframe, text=iconNames[i], width=9, height=3, wraplength=70, bg="white"
            )

        i += 1
    # passing the required data to construct the display screen
    addIcons(myframe, buttonObjects, iconObjects, 1)


def search(none):
    global searchBar
    global path

    searchString = searchBar.get("1.0", "end-1c")

    myframe = createFrame()

    # getting files to display
    tempFileContent = subprocess.check_output("ls -l -R /home/jh", shell=True)

    # writing the list of files in a temp txt file
    f = open("/home/jh/Desktop/tempFile.txt", "w+")
    f.write(tempFileContent)
    f.close()
    i = 1
    # assigning data and functions to tkinter buttons to display

    with open("/home/jh/Desktop/tempFile.txt", "r") as f:
        for line in f:
            if "/" in line:
                loc = line
                loc = loc.strip()
                loc = loc.strip(":")

            elif searchString in line:
                iconNames[i] = line.rsplit(" ", 1)[-1]
                directoryType = line[0]
                resNum = i

                if directoryType == "d":
                    buttonObjects[i] = tk.Button(
                        myframe,
                        image=photo1,
                        command=partial(openDirectory, loc, iconNames[i]),
                        width=50,
                        height=50,
                        compound=TOP,
                        bg="white",
                        bd=0,
                    )
                    iconObjects[i] = Label(
                        myframe,
                        text=iconNames[i],
                        width=9,
                        height=3,
                        wraplength=70,
                        bg="white",
                    )

                elif directoryType == "-":
                    buttonObjects[i] = tk.Button(
                        myframe,
                        image=photo2,
                        command=partial(openFileFromSearch, loc, iconNames[i]),
                        width=50,
                        height=50,
                        compound=TOP,
                        bg="white",
                        bd=0,
                    )
                    iconObjects[i] = Label(
                        myframe,
                        text=iconNames[i],
                        width=9,
                        height=3,
                        wraplength=70,
                        bg="white",
                    )
                i += 1

    path = "/home/jh"
    # passing the required data to construct the display screen
    addIcons(myframe, buttonObjects, iconObjects, 1)


def reverseBack(name_del):
    global searchBar
    global path

    myframe = createFrame()

    if path == "/home/jh":
        path = "/home/jh"
    else:
        p = path.rsplit("/")[-1]
        path = re.sub(p, "", path)
        path = path.rstrip("/")

    terminalCommand = "ls -l  " + path.strip()

    # getting files to display
    tempFileContent = subprocess.check_output(terminalCommand, shell=True)

    # writing the list of files in a temp txt file
    f = open("/home/jh/Desktop/tempFile.txt", "w+")
    f.write(tempFileContent)
    f.close()

    noOfIcons = subprocess.check_output("wc -l < ~/Desktop/tempFile.txt", shell=True)

    # Getting no of files or directories to display from txt file
    noOfIcons = int(noOfIcons) - 1

    buttonObjects = {}
    iconObjects = {}
    iconNames = {}
    i = 1

    # assigning data and functions to tkinter buttons to display
    while i <= noOfIcons:
        file = open("/home/jh/Desktop/tempFile.txt", "r+")
        all_lines = file.readlines()
        directoryType = all_lines[i]
        iconNames[i] = directoryType.rsplit(None, 1)[-1]
        directoryType = directoryType[0]

        if directoryType == "d":
            buttonObjects[i] = tk.Button(
                myframe,
                image=photo1,
                command=partial(appendPath, iconNames[i]),
                width=50,
                height=50,
                compound=TOP,
                bg="white",
                bd=0,
            )
            iconObjects[i] = Label(
                myframe, text=iconNames[i], width=9, height=3, wraplength=70, bg="white"
            )

        else:
            buttonObjects[i] = tk.Button(
                myframe,
                image=photo2,
                command=partial(openFile, iconNames[i]),
                width=50,
                height=50,
                compound=TOP,
                bg="white",
                bd=0,
            )
            iconObjects[i] = Label(
                myframe, text=iconNames[i], width=9, height=3, wraplength=70, bg="white"
            )

        i += 1
    # passing the required data to construct the display screen
    addIcons(myframe, buttonObjects, iconObjects, 0)


def appendPath(name_add):
    global path

    path = path.strip() + "/" + name_add.strip()

    myframe = createFrame()

    terminalCommand = "ls -l  " + path.strip()

    # getting files to display
    tempFileContent = subprocess.check_output(terminalCommand, shell=True)

    # writing the list of files in a temp txt file
    f = open("/home/jh/Desktop/tempFile.txt", "w+")
    f.write(tempFileContent)
    f.close()

    # Getting no of files or directories to display from txt file
    noOfIcons = subprocess.check_output("wc -l < ~/Desktop/tempFile.txt", shell=True)

    noOfIcons = int(noOfIcons) - 1

    buttonObjects = {}
    iconObjects = {}
    iconNames = {}
    i = 1

    while i <= noOfIcons:
        file = open("/home/jh/Desktop/tempFile.txt", "r+")
        all_lines = file.readlines()
        directoryType = all_lines[i]

        iconNames[i] = directoryType.rsplit(None, 1)[-1]
        directoryType = directoryType[0]

        if directoryType == "d":
            buttonObjects[i] = tk.Button(
                myframe,
                image=photo1,
                command=partial(appendPath, iconNames[i]),
                width=50,
                height=50,
                compound=TOP,
                bg="white",
                bd=0,
            )
            iconObjects[i] = Label(
                myframe, text=iconNames[i], width=9, height=3, wraplength=70, bg="white"
            )

        elif directoryType == "-":
            buttonObjects[i] = tk.Button(
                myframe,
                image=photo2,
                command=partial(openFile, iconNames[i]),
                width=50,
                height=50,
                compound=TOP,
                bg="white",
                bd=0,
            )
            iconObjects[i] = Label(
                myframe, text=iconNames[i], width=9, height=3, wraplength=70, bg="white"
            )

        i += 1

    # passing the required data to construct the display screen
    addIcons(myframe, buttonObjects, iconObjects, 1)


myframe = createFrame()
terminalCommand = "ls -l  " + path.strip()
# getting files to display
tempFileContent = subprocess.check_output(terminalCommand, shell=True)

# writing the list of files in a temp txt file
f = open("/home/jh/Desktop/tempFile.txt", "w+")
f.write(tempFileContent)
f.close()

# Getting no of files or directories to display from txt file
noOfIcons = subprocess.check_output(
    "wc -l < ~/Desktop/tempFile.txt", shell=True
)  # Getting the no of files to display


noOfIcons = int(noOfIcons) - 1
buttonObjects = {}
iconObjects = {}
iconNames = {}
i = 1

# assigning data and functions to tkinter buttons to display
while i <= noOfIcons:
    file = open("/home/jh/Desktop/tempFile.txt", "r+")
    all_lines = file.readlines()
    directoryType = all_lines[i]
    iconNames[i] = directoryType[41:]
    directoryType = directoryType[0]

    if directoryType == "d":
        buttonObjects[i] = tk.Button(
            myframe,
            image=photo1,
            command=partial(appendPath, iconNames[i]),
            width=50,
            height=50,
            compound=TOP,
            bg="white",
            bd=0,
        )
        iconObjects[i] = Label(
            myframe, text=iconNames[i], width=9, height=3, wraplength=70, bg="white"
        )

    else:
        buttonObjects[i] = tk.Button(
            myframe,
            image=photo2,
            command=partial(openFile, iconNames[i]),
            width=50,
            height=50,
            compound=TOP,
            bg="white",
            bd=0,
        )
        iconObjects[i] = Label(
            myframe, text=iconNames[i], width=8, height=3, wraplength=70, bg="white"
        )

    i += 1

# passing the required data to construct the display screen
addIcons(myframe, buttonObjects, iconObjects, 0)

rootWindow.mainloop()
