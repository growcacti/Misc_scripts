import tkinter as tk
from tkinter import messagebox

def wheatstone_solver(resistance_1: float, resistance_2: float, resistance_3: float) -> float:
    if resistance_1 <= 0 or resistance_2 <= 0 or resistance_3 <= 0:
        raise ValueError("All resistance values must be positive")
    else:
        return float((resistance_2 / resistance_1) * resistance_3)

def calculate_resistance():
    try:
        r1 = float(entry_r1.get())
        r2 = float(entry_r2.get())
        r3 = float(entry_r3.get())
        result = wheatstone_solver(r1, r2, r3)
        label_result.config(text=f"Unknown Resistance Rx: {result:.2f} Ω")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Wheatstone Bridge Solver")

# Create and place the labels and entry widgets for resistances
tk.Label(root, text="Resistance R1 (Ω):").grid(row=0, column=0, padx=10, pady=5)
entry_r1 = tk.Entry(root)
entry_r1.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Resistance R2 (Ω):").grid(row=1, column=0, padx=10, pady=5)
entry_r2 = tk.Entry(root)
entry_r2.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Resistance R3 (Ω):").grid(row=2, column=0, padx=10, pady=5)
entry_r3 = tk.Entry(root)
entry_r3.grid(row=2, column=1, padx=10, pady=5)

# Create and place the Calculate button
button_calculate = tk.Button(root, text="Calculate", command=calculate_resistance)
button_calculate.grid(row=3, column=0, columnspan=2, pady=10)

# Create and place the result label
label_result = tk.Label(root, text="Unknown Resistance Rx: ")
label_result.grid(row=4, column=0, columnspan=2, pady=5)

# Run the main loop
root.mainloop()
