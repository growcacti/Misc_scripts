import tkinter as tk
from tkinter import filedialog

class TextToListConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to Lists Converter")

        self.setup_widgets()

    def setup_widgets(self):
        self.text_widget = tk.Text(self.root, height=10, width=50)
        self.text_widget.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        convert_button_lines = tk.Button(self.root, text="Lines to list", command=self.text_to_line_list)
        convert_button_lines.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        btn= tk.Button(self.root, text="", command=None)
        btn.grid(row=2,column=0)
        self.listbox_lines = tk.Listbox(self.root, width=25, height=10)
        self.listbox_lines.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        save_button_lines = tk.Button(self.root, text="Save Line List", command=self.save_line_list)
        save_button_lines.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        convert_button_words = tk.Button(self.root, text="Convert Text to Word List", command=self.text_to_word_list)
        convert_button_words.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        
        btn2= tk.Button(self.root, text="add quotes", command=self.add_qouteslist)
        btn2.grid(row=2,column=2)
        self.listbox_words = tk.Listbox(self.root, width=25, height=10)
        self.listbox_words.grid(row=4, column=2, columnspan=2, padx=5, pady=5)

        save_button_words = tk.Button(self.root, text="Save Word List", command=self.save_word_list)
        save_button_words.grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky="ew")
        
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

    def text_to_line_list(self):
        self.listbox_lines.delete(0, tk.END)
        text_contents = self.text_widget.get("1.0", tk.END).strip().split('\n')
        for item in text_contents:
            self.listbox_lines.insert(tk.END, item)

    def text_to_word_list(self):
        self.listbox_words.delete(0, tk.END)
        words = self.text_widget.get("1.0", tk.END).strip().split()
        seen = set()
        ordered_unique_words = [seen.add(word) or word for word in words if word not in seen]
        for word in ordered_unique_words:
            self.listbox_words.insert(tk.END, word)

    def save_line_list(self):
        lines = [self.listbox_lines.get(idx) for idx in range(self.listbox_lines.size())]
        filepath = filedialog.asksaveasfilename(defaultextension="txt")
        if filepath:
            with open(filepath, 'w') as file:
                for line in lines:
                    file.write(line + '\n')
    def add_qouteslist (self):
        self.listbox_lines.delete(0, tk.END)
        words = self.text_widget.get("1.0", tk.END).strip().split()
        seen = set()
        ordered_unique_words = [seen.add(word) or word for word in words if word not in seen]
        for word in ordered_unique_words:
            quoted_word = f'"{word}"'  # Add quotes around the word
            self.listbox_words.insert(tk.END, quoted_word)

        
    def save_word_list(self):
        words = [self.listbox_words.get(idx) for idx in range(self.listbox_words.size())]
        filepath = filedialog.asksaveasfilename(defaultextension="txt")
        if filepath:
            with open(filepath, 'w') as file:
                for word in words:
                    file.write(word + '\n')

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToListConverter(root)
    root.mainloop()
