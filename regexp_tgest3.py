import tkinter as tk
from tkinter import scrolledtext, filedialog
import re

class RegexTester(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Regex Tester with Syntax Highlighting")
        self.geometry("800x600")
        self.create_widgets()
        self.pattern_highlight_rules()

    def create_widgets(self):
        # Simplified widget setup for brevity
        self.regex_text_widget = tk.Text(self, height=1)
        self.regex_text_widget.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.regex_text_widget.bind("<KeyRelease>", self.apply_syntax_highlighting)
        # Additional widgets setup...

    def pattern_highlight_rules(self):
        self.regex_text_widget.tag_configure("quantifier", foreground="blue")
        self.regex_text_widget.tag_configure("charClass", foreground="green")
        self.regex_text_widget.tag_configure("specialChar", foreground="red")
        # Add more styles as needed

    def apply_syntax_highlighting(self, event=None):
        for tag in self.regex_text_widget.tag_names():
            self.regex_text_widget.tag_remove(tag, "1.0", "end")
        
        patterns = [
            (r"[\+\*\?\{\}]", "quantifier"),
            (r"\[[^\]]*\]", "charClass"),
            (r"\\.", "specialChar"),
            # Add more patterns as needed
        ]
        
        for pattern, tag in patterns:
            start_index = "1.0"
            while True:
                match = re.search(pattern, self.regex_text_widget.get("1.0", "end"), re.MULTILINE)
                if not match: break
                start_index = self.regex_text_widget.search(pattern, start_index, tk.END)
                if not start_index: break
                end_index = f"{start_index}+{len(match.group(0))}c"
                self.regex_text_widget.tag_add(tag, start_index, end_index)
                start_index = end_index

        self.regex_text_widget.tag_configure("quantifier", foreground="blue")
        self.regex_text_widget.tag_configure("charClass", foreground="green")
        self.regex_text_widget.tag_configure("specialChar", foreground="red")
        # Additional tag configurations...

if __name__ == "__main__":
    app = RegexTester()
    app.mainloop()
