import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import time
class WidgetDesignerApp:
    def __init__(self, root,colorlist):
        self.root = root
        self.root.title("Widget Designer")
        self.color = colorlist
        # Selection frame
        selection_frame = ttk.LabelFrame(self.root, text="Widget Properties")
        selection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Preview frame
        self.preview_frame = ttk.LabelFrame(self.root, text="Widget Preview")
        self.preview_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Use Frame as container for preview widgets
        self.preview_area = ttk.Frame(self.preview_frame)
        self.preview_area.pack(fill="both", expand=True)

        # Widget type selection
        ttk.Label(selection_frame, text="Widget Type:").grid(row=0, column=0, sticky="w", pady=2)
        self.widget_type_combo = ttk.Combobox(
            selection_frame,
            values=["Entry", "Button", "ComboBox", "ListBox","Text","Canvas","ScrolledText"],
        )
        self.widget_type_combo.grid(row=0, column=1, sticky="ew", pady=2)
        self.widget_type_combo.set("Entry")

        # Entry for text
        ttk.Label(selection_frame, text="Text:").grid(row=1, column=0, sticky="w", pady=2)
        self.text_entry = ttk.Entry(selection_frame)
        self.text_entry.grid(row=1, column=1, sticky="ew", pady=2)

        # Combo box for width
        ttk.Label(selection_frame, text="Width:").grid(row=2, column=0, sticky="w", pady=2)
        self.width_spin = ttk.Spinbox(selection_frame, from_=10, to=500)
        self.width_spin.grid(row=2, column=1, sticky="ew", pady=2)
        self.width_spin.insert(0, "10")

        # Height
        ttk.Label(selection_frame, text="Height:").grid(row=3, column=0, sticky="w", pady=2)
        self.height_spin = ttk.Spinbox(selection_frame, from_=1, to=50)
        self.height_spin.grid(row=3, column=1, sticky="ew", pady=2)
        self.height_spin.insert(0, "1")

        # Relief
        ttk.Label(selection_frame, text="Relief:").grid(row=4, column=0, sticky="w", pady=2)
        self.relief_combo = ttk.Combobox(
            selection_frame,
            values=["flat", "raised", "sunken", "groove", "ridge"],
        )
        self.relief_combo.grid(row=4, column=1, sticky="ew", pady=2)
        self.relief_combo.set("flat")

        # Background color
        ttk.Label(selection_frame, text="Background (bg):").grid(row=5, column=0, sticky="w", pady=2)
        self.bg_var = tk.StringVar(value="white")
        ttk.Combobox(selection_frame, textvariable=self.bg_var,values = self.color).grid(row=5, column=1, sticky="ew", pady=2)
        ttk.Label(selection_frame, text="Foreground (fg):").grid(row=6, column=0, sticky="w", pady=2)
        self.fg_var = tk.StringVar(value="black")
        ttk.Combobox(selection_frame, textvariable=self.fg_var,values = self.color).grid(row=6, column=1, sticky="ew", pady=2)
        # Border width
        ttk.Label(selection_frame, text="Border Width (bd):").grid(row=7, column=0, sticky="w", pady=2)
        self.bd_var = tk.IntVar(value=2)
        ttk.Entry(selection_frame, textvariable=self.bd_var).grid(row=7, column=1, sticky="ew", pady=2)

        # Add widget button
        generate_button = ttk.Button(selection_frame, text="Add Widget", command=self.generate_code)
        generate_button.grid(row=8, column=0, columnspan=2, pady=10)

        # Code frame
        code_frame = ttk.LabelFrame(self.root, text="Generated Code")
        code_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.code_text = tk.Text(code_frame, height=15, width=80)
        self.code_text.grid(row=0, column=0, padx=10, pady=10)

        # Actions
        action_frame = ttk.Frame(self.root)
        action_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(action_frame, text="Clear All", command=self.clear_all).grid(row=0, column=0, padx=5)
        ttk.Button(action_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).grid(row=0, column=1, padx=5)
        ttk.Button(action_frame, text="Save to File", command=self.save_to_file).grid(row=0, column=2, padx=5)

    def generate_code(self):
        try:
            widget_type = self.widget_type_combo.get()
            text = self.text_entry.get()
            width = int(self.width_spin.get())
            height = int(self.height_spin.get())
            relief = self.relief_combo.get()
            bg = self.bg_var.get()
            fg = self.fg_var.get()
            bd = int(self.bd_var.get())

            if widget_type == "Entry":
                code = f"""tk.Entry(root, width={width}, bg="{bg}", bd={bd}).pack(padx=10, pady=10)"""
                widget = tk.Entry(self.preview_area, width=width, bg=bg, bd=bd)
            elif widget_type == "Button":
                code = f"""tk.Button(root, text="{text}", width={width}, bg="{bg}", bd={bd}).pack(padx=10, pady=10)"""
                widget = tk.Button(self.preview_area, text=text, width=width, bg=bg, bd=bd)
            elif widget_type == "ComboBox":
                code = f"""ttk.Combobox(root, values=["Option 1", "Option 2"], width={width}).pack(padx=10, pady=10)"""
                widget = ttk.Combobox(self.preview_area, values=["Option 1", "Option 2"], width=width)
            elif widget_type == "ListBox":
                code = f"""tk.Listbox(root, height={height}, width={width}, bg="{bg}", bd={bd}, relief="{relief}").pack(padx=10, pady=10)"""
                widget = tk.Listbox(self.preview_area, height=height, width=width, bg=bg, bd=bd, relief=relief)
            elif widget_type == "Text":
                code = f"""tk.Text(root, height={height}, width={width}, bg="{bg}", bd={bd}, relief="{relief}").pack(padx=10, pady=10)"""
                widget = tk.Text(self.preview_area, height=height, width=width, bg=bg, bd=bd, relief=relief)


            elif widget_type == "Canvas":
                code = f"""tk.Canvas(root, height={height}, width={width}, bg="{bg}", bd={bd}, relief="{relief}").pack(padx=10, pady=10)"""
                widget = tk.Canvas(self.preview_area, height=height, width=width, bg=bg, bd=bd, relief=relief)

            elif widget_type == "ScrolledText":
                code = f"""ScrolledText(root, height={height}, width={width}, bg="{bg}", bd={bd}, relief="{relief}").pack(padx=10, pady=10)"""
                widget = tk.Canvas(self.preview_area, height=height, width=width, bg=bg, bd=bd, relief=relief)
            else:
                raise ValueError("Unsupported widget type!")

            # Add widget to preview and code to text area
            widget.pack(padx=10, pady=10)
            self.code_text.insert(tk.END, code + "\n")

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def clear_all(self):
        for child in self.preview_area.winfo_children():
            child.destroy()
        self.code_text.delete("1.0", tk.END)

    def copy_to_clipboard(self):
        code = self.code_text.get("1.0", tk.END).strip()
        if code:
            self.root.clipboard_clear()
            self.root.clipboard_append(code)
            messagebox.showinfo("Copied", "Code copied to clipboard!")

    def save_to_file(self):
        code = self.code_text.get("1.0", tk.END).strip()
        filename =f"generated_widget_code_{time.time()}.py"
        if code:
            with open(filename, "w") as file:
                file.write(code)
            messagebox.showinfo("Saved", filename)

