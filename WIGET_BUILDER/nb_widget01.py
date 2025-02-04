import tkinter as tk
from tkinter import ttk

class CodeEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Editor with Tabs")
        self.root.geometry("800x600")
        
        # Create Notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        # Configure grid layout for resizing
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # Create Tabs
        self.create_button_tab()
        self.create_edit_tab()
        self.create_code_tab()

    def create_button_tab(self):
        self.button_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.button_tab, text="Buttons")

        # Add buttons to the first tab
        button_data = [
            ("For Loop", "for i in range(10):\n    print(i)\n"),
            ("If Statement", "if condition:\n    pass\n"),
            ("Function", "def my_function():\n    pass\n"),
        ]

        for idx, (label, code) in enumerate(button_data):
            button = ttk.Button(
                self.button_tab, 
                text=label, 
                command=lambda c=code: self.insert_code_to_editor(c)
            )
            button.grid(row=idx, column=0, padx=10, pady=10, sticky="w")

    def create_edit_tab(self):
        self.edit_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.edit_tab, text="Edit Features")

        # Add spinbox for loop customization
        ttk.Label(self.edit_tab, text="Loop Range:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.loop_start = tk.IntVar(value=0)
        self.loop_end = tk.IntVar(value=10)

        start_spinbox = ttk.Spinbox(self.edit_tab, from_=0, to=100, textvariable=self.loop_start, width=5)
        start_spinbox.grid(row=0, column=1, padx=5, pady=10)

        end_spinbox = ttk.Spinbox(self.edit_tab, from_=0, to=100, textvariable=self.loop_end, width=5)
        end_spinbox.grid(row=0, column=2, padx=5, pady=10)

        apply_button = ttk.Button(self.edit_tab, text="Insert Loop", command=self.insert_custom_loop)
        apply_button.grid(row=0, column=3, padx=10, pady=10)

    def create_code_tab(self):
        self.code_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.code_tab, text="Code Editor")

        # Text widget for displaying and editing code
        self.text_editor = tk.Text(self.code_tab, wrap="word")
        self.text_editor.grid(row=0, column=0, sticky="nsew")

        # Scrollbar for the text widget
        scrollbar = ttk.Scrollbar(self.code_tab, command=self.text_editor.yview)
        self.text_editor.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure grid for resizing
        self.code_tab.grid_rowconfigure(0, weight=1)
        self.code_tab.grid_columnconfigure(0, weight=1)

    def insert_code_to_editor(self, code):
        """Insert code snippet into the text editor."""
        self.text_editor.insert(tk.END, code)

    def insert_custom_loop(self):
        """Insert a customized loop based on spinbox values."""
        start = self.loop_start.get()
        end = self.loop_end.get()
        loop_code = f"for i in range({start}, {end}):\n    print(i)\n"
        self.insert_code_to_editor(loop_code)

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeEditorApp(root)
    root.mainloop()
