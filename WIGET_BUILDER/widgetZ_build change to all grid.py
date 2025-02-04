import tkinter as tk
from tkinter import ttk, messagebox,Toplevel
import time
import subprocess
import colorlist
# GLOBAL CONSTANT
COLORLIST =colorlist.COLORLIST

class CodeEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Widget Code Generator with Boilerplate")
        self.top = None  # Initialize with None
        self.create_toplevel()  # Create the initial Toplevel window
       
        # Track current grid row and column in the preview area
        self.current_row = 0
        self.current_column = 0
        self.max_columns = 3  # Example: Limit to 3 columns before moving to the next row

        # Boilerplate code
        self.prefix_boilerplate = """# Auto-generated Script\nimport tkinter as tk\nfrom tkinter import ttk\n\nroot = tk.Tk()\ndef main():\n"""
        self.suffix_boilerplate = """\nif __name__ == "__main__":\n    main()\n    root.mainloop()\n"""

        self.colors = COLORLIST

        # Set up the UI layout
        self.setup_ui()
    def create_toplevel(self):
        """Create or recreate the Toplevel window."""
        if self.top is None or not self.top.winfo_exists():  # Check if Toplevel exists
            self.top = tk.Toplevel(self.root)
            self.top.title("Widget Preview")
            self.top.protocol("WM_DELETE_WINDOW", self.on_toplevel_close)  # Handle close event
            # Recreate the preview frame
            self.preview_frame = tk.LabelFrame(self.top, text="Widget Preview")
            self.preview_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            self.preview_area = tk.Frame(self.preview_frame)
            self.preview_area.pack(fill="both", expand=True)
    def on_toplevel_close(self):
        """Handle the Toplevel close event."""
        self.top.destroy()  # Destroy the Toplevel
        self.top = None  # Reset the reference

        
    def setup_ui(self):
        self.create_toplevel()

        # Selection frame for widget properties
        selection_frame = tk.LabelFrame(self.root, text="Widget Properties")
        selection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Preview frame for showing widgets
        self.preview_frame = tk.LabelFrame(self.top, text="Widget Preview")
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
        self.text_entry = tk.Entry(selection_frame,bd=6,bg="seashell2")
        self.text_entry.grid(row=1, column=1, sticky="ew", pady=2)

        # Widget Width
        tk.Label(selection_frame, text="Width:").grid(row=2, column=0, sticky="w", pady=2)
        self.width_spin = ttk.Spinbox(selection_frame, from_=10, to=500)
        self.width_spin.grid(row=2, column=1, sticky="ew", pady=2)
        self.width_spin.insert(0, "10")

        # Widget Height
        tk.Label(selection_frame, text="Height:").grid(row=3, column=0, sticky="w", pady=2)
        self.height_spin = ttk.Spinbox(selection_frame, from_=1, to=50)
        self.height_spin.grid(row=3, column=1, sticky="ew", pady=2)
        self.height_spin.insert(0, "5")

        # Relief Style
        tk.Label(selection_frame, text="Relief:").grid(row=4, column=0, sticky="w", pady=2)
        self.relief_combo = ttk.Combobox(
            selection_frame, values=["flat", "raised", "sunken", "groove", "ridge"]
        )
        self.relief_combo.grid(row=4, column=1, sticky="ew", pady=2)
        self.relief_combo.set("flat")

        #  def setup_ui(self):
        # Selection frame for widget properties
        selection_frame = tk.LabelFrame(self.root, text="Widget Properties")
        selection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
       
        # Preview frame for showing widgets
