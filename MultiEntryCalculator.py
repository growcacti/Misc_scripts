import tkinter as tk
import math
from functools import reduce

class MultiEntryCalculator:
    def __init__(self, parent):
        self.parent = parent
        # Number of values input
        self.num_entry = tk.Entry(self.parent, bd=6, bg='cornsilk')
        self.num_entry.grid(row=0, column=1)
        self.update_btn = tk.Button(self.parent, text='Update Number of Values and/or Clear', command=self.update_value_entries)
        self.update_btn.grid(row=0, column=2)
        self.entry_list = []
        tk.Label(self.parent, text='Number of Values').grid(row=0, column=0)

        b1 = tk.Button(self.parent, text='Calculate SUM & AVG', command=self.do_sum_avg_math)
        b1.grid(row=22, column=3)
        b2 = tk.Button(self.parent, text='Clear', command=self.clear)
        b2.grid(row=30, column=3)

        # Listbox
        self.lb7 = tk.Listbox(self.parent, bd=9, bg='alice blue', width=25, height=5)
        self.lb7.grid(row=12, column=3, rowspan=5)
        b3 = tk.Button(self.parent, text='Calculate Product', command=self.do_multiply)
        b3.grid(row=25, column=5)

    def update_value_entries(self):
        try:
            self.clear_values()  # Clear existing entries

            self.num_values = int(self.num_entry.get())

            self.num_entries = [tk.Entry(self.parent, bd=6, bg='azure') for _ in range(self.num_values)]
            for i, entry in enumerate(self.num_entries):
                entry.grid(row=i+1, column=1)
                self.entry_list.append(entry)
        except ValueError:
            print('Please enter a valid number of values.')

    def clear_values(self):
        # Destroy or hide existing value entries
        for entry in getattr(self, 'num_entries', []):
            entry.grid_forget()
        self.entry_list.clear()

    def do_sum_avg_math(self):
        try:
            values = [float(entry.get()) for entry in self.entry_list if entry.get()]
            if values:
                total_value_of = sum(values)
                avg = total_value_of / len(values)
                variance = sum((x - avg) ** 2 for x in values) / len(values)
                standard_deviation = math.sqrt(variance)

                # Update the listbox with results
                self.lb7.insert(tk.END, "Total Value:")
                self.lb7.insert(tk.END, total_value_of)
                self.lb7.insert(tk.END, 'Average:')
                self.lb7.insert(tk.END, avg)
                self.lb7.insert(tk.END, "Variance:")
                self.lb7.insert(tk.END, variance)
                self.lb7.insert(tk.END, 'Standard Deviation:')
                self.lb7.insert(tk.END, standard_deviation)
            else:
                print("No values entered.")
        except ValueError:
            print('Invalid input! Please enter only numbers.')
        except Exception as ex:
            print(ex)

    def power_of_num(self):
        try:
            top = tk.Toplevel()
            tk.Label(top, text="Enter the power to raise each number to:").grid(row=0, column=1)
            power_of_entry = tk.Entry(top, bd=5)
            power_of_entry.grid(row=1, column=1)

            def calculate_power():
                try:
                    power = float(power_of_entry.get())
                    values = [float(entry.get()) for entry in self.entry_list if entry.get()]
                    results = [x ** power for x in values]
                    self.lb7.delete(0, tk.END)
                    self.lb7.insert(tk.END, "Powers:")
                    for result in results:
                        self.lb7.insert(tk.END, result)
                except ValueError:
                    print("Invalid input! Please enter valid numbers.")

            calc_btn = tk.Button(top, text="Calculate", command=calculate_power)
            calc_btn.grid(row=2, column=1)

        except Exception as ex:
            print(ex)

    def do_multiply(self):
        try:
            values = [float(entry.get()) for entry in self.entry_list if entry.get()]
            if values:
                product = reduce(lambda x, y: x * y, values)
                self.lb7.delete(0, tk.END)
                self.lb7.insert(tk.END, "Product:")
                self.lb7.insert(tk.END, product)
            else:
                print("No values entered.")
        except ValueError:
            print('Invalid input! Please enter only numbers.')
        except Exception as ex:
            print(ex)

    def clear(self):
        self.lb7.delete(0, tk.END)

if __name__ == '__main__':
    root = tk.Tk()
    mec = MultiEntryCalculator(root)
    root.mainloop()
