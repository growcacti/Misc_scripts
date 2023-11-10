import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import autopep8
import os

def format_file(file_path, original=False):
    try:
        with open(file_path, 'r') as file:
            original_code = file.read()

        formatted_code = autopep8.fix_code(original_code, options={'aggressive': 1})

        # If original is True, save the formatted code to a new file
        if original:
            base, ext = os.path.splitext(file_path)
            new_file_path = f"{base}_formatted{ext}"
            with open(new_file_path, 'w') as file:
                file.write(formatted_code)
            output(f"Formatted and saved as new file: {os.path.basename(new_file_path)}")
        else:
            with open(file_path, 'w') as file:
                file.write(formatted_code)
            output(f"Formatted: {os.path.basename(file_path)}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while formatting: {e}")

def select_directory():
    directory_path = filedialog.askdirectory()
    if not directory_path:
        return

    # Clear the listbox and text widget
    file_listbox.delete(0, tk.END)
    text_widget.delete(1.0, tk.END)

    # List .py files in the directory
    for filename in sorted(os.listdir(directory_path)):
        if filename.endswith('.py'):
            file_listbox.insert(tk.END, filename)

    # Update the current directory path
    global current_directory
    current_directory = directory_path

def format_selected_file():
    if not current_directory:
        messagebox.showinfo("Info", "Please select a directory first.")
        return

    selected = file_listbox.curselection()
    if not selected:
        messagebox.showinfo("Info", "Please select a file to format.")
        return

    filename = file_listbox.get(selected[0])
    file_path = os.path.join(current_directory, filename)

    # Ask if the user wants to keep the original file
    keep_original = messagebox.askyesno("Keep Original", "Do you want to keep the original file?")
    format_file(file_path, original=keep_original)

def output(message):
    text_widget.insert(tk.END, message + '\n')
    text_widget.see(tk.END)

# Create the main window
root = tk.Tk()
root.title("AutoPEP8 Formatter")

current_directory = ''

# Create and place the select directory button
select_button = tk.Button(root, text="Select Directory", command=select_directory)
select_button.pack(pady=5)

# Create and place the listbox for file selection
file_listbox = tk.Listbox(root)
file_listbox.pack(pady=5, fill=tk.BOTH, expand=True)

# Create and place the format button
format_button = tk.Button(root, text="Format Selected File", command=format_selected_file)
format_button.pack(pady=5)

# Create and place the text widget for output
text_widget = tk.Text(root, height=10)
text_widget.pack(pady=5, fill=tk.BOTH, expand=True)

# Start the GUI event loop
root.mainloop()
