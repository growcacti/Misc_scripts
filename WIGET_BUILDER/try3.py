import tkinter as tk
from tkinter import ttk, messagebox
import time

# GLOBAL CONSTANT
COLORLIST = [
    "AntiqueWhite1",
    "AntiqueWhite2",
    "AntiqueWhite3",
    "AntiqueWhite4",
    "CadetBlue1",
    "CadetBlue2",
    "CadetBlue3",
    "yellow2",
    "yellow3",
    "yellow4",
]

class CodeEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Widget Code Generator with Boilerplate")

        # Boilerplate code
        self.prefix_boilerplate = """# Auto-generated Script\nimport tkinter as tk\nfrom tkinter import ttk\n\nroot = tk.Tk()\ndef main():\n"""
        self.suffix_boilerplate = """ \nif __name__ == "__main__":\n    main()"""

   
        self.colors = COLORLIST

        # Set up the UI layout
        self.setup_ui()

    def setup_ui(self):
        # Selection frame for widget properties
        selection_frame = tk.LabelFrame(self.root, text="Widget Properties")
        selection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Preview frame for showing widgets
        self.preview_frame = tk.LabelFrame(self.root, text="Widget Preview")
        self.preview_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Use a frame as a container for preview widgets
        self.preview_area = tk.Frame(self.preview_frame)
        self.preview_area.pack(fill="both", expand=True)

        # Widget type selection
        tk.Label(selection_frame, text="Widget Type:").grid(row=0, column=0, sticky="w", pady=2)
        self.widget_type_combo = ttk.Combobox(
            selection_frame,
            values=["Entry", "Button", "ComboBox", "ListBox", "Text", "Canvas"]
        )
        self.widget_type_combo.grid(row=0, column=1, sticky="ew", pady=2)
        self.widget_type_combo.set("Entry")

        # Text Entry
        tk.Label(selection_frame, text="Text:").grid(row=1, column=0, sticky="w", pady=2)
        self.text_entry = tk.Entry(selection_frame)
        self.text_entry.grid(row=1, column=1, sticky="ew", pady=2)

        # Widget Width
        tk.Label(selection_frame, text="Width:").grid(row=2, column=0, sticky="w", pady=2)
        self.width_spin = ttk.Spinbox(selection_frame, from_=10, to=500)
        self.width_spin.grid(row=2, column=1, sticky="ew", pady=2)
        self.width_spin.insert(0, "100")

        # Widget Height
        tk.Label(selection_frame, text="Height:").grid(row=3, column=0, sticky="w", pady=2)
        self.height_spin = ttk.Spinbox(selection_frame, from_=1, to=50)
        self.height_spin.grid(row=3, column=1, sticky="ew", pady=2)
        self.height_spin.insert(0, "1")

        # Relief Style
        tk.Label(selection_frame, text="Relief:").grid(row=4, column=0, sticky="w", pady=2)
        self.relief_combo = ttk.Combobox(
            selection_frame, values=["flat", "raised", "sunken", "groove", "ridge"]
        )
        self.relief_combo.grid(row=4, column=1, sticky="ew", pady=2)
        self.relief_combo.set("flat")

        # Background and Foreground Colors
        tk.Label(selection_frame, text="Background (bg):").grid(row=5, column=0, sticky="w", pady=2)
        self.bg_var = tk.StringVar(value="white")
        ttk.Combobox(selection_frame, textvariable=self.bg_var, values=self.colors).grid(row=5, column=1, sticky="ew", pady=2)

        tk.Label(selection_frame, text="Foreground (fg):").grid(row=6, column=0, sticky="w", pady=2)
        self.fg_var = tk.StringVar(value="black")
        ttk.Combobox(selection_frame, textvariable=self.fg_var, values=self.colors).grid(row=6, column=1, sticky="ew", pady=2)

        # Border Width
        tk.Label(selection_frame, text="Border Width (bd):").grid(row=7, column=0, sticky="w", pady=2)
        self.bd_var = tk.IntVar(value=2)
        tk.Entry(selection_frame, textvariable=self.bd_var).grid(row=7, column=1, sticky="ew", pady=2)

        # Add widget button
        generate_button = tk.Button(selection_frame, text="Add Widget", command=self.generate_code)
        generate_button.grid(row=8, column=0, columnspan=2, pady=10)

        # Code frame for displaying generated code
        code_frame = tk.LabelFrame(self.root)
        code_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.code_text = tk.Text(code_frame, height=15, width=50)
        self.code_text.grid(row=0, column=0, padx=10, pady=10)
        self.code_frame2 = tk.LabelFrame(self.root)
        self.code_frame2.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")

        self.code_text = tk.Text(code_frame, height=15, width=50)
        self.code_text.grid(row=0, column=0, padx=10, pady=10)
        self.code_text2 = tk.Text(code_frame, height=15, width=50)
        self.code_text2.grid(row=0, column=4, padx=10, pady=10)
        # Actions frame
        action_frame = tk.Frame(self.root)
        action_frame.grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(action_frame, text="Insert Boilerplate", command=self.insert_boilerplate).grid(row=0, column=0, padx=5)
        tk.Button(action_frame, text="Clear All", command=self.clear_all).grid(row=0, column=1, padx=5)
        tk.Button(action_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).grid(row=0, column=2, padx=5)
        tk.Button(action_frame, text="Save to File", command=self.save_to_file).grid(row=0, column=3, padx=5)

    def generate_code(self):
        """Generate widget and display its code."""
        widget_type = self.widget_type_combo.get()
        text = self.text_entry.get()
        width = int(self.width_spin.get())
        height = int(self.height_spin.get())
        relief = self.relief_combo.get()
        bg = self.bg_var.get()
        fg = self.fg_var.get()
        bd = int(self.bd_var.get())

        # Generate widget and code
        if widget_type == "Entry":
            code = f'tk.Entry(root, width={width}, bg="{bg}", bd={bd}).pack()'
        elif widget_type == "Button":
            code = f'tk.Button(root, text="{text}", width={width}, bg="{bg}", bd={bd}).pack()'
        elif widget_type == "ListBox":
            code = f'tk.Listbox(root, width={width}, height={height}, bg="{bg}", bd={bd}).pack()'
        elif widget_type == "Text":
            code = f'tk.Text(root, width={width}, height={height}, bg="{bg}", bd={bd}).pack()'
        elif widget_type == "Canvas":
            code = f'tk.Canvas(root, width={width}, height={height}, bg="{bg}", bd={bd}).pack()'
        else:
            messagebox.showerror("Error", "Unsupported widget type!")
            return

        self.code_text2.insert(tk.END, code + "\n")

    def insert_boilerplate(self):
        """Insert boilerplate code into the code area."""
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert("1.0", self.prefix_boilerplate)
        self.code_text.insert(tk.END, self.code_text2.get("1.0", tk.END))
        self.code_text.insert("6.0", self.suffix_boilerplate)

    def clear_all(self):
        """Clear preview and code area."""
        self.code_text.delete("1.0", tk.END)

    def copy_to_clipboard(self):
        """Copy code to clipboard."""
        code = self.code_text.get("1.0", tk.END).strip()
        if code:
            self.root.clipboard_clear()
            self.root.clipboard_append(code)
            messagebox.showinfo("Copied", "Code copied to clipboard!")

    def save_to_file(self):
        """Save code to a file."""
        code = self.code_text.get("1.0", tk.END).strip()
        if code:
            filename = f"generated_code_{int(time.time())}.py"
            with open(filename, "w") as file:
                file.write(code)
            messagebox.showinfo("Saved", f"Code saved as {filename}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeEditorApp(root)
    root.mainloop()
