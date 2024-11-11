import tkinter as tk
from tkinter import messagebox
from subprocess import Popen, PIPE, STDOUT

def display_output(output):
    # Display output in the terminal Text widget
    terminal_output.insert(tk.END, output + "\n")
    terminal_output.see(tk.END)  # Auto-scroll to the end

def run_pip_command(command):
    # Run a pip command and display real-time output in the terminal Text widget
    process = Popen(command, stdout=PIPE, stderr=STDOUT, text=True)
    for line in process.stdout:
        display_output(line.strip())
    process.stdout.close()
    process.wait()

def install_packages():
    # Get selected packages from Listbox
    selected_indices = listbox.curselection()
    selected_packages = [listbox.get(i) for i in selected_indices]

    # Run pip install for each selected package
    for package in selected_packages:
        display_output(f"Installing {package}...")
        run_pip_command(["pip3", "install", package, "--break-system-package"])

def install_single_package():
    # Get the package name from Entry widget
    package = single_package_entry.get().strip()
    if not package:
        messagebox.showwarning("Warning", "Please enter a package name.")
        return
    
    # Run pip install for the single package
    display_output(f"Installing {package}...")
    run_pip_command(["pip3", "install", package, "--break-system-package"])

def load_requirements():
    # Load requirements from a file and add to the Listbox
    try:
        with open("requirements.txt", "r") as req_file:
            packages = req_file.readlines()
            for package in packages:
                listbox.insert(tk.END, package.strip())
    except FileNotFoundError:
        messagebox.showerror("Error", "requirements.txt file not found.")

# Initialize Tkinter window
root = tk.Tk()
root.title("Pip Package Installer")

# Listbox for packages
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=50, height=15)
listbox.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

# Load button to populate the Listbox with packages from requirements.txt
load_button = tk.Button(root, text="Load Requirements", command=load_requirements)
load_button.grid(row=1, column=0, padx=10, pady=5)

# Install button to install selected packages from Listbox
install_button = tk.Button(root, text="Install Selected", command=install_packages)
install_button.grid(row=1, column=1, padx=10, pady=5)

# Entry widget for single package name
single_package_entry = tk.Entry(root, width=30)
single_package_entry.grid(row=2, column=0, padx=10, pady=5)

# Button to install the single package from Entry widget
single_install_button = tk.Button(root, text="Install Single Package", command=install_single_package)
single_install_button.grid(row=2, column=1, padx=10, pady=5)

# Text widget to display terminal output
terminal_output = tk.Text(root, width=80, height=15, wrap="word", state=tk.NORMAL)
terminal_output.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Initial message in terminal
display_output("Terminal output will appear here...")

root.mainloop()
