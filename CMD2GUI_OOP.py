import tkinter as tk
import subprocess
import shlex
import sys
from tkinter import filedialog

class CommandExecutorApp:
    def __init__(self, root):
        self.root = root
        root.title("Command Executor")

        self.entry = tk.Entry(root, width=50)
        self.entry.pack()

        run_button = tk.Button(root, text="Run Command", command=self.run_command)
        run_button.pack()

        self.output_text = tk.Text(root, height=10, width=50)
        self.output_text.pack()

        save_button = tk.Button(root, text="Save Output", command=self.save_output)
        save_button.pack()
        clear_button = tk.Button(root, text="Clear Output", command=self.clear)
        clear_button.pack()

    def run_command(self):
        command = self.entry.get()
        try:
            if sys.platform == "linux" or sys.platform == "linux2":
                # For Linux, execute the command using the shell
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            elif sys.platform == "win32":
                # For Windows, execute the command in PowerShell
                process = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            
            output, error = process.communicate()
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, output.decode())
            self.output_text.insert(tk.END, error.decode())
        except Exception as e:
            self.output_text.insert(tk.END, str(e))
    def clear(self):
        self.output_text.delete('1.0', tk.END)
    def save_output(self):
        output = self.output_text.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                file.write(output)

# Running the application
root = tk.Tk()
app = CommandExecutorApp(root)
root.mainloop()
