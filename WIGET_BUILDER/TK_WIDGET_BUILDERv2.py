import tkinter as tk
from tkinter import ttk, messagebox
import time


class CodeEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Widget Code Generator with Boilerplate")

        # Boilerplate code
        self.boilerplate_code = """# Auto-generated Script\nimport pyautogui\n\nif __name__ == '__main__':\n    # Your code starts here\n"""

        # List of colors
        self.colors = [
            "white", "black", "red", "green", "blue", "yellow", "cyan", "magenta",
            "AntiqueWhite1", "CadetBlue1", "DarkOrange1", "DarkSeaGreen1", "HotPink1"
        ]

        # Set up the UI layout
        self.setup_ui()

    def setup_ui(self):
        # Selection frame for widget properties
        selection_frame = ttk.LabelFrame(self.root, text="Widget Properties")
        selection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Preview frame for showing widgets
        self.preview_frame = ttk.LabelFrame(self.root, text="Widget Preview")
        self.preview_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Use a frame as a container for preview widgets
        self.preview_area = ttk.Frame(self.preview_frame)
        self.preview_area.pack(fill="both", expand=True)

        # Widget type selection
        ttk.Label(selection_frame, text="Widget Type:").grid(row=0, column=0, sticky="w", pady=2)
        self.widget_type_combo = ttk.Combobox(
            selection_frame,
            values=["Entry", "Button", "ComboBox", "ListBox", "Text", "Canvas", "ScrolledText"]
        )
        self.widget_type_combo.grid(row=0, column=1, sticky="ew", pady=2)
        self.widget_type_combo.set("Entry")

        # Text Entry
        ttk.Label(selection_frame, text="Text:").grid(row=1, column=0, sticky="w", pady=2)
        self.text_entry = ttk.Entry(selection_frame)
        self.text_entry.grid(row=1, column=1, sticky="ew", pady=2)

        # Widget Width
        ttk.Label(selection_frame, text="Width:").grid(row=2, column=0, sticky="w", pady=2)
        self.width_spin = ttk.Spinbox(selection_frame, from_=10, to=500)
        self.width_spin.grid(row=2, column=1, sticky="ew", pady=2)
        self.width_spin.insert(0, "100")

        # Widget Height
        ttk.Label(selection_frame, text="Height:").grid(row=3, column=0, sticky="w", pady=2)
        self.height_spin = ttk.Spinbox(selection_frame, from_=1, to=50)
        self.height_spin.grid(row=3, column=1, sticky="ew", pady=2)
        self.height_spin.insert(0, "1")

        # Relief Style
        ttk.Label(selection_frame, text="Relief:").grid(row=4, column=0, sticky="w", pady=2)
        self.relief_combo = ttk.Combobox(
            selection_frame, values=["flat", "raised", "sunken", "groove", "ridge"]
        )
        self.relief_combo.grid(row=4, column=1, sticky="ew", pady=2)
        self.relief_combo.set("flat")

        # Background and Foreground Colors
        ttk.Label(selection_frame, text="Background (bg):").grid(row=5, column=0, sticky="w", pady=2)
        self.bg_var = tk.StringVar(value="white")
        ttk.Combobox(selection_frame, textvariable=self.bg_var, values=self.colors).grid(row=5, column=1, sticky="ew", pady=2)

        ttk.Label(selection_frame, text="Foreground (fg):").grid(row=6, column=0, sticky="w", pady=2)
        self.fg_var = tk.StringVar(value="black")
        ttk.Combobox(selection_frame, textvariable=self.fg_var, values=self.colors).grid(row=6, column=1, sticky="ew", pady=2)

        # Border Width
        ttk.Label(selection_frame, text="Border Width (bd):").grid(row=7, column=0, sticky="w", pady=2)
        self.bd_var = tk.IntVar(value=2)
        ttk.Entry(selection_frame, textvariable=self.bd_var).grid(row=7, column=1, sticky="ew", pady=2)

        # Add widget button
        generate_button = ttk.Button(selection_frame, text="Add Widget", command=self.generate_code)
        generate_button.grid(row=8, column=0, columnspan=2, pady=10)

        # Code frame for displaying generated code
        code_frame = ttk.LabelFrame(self.root, text="Generated Code")
        code_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.code_text = tk.Text(code_frame, height=15, width=50)
        self.code_text.grid(row=0, column=0, padx=10, pady=10)

        # Actions frame
        action_frame = ttk.Frame(self.root)
        action_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(action_frame, text="Clear All", command=self.clear_all).grid(row=0, column=0, padx=5)
        ttk.Button(action_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).grid(row=0, column=1, padx=5)
        ttk.Button(action_frame, text="Save to File", command=self.save_to_file).grid(row=0, column=2, padx=5)

    def generate_code(self):
        # Implementation for widget generation and preview
        pass

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
        if code:
            filename = f"generated_code_{int(time.time())}.py"
            with open(filename, "w") as file:
                file.write(code)
            messagebox.showinfo("Saved", f"Code saved as {filename}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeEditorApp(root)
    root.mainloop()
