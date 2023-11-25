

import tkinter as tk
from subprocess import Popen, PIPE
import os

# Initialize the main window
root = tk.Tk()
root.title("Program Installer")

# Add GUI components (e.g., labels, buttons, text boxes)
output_text = tk.Text(root, height=10, width=50)
output_text.grid(row=4, column=2)
package_name = tk.Entry(root, bd=5, width=20)
package_name.grid(row=0, column=1)

def run_command(command):
    process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    output, error = process.communicate()
    output_text.insert(tk.END, output.decode() + error.decode())

def apt_install():
    pn = package_name.get()
    command = f"sudo apt-get install {pn}"
    run_command(command)

def pyinstall():
    pn = package_name.get()
    command = f"pyinstaller --onefile --noconsole {pn}.py"
    run_command(command)

# Define buttons and actions
install_button = tk.Button(root, text="Install", command=apt_install)
compile_button = tk.Button(root, text="Compile", command=lambda: run_command("gcc -o outputfile sourcefile.c"))
pyinstaller_button = tk.Button(root, text="PyInstaller", command=pyinstall)

# Positioning the buttons
install_button.grid(row=6, column=2)
compile_button.grid(row=8, column=2)
pyinstaller_button.grid(row=10, column=2)

# Start the GUI event loop
root.mainloop()
