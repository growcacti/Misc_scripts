import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_graph():
    try:
        # Get user input
        func = entry_function.get()
        x_min = float(entry_xmin.get())
        x_max = float(entry_xmax.get())

        # Generate X values
        x = np.linspace(x_min, x_max, 400)
        y = eval(func)

        # Clear the previous plot
        ax.clear()
        ax.plot(x, y)
        canvas.draw()
    except Exception as e:
        print("Error: ", e)

# Create the main window
root = tk.Tk()
root.title("Graphing Calculator")

# Create and place widgets
label_function = tk.Label(root, text="Function f(x):")
label_function.pack()

entry_function = tk.Entry(root)
entry_function.pack()

label_xmin = tk.Label(root, text="x min:")
label_xmin.pack()

entry_xmin = tk.Entry(root)
entry_xmin.pack()

label_xmax = tk.Label(root, text="x max:")
label_xmax.pack()

entry_xmax = tk.Entry(root)
entry_xmax.pack()

button_plot = tk.Button(root, text="Plot", command=plot_graph)
button_plot.pack()

# Setting up Matplotlib
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
widget = canvas.get_tk_widget()
widget.pack()

# Run the application
root.mainloop()
