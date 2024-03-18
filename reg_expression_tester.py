import tkinter as tk
from tkinter import scrolledtext, messagebox
import re

class RegexTester(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Regex Tester")
        self.geometry("800x600")
        
        self.create_widgets()
        self.pattern_entry.bind('<KeyRelease>', self.on_pattern_change)

    def create_widgets(self):
        # Input text widget
        self.text_widget = scrolledtext.ScrolledText(self, height=10, wrap=tk.WORD, background="white")
        self.text_widget.pack(pady=5)
        self.result_widget = scrolledtext.ScrolledText(self, height=10, wrap=tk.WORD, background="white")
        self.result_widget.pack(pady=5)
        # Regex pattern entry
        pattern_label = tk.Label(self, text="Enter Regex Pattern:")
        pattern_label.pack()
        self.pattern_entry = tk.Entry(self)
        self.pattern_entry.pack(pady=5)

        # Replace text entry (for replace operation)
        replace_label = tk.Label(self, text="Replace With (for Replace operation):")
        replace_label.pack()
        self.replace_entry = tk.Entry(self)
        self.replace_entry.pack(pady=5)

        # Buttons for regex operations
        operations = ["match", "search", "findall", "split", "replace"]
        for op in operations:
            button = tk.Button(self, text=op.capitalize(), command=lambda op=op: self.perform_regex(op))
            button.pack(pady=2, fill=tk.X)

        # Result display
        self.result_label = tk.Label(self, text="Result:", wraplength=750, justify="left")
        self.result_label.pack(pady=5)

    def perform_regex(self, operation):
        pattern = self.pattern_entry.get()
        input_text = self.text_widget.get("1.0", tk.END)
        self.highlight_text(pattern)
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
                result_text = ", ".join(re.split(pattern, input_text))
            elif operation == "replace":
                replace_with = self.replace_entry.get()
                result_text = re.sub(pattern, replace_with, input_text)
            self.result_label.config(text=f"Result: {result_text}")
        except re.error as e:
            messagebox.showerror("Regex Error", str(e))

    def on_pattern_change(self, event=None):
        pattern = self.pattern_entry.get()
        self.highlight_text(pattern)

    def highlight_text(self, pattern):
        '''Highlight matching text as the user types the regex pattern.'''
        try:
            self.text_widget.tag_remove('match', '1.0', tk.END)
            if pattern:
                start_pos = '1.0'
                while True:
                    start_pos = self.text_widget.search(pattern, start_pos, tk.END, regexp=True)
                    if not start_pos:
                        break
                    end_pos = f"{start_pos}+{len(self.text_widget.get(start_pos, 'end-1c'))}c"
                    self.text_widget.tag_add('match', start_pos, end_pos)
                    start_pos = end_pos
                self.text_widget.tag_config('match', background='yellow')
        except tk.TclError:
            pass  # Handle the error silently if the regex pattern is invalid.

if __name__ == "__main__":
    app = RegexTester()
    app.mainloop()
