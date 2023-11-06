import tkinter as tk

from tkinter import filedialog
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory

from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import Button, GROOVE, INSERT, END, Toplevel
from tkinter.colorchooser import askcolor
import os, sys, subprocess
from tkinter.scrolledtext import ScrolledText
import re
import runpy
import glob
import time


class Codeview(ttk.Frame):
    def __init__(self, parent):
        super().__init__()
        self.path = os.getcwd()
        self.parent = parent
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.grid(row=0, column=0)

        self.f1 = ttk.Frame(self.notebook, width=2100, height=1080)
        self.notebook.add(self.f1, text="View")
        ##        self.f1.grid_columnconfigure(0, weight=1)  # Expand first column
        self.wkcurdir = os.getcwd()
        self.dirfr = ttk.Frame(self.f1, width=30, height=10)
        self.dirfr.grid(
            row=0, column=1, sticky="nw"
        )  # Place in first row, first column

        tk.Label(self.dirfr, text="--------------").grid(row=1, column=0, pady=5)

        self.fram = tk.Frame(self.f1, width=20, height=20)
        self.fram.grid(
            row=0, column=1, pady=10, padx=(0, 4), sticky="w"
        )  # Place in second row, first column

        self.lb = tk.Listbox(
            self.fram,
            bg="cyan2",
            bd=12,
            width=55,
            height=45,
            exportselection=False,
            selectmode=tk.SINGLE,
        )
        self.lb.grid(row=1, column=1, rowspan=2, padx=(0, 1), pady=20, sticky="nw")
        self.lb.columnconfigure(1, weight=0, minsize=55)
        self.fram.columnconfigure(1, weight=0, minsize=55)
        self.dirpath = tk.Entry(self.fram, bd=12, bg="seashell", width=40)
        self.dirpath.grid(row=0, column=1)

        self.lb.focus()
        self.lb.configure(selectmode="")

        self.curtxt = None
        self.x = self.lb.curselection()
        self.textfr = ttk.Frame(self.f1, width=200, height=44)
        self.textfr.grid(row=0, column=2, padx=(0, 4), sticky="w")
        self.textfr.columnconfigure(1, weight=5, minsize=300)
        self.tx = ScrolledText(
            self.textfr,
            bg="white",
            bd=12,
            relief=GROOVE,
            height=44,
            width=100,
            font="TkFixedFont",
        )
        self.tx.grid(row=1, column=0, padx=(0, 4))
        self.f2 = ttk.Frame(self.notebook, width=1900, height=1080)
        self.f2.grid(row=0, column=1)
        self.notebook.add(self.f2, text="read")
        self.txx = ScrolledText(
            self.f2,
            bg="white",
            bd=12,
            relief=GROOVE,
            height=50,
            width=100,
            font="TkFixedFont",
        )
        self.txx.grid(row=0, column=5)
        self.sb2 = SideButtonframe(self.f2, self.txx)

        self.f3 = ttk.Frame(self.notebook, width=1900, height=1080)
        self.f3.grid(row=0, column=1)

        self.notebook.add(self.f3, text="Editor")

        self.ttt = ScrolledText(
            self.f3,
            bg="white",
            bd=12,
            relief=GROOVE,
            height=50,
            width=100,
            font="TkFixedFont",
        )
        self.ttt.grid(row=0, column=6)
        self.sbf3 = SideButtonframe(self.f3, self.ttt)

        self.f4 = ttk.Frame(self.notebook, width=1900, height=1080)
        self.f4.grid(row=0, column=1)
        self.notebook.add(self.f4, text="Proof read")
        self.txx = ScrolledText(
            self.f4,
            bg="white",
            bd=12,
            relief=GROOVE,
            height=50,
            width=100,
            font="TkFixedFont",
        )
        self.txx.grid(row=0, column=5)
        self.sb2 = SideButtonframe(self.f4, self.txx)

        self.f5 = ttk.Frame(self.notebook, width=1900, height=1080)
        self.f5.grid(row=0, column=1)
        self.notebook.add(self.f5, text="Snippet")
        self.txxx = ScrolledText(
            self.f5,
            bg="white",
            bd=12,
            relief=GROOVE,
            height=50,
            width=100,
            font="TkFixedFont",
        )
        self.txxx.grid(row=0, column=5)
        self.sbf5 = SideButtonframe(self.f5, self.txxx)

        self.f6 = ttk.Frame(self.notebook, width=1900, height=1080)
        self.f6.grid(row=0, column=1)
        self.notebook.add(self.f6, text="formater")

        self.f7 = ttk.Frame(self.notebook, width=1900, height=1080)
        self.f7.grid(row=0, column=1)
        self.notebook.add(self.f7, text="out")

        self.ent1 = tk.Entry(self.f6, bg="seashell", bd=15)
        self.ent1.grid(row=1, column=1)
        self.ent2 = tk.Entry(self.f6, bg="seashell", bd=15)
        self.ent2.grid(row=1, column=3)
        self.blkbtn = tk.Button(
            self.f6,
            text="run black on dir",
            bd=8,
            bg="orange",
            command=lambda: self.reformat_code(self.wkcurdir),
        )
        self.blkbtn.grid(row=8, column=3)
        self.dirbtn = tk.Button(
            self.f6,
            text="change wkdir",
            bd=2,
            command=self.wkdir,
        )
        self.dirbtn.grid(row=8, column=1)
        self.dirbtn2 = tk.Button(
            self.f6,
            text="STORE PATH IN ENTRY1",
            bd=2,
            bg="light pink",
            command=self.storepath,
        )
        self.dirbtn2.grid(row=9, column=2)

        ##        btn= tk.Button(f6, text="get py2 script", bd=8,bg="orange", command : lambda =  self.py2)
        ##        btnbtn.grid(row=4, column=1)
        ##        btn2= tk.Button(f6, text="get py2 script", bd=8,bg="light blue", command = lambda self.py2to3convert)
        ##        btnbtn.grid(row=4, column=3)
        self.out = ScrolledText(
            self.f7,
            bg="white",
            bd=12,
            relief=GROOVE,
            height=50,
            width=100,
            font="TkFixedFont",
        )
        self.out.grid(row=1, column=1)
        self.f8 = ttk.Frame(self.notebook, width=1900, height=1080)
        self.f8.grid(row=0, column=1)
        self.notebook.add(self.f8, text="Compare")
        self.f9 = ttk.Frame(self.notebook, width=1900, height=1080)
        self.f9.grid(row=0, column=1)

        self.notebook.add(self.f9, text="------")

        comparator = TextFileComparator(self.f8)
        comparator.run()
        self.out.insert("end", comparator.output_text)

        self.flist = os.listdir(self.path)
        self.dirpath.delete(0, END)
        self.dirpath.insert(INSERT, self.path)

        for self.item in self.flist:
            if self.item.endswith(".py" or ".txt"):
                self.lb.insert(tk.END, self.item)

                self.lb.focus()
        self.cvw = Cview_Buttons(self.f1, self.tx, self.lb, self.txx, self.dirpath)

        self.lb.bind("<Double-Button-1>", self.cvw.listing)
        self.lb.bind("<<ListboxSelect>>", self.cvw.showcontent)
        self.lb.bind(
            "<Double-Button-2>", lambda event: self.cvw.run(self.path, self.lb)
        )
        self.lb.bind("<<ListboxSelect>>", lambda event: self.cvw.listing(event))

    def storepath(self):
        self.path = askdirectory()
        os.chdir(self.path)
        self.ent1.delete(0, END)
        self.ent1.insert(0, self.path)

    def wkdir(self):
        os.chdir(self.path)
        self.ent2.delete(0, END)
        self.ent2.insert(0, self.path)
        self.wkcurdir = os.getcwd()
        self.ent2.insert(END, self.wkcurdir)

    def reformat_code(self, directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)
                    result = subprocess.run(f"python -m black {filepath}", shell=True)
                    if result.returncode == 0:
                        print(f"Successfully formatted: {filepath}")
                    else:
                        print(f"Error occurred while formatting: {filepath}")


