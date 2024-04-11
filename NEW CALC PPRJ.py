import tkinter as tk
from tkinter import simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class ScientificCalculatorGrapher:
    def __init__(self, master):
        self.master = master
        self.master.title("Scientific Calculator and Grapher")
        self.hex_dict= {'A' : 10, 'B' : 11, 'C' : 12, 'D' : 13, 'E' : 14, 'F' : 15}
        # Calculator display
        self.display = tk.Entry(self.master,bd=8,bg="seashell3", width=25)
        self.display.grid(row=0, column=0, columnspan=3)
        self.display2 = tk.Entry(self.master,bd=8,bg="seashell3", width=25)
        self.display2.grid(row=0, column=5, columnspan=2)
        self.memfunct= None
        # Initialize buttons
        self.initialize_buttons()

    def initialize_buttons(self):
        # Numeric buttons
        self.button_1 = tk.Button(self.master, text="1", command=lambda: self.button_click(1))
        self.button_2 = tk.Button(self.master, text="2", command=lambda: self.button_click(2))
        self.button_3 = tk.Button(self.master, text="3", command=lambda: self.button_click(3))
        self.button_4 = tk.Button(self.master, text="4", command=lambda: self.button_click(4))
        self.button_5 = tk.Button(self.master, text="5", command=lambda: self.button_click(5))
        self.button_6 = tk.Button(self.master, text="6", command=lambda: self.button_click(6))
        self.button_7 = tk.Button(self.master, text="7", command=lambda: self.button_click(7))
        self.button_8 = tk.Button(self.master, text="8", command=lambda: self.button_click(8))
        self.button_9 = tk.Button(self.master, text="9", command=lambda: self.button_click(9))
        self.button_10 = tk.Button(self.master, text="10", command=lambda: self.button_click())
        self.button_A= tk.Button(self.master, text="A", command=lambda: self.button_hex(A))
        self.button_B = tk.Button(self.master, text="B", command=lambda: self.button_hex(B))
        self.button_C = tk.Button(self.master, text="C", command=lambda: self.button_hex(C))
        self.button_D = tk.Button(self.master, text="D", command=lambda: self.button_hex(D))
        self.button_E = tk.Button(self.master, text="E", command=lambda: self.button_hex(E))
        self.button_F = tk.Button(self.master, text="F", command=lambda: self.button_hex(F))
        self.button_1.grid(row=3, column=1)
        self.button_2.grid(row=3, column=2,sticky="w")
        self.button_3.grid(row=3, column=3,sticky="w")
        self.button_4.grid(row=4, column=1)
        self.button_5.grid(row=4, column=2,sticky="w")
        self.button_6.grid(row=4, column=3,sticky="w")
        self.button_7.grid(row=5, column=1)
        self.button_8.grid(row=5, column=2,sticky="w")
        self.button_9.grid(row=5, column=3,sticky="w")
        self.button_10.grid(row=6, column=1)
        self.button_A.grid(row=6, column=2,sticky="w")
        self.button_B.grid(row=6, column=3,sticky="w")
        self.button_C.grid(row=7, column=1)
        self.button_D.grid(row=7, column=2,sticky="w")
        self.button_E.grid(row=7, column=3,sticky="w")
        self.button_F.grid(row=8, column=1)

        self.button_add = tk.Button(self.master, text="+", command=lambda: self.button_click('+'))
        self.button_subtract = tk.Button(self.master, text="-", command=lambda: self.button_click('-'))
        self.button_multiply = tk.Button(self.master, text="*", command=lambda: self.button_click('*'))
        self.button_divide = tk.Button(self.master, text="/", command=lambda: self.button_click('/'))
        self.button_power = tk.Button(self.master, text="**", command=lambda: self.button_click('**'))

        # Place operation buttons on the grid
        self.button_add.grid(row=2, column=6)
        self.button_subtract.grid(row=3, column=6)
        self.button_multiply.grid(row=4, column=6)
        self.button_divide.grid(row=5, column=6)
        self.button_power.grid(row=6, column=6)


        # Function buttons
        tk.Button(self.master, text="sin", command=lambda: self.button_click("np.sin(")).grid(row=1, column=9)
        # Define more function buttons...

        # Equal button
        tk.Button(self.master, text="=", command=self.button_equal).grid(row=5, column=9, columnspan=2)

        # Clear button
        tk.Button(self.master, text="Clear", command=self.button_clear).grid(row=4, column=7, columnspan=2)

        # Graph button
        tk.Button(self.master, text="Graph Function", command=self.plot_function).grid(row=6, column=8)

    def button_click(self, value):
        current = self.display.get()
        self.display.delete(0, tk.END)
        self.display.insert(0, str(current) + str(value))

    def button_clear(self):
        self.display.delete(0, tk.END)

    def button_equal(self):
        try:
            result = str(eval(self.display.get()))  # Needs refinement for complex calculations
            self.display.delete(0, tk.END)
            self.display.insert(0, result)
        except:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")
          
    def button_hex(self, hex_digit):
        """Appends the pressed hexadecimal digit or operation to the current input."""
        self.current_input += str(hex_digit)
        self.display_var.set(self.current_input)

    def evaluate_expression(self):
        """Evaluates the current input as a hexadecimal operation."""
       
        try:
            # Evaluate the expression within the context of hexadecimal operations
            result = eval(self.current_input, {}, {"__builtins__": None})
            self.display_var.set(result)
            self.current_input = str(result)
        except Exception as e:
            self.display_var.set("Error")
            self.current_input = ""
    def preprocess_input(self, input_str):
        """
        Preprocesses the calculator input to handle hexadecimal numbers correctly.
        
        Args:
        input_str (str): The raw input string from the calculator interface.
        
        Returns:
        str: A preprocessed input string with hexadecimal numbers converted to decimal.
        """
        # Example pattern: Detecting 'hex' followed by A-F or 0-9 digits, indicating a hexadecimal number.
        hex_pattern = re.compile(r'hex([A-Fa-f0-9]+)')
        
        # Function to convert found hexadecimal patterns to decimal
        def hex_to_dec(match):
            hex_number = match.group(1)  # Extract the hexadecimal part
            return str(int(hex_number, 16))  # Convert to decimal and return as string
        
        # Replace all hexadecimal patterns in the input with their decimal equivalents
        processed_input = hex_pattern.sub(hex_to_dec, input_str)
        
        # Further processing for other operations, e.g., replacing '^' with '**' for exponentiation
        processed_input = processed_input.replace('^', '**')
        
        return processed_input
    def mem(self):
        self.memfunct = self.display.get()
        self.display2.delete(0, tk.END)
        self.display2.insert(0, self.memfunct)
        self.display1.delete(0, tk.END)
        return self.memfunct                     
                             
    def plot_function(self):
        function_input = simpledialog.askstring("Input", "Enter a function of x (e.g., np.sin(x), x**2):")
        range_input = simpledialog.askstring("Input", "Enter the range (e.g., -10:10):")
        range_start, range_end = map(int, range_input.split(':'))
        x = np.linspace(range_start, range_end, 400)
        y = eval(function_input, {"__builtins__": None}, {"np": np, "x": x})

        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set(title=function_input)

        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=7, column=0, columnspan=4)
        canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculatorGrapher(root)
    root.mainloop()
