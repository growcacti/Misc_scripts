import tkinter as tk
from tkinter import scrolledtext, filedialog
import re

class RegexTester(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Regex Tester with File Handling and Grid Layout")
        self.geometry("800x600")
        
        self.create_widgets()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)  # Give the result box expandable space

        # Menu for file operations
        self.menu_bar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save Results", command=self.save_results)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.config(menu=self.menu_bar)
        
        # Input text widget
        self.text_widget = scrolledtext.ScrolledText(self, height=10)
        self.text_widget.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # Regex pattern entry
        tk.Label(self, text="Enter Regex Pattern:").grid(row=1, column=0, sticky="w", padx=10)
        self.pattern_entry = tk.Entry(self)
        self.pattern_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Replace text entry (for replace operation)
        tk.Label(self, text="Replace With (for Replace operation):").grid(row=2, column=0, sticky="w", padx=10)
        self.replace_entry = tk.Entry(self)
        self.replace_entry.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # Buttons for regex operations
        operations_frame = tk.Frame(self)
        operations_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        operations = ["match", "search", "findall", "split", "replace"]
        for op in operations:
            button = tk.Button(operations_frame, text=op.capitalize(), command=lambda op=op: self.perform_regex(op))
            button.pack(side=tk.LEFT, padx=2)

        # Result display text widget
        self.result_text_widget = scrolledtext.ScrolledText(self, height=10)
        self.result_text_widget.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_widget.delete('1.0', tk.END)
                self.text_widget.insert(tk.END, content)

    def save_results(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.result_text_widget.get("1.0", tk.END))

    def perform_regex(self, operation):
        pattern = self.pattern_entry.get()
        input_text = self.text_widget.get("1.0", tk.END)
        result_text = ""
        try:
            if operation == "match":
                result = re.match(pattern, input_text)
                result_text = result.group() if result else "No match found."
            elif operation == "search":
                result = re.search(pattern, input_text)
                result_text = result.group() if result else "No match found."
            elif operation == "findall":
                result_text = ", ".join(re.findall(pattern, input_text))
                if not result_text: result_text = "No matches found."
            elif operation == "split":
                result_text = "\n".join(re.split(pattern, input_text))
            elif operation == "replace":
                replace_with = self.replace_entry.get()
                result_text = re.sub(pattern, replace_with, input_text)
            self.result_text_widget.delete('1.0', tk.END)
            self.result_text_widget.insert(tk.END, result_text)
        except re.error as e:
            self.result_text_widget.delete('1.0', tk.END)
            self.result_text_widget.insert(tk.END, f"Regex Error: {e}")

if __name__ == "__main__":
    app = RegexTester()
    app.mainloop()
