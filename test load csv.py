import tkinter as tk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import csv

x = []
y = []
def getfile():
    filename = askopenfilename(filetypes=[("Comma Separated Values", "*.csv")])
    with open(filename, 'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines:
            x.append(row[0])
            y.append(float(row[1]))  # Convert the string to a float

    plt.plot(x, y, color='g', linestyle='dashed',
             marker='o', label=" Data")

    plt.xticks(rotation=25)
    plt.xlabel('Data')
    plt.ylabel('data')
    plt.title('data', fontsize=20)
    plt.grid()
    plt.legend()
    plt.show()



# Create a tkinter window and button to trigger the file dialog
root = tk.Tk()
root.title("CSV Data Plotter")
button = tk.Button(root, text="Open CSV File", command=getfile)
button.pack()

root.mainloop()
