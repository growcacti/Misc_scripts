import tkinter as tk
from tkinter import filedialog, messagebox
import autopep8
import os


def format_directory():
    # Ask user to select directory
    directory_path = filedialog.askdirectory()
    if not directory_path:
        return

    # Format all .py files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.py'):
            file_path = os.path.join(directory_path, filename)
            try:
                with open(file_path, 'r') as file:
                    original_code = file.read()

                formatted_code = autopep8.fix_code(
                    original_code, options={'aggressive': 1})

                with open(file_path, 'w') as file:
                    file.write(formatted_code)

                print(f"Formatted {filename}")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"An error occurred while formatting {filename}: {e}")
                continue

    messagebox.showinfo("Complete", "Formatting complete.")


# Create the main window
root = tk.Tk()
root.title("AutoPEP8 Formatter")

# Create and place the format button
format_button = tk.Button(
    root,
    text="Format Directory",
    command=format_directory)
format_button.pack(pady=20)

# Start the GUI event loop
root.mainloop()
