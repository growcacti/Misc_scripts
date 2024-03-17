import tkinter as tk
from tkinter import filedialog
import re
import os

class ListEditorApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
    
    def setup_ui(self):
        self.load_button = tk.Button(self.root, text="Load File", command=self.load_file)
        self.load_button.grid(row=0, column=0, padx=10, pady=10)

        self.save_re = tk.Button(self.root, text="Save Regex list", command=self.save_regex_pattern)
        self.save_re.grid(row=0, column=2, padx=10, pady=10)
        self.load_re = tk.Button(self.root, text="Load Regex List", command=self.load_regex)
        self.load_re.grid(row=0, column=3, padx=10, pady=10)

        self.save_button = tk.Button(self.root, text="Save as List", command=self.save_as_list)
        self.save_button.grid(row=1, column=1, padx=10, pady=10)
        self.regex_label = tk.Label(self.root, text="Regex Pattern: ex  ==\s*\d+(\.\d+)?")
        self.regex_label.grid(row=2, column=0, padx=10, pady=10)

        self.regex_entry = tk.Entry(self.root)
        self.regex_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.apply_button = tk.Button(self.root, text="Apply Regex Remove", command=self.apply_regex)
        self.apply_button.grid(row=14, column=2, padx=10, pady=10)

        self.listbox = tk.Listbox(self.root)
        self.listbox.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.listbox2 = tk.Listbox(self.root)
        self.listbox2.grid(row=4, column=4, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.regexpress = "==\s*\d+(\.\d+)?"
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def save_regex_pattern(self):
        if self.regex_entry.len() != 0:
            self.regexpress = self.regex.get()
            self.listbox2.insert(tk.END, self.regexpress)
            file_path = os.getcwd() + "/" + "regex.txt"
            with open (file_path, "a") as file:
                file.write(self.regexpress)
        else:
            return
      
    def load_regex(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                for line in file:
                    self.listbox2.insert(tk.END, line.strip())


    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                for line in file:
                    self.listbox.insert(tk.END, line.strip())

    def save_as_list(self):
        items = [self.listbox.get(idx) for idx in range(self.listbox.size())]
        with open("edited_list.py", "w") as file:
            file.write(f"my_list = {items}\n")

    def apply_regex(self):
        pattern = self.regex_entry.get()
        if pattern:
            for idx in range(self.listbox.size()):
                item = self.listbox.get(idx)
                new_item = re.sub(pattern, '', item)
                self.listbox.delete(idx)
                self.listbox.insert(idx, new_item)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("List Editor")
    app = ListEditorApp(root)
    root.mainloop()