class FindReplaceWidget:
    def __init__(self, textwidget):
        self.top = Toplevel()
        self.textwidget = textwidget
        self.sfr = ttk.Frame(self.top, relief=tk.RAISED)

        self.label1 = tk.Label(self.sfr, text="Find").grid(row=11, column=0)
        self.entry = tk.Entry(self.sfr, width=15, bd=12, bg="wheat")
        self.entry.grid(row=12, column=0)

        self.find1 = tk.Button(
            self.sfr,
            text="Find",
            bd=8,
            command=lambda: self.find(self.textwidget),
        )
        self.find1.grid(row=13, column=0)
        self.label2 = tk.Label(self.sfr, text="Replace With ").grid(row=14, column=0)

        self.entry2 = tk.Entry(self.sfr, width=15, bd=12, bg="seashell")
        self.entry2.grid(row=15, column=0)
        self.entry2.focus_set()
        self.replace1 = tk.Button(
            self.sfr,
            text="Find&Replace",
            bd=8,
            command=lambda: self.find_replace(self.textwidget),
        )
        self.replace1.grid(row=16, column=0)
        self.sfr.grid(row=0, column=0, sticky="ns")

    def find(self, textwidget):
        self.textwidget = textwidget
        self.var1 = self.entry.get()

        # remove tag 'found' from index 1 to END
        self.textwidget.tag_remove("found", "1.0", END)

        # self.finder = self.entry.get()

        if self.var1:
            idx = "1.0"
            while 1:
                # searches for desired string from index 1
                idx = self.textwidget.search(self.var1, idx, nocase=1, stopindex=END)

                if not idx:
                    break

                lastidx = "% s+% dc" % (idx, len(self.var1))

                # overwrite 'Found' at idx
                self.textwidget.tag_add("found", idx, lastidx)
                idx = lastidx

                # mark located string as red

                self.textwidget.tag_config("found", background="yellow")
            self.entry.focus.set()

    def find_replace(self, textwidget):
        self.textwidget = textwidget
        self.var1 = self.entry.get()

        self.var2 = self.entry2.get()

        # remove tag 'found' from index 1 to END
        self.textwidget.tag_remove("found", "1.0", END)

        # returns to widget currently in focus
        self.fin = self.var1
        self.repl = self.var2

        if self.fin and self.repl:
            idx = "1.0"
            while 1:
                # searches for desired string from index 1
                idx = self.textwidget.search(self.fin, idx, nocase=1, stopindex=END)
                print(idx)
                if not idx:
                    break

                # last index sum of current index and
                # length of text
                lastidx = "% s+% dc" % (idx, len(self.fin))

                self.textwidget.delete(idx, lastidx)
                self.textwidget.insert(idx, self.repl)

                lastidx = "% s+% dc" % (idx, len(self.repl))

                # overwrite 'Found' at idx
                self.textwidget.tag_add("found", idx, lastidx)
                idx = lastidx

            # mark located string as red
            self.textwidget.tag_config("found", foreground="green", background="yellow")


