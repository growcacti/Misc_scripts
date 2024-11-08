import os
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import runpy

class ScriptLauncher(tk.Tk):
    def __init__(self, config_file="scripts.json"):
        super().__init__()
        self.title("Python Script Launcher")
        self.geometry("500x400")
        self.config_file = config_file

        # Load or initialize scripts dictionary
        self.scripts = self.load_scripts()

        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Select a script to run:")
        self.label.pack(pady=10)

        # Frame for script buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill='x', pady=10)

        self.update_script_buttons()

        # Buttons to add/replace scripts
        self.add_button = ttk.Button(self, text="Add Script", command=self.add_script)
        self.add_button.pack(pady=5, fill='x')

        self.replace_button = ttk.Button(self, text="Replace Script", command=self.replace_script)
        self.replace_button.pack(pady=5, fill='x')

        # Save changes button
        self.save_button = ttk.Button(self, text="Save Scripts", command=self.save_scripts)
        self.save_button.pack(pady=10, fill='x')

    def load_scripts(self):
        # Load scripts from JSON file, if exists
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                return json.load(file)
        return {}

    def update_script_buttons(self):
        # Clear current buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        # Add buttons for each script
        for script_name, script_path in self.scripts.items():
            button = ttk.Button(self.button_frame, text=script_name, command=lambda sp=script_path: self.run_script_option(sp))
            button.pack(pady=2, fill='x')

    def run_script_option(self, script_path):
        # Ask user to choose the execution method
        choice = messagebox.askyesno("Run Method", "Run script in terminal? (Yes = Terminal, No = runpy)")
        if choice:
            self.run_script_in_terminal(script_path)
        else:
            self.run_script_with_runpy(script_path)

    def run_script_in_terminal(self, script_path):
        # Check if the script path exists
        if not os.path.exists(script_path):
            messagebox.showerror("Error", f"Script not found: {script_path}")
            return

        # Run the script in a new terminal window
        try:
            subprocess.Popen(['x-terminal-emulator', '-e', f'python3 "{script_path}"'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run script in terminal:\n{e}")

    def run_script_with_runpy(self, script_path):
        # Check if the script path exists
        if not os.path.exists(script_path):
            messagebox.showerror("Error", f"Script not found: {script_path}")
            return

        # Run the script using runpy
        try:
            runpy.run_path(script_path, run_name="__main__")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run script with runpy:\n{e}")

    def add_script(self):
        # Open file dialog to select a script
        script_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if script_path:
            script_name = os.path.basename(script_path)
            if script_name in self.scripts:
                messagebox.showinfo("Duplicate", "Script already exists. Use Replace to change the path.")
            else:
                self.scripts[script_name] = script_path
                self.update_script_buttons()

    def replace_script(self):
        # Open file dialog to select a script
        script_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if script_path:
            script_name = os.path.basename(script_path)
            self.scripts[script_name] = script_path
            self.update_script_buttons()

    def save_scripts(self):
        try:
            with open(self.config_file, 'w') as file:
                json.dump(self.scripts, file, indent=4)
            messagebox.showinfo("Success", "Scripts saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save scripts:\n{e}")

if __name__ == "__main__":
    app = ScriptLauncher()
    app.mainloop()
