import os
import tkinter as tk
from tkinter import filedialog, Text, messagebox
from tkinter import ttk

class TextFileEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text File Extractor and Editor")

        # Variables
        self.directory_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.replace_var = tk.StringVar()

        # GUI Elements
        self.create_widgets()

    def create_widgets(self):
        # Directory selection
        tk.Label(self.root, text="Select Directory:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(self.root, textvariable=self.directory_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_directory).grid(row=0, column=2, padx=5, pady=5)

        # Listbox to display text files in directory
        tk.Label(self.root, text="Text Files:").grid(row=1, column=0, padx=5, pady=5, sticky='ne')
        self.file_listbox = tk.Listbox(self.root, width=50, height=5)
        self.file_listbox.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Extract Text", command=self.extract_text).grid(row=1, column=2, padx=5, pady=5)

        # Spinboxes to select line range
        tk.Label(self.root, text="Select Line Range:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.start_line_spinbox = ttk.Spinbox(self.root, from_=1, to=100, width=5)
        self.start_line_spinbox.grid(row=2, column=1, padx=(5, 0), pady=5, sticky='w')
        tk.Label(self.root, text="to").grid(row=2, column=1, padx=(50, 0), pady=5, sticky='w')
        self.end_line_spinbox = ttk.Spinbox(self.root, from_=1, to=100, width=5)
        self.end_line_spinbox.grid(row=2, column=1, padx=(80, 0), pady=5, sticky='w')

        # Text widget to display extracted text
        tk.Label(self.root, text="Extracted Text:").grid(row=3, column=0, padx=5, pady=5, sticky='ne')
        self.result_text = Text(self.root, width=60, height=10)
        self.result_text.grid(row=3, column=1, padx=5, pady=5)

        # Find and Replace
        tk.Label(self.root, text="Find:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(self.root, textvariable=self.search_var, width=30).grid(row=4, column=1, padx=5, pady=5, sticky='w')
        tk.Label(self.root, text="Replace:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(self.root, textvariable=self.replace_var, width=30).grid(row=5, column=1, padx=5, pady=5, sticky='w')
        tk.Button(self.root, text="Find and Replace", command=self.find_and_replace).grid(row=5, column=2, padx=5, pady=5)

        # Save button
        tk.Button(self.root, text="Save to File", command=self.save_to_file).grid(row=6, column=1, padx=5, pady=5, sticky='e')

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_var.set(directory)
            file_list = [f for f in os.listdir(directory) if f.endswith('.txt')]
            self.file_listbox.delete(0, tk.END)
            for file in file_list:
                self.file_listbox.insert(tk.END, file)

    def extract_text(self):
        directory = self.directory_var.get()
        selected_file = self.file_listbox.get(tk.ACTIVE)
        file_path = os.path.join(directory, selected_file)

        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                start_line = int(self.start_line_spinbox.get())
                end_line = int(self.end_line_spinbox.get())
                parsed_text = ''.join(lines[start_line - 1:end_line])
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, parsed_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def find_and_replace(self):
        search_text = self.search_var.get()
        replace_text = self.replace_var.get()

        content = self.result_text.get(1.0, tk.END)
        modified_content = content.replace(search_text, replace_text)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, modified_content)

    def save_to_file(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if save_path:
            try:
                with open(save_path, 'w') as file:
                    file.write(self.result_text.get(1.0, tk.END))
                messagebox.showinfo("Success", "File saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = TextFileEditorApp(root)
    root.mainloop()
