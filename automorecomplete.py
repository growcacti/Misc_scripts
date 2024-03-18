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
        python_keywords = [ # Import statements and tkinter basics
            "import", "tkinter", "as", "tk", "from", "tkinter.scrolledtext", "ScrolledText",
            "ttk,", "INSERT,", "END,", "ANCHOR,", "font,", "Toplevel", "Button,", "Frame,", "Entry,", "Canvas,", "Scrollbar",

            # Dialogs and color chooser
            "messagebox", "mb", "filedialog", "tkinter.colorchooser", "askcolor",

            # Date and time
            "datetime", "tkinter.font", "Font,", "families",

            # Standard libraries
            "string", "punctuation", "subprocess", "collections", "Counter", "re",

            # Code quality tools
            "pylint", "autopep8",

            # System and execution
            "sys", "os", "runpy",

            # Custom elements and functionalities
            "compare", "for", "treeview,", "sort", "button", "resized", "textwidget", "and", "others", "added", "multi-file",
            "find", "replace", "app", "#camel", "case", "to", "snake", "remove", "line", "is", "word", "exist", "class",

            # Complex class definition example
            "MenuBar(tk.Menu):", "def", "__init__(self,", "parent):", "tk.Menu.__init__(self,", "parent)", "self.parent", "=",
            "parent", "tk.Frame(self.parent)", "self.bar_frm.grid(row=0,", "column=0,", "sticky='ew')", "self.parent.columnconfigure(0,", "weight=1)",

            # Notebook setup
            "Notebook", "setup", "self.notebook", "ttk.Notebook(self.parent)", "self.notebook.grid(row=1,", "sticky='nsew',",
            "padx=5,", "pady=5)", "self.parent.rowconfigure(1,", "self.frm1", "ttk.Frame(self.notebook)", "self.notebook.add(self.frm1,", "text='View')",

            # Frames inside frm1 and different sections
            "Frames", "inside", "frm1", "different", "sections", "self.txtfrm", "tk.Frame(self.frm1)", "self.txtfrm.grid(row=0,",
            "column=2,", "sticky=", "self.frm1.columnconfigure(2,", "weight=3)", "self.tx", "ScrolledText(self.txtfrm,", "bd=12)",
            "self.tx.grid(row=0,", "column=1,", "self.txtfrm.rowconfigure(0,", "self.textwidget", "self.path", "os.getcwd()",
            "self.tree_frame", "self.tree_frame.grid(row=0,",

            # Update columns to include file size, date
            "Update", "columns", "include", "file", "size", "date", "self.columns", "size,", "modified)", "self.treeview",
            "ttk.Treeview(", "self.tree_frame,", "columns=self.columns,", "show='headings')", "self.treeview.grid(row=0,",
            "self.frm1.columnconfigure(1,", "Configure", "column", "headings", "widths", "self.treeview.heading("

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
