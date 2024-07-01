import tkinter as tk
from tkinter import messagebox

def resistor_parallel(resistors: list[float]) -> float:
    first_sum = 0.00
    for index, resistor in enumerate(resistors):
        if resistor <= 0:
            msg = f"Resistor at index {index} has a negative or zero value!"
            raise ValueError(msg)
        first_sum += 1 / float(resistor)
    return 1 / first_sum

def resistor_series(resistors: list[float]) -> float:
    sum_r = 0.00
    for index, resistor in enumerate(resistors):
        if resistor < 0:
            msg = f"Resistor at index {index} has a negative value!"
            raise ValueError(msg)
        sum_r += resistor
    return sum_r

def calculate_parallel():
    try:
        resistances = list(map(float, entry_resistors.get().split(',')))
        result = resistor_parallel(resistances)
        label_result_parallel.config(text=f"Equivalent Parallel Resistance: {result:.2f} Ω")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def calculate_series():
    try:
        resistances = list(map(float, entry_resistors.get().split(',')))
        result = resistor_series(resistances)
        label_result_series.config(text=f"Equivalent Series Resistance: {result:.2f} Ω")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Resistor Network Solver")

# Create and place the label and entry widget for resistances
tk.Label(root, text="Resistances (comma-separated values, Ω):").grid(row=0, column=0, padx=10, pady=5)
entry_resistors = tk.Entry(root, width=30)
entry_resistors.grid(row=0, column=1, padx=10, pady=5)

# Create and place the Calculate buttons
button_calculate_parallel = tk.Button(root, text="Calculate Parallel", command=calculate_parallel)
button_calculate_parallel.grid(row=1, column=0, columnspan=2, pady=10)

button_calculate_series = tk.Button(root, text="Calculate Series", command=calculate_series)
button_calculate_series.grid(row=2, column=0, columnspan=2, pady=10)

# Create and place the result labels
label_result_parallel = tk.Label(root, text="Equivalent Parallel Resistance: ")
label_result_parallel.grid(row=3, column=0, columnspan=2, pady=5)

label_result_series = tk.Label(root, text="Equivalent Series Resistance: ")
label_result_series.grid(row=4, column=0, columnspan=2, pady=5)

# Run the main loop
root.mainloop()