##        self.preview_frame = tk.LabelFrame(self.top, text="Widget Preview")
##        self.preview_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
##
##        # Use a frame as a container for preview widgets
##        self.preview_area = tk.Frame(self.preview_frame)
##        self.preview_area.pack(fill="both", expand=True)

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
        self.text_entry = tk.Entry(selection_frame,bd=6,bg="seashell2")
        self.text_entry.grid(row=1, column=1, sticky="ew", pady=2)

        # Widget Width
        tk.Label(selection_frame, text="Width:").grid(row=2, column=0, sticky="w", pady=2)
        self.width_spin = ttk.Spinbox(selection_frame, from_=10, to=500)
        self.width_spin.grid(row=2, column=1, sticky="ew", pady=2)
        self.width_spin.insert(0, "10")

        # Widget Height
        tk.Label(selection_frame, text="Height:").grid(row=3, column=0, sticky="w", pady=2)
        self.height_spin = ttk.Spinbox(selection_frame, from_=1, to=50)
        self.height_spin.grid(row=3, column=1, sticky="ew", pady=2)
        self.height_spin.insert(0, "5")

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
        generate_button = tk.Button(selection_frame,bd=6,bg="orange", text="Add Widget", command=self.generate_code)
        generate_button.grid(row=8, column=0, columnspan=2, pady=10)
        
        clear_preview_button = tk.Button(selection_frame,bd=5,bg="thistle", text="Clear Preview", command=self.clear_preview)
        clear_preview_button.grid(row=9, column=0, pady=10)
        # Code frame for displaying generated code
        code_frame = tk.LabelFrame(self.root, text="Generated Code")
        code_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.code_text = tk.Text(code_frame, height=30, width=50)
        self.code_text.pack(padx=10, pady=10)

        # Actions frame
        action_frame = tk.Frame(self.root)
        action_frame.grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(action_frame, text="Insert Boilerplate", command=self.insert_boilerplate).grid(row=0, column=0, padx=5)
        tk.Button(action_frame, text="Clear All", command=self.clear_all).grid(row=0, column=1, padx=5)
        tk.Button(action_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).grid(row=0, column=2, padx=5)
        tk.Button(action_frame, text="Save to File", command=self.save_to_file).grid(row=0, column=3, padx=5)
        tk.Button(action_frame, text="Combine Code and Run", command=self.combine_and_run).grid(row=0, column=4, padx=5)
        

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
        generate_button = tk.Button(selection_frame,bd=6,bg="orange", text="Add Widget", command=self.generate_code)
        generate_button.grid(row=8, column=0, columnspan=2, pady=10)
        
        clear_preview_button = tk.Button(selection_frame,bd=5,bg="thistle", text="Clear Preview", command=self.clear_preview)
        clear_preview_button.grid(row=9, column=0, pady=10)
        # Code frame for displaying generated code
        code_frame = tk.LabelFrame(self.root, text="Generated Code")
        code_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.code_text = tk.Text(code_frame, height=30, width=50)
        self.code_text.pack(padx=10, pady=10)

        # Actions frame
        action_frame = tk.Frame(self.root)
        action_frame.grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(action_frame, text="Insert Boilerplate", command=self.insert_boilerplate).grid(row=0, column=0, padx=5)
        tk.Button(action_frame, text="Clear All", command=self.clear_all).grid(row=0, column=1, padx=5)
        tk.Button(action_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).grid(row=0, column=2, padx=5)
        tk.Button(action_frame, text="Save to File", command=self.save_to_file).grid(row=0, column=3, padx=5)
        tk.Button(action_frame, text="Combine Code and Run", command=self.combine_and_run).grid(row=0, column=4, padx=5)
        

    def generate_code(self):
        """Generate widget and display its code."""
        self.create_toplevel()  # Ensure Toplevel is available before adding widgets
        widget_type = self.widget_type_combo.get()
        text = self.text_entry.get()
        width = int(self.width_spin.get())
        height = int(self.height_spin.get())
        relief = self.relief_combo.get()
        bg = self.bg_var.get()
        fg = self.fg_var.get()
        bd = int(self.bd_var.get())

        # Create widget code string
        if widget_type == "Entry":
            code = f"""tk.Entry(root, width={width}, bg="{bg}", bd={bd}).grid(row={self.current_row}, column={self.current_column}, padx=10, pady=10)"""
            widget = tk.Entry(self.preview_area, width=width, bg=bg, bd=bd)
        elif widget_type == "Button":
            code = f"""tk.Button(root, text="{text}", width={width}, bg="{bg}", bd={bd}).grid(row={self.current_row}, column={self.current_column}, padx=10, pady=10)"""
            widget = tk.Button(self.preview_area, text=text, width=width, bg=bg, bd=bd)
        elif widget_type == "ComboBox":
            code = f"""ttk.Combobox(root, values=["Option 1", "Option 2"], width={width}).grid(row={self.current_row}, column={self.current_column}, padx=10, pady=10)"""
            widget = ttk.Combobox(self.preview_area, values=["Option 1", "Option 2"], width=width)
        elif widget_type == "ListBox":
            code = f"""tk.Listbox(root, height={height}, width={width}, bg="{bg}", bd={bd}, relief="{relief}").grid(row={self.current_row}, column={self.current_column}, padx=10, pady=10)"""
            widget = tk.Listbox(self.preview_area, height=height, width=width, bg=bg, bd=bd, relief=relief)
        elif widget_type == "Text":
            code = f"""tk.Text(root, height={height}, width={width}, bg="{bg}", bd={bd}, relief="{relief}").grid(row={self.current_row}, column={self.current_column}, padx=10, pady=10)"""
            widget = tk.Text(self.preview_area, height=height, width=width, bg=bg, bd=bd, relief=relief)
        elif widget_type == "Canvas":
            code = f"""tk.Canvas(root, height={height}, width={width}, bg="{bg}", bd={bd}, relief="{relief}").grid(row={self.current_row}, column={self.current_column}, padx=10, pady=10)"""
            widget = tk.Canvas(self.preview_area, height=height, width=width, bg=bg, bd=bd, relief=relief)
        else:
            raise ValueError("Unsupported widget type!")

        # Place widget in the preview area using grid
        widget.grid(row=self.current_row, column=self.current_column, padx=10, pady=10)
        
        # Update code text area
        self.code_text.insert(tk.END, f"    {code}\n")  # Indented for placement in main()

        # Update grid position for the next widget
        self.current_column += 1
        if self.current_column >= self.max_columns:
            self.current_column = 0
            self.current_row += 1
    def insert_boilerplate(self):
        """Insert boilerplate code into the code area."""
        full_code = self.prefix_boilerplate + self.code_text.get("1.0", tk.END) + self.suffix_boilerplate
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert("1.0", full_code)

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
        full_code = self.prefix_boilerplate + self.code_text.get("1.0", tk.END) + self.suffix_boilerplate
        filename = f"generated_code_{int(time.time())}.py"
        with open(filename, "w") as file:
            file.write(full_code)
        messagebox.showinfo("Saved", f"Code saved as {filename}")

    def combine_and_run(self):
        """Combine the code and execute it."""
        full_code = self.prefix_boilerplate + self.code_text.get("1.0", tk.END) + self.suffix_boilerplate
        filename = f"temp_code_{int(time.time())}.py"
        with open(filename, "w") as file:
            file.write(full_code)

        try:
            subprocess.run(["python3 -m ", filename], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to run script: {e}")

    def clear_preview(self):
        """Clear all widgets from the preview area."""
        pass
##        for widget in self.preview_area.winfo_children():
##            widget.destroy()
if __name__ == "__main__":
    root = tk.Tk()   
    app = CodeEditorApp(root)
    root.mainloop()
