import tkinter as tk
from tkinter import ttk, END


class UnitConverter:
    def __init__(self, conversion_factors):
        self.conversion_factors = conversion_factors

    def convert(self, unit1, unit2, value):
        if unit1 in self.conversion_factors and unit2 in self.conversion_factors[unit1]:
            factor = self.conversion_factors[unit1][unit2]
            converted_value = value * factor
            return converted_value, unit2
        else:
            return None


class LengthUnitConverter(UnitConverter):
    def __init__(self):
        conversion_factors = {
            "cm": {
                "inch": 1 / 2.54,
                "mm": 10,
                "m": 0.01,
                "ft": 1 / 30.48,
                "mi": 1 / 160934.4,
            },
            "inch": {
                "cm": 2.54,
                "mm": 25.4,
                "m": 0.0254,
                "ft": 1 / 12,
                "mi": 1 / 63360,
            },
            "m": {
                "cm": 100,
                "inch": 39.37,
                "mm": 1000,
                "ft": 3.28084,
                "mi": 0.000621371,
            },
            "ft": {"cm": 30.48, "inch": 12, "mm": 304.8, "m": 0.3048, "mi": 1 / 5280},
            "km": {
                "mi": 0.621371,
                "ft": 3280.84,
                "inch": 39370.1,
                "cm": 100000,
                "mm": 1000000,
                "m": 1000,
            },
        }
        super().__init__(conversion_factors)


class LiquidUnitConverter(UnitConverter):
    def __init__(self):
        conversion_factors = {
            "ml": {
                "liters": 0.001,
                "fl oz": 0.033814,
                "cup": 0.00416667,
                "pint": 0.00211338,
                "quart": 0.00105669,
                "gallon": 0.000264172,
            },
            "liters": {
                "ml": 1000,
                "fl oz": 33.814,
                "cup": 4.16667,
                "pint": 2.11338,
                "quart": 1.05669,
                "gallon": 0.264172,
            },
            "fl oz": {
                "ml": 29.5735,
                "liters": 0.0295735,
                "cup": 0.123223,
                "pint": 0.0625,
                "quart": 0.03125,
                "gallon": 0.0078125,
            },
            "cup": {
                "ml": 240,
                "liters": 0.24,
                "fl oz": 8.11537,
                "pint": 0.50721,
                "quart": 0.253605,
                "gallon": 0.0634013,
            },
            "pint": {
                "ml": 473.176,
                "liters": 0.473176,
                "fl oz": 16,
                "cup": 1.97157,
                "quart": 0.5,
                "gallon": 0.125,
            },
            "quart": {
                "ml": 946.353,
                "liters": 0.946353,
                "fl oz": 32,
                "cup": 3.94314,
                "pint": 2,
                "gallon": 0.25,
            },
            "gallon": {
                "ml": 3785.41,
                "liters": 3.78541,
                "fl oz": 128,
                "cup": 15.7725,
                "pint": 7.74597,
                "quart": 4,
            },
        }
        super().__init__(conversion_factors)


