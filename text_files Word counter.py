
import os
from tkinter import Tk, Frame, Label, Entry, Button, Text, filedialog, Scrollbar, END
from collections import Counter

class WordCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word/Number Occurrence Counter")

        self.frame = Frame(root)
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        self.label = Label(self.frame, text="Enter word/number to count:")
        self.label.grid(row=0, column=0, padx=5, pady=5)

        self.entry = Entry(self.frame, width=30)
        self.entry.grid(row=0, column=1, padx=5, pady=5)

        self.browse_button = Button(self.frame, text="Select Directory", command=self.browse_directory)
        self.browse_button.grid(row=1, column=0, padx=5, pady=5)

        self.count_button = Button(self.frame, text="Count Occurrences", command=self.count_occurrences)
        self.count_button.grid(row=1, column=1, padx=5, pady=5)

        self.save_button = Button(self.frame, text="Save Results", command=self.save_results)
        self.save_button.grid(row=2, column=0, padx=5, pady=5)

        self.load_button = Button(self.frame, text="Load Results", command=self.load_results)
        self.load_button.grid(row=2, column=1, padx=5, pady=5)

        self.text_area = Text(self.frame, wrap='word', height=20, width=60)
        self.text_area.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.scrollbar = Scrollbar(self.frame, command=self.text_area.yview)
        self.scrollbar.grid(row=3, column=2, sticky='nsew')
        self.text_area['yscrollcommand'] = self.scrollbar.set

        self.directory = None

    def browse_directory(self):
        self.directory = filedialog.askdirectory()
        self.text_area.insert(END, f"Selected directory: {self.directory}\n")

    def count_occurrences(self):
        if not self.directory:
            self.text_area.insert(END, "Please select a directory first.\n")
            return

        search_term = self.entry.get().strip()
        if not search_term:
            self.text_area.insert(END, "Please enter a word or number to count.\n")
            return

        self.text_area.insert(END, f"Counting occurrences of '{search_term}'...\n")

        counter = Counter()
        results = []

        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                        word_count = text.count(search_term)
                        char_count = len(text)
                        line_count = text.count('\n') + 1

                        results.append((file_path, word_count, char_count, line_count))

        self.text_area.insert(END, f"Results for '{search_term}':\n")
        for file_path, word_count, char_count, line_count in results:
            self.text_area.insert(END, f"{file_path}:\n")
            self.text_area.insert(END, f"  {word_count} occurrences\n")
            self.text_area.insert(END, f"  {char_count} characters\n")
            self.text_area.insert(END, f"  {line_count} lines\n")

    def save_results(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(self.text_area.get(1.0, END))
            self.text_area.insert(END, f"Results saved to {save_path}\n")

    def load_results(self):
        load_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if load_path:
            with open(load_path, 'r', encoding='utf-8') as f:
                self.text_area.delete(1.0, END)
                self.text_area.insert(END, f.read())
            self.text_area.insert(END, f"Results loaded from {load_path}\n")

if __name__ == "__main__":
    root = Tk()
    app = WordCounterApp(root)
    root.mainloop()
