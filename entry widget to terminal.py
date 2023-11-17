import tkinter as tk
import subprocess
import sys
import shlex
def run_command():
    command = entry.get()
    try:
        # Split the command into arguments
        args = shlex.split(command)

        # Detect the operating system
        if sys.platform == "linux" or sys.platform == "linux2":
            # Linux
            process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif sys.platform == "win32":
            # Windows - Convert the command into PowerShell syntax if needed
            args = ["powershell", "-Command"] + args
            process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        output, error = process.communicate()
        output_text.delete('1.0', tk.END)  # Clear previous output
        output_text.insert(tk.END, output.decode())  # Show output
        output_text.insert(tk.END, error.decode())   # Show errors, if any
    except Exception as e:
        output_text.insert(tk.END, str(e))  # Show exception message, if any
def clear():
    output_text.delete('1.0', tk.END)
# [The rest of the code remains the same]# Create the main window

def save_output():
    # Get the output text
    output = output_text.get("1.0", tk.END)
    # Ask the user where to save the file
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w") as file:
            file.write(output)

# Create the main window
# [Your existing Tkinter setup code]




root = tk.Tk()
root.title("Command Executor")

# Create entry widget
entry = tk.Entry(root, width=50)
entry.pack()

# Create a button to run the command
run_button = tk.Button(root, text="Run Command", command=run_command)
run_button.pack()
clear_button = tk.Button(root, text="Clear Output", command=clear)
clear_button.pack()
# Add a save button
save_button = tk.Button(root, text="Save Output", command=save_output)
save_button.pack()
# Text widget to show the output
output_text = tk.Text(root, height=10, width=50)
output_text.pack()

# List of prebuilt commands
prebuilt_commands = ["ls", "pwd", "echo Hello World", "ipconfig"]

# Create a Combobox for the commands
command_combobox = ttk.Combobox(root, values=prebuilt_commands)
command_combobox.pack()

# Bind the selection event of the Combobox
command_combobox.bind("<<ComboboxSelected>>", insert_command)


# Run the application
root.mainloop()