class SideButtonframe:
    def __init__(self, parent, textwidget):
        self.textwidget = textwidget
        self.parent = parent
        self.textwidget.tag_configure("highlight", background="cornsilk")
        self.sfr = tk.Frame(self.parent, width=5)
        self.sfr.grid(row=0, column=0, padx=(0, 0), sticky="w")
        self.sfr.columnconfigure(0, weight=0, minsize=5)

        # Create a Combobox to select the method
        self.method_combobox = ttk.Combobox(self.sfr)
        self.method_combobox["values"] = [
            "Open",
            "Save As...",
            "Clear",
            "Change FG Color",
            "Change BG Color",
            "Select All",
            "Cut",
            "Copy",
            "Paste",
            "Undo",
            "Redo",
            "Insert Self",
            "Highlighted Insert Self",
            "Find & Replace",
            "Update Info",
            "Indent",
            "Dedent",
            "Indent num",
        ]
        self.method_combobox.grid(row=1, column=0)

        # Create a button to initiate the selected method
        self.execute_button = tk.Button(
            self.sfr, text="Execute", bd=2, command=self.execute_method
        )
        self.execute_button.grid(row=2, column=0)

        self.update_info()
        indent_spaces = tk.StringVar()
        indent_spinbox = ttk.Spinbox(
            self.sfr, from_=1, to=10, textvariable=indent_spaces, width=3
        )
        indent_spinbox.set("4")  # Default indent spaces
        indent_spinbox.grid(row=4, column=0)

    def execute_method(self):
        selected_method = self.method_combobox.get()

        if selected_method == "Open":
            self.open_file(self.textwidget)
        elif selected_method == "Save As...":
            self.save_file(self.textwidget)
        elif selected_method == "Clear":
            self.clear(self.textwidget)
        elif selected_method == "Change FG Color":
            self.changeFg(self.textwidget)
        elif selected_method == "Change BG Color":
            self.changeBg(self.textwidget)
        elif selected_method == "Select All":
            self.textwidget.event_generate("<<SelectAll>>")
        elif selected_method == "Cut":
            self.textwidget.event_generate("<<Cut>>")
        elif selected_method == "Copy":
            self.textwidget.event_generate("<<Copy>>")
        elif selected_method == "Paste":
            self.textwidget.event_generate("<<Paste>>")
        elif selected_method == "Undo":
            self.undo()
        elif selected_method == "Redo":
            self.redo()
        elif selected_method == "Insert Self":
            self.insert_self(self.textwidget)
        elif selected_method == "Highlighted Insert Self":
            self.insert_selfs(self.textwidget)
        elif selected_method == "Find & Replace":
            self.finder(self.textwidget)
        elif selected_method == "Update Info":
            self.update_info()
        elif selected_method == "Indent":
            self.indent()
        elif selected_method == "Dedent":
            self.dedent()
        elif selected_method == "adjust indent":
            self.indent_text()
        elif selected_method == "adj dedent":
            self.dedent_text()
        elif selected_method == "change indent dedent text":
            self.change_indent_spaces()

    def update_info(self, event=None):
        self.content = self.textwidget.get("1.0", "end-1c")
        self.label = tk.Label(self.sfr, text="             ").grid(row=18, column=0)
        self.label1 = tk.Label(self.sfr, text="             ").grid(row=19, column=0)
        lines = self.textwidget.index("end-1c").split(".")[0]
        words = len(self.content.split())
        characters = len(self.content)
        self.info_label = tk.Label(
            self.sfr, text="Lines: 0 | Words: 0 |\n Characters: 0"
        )
        self.info_label.grid(row=20, column=0)
        # Get the current text content
        self.content = self.textwidget.get("1.0", "end-1c")

        # Count the lines, words, and characters

        self.info_label.config(
            text=f"Lines: {lines} |  \n Words: {words} |\n Characters: {characters}"
        )

        # Update the label with the information

    def finder(self, textwidget):
        self.textwidget = textwidget
        fr = FindReplaceWidget(self.textwidget)

    def changeBg(self, textwidget):
        (triple, hexstr) = askcolor()
        if hexstr:
            textwidget.config(bg=hexstr)

    def changeFg(self, textwidget):
        (triple, hexstr) = askcolor()
        if hexstr:
            textwidget.config(fg=hexstr)

    def clear(self, textwidget):
        self.textwidget = textwidget
        self.textwidget.delete("1.0", tk.END)

    def open_file(self, textwidget):
        filepath = filedialog.askopenfilename(
            initialdir=os.path.expanduser("/Desktop"),
            title="Select File",
            filetypes=(("Python files", "*.py"), ("All files", "*.*")),
        )
        if filepath:
            # Check if the file is hidden
            if os.path.basename(filepath).startswith("."):
                print("Hidden file selected. Ignoring...")
            else:
                print("Selected file:", file_path)
        """Open a file for editing."""

        if not filepath:
            return
        textwidget.delete(1.0, tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.read()
            textwidget.insert(tk.END, text)

    def save_file(self, textwidget):
        """Save the current file as a new file."""
        filepath = asksaveasfilename(
            defaultextension="self.txt",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = textwidget.get(1.0, tk.END)
            output_file.write(text)

    def undo(self):
        try:
            self.textwidget.edit_undo()
        except:
            print("No previous action")

    def redo(self):
        try:
            self.textwidget.edit_redo()
        except:
            print("No previous action")

    def copy(self, event=None):
        self.clipboard_clear()
        text = self.textwidget.get("sel.first", "sel.last")
        self.clipboard_append(text)

    def cut(self, event):
        self.copy()
        self.delete("sel.first", "sel.last")

    def paste(self, event):
        text = self.selection_get(selection="CLIPBOARD")
        self.insert("insert", text)

    def select_all(self, event=None):
        self.textwidget.tag_add("sel", "1.0", tk.END)
        return "break"

    def indent2(self, event=None):
        # Get the current line and its content
        index = self.textwidget.index("insert linestart")
        line = self.textwidget.get(index, index + "lineend")

        # Check if the line starts with specific keywords
        keywords = ["if", "elif", "else", "while", "for", "def", "class"]
        if any(line.startswith(keyword) for keyword in keywords):
            # Insert four spaces at the start of the new line
            self.textwidget.insert("insert", " " * 4)

    def auto_indent(self, event=None):
        self.textwidget = event.widget

        # get leading whitespace from current line

    def apply_indent_dedent():
        sel_start, sel_end = text.tag_ranges(tk.SEL)
        if sel_start and sel_end:
            text.tag_add("indent", sel_start, sel_end)
            self.textwidget.get("insert linestart", "insert")
            match = re.match(r"^(\s+)", line)
            whitespace = match.group(0) if match else ""

            # insert the newline and the whitespace
            self.textwidget.insert("insert", f"\n{whitespace}")

        # return "break" to inhibit default insertion of newline
        return "break"

    def indent_text(self):
        text.tag_configure("indent", lmargin1=30)

    def dedent_text(self):
        text.tag_configure("indent", lmargin1=0)

    def change_indent_spaces(self):
        spaces = int(indent_spaces.get())
        text.tag_configure("indent", lmargin1=spaces * 7)

    def indent(self):
        selected_text = text_widget.get("sel.first", "sel.last")
        if selected_text:
            # Add four spaces to the beginning of each line
            indented_text = "\n".join(
                f"    {line}" for line in selected_text.split("\n")
            )
            text_widget.replace("sel.first", "sel.last", indented_text)

    def dedent(self):
        selected_text = text_widget.get("sel.first", "sel.last")
        if selected_text:
            # Remove four spaces from the beginning of each line if present
            dedented_text = "\n".join(
                line[4:] if line.startswith("    ") else line
                for line in selected_text.split("\n")
            )
            text_widget.replace("sel.first", "sel.last", dedented_text)

    def highlight(self):
        selected_text = text_widget.get("sel.first", "sel.last")
        if selected_text:
            text_widget.tag_add("highlight", "sel.first", "sel.last")

    def apply_indent_dedent(self):
        sel_start, sel_end = text.tag_ranges(tk.SEL)
        if sel_start and sel_end:
            text.tag_add("indent", sel_start, sel_end)

    def insert_self(self, textwidget):
        self.textwidget = textwidget
        start_index = self.textwidget.index("sel.first")
        end_index = self.textwidget.index("sel.last")

        selected_text = self.textwidget.get(start_index, end_index)
        modified_text = "\n".join(
            [
                "self." + line if line.strip() else line
                for line in selected_text.split("\n")
            ]
        )

        self.textwidget.delete(start_index, end_index)
        self.textwidget.insert(start_index, modified_text)

    def insert_selfs(self, textwidget):
        self.textwidget = textwidget

        start_index = self.textwidget.index("sel.first")
        end_index = self.textwidget.index("sel.last")

        selected_text = self.textwidget.get(start_index, end_index)
        modified_lines = [
            "self." + line.strip() if line.strip() else line
            for line in selected_text.split("\n")
        ]
        modified_text = "\n".join(modified_lines)

        self.textwidget.delete(start_index, end_index)
        self.textwidget.insert(start_index, modified_text)

    def insert_self_in_parentheses(self, text_widget):
        start_index = text_widget.index("sel.first")
        end_index = text_widget.index("sel.last")

        selected_text = text_widget.get(start_index, end_index)
        modified_lines = []

        for line in selected_text.split("\n"):
            if line.strip():
                modified_line = line.replace("()", "(self)")  # Replace () with (self)
            else:
                modified_line = line
            modified_lines.append(modified_line)

        modified_text = "\n".join(modified_lines)
        text_widget.delete(start_index, end_index)
        text_widget.insert(start_index, modified_text)

    def bindings(self):
        self.textwidget.bind("<Return>", self.auto_indent)
        self.textwidget.bind("<Key>", self.update_info)
        self.textwidget.bind("<<Selection>>", self.update_info)

    def quit(self):
        sys.exit(0)


class Cview_Buttons(SideButtonframe):
    def __init__(self, container, textwidget, lb, tx2, dirpath):
        super().__init__(container, textwidget)
        self.text = textwidget
        self.lb = lb
        self.tx2 = tx2
        self.parent = container
        self.dirpath = dirpath
        self.path = dirpath.get()

        self.dir = tk.Button(
            self.sfr,
            text="get dir",
            bd=2,
            bg="light pink",
            command=lambda: self.newdirlist(),
        )
        self.dir.grid(row=23, column=0)

        self.btn_grab = tk.Button(
            self.sfr,
            text="Send to ",
            bd=2,
            bg="orange",
            command=lambda: self.ggtxt(self.textwidget),
        )
        self.btn_grab.grid(row=24, column=0)

        self.btn_run = tk.Button(
            self.sfr,
            text="run py ",
            bd=2,
            bg="light green",
            command=lambda: self.run(self.path, self.lb),
        )
        self.btn_run.grid(row=25, column=0)
        self.btn_run2 = tk.Button(
            self.sfr,
            text="run py2 ",
            bd=2,
            bg="light green",
            command=lambda: self.run2(self.path, self.lb),
        )
        self.btn_run2.grid(row=26, column=0)

    def listing(self, event=None):
        x = event.widget
        try:
            x = int(self.lb.curselection()[0])
            file = self.lb.get(x)
        except IndexError:
            v = self.lb.get(x)
            v = self.lb.curselection()[0]
            file = self.lb.get(v)

        with open(file, "r") as file:
            content = file.read()
            self.textwidget.delete("1.0", tk.END)
            self.textwidget.insert(tk.END, content)
            self.curtxt = content
            return self.curtxt

    def newdirlist(self):
        self.path = askdirectory()
        os.chdir(self.path)
        self.flist = os.listdir(self.path)
        self.lb.delete(0, tk.END)

        self.flist = os.listdir(self.path)
        self.dirpath.delete(0, END)
        self.dirpath.insert(INSERT, self.path)
        for self.item in self.flist:
            if self.item.endswith(".py" or ".txt"):
                self.flist.append(self.item)

                self.lb.insert(tk.END, self.item)

                self.lb.focus()

        return self.flist

    def showcontent(self, x, event=None):
        for i in self.lb.curselection():
            file = self.lb.get(i)
            with open(file, "r") as file:
                file = file.read()
                self.textwidget.delete("1.0", tk.END)
                self.textwidget.insert(tk.END, file)

            return

    def ggtxt(self, tx):
        self.textwidget = tx
        gettxt = self.textwidget.get("1.0", tk.END)
        self.tx2.insert(tk.END, gettxt)

    def run(self, path, lb, event=None):
        self.path = path
        self.lb = lb

        try:
            x = int(self.lb.curselection()[0])
            file = self.lb.get(x)
        except IndexError:
            v = self.lb.get(x)
            v = self.lb.curselection()[0]
            file = self.lb.get(v)
        self.file = self.lb.get(ANCHOR)
        self.filepath = self.path + "/" + self.file
        runpy.run_path(self.filepath)

    def run2(self, path, lb):
        self.path = path
        self.lb = lb

        try:
            x = int(self.lb.curselection()[0])
            file = self.lb.get(x)
        except IndexError:
            v = self.lb.get(x)
            v = self.lb.curselection()[0]
            file = self.lb.get(v)
        self.file = self.lb.get(ANCHOR)
        self.filepath = self.path + "/" + self.file
        base = os.path.basename(self.filepath)


class TextFileComparator:
    def __init__(self, master):
        self.master = master
        self.text1 = None
        self.text2 = None
        self.output_text = None
        self.btfr = ttk.Frame(master, width=10, height=10)
        self.btfr.grid(row=0, column=0)
        self.txtfrm1 = ttk.Frame(self.master, width=60, height=60)
        self.txtfrm1.grid(row=0, column=1)
        self.txtfrm2 = ttk.Frame(self.master, width=60, height=60)
        self.txtfrm2.grid(row=0, column=2)
        self.txtfrm3 = ttk.Frame(self.master, width=50, height=15)
        self.txtfrm3.grid(row=12, column=0, columnspan=4)

    def create_gui(self):
        # Create text widgets for displaying the files
        self.text1 = ScrolledText(self.txtfrm1)
        self.text1.grid(row=0, column=0, sticky="nsew")

        self.text2 = ScrolledText(self.txtfrm2)
        self.text2.grid(row=0, column=0, sticky="nsew")

        # Create the output text widget
        self.output_text = tk.Text(self.txtfrm3, height=15)
        self.output_text.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Create a button to load the files
        load_button = tk.Button(self.btfr, text="Load Files", command=self.load_files)
        load_button.grid(row=2, column=0, sticky="w")

        # Create a button to compare the files
        compare_button = tk.Button(
            self.btfr, text="Compare", command=self.compare_files
        )
        compare_button.grid(row=3, column=0, sticky="w")

        # Create a button to clear all text widgets
        clear_button = tk.Button(
            self.btfr, text="Clear All", command=self.clear_text_widgets
        )
        clear_button.grid(row=4, column=0, sticky="w")

    def clear_text_widgets(self):
        self.text1.delete("1.0", tk.END)
        self.text2.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)

    def load_files(self):
        file1 = filedialog.askopenfilename(title="Select First File")
        if file1:
            with open(file1, "r") as f:
                content = f.read()
                self.text1.delete("1.0", tk.END)
                self.text1.insert(tk.END, content)

        file2 = filedialog.askopenfilename(title="Select Second File")
        if file2:
            with open(file2, "r") as f:
                content = f.read()
                self.text2.delete("1.0", tk.END)
                self.text2.insert(tk.END, content)

    def compare_files(self):
        # Get the content from the text widgets
        content1 = self.text1.get("1.0", tk.END)
        content2 = self.text2.get("1.0", tk.END)

        # Split the content into lines
        lines1 = content1.splitlines()
        lines2 = content2.splitlines()

        # Initialize a counter for differences
        diff_count = 0

        # Clear the text widgets
        self.text1.delete("1.0", tk.END)
        self.text2.delete("1.0", tk.END)

        # Compare the lines and highlight the differences
        diff_line_numbers = []
        for i, (line1, line2) in enumerate(zip(lines1, lines2), start=1):
            if line1 != line2:
                # Increase the difference count
                diff_count += 1
                diff_line_numbers.append(i)

                # Highlight the difference by inserting tags
                self.text1.insert(tk.END, line1 + "\n", "diff")
                self.text2.insert(tk.END, line2 + "\n", "diff")
            else:
                # Insert the lines without any difference
                self.text1.insert(tk.END, line1 + "\n")
                self.text2.insert(tk.END, line2 + "\n")

        # Add the remaining lines, if any
        if len(lines1) > len(lines2):
            for line in lines1[len(lines2) :]:
                self.text1.insert(tk.END, line + "\n")
                diff_count += 1
                diff_line_numbers.append(len(lines2) + 1)
        elif len(lines2) > len(lines1):
            for line in lines2[len(lines1) :]:
                self.text2.insert(tk.END, line + "\n")
                diff_count += 1
                diff_line_numbers.append(len(lines1) + 1)

        # Configure the tag for highlighting differences
        self.text1.tag_configure("diff", background="yellow")
        self.text2.tag_configure("diff", background="yellow")

        # Show the difference count and line numbers
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"Number of differences: {diff_count}\n")
        self.output_text.insert(tk.END, f"Lines in Text 1: {len(lines1)}\n")
        self.output_text.insert(tk.END, f"Lines in Text 2: {len(lines2)}\n")
        self.output_text.insert(tk.END, "Line numbers with differences: ")
        self.output_text.insert(tk.END, ", ".join(map(str, diff_line_numbers)))

    def update_info(self, event=None):
        self.content = self.text1.get("1.0", "end-1c")
        self.content2 = self.text2.get("1.0", "end-1c")

        lines = self.textwidget.index("end-1c").split(".")[0]
        words = len(self.content.split())
        characters = len(self.content)
        self.info_label = tk.Label(
            self.master, text="Lines: 0 | Words: 0 |\n Characters: 0"
        )
        self.info_label.grid(row=20, column=0)
        lines = self.text2.index("end-1c").split(".")[0]
        words = len(self.content.split())
        characters = len(self.content)
        self.info_label2 = tk.Label(
            self.master, text="Lines: 0 | Words: 0 |\n Characters: 0"
        )
        self.info_label2.grid(row=20, column=3)
        # Get the current text content
        self.content = self.textwidget.get("1.0", "end-1c")

        # Count the lines, words, and characters

        self.info_label.config(
            text=f"Lines: {lines} |  \n Words: {words} |\n Characters: {characters}"
        )

        # Update the label with the information

    def run(self):
        self.create_gui()


def setup_and_run():
    root = tk.Tk()
    app = Codeview(root)
    root.geometry("1200x1000")
    root.resizable(True, True)
    app.mainloop()


if __name__ == "__main__":
    setup_and_run()