class WeightUnitConverter(UnitConverter):
    def __init__(self):
        conversion_factors = {
            "g": {"lbs": 0.00220462, "kg": 0.001, "tons": 0.000001, "oz": 0.035274},
            "lbs": {"g": 453.592, "kg": 0.453592, "tons": 0.0005, "oz": 16},
            "kg": {"g": 1000, "lbs": 2.20462, "tons": 0.001, "oz": 35.274},
            "tons": {"g": 1000000, "lbs": 2000, "kg": 1000, "oz": 35274},
            "oz": {"g": 28.3495, "lbs": 0.0625, "kg": 0.0283495, "tons": 0.0000283495},
        }
        super().__init__(conversion_factors)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Unit Converter")
        self.geometry("600x350")

        self.length_converter = LengthUnitConverter()
        self.liquid_converter = LiquidUnitConverter()
        self.weight_converter = WeightUnitConverter()

        notebook = ttk.Notebook(self)

        length_frame = ttk.Frame(notebook)
        self.setup_length_conversion(length_frame)
        notebook.add(length_frame, text="Length")

        liquid_frame = ttk.Frame(notebook)
        self.setup_liquid_conversion(liquid_frame)
        notebook.add(liquid_frame, text="Liquid")

        weight_frame = ttk.Frame(notebook)
        self.setup_weight_conversion(weight_frame)
        notebook.add(weight_frame, text="Weight")

        notebook.pack(fill=tk.BOTH, expand=True)

    def setup_length_conversion(self, frame):
        from_units = list(self.length_converter.conversion_factors.keys())
        to_units = list(self.length_converter.conversion_factors.keys())

        tk.Label(frame, text="From:").grid(row=0, column=0)
        self.cb1_length = ttk.Combobox(frame, values=from_units)
        self.cb1_length.grid(row=0, column=1)

        tk.Label(frame, text="To:").grid(row=1, column=0)
        self.cb2_length = ttk.Combobox(frame, values=to_units)
        self.cb2_length.grid(row=1, column=1)

        tk.Label(frame, text="Value:").grid(row=2, column=0)
        self.e1_length = tk.Entry(frame, bd=5, bg="seashell")
        self.e1_length.grid(row=2, column=1)
        self.e2_length = tk.Entry(frame, bd=5, width=30, bg="seashell")
        self.e2_length.grid(row=4, column=1)
        self.e3_length = tk.Entry(frame, bd=5, width=30, bg="seashell")
        self.e3_length.grid(row=4, column=2)

        self.btn_length = tk.Button(
            frame, text="Calculate", bd=5, bg="light green", command=self.convert_length
        )
        self.btn_length.grid(row=6, column=0, columnspan=2)
        self.btn_liquid = tk.Button(
            frame, text="Clear", bd=5, bg="light green", command=self.clear_length
        )
        self.btn_liquid.grid(row=8, column=0, columnspan=2)

    def setup_liquid_conversion(self, frame):
        from_units = list(self.liquid_converter.conversion_factors.keys())
        to_units = list(self.liquid_converter.conversion_factors.keys())

        tk.Label(frame, text="From:").grid(row=0, column=0)
        self.cb1_liquid = ttk.Combobox(frame, values=from_units)
        self.cb1_liquid.grid(row=0, column=1)

        tk.Label(frame, text="To:").grid(row=1, column=0)
        self.cb2_liquid = ttk.Combobox(frame, values=to_units)
        self.cb2_liquid.grid(row=1, column=1)

        tk.Label(frame, text="Value:").grid(row=2, column=0)
        self.e1_liquid = tk.Entry(frame, bd=5, bg="seashell")
        self.e1_liquid.grid(row=2, column=1)
        self.e2_liquid = tk.Entry(frame, bd=5, width=30, bg="seashell")
        self.e2_liquid.grid(row=4, column=1)
        self.e3_liquid = tk.Entry(frame, bd=5, width=30, bg="seashell")
        self.e3_liquid.grid(row=4, column=2)

        self.btn_liquid = tk.Button(
            frame, text="Calculate", bd=5, bg="light green", command=self.convert_liquid
        )
        self.btn_liquid.grid(row=6, column=0, columnspan=2)

        self.btn_liquid = tk.Button(
            frame, text="Clear", bd=5, bg="light green", command=self.clear_liquid
        )
        self.btn_liquid.grid(row=8, column=0, columnspan=2)

    def setup_weight_conversion(self, frame):
        from_units = list(self.weight_converter.conversion_factors.keys())
        to_units = list(self.weight_converter.conversion_factors.keys())

        tk.Label(frame, text="From:").grid(row=0, column=0)
        self.cb1_weight = ttk.Combobox(frame, values=from_units)
        self.cb1_weight.grid(row=0, column=1)

        tk.Label(frame, text="To:").grid(row=1, column=0)
        self.cb2_weight = ttk.Combobox(frame, values=to_units)
        self.cb2_weight.grid(row=1, column=1)

        tk.Label(frame, text="Value:").grid(row=2, column=0)
        self.e1_weight = tk.Entry(frame, bd=5, bg="seashell")
        self.e1_weight.grid(row=2, column=1)
        self.e2_weight = tk.Entry(frame, bd=5, width=30, bg="seashell")
        self.e2_weight.grid(row=4, column=1)
        self.e3_weight = tk.Entry(frame, bd=5, width=30, bg="seashell")
        self.e3_weight.grid(row=4, column=2)

        self.btn_weight = tk.Button(
            frame, text="Calculate", bd=5, bg="light green", command=self.convert_weight
        )
        self.btn_weight.grid(row=6, column=0, columnspan=2)
        self.btn_liquid = tk.Button(
            frame, text="Clear", bd=5, bg="light green", command=self.clear_weight
        )
        self.btn_liquid.grid(row=8, column=0, columnspan=2)

    def convert_length(self):
        try:
            unit1 = self.cb1_length.get()
            unit2 = self.cb2_length.get()
            value = float(self.e1_length.get())

            result = self.length_converter.convert(unit1, unit2, value)
            if result is not None:
                converted_value, converted_unit = result
                self.e2_length.insert(0, converted_value)
                self.e3_length.insert(1, converted_unit)

        except ValueError:
            pass

    def convert_liquid(self):
        try:
            unit1 = self.cb1_liquid.get()
            unit2 = self.cb2_liquid.get()
            value = float(self.e1_liquid.get())

            result = self.liquid_converter.convert(unit1, unit2, value)
            if result is not None:
                converted_value, converted_unit = result
                self.e2_liquid.insert(0, converted_value)
                self.e3_liquid.insert(0, converted_unit)

        except ValueError:
            pass

    def convert_weight(self):
        try:
            unit1 = self.cb1_weight.get()
            unit2 = self.cb2_weight.get()
            value = float(self.e1_weight.get())

            result = self.weight_converter.convert(unit1, unit2, value)
            if result is not None:
                converted_value, converted_unit = result
                self.e2_weight.insert(0, converted_value)
                self.e3_weight.insert(0, converted_unit)

        except ValueError:
            pass

    def clear_length(self):
        self.e1_length.delete(0, END)
        self.e2_length.delete(0, END)
        self.e3_length.delete(0, END)

    def clear_liquid(self):
        self.e1_liquid.delete(0, END)
        self.e2_liquid.delete(0, END)
        self.e3_liquid.delete(0, END)

    def clear_weight(self):
        self.e1_weight.delete(0, END)
        self.e2_weight.delete(0, END)
        self.e3_weight.delete(0, END)


app = App()
app.mainloop()