colorlist = [
            "AntiqueWhite1",
            "AntiqueWhite2",
            "AntiqueWhite3",
            "AntiqueWhite4",
            "CadetBlue1",
            "CadetBlue2",
            "CadetBlue3",
            "CadetBlue4",
            "DarkGoldenrod1",
            "DarkGoldenrod2",
            "DarkGoldenrod3",
            "DarkGoldenrod4",
            "DarkOliveGreen1",
            "DarkOliveGreen2",
            "DarkOliveGreen3",
            "DarkOliveGreen4",
            "DarkOrange1",
            "DarkOrange2",
            "DarkOrange3",
            "DarkOrange4",
            "DarkOrchid1",
            "DarkOrchid2",
            "DarkOrchid3",
            "DarkOrchid4",
            "DarkSeaGreen1",
            "DarkSeaGreen2",
            "DarkSeaGreen3",
            "DarkSeaGreen4",
            "DarkSlateGray1",
            "DarkSlateGray2",
            "DarkSlateGray3",
            "DarkSlateGray4",
            "DeepPink2",
            "DeepPink3",
            "DeepPink4",
            "DeepSkyBlue2",
            "DeepSkyBlue3",
            "DeepSkyBlue4",
            "DodgerBlue2",
            "DodgerBlue3",
            "DodgerBlue4",
            "HotPink1",
            "HotPink2",
            "HotPink3",
            "HotPink4",
            "IndianRed1",
            "IndianRed2",
            "IndianRed3",
            "IndianRed4",
            "LavenderBlush2",
            "LavenderBlush3",
            "LavenderBlush4",
            "LemonChiffon2",
            "LemonChiffon3",
            "LemonChiffon4",
            "LightBlue1",
            "LightBlue2",
            "LightBlue3",
            "LightBlue4",
            "LightCyan2",
            "LightCyan3",
            "LightCyan4",
            "LightGoldenrod1",
            "LightGoldenrod2",
            "LightGoldenrod3",
            "LightGoldenrod4",
            "LightPink1",
            "LightPink2",
            "LightPink3",
            "LightPink4",
            "LightSalmon2",
            "LightSalmon3",
            "LightSalmon4",
            "LightSkyBlue1",
            "LightSkyBlue2",
            "LightSkyBlue3",
            "LightSkyBlue4",
            "LightSteelBlue1",
            "LightSteelBlue2",
            "LightSteelBlue3",
            "LightSteelBlue4",
            "LightYellow2",
            "LightYellow3",
            "LightYellow4",
            "MediumOrchid1",
            "MediumOrchid2",
            "MediumOrchid3",
            "MediumOrchid4",
            "MediumPurple1",
            "MediumPurple2",
            "MediumPurple3",
            "MediumPurple4",
            "MistyRose2",
            "MistyRose3",
            "MistyRose4",
            "NavajoWhite2",
            "NavajoWhite3",
            "NavajoWhite4",
            "OliveDrab1",
            "OliveDrab2",
            "OliveDrab4",
            "OrangeRed2",
            "OrangeRed3",
            "OrangeRed4",
            "PaleGreen1",
            "PaleGreen2",
            "PaleGreen3",
            "PaleGreen4",
            "PaleTurquoise1",
            "PaleTurquoise2",
            "PaleTurquoise3",
            "PaleTurquoise4",
            "PaleVioletRed1",
            "PaleVioletRed2",
            "PaleVioletRed3",
            "PaleVioletRed4",
            "PeachPuff2",
            "PeachPuff3",
            "PeachPuff4",
            "RosyBrown1",
            "RosyBrown2",
            "RosyBrown3",
            "RosyBrown4",
            "RoyalBlue1",
            "RoyalBlue2",
            "RoyalBlue3",
            "RoyalBlue4",
            "SeaGreen1",
            "SeaGreen2",
            "SeaGreen3",
            "SkyBlue1",
            "SkyBlue2",
            "SkyBlue3",
            "SkyBlue4",
            "SlateBlue1",
            "SlateBlue2",
            "SlateBlue3",
            "SlateBlue4",
            "SlateGray1",
            "SlateGray2",
            "SlateGray3",
            "SlateGray4",
            "SpringGreen2",
            "SpringGreen3",
            "SpringGreen4",
            "SteelBlue1",
            "SteelBlue2",
            "SteelBlue3",
            "SteelBlue4",
            "VioletRed1",
            "VioletRed2",
            "VioletRed3",
            "VioletRed4",
            "alice blue",
            "antique white",
            "aquamarine",
            "aquamarine2",
            "aquamarine4",
            "azure",
            "azure2",
            "azure3",
            "azure4",
            "bisque",
            "bisque2",
            "bisque3",
            "bisque4",
            "blanched almond",
            "blue",
            "blue violet",
            "blue2",
            "blue4",
            "brown1",
            "brown2",
            "brown3",
            "brown4",
            "burlywood1",
            "burlywood2",
            "burlywood3",
            "burlywood4",
            "cadet blue",
            "chartreuse2",
            "chartreuse3",
            "chartreuse4",
            "chocolate1",
            "chocolate2",
            "chocolate3",
            "coral",
            "coral1",
            "coral2",
            "coral3",
            "coral4",
            "cornflower blue",
            "cornsilk2",
            "cornsilk3",
            "cornsilk4",
            "cyan",
            "cyan2",
            "cyan3",
            "cyan4",
            "dark goldenrod",
            "dark green",
            "dark khaki",
            "dark olive green",
            "dark orange",
            "dark orchid",
            "dark salmon",
            "dark sea green",
            "dark slate blue",
            "dark slate gray",
            "dark turquoise",
            "dark violet",
            "deep pink",
            "deep sky blue",
            "dim gray",
            "dodger blue",
            "firebrick1",
            "firebrick2",
            "firebrick3",
            "firebrick4",
            "floral white",
            "forest green",
            "gainsboro",
            "ghost white",
            "gold",
            "gold2",
            "gold3",
            "gold4",
            "goldenrod",
            "goldenrod1",
            "goldenrod2",
            "goldenrod3",
            "goldenrod4",
            "gray",
            "gray1",
            "gray10",
            "gray11",
            "gray12",
            "gray13",
            "gray14",
            "gray15",
            "gray16",
            "gray17",
            "gray18",
            "gray19",
            "gray2",
            "gray20",
            "gray21",
            "gray22",
            "gray23",
            "gray24",
            "gray25",
            "gray26",
            "gray27",
            "gray28",
            "gray29",
            "gray3",
            "gray30",
            "gray31",
            "gray32",
            "gray33",
            "gray34",
            "gray35",
            "gray36",
            "gray37",
            "gray38",
            "gray39",
            "gray4",
            "gray40",
            "gray42",
            "gray43",
            "gray44",
            "gray45",
            "gray46",
            "gray47",
            "gray48",
            "gray49",
            "gray5",
            "gray50",
            "gray51",
            "gray52",
            "gray53",
            "gray54",
            "gray55",
            "gray56",
            "gray57",
            "gray58",
            "gray59",
            "gray6",
            "gray60",
            "gray61",
            "gray62",
            "gray63",
            "gray64",
            "gray65",
            "gray66",
            "gray67",
            "gray68",
            "gray69",
            "gray7",
            "gray70",
            "gray71",
            "gray72",
            "gray73",
            "gray74",
            "gray75",
            "gray76",
            "gray77",
            "gray78",
            "gray79",
            "gray8",
            "gray80",
            "gray81",
            "gray82",
            "gray83",
            "gray84",
            "gray85",
            "gray86",
            "gray87",
            "gray88",
            "gray89",
            "gray9",
            "gray90",
            "gray91",
            "gray92",
            "gray93",
            "gray94",
            "gray95",
            "gray97",
            "gray98",
            "gray99",
            "green yellow",
            "green2",
            "green3",
            "green4",
            "honeydew2",
            "honeydew3",
            "honeydew4",
            "hot pink",
            "indian red",
            "ivory2",
            "ivory3",
            "ivory4",
            "khaki",
            "khaki1",
            "khaki2",
            "khaki3",
            "khaki4",
            "lavender",
            "lavender blush",
            "lawn green",
            "lemon chiffon",
            "light blue",
            "light coral",
            "light cyan",
            "light goldenrod",
            "light goldenrod yellow",
            "light grey",
            "light pink",
            "light salmon",
            "light sea green",
            "light sky blue",
            "light slate blue",
            "light slate gray",
            "light steel blue",
            "light yellow",
            "lime green",
            "linen",
            "magenta2",
            "magenta3",
            "magenta4",
            "maroon",
            "maroon1",
            "maroon2",
            "maroon3",
            "maroon4",
            "medium aquamarine",
            "medium blue",
            "medium orchid",
            "medium purple",
            "medium sea green",
            "medium slate blue",
            "medium spring green",
            "medium turquoise",
            "medium violet red",
            "midnight blue",
            "mint cream",
            "misty rose",
            "navajo white",
            "navy",
            "old lace",
            "olive drab",
            "orange",
            "orange red",
            "orange2",
            "orange3",
            "orange4",
            "orchid1",
            "orchid2",
            "orchid3",
            "orchid4",
            "pale goldenrod",
            "pale green",
            "pale turquoise",
            "pale violet red",
            "papaya whip",
            "peach puff",
            "pink",
            "pink1",
            "pink2",
            "pink3",
            "pink4",
            "plum1",
            "plum2",
            "plum3",
            "plum4",
            "powder blue",
            "purple",
            "purple1",
            "purple2",
            "purple3",
            "purple4",
            "red",
            "red2",
            "red3",
            "red4",
            "rosy brown",
            "royal blue",
            "saddle brown",
            "salmon",
            "salmon1",
            "salmon2",
            "salmon3",
            "salmon4",
            "sandy brown",
            "sea green",
            "seashell2",
            "seashell3",
            "seashell4",
            "sienna1",
            "sienna2",
            "sienna3",
            "sienna4",
            "sky blue",
            "slate blue",
            "slate gray",
            "snow",
            "snow2",
            "snow3",
            "snow4",
            "spring green",
            "steel blue",
            "tan1",
            "tan2",
            "tan4",
            "thistle",
            "thistle1",
            "thistle2",
            "thistle3",
            "thistle4",
            "tomato",
            "tomato2",
            "tomato3",
            "tomato4",
            "turquoise",
            "turquoise1",
            "turquoise2",
            "turquoise3",
            "turquoise4",
            "violet red",
            "wheat1",
            "wheat2",
            "wheat3",
            "wheat4",
            "white smoke",
            "yellow",
            "yellow green",
            "yellow2",
            "yellow3",
            "yellow4",
        ]

if __name__ == "__main__":

    root = tk.Tk()
    app = WidgetDesignerApp(root, colorlist)
    root.mainloop()
