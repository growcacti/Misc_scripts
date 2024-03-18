import tkinter as tk
from tkinter import Listbox, Entry
from tkinter.scrolledtext import ScrolledText

class AutoCompleteEntry(Entry):
    def __init__(self, suggestions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.suggestions = suggestions
        self.listbox = None
        self.bind("<KeyRelease>", self.check_key)
        self.bind("<Return>", self.complete)
        
    def check_key(self, event):
        if self.listbox:
            self.listbox.destroy()
        text = self.get()
        if text == '':
            return
        matches = [s for s in self.suggestions if text in s]
        if not matches:
            return
        self.listbox = Listbox(self.master, height=4)
        self.listbox.bind("<Double-1>", self.complete)
        for match in matches:
            self.listbox.insert(tk.END, match)
        self.listbox.grid(row=1, column=0, sticky='nwes')
        self.listbox.lift()

    def complete(self, event):
        if not self.listbox:
            return
        self.delete(0, tk.END)
        self.insert(tk.END, self.listbox.get(tk.ANCHOR))
        self.listbox.destroy()
        self.listbox = None

class TextEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text Editor with Auto-completion")
        self.geometry("600x400")
        python_keywords = [
            # Your python_keywords list here...
        ]

        self.entry = AutoCompleteEntry(python_keywords, self)
        self.entry.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        
        # Insert Button
        self.insert_button = tk.Button(self, text="Insert", command=self.insert_text)
        self.insert_button.grid(row=2, column=0, pady=10)

        self.textwidget = ScrolledText(self, bg="white", bd=12)
        self.textwidget.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

    def insert_text(self):
        # Method to insert text from entry to ScrolledText widget
        text_to_insert = self.entry.get()
        self.textwidget.insert(tk.END, text_to_insert + '\n')
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    app = TextEditor()
    app.mainloop()
