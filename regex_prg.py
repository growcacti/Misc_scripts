import tkinter as tk
from tkinter import scrolledtext

class RegexHelper:
    def __init__(self, root):
        self.root = root
        self.root.title("Regex Helper")

        # Create a label for instructions
        self.instruction_label = tk.Label(root, text="Enter a regex pattern and click 'Translate':")
        self.instruction_label.pack(pady=5)

        # Create an entry widget for the regex pattern
        self.regex_entry = tk.Entry(root, width=50)
        self.regex_entry.pack(pady=5)

        # Create a button to translate the regex pattern
        self.translate_button = tk.Button(root, text="Translate", command=self.translate_regex)
        self.translate_button.pack(pady=5)

        # Create a text box to display the translation
        self.translation_box = scrolledtext.ScrolledText(root, width=60, height=10)
        self.translation_box.pack(pady=5)

        # Create a label for example regex patterns
        self.example_label = tk.Label(root, text="Example Regex Patterns:\n1. ^a...s$\n2. [abc]\n3. [0-9]{2,4}\n4. (a|b)")
        self.example_label.pack(pady=5)

    def translate_regex(self):
        regex_pattern = self.regex_entry.get()
        translation = self.get_translation(regex_pattern)
        self.translation_box.delete(1.0, tk.END)
        self.translation_box.insert(tk.END, translation)

    def get_translation(self, pattern):
        translations = {
            "^": "Matches the beginning of a line",
            "$": "Matches the end of a line",
            ".": "Matches any single character",
            "[abc]": "Matches any of the characters a, b, or c",
            "[0-9]": "Matches any digit",
            "{2,4}": "Matches the preceding element 2 to 4 times",
            "(a|b)": "Matches either a or b"
        }
        explanation = "Translation:\n"
        for key, value in translations.items():
            if key in pattern:
                explanation += f"{key}: {value}\n"
        if explanation == "Translation:\n":
            explanation += "No translation available for the given pattern."
        return explanation

if __name__ == "__main__":
    root = tk.Tk()
    app = RegexHelper(root)
    root.mainloop()
