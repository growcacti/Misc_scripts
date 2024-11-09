import tkinter as tk
from tkinter import filedialog, ttk
import os

def load_files():
    files = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            filename = os.path.basename(file)
            file_dict[filename] = f.read()
    update_file_list()

def update_file_list():
    file_listbox.delete(0, tk.END)
    for filename in file_dict.keys():
        file_listbox.insert(tk.END, filename)

def display_file_content(event):
    selected_file = file_listbox.get(file_listbox.curselection())
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, file_dict[selected_file])

def save_file():
    selected_file = file_listbox.get(file_listbox.curselection())
    content = text_area.get(1.0, tk.END).strip()
    if selected_file:
        file_dict[selected_file] = content
        filepath = filedialog.asksaveasfilename(initialfile=selected_file, defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            tk.messagebox.showinfo("Save File", "File saved successfully!")

# Create the main window
root = tk.Tk()
root.title("File Viewer")

# Create a dictionary to store file contents
file_dict = {}

# Grid layout
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# Widgets
load_button = ttk.Button(root, text="Load Text Files", command=load_files)
load_button.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

file_listbox = tk.Listbox(root)
file_listbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
file_listbox.bind("<<ListboxSelect>>", display_file_content)

text_area = tk.Text(root, wrap="word")
text_area.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

save_button = ttk.Button(root, text="Save File", command=save_file)
save_button.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

# Run the application
root.mainloop()
