import tkinter as tk
from tkinter import ttk, Toplevel
from tkinter import messagebox as mb
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import filedialog
from string import punctuation
from collections import Counter
import re
from tkinter import Button, Frame, Entry, END, Canvas
import autopep8
from tkinter.scrolledtext import ScrolledText

import sys
import os

class AutoPEP8Formatter(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.current_directory = os.getcwd()

    def initUI(self):
        tk.Label(self.parent,text = "AutoPEP8 Formatter").grid(row=0 ,column=3)

        self.select_button = tk.Button(self.parent, text="Select Directory", command=self.select_directory)
        self.select_button.grid(row=1, column=1)

        self.file_listbox = tk.Listbox(self.parent)
        self.file_listbox.grid(row=2, column=1)

        self.format_button = tk.Button(self.parent, text="Format Selected File", command=self.format_selected_file)
        self.format_button.grid(row=6, column=3)

        self.textwidget = tk.Text(self.parent, height=10)
        self.textwidget.grid(row=10, column=3)
        

    def select_directory(self):
        self.current_directory = filedialog.askdirectory()
        if self.current_directory:
            self.file_listbox.delete(0, tk.END)
            self.textwidget.delete(1.0, tk.END)

            for filename in sorted(os.listdir(self.current_directory)):
                if filename.endswith('.py'):
                    self.file_listbox.insert(tk.END, filename)

    def format_selected_file(self):
        if not self.current_directory:
           mb.showinfo("Info", "Please select a directory first.")
           return

        selected = self.file_listbox.curselection()
        if not selected:
           mb.showinfo("Info", "Please select a file to format.")
           return

        filename = self.file_listbox.get(selected[0])
        file_path = os.path.join(self.current_directory, filename)

        keep_original =mb.askyesno("Keep Original", "Do you want to keep the original file?")
        self.format_file(file_path, original=keep_original)

    def format_file(self, file_path, original=False):
        try:
            with open(file_path, 'r') as file:
                original_code = file.read()

            formatted_code = autopep8.fix_code(original_code, options={'aggressive': 1})

            if original:
                base, ext = os.path.splitext(file_path)
                new_file_path = f"{base}_formatted{ext}"
                with open(new_file_path, 'w') as file:
                    file.write(formatted_code)
                self.output(f"Formatted and saved as new file: {os.path.basename(new_file_path)}")
            else:
                with open(file_path, 'w') as file:
                    file.write(formatted_code)
                self.output(f"Formatted: {os.path.basename(file_path)}")

        except Exception as e:
           mb.showerror("Error", f"An error occurred while formatting: {e}")

    def output(self, message):
        self.textwidget.insert(tk.END, message + '\n')
        self.textwidget.insert(tk.END)





class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        self.parent = parent
     
       
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.grid(row=0, column=0)

        self.frm1 = ttk.Frame(self.notebook, width=2100, height=1000)
        self.notebook.add(self.frm1, text="Text")
        self.textwidget = ScrolledText(self.frm1, height=45, width=100, bg="white", bd=10)
        self.textwidget.grid(row=0, column=0, sticky="nsew")
        self.textwidget.insert("1.0", "end-1c")
        self.frm2 = ttk.Frame(self.notebook, width=2100, height=1080)
        self.notebook.add(self.frm2, text="Canvas")
        self.frm3 = ttk.Frame(self.notebook, width=2100, height=1080)
        self.notebook.add(self.frm3, text="PEP8")
        self.autopep8 = AutoPEP8Formatter(self.frm3)
        self.canvas = tk.Canvas(self.frm2, width=100, height=10, bg="lavender")
        self.canvas.grid(row=2, column=0)
        self.info_label = tk.Label(self.frm1, text="  Lines: 0    | Words: 0       |  Characters: 0")
        self.info_label.grid(row=20, column=0)
        self.update_info()
        self.menubar = tk.Menu(self.parent, tearoff=False)
       
        self.file_menu = tk.Menu(self.menubar)
        self.edit_menu = tk.Menu(self.menubar)
        self.view_menu = tk.Menu(self.menubar)
        self.cursor_menu = tk.Menu(self.menubar)
        self.format_menu = tk.Menu(self.menubar)
        self.tool_menu = tk.Menu(self.menubar)
        self.text = self.textwidget.get("1.0", "end-1c")
        self.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(
            label="New", underline=1, command=lambda: self.clear()
        )
        self.file_menu.add_command(
            label="Open", underline=1, command=lambda: self.open_file()
        )
        self.file_menu.add_command(
            label="Save", underline=1, command=lambda: self.save_file()
        )
        self.file_menu.add_command(
            label="readlines", underline=1, command=lambda: self.readlines()
        )
        self.file_menu.add_command(label="-----", underline=1, command=self.quit)
        self.file_menu.add_command(label="-------", underline=1, command=self.quit)
        self.file_menu.add_command(label="Exit", underline=1, command=self.quit)
###################
        self.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(
            label="Select All",
            accelerator="Ctrl+A",
            compound="left",
            underline=0,
            command=lambda: self.textwidget.event_generate("<<SelectAll>>"),
        )
        self.edit_menu.add_command(
            label="Cut",
            accelerator="Ctrl+X",
            compound="left",
            underline=0,
            command=lambda: self.textwidget.event_generate("<<Cut>>"),
        )
        self.edit_menu.add_command(
            label="Copy",
            accelerator="Ctrl+C",
            compound="left",
            underline=0,
            command=lambda: self.textwidget.event_generate("<<Copy>>"),
        )
        self.edit_menu.add_command(
            label="Paste",
            accelerator="Ctrl+V",
            compound="left",
            underline=0,
            command=lambda: self.textwidget.event_generate("<<Paste>>"),
        )
        self.edit_menu.add_command(
            label="Undo",
            accelerator="Ctrl+Z",
            compound="left",
            underline=0,
            command=lambda: self.undo(),
        )
        self.edit_menu.add_command(
            label="Redo",
            accelerator="Ctrl+Y",
            compound="left",
            underline=0,
            command=lambda: self.redo(),
        )
        self.edit_menu.add_command(
            label="Find",
            accelerator="Ctrl+F",
            compound="left",
            underline=0,
            command=lambda: self.find(),
        )
        self.edit_menu.add_command(
            label="Replace",
            accelerator="Ctrl+R",
            compound="left",
            underline=0,
            command=lambda: self.replace(),
        )
        self.edit_menu.add_command(
            label="cleartags",
            accelerator="Ctrl+G",
            compound="left",
            underline=0,
            command=lambda: self.cleartags(),
        )
#######################
        self.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(
            label="----", compound="left", underline=0, command=None
        )
        self.view_menu.add_command(
            label="Backgrounbd Color",
            compound="left",
            underline=0,
            command=lambda: self.change_bg(),
        )
        self.view_menu.add_command(
            label="Foreground Color",
            compound="left",
            underline=0,
            command=lambda: self.change_fg(),
        )
        self.view_menu.add_command(
            label="Highlight Line",
            compound="left",
            underline=0,
            command=lambda: self.highlight_line(),
        )
        self.view_menu.add_command(
            label="Foreground Color",
            compound="left",
            underline=0,
            command=lambda: self.change_fg(),
            )
############################
        self.add_cascade(label="Cursor", menu=self.cursor_menu)
        self.cursor_menu.add_command(
            label="ahead_four_chars",
            underline=1,
            command=lambda: self.ahead_four_chars(),
            )
        self.cursor_menu.add_command(
            label="highlight_line", underline=1, command=lambda: self.highlight_line()
            )
        self.cursor_menu.add_command(
            label="back_four_chars", underline=1, command=lambda: self.back_four_chars()
            )
        self.cursor_menu.add_command(
            label="down_three_lines",
            underline=1,
            command=lambda: self.down_three_lines(),
        )
        self.cursor_menu.add_command(
            label="downlines", underline=1, command=lambda: self.downlines()
            )
        self.cursor_menu.add_command(
            label="tag alternating",
            underline=1,
            command=self.tag_alternating,
            )
        self.cursor_menu.add_command(
            label=" raise_selected",
            underline=1,
            command=lambda: self.raise_selected(),
            )

        self.cursor_menu.add_command(
            label="underline_selected",
            underline=1,
            command=lambda: self.underline_selected(),
            )

        self.cursor_menu.add_command(
            label="remove selected underline",
            underline=1,
            command=lambda: self.remove_underline(),
            )
        self.cursor_menu.add_command(label="update_info",underline=1, command=self.update_info,)



        self.cursor_menu.add_command(
            label="cursor to top of page",
            underline=1,
            command=self.cursor_to_top,)
        self.cursor_menu.add_command(
            label="cursor to bottem",
            underline=1,
            command=self.cursor_to_bottom,
            )
        self.cursor_menu.add_command(
                label="-----",
                underline=1,
                command=None,
                )













############################
        self.add_cascade(label="Format", menu=self.format_menu)

        self.format_menu.add_command(
        label="Indent",
        accelerator="Ctrl+[",
        compound="left",
        underline=0,
        command=lambda: self.indent(self.textwidget),
        )
        self.format_menu.add_command(
        label="Dedent",
        accelerator="Ctrl+[",
        compound="left",
        underline=0,
        command=lambda: self.dedent(self.textwidget),
        )
        self.format_menu.add_command(
        label="Insert Self make OOP",
        compound="left",
        underline=0,
        command=lambda: self.insert_selfs(self.textwidget),
        )
        self.format_menu.add_command(
        label=" highlight_line",
        compound="left",
        underline=0,
        command=self.highlight_line,
        )
        self.format_menu.add_command(
        label="Change funct to Method",
        compound="left",
        underline=0,
        command=lambda : self.insert_self_in_parentheses(self.textwidget),
        )
        self.format_menu.add_command(
        label="Auto PEP Format",
        compound="left",
        underline=0,
        command=self.format_file,
        )
        self.format_menu.add_command(
        label="-----",
        compound="left",
        underline=0,
        command=None,
        )
        self.format_menu.add_command(
        label="-------",
        compound="left",
        underline=0,
        command=None,
        )
        self.format_menu.add_command(
        label="------",
        compound="left",
        underline=0,
        command=None,
        )
        self.binding()



    def cursor_to_top(self):
        self.textwidget.mark_set("insert", "1.0")
        self.textwidget.see("insert")
    def cursor_to_bottom(self):
        self.textwidget.mark_set("insert", "end-1c")
        self.textwidget.see("insert")

    def cleartags(self):
        self.textwidget.tag_config("found", foreground="black", background="white")

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

    def select_all(self, event=None):
        self.textwidget.tag_add("sel", "1.0", tk.END)
        return "break"

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

    def quit(self):
        sys.exit(0)

    def clear(self):
        self.textwidget.delete("1.0", tk.END)

    def cleare1(self):
        self.e1.delete(0, END)

    def change_bg(self):
        (triple, hexstr) = askcolor()
        if hexstr:
            self.textwidget.config(bg=hexstr)

    def change_fg(self):
        (triple, hexstr) = askcolor()

        if hexstr:
            self.textwidget.config(fg=hexstr)

    def command(self):
        pass

    def open_file(self):
        """Open a file for editing."""
        filepath = askopenfilename(
            filetypes=[
                ("Python Scripts", "*.py"),
                ("Text Files", "*.txt"),
                ("All Files", "*.*"),
            ]
        )
        if not filepath:
            return
        self.textwidget.delete(1.0, tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.read()
            self.textwidget.insert(tk.END, text)

    def save_file(self):
        filepath = asksaveasfilename(
            defaultextension="py",
            filetypes=[("All Files", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = self.textwidget.get(1.0, tk.END)
            output_file.write(text)

    def readlines(self):
        filepath = askopenfilename(filetypes=[("All Files", "*.*")])
        if not filepath:
            return
        self.textwidget.delete("1.0", tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.readlines()
            self.textwidget.insert(tk.END, text)
            return filepath2

    def ggtxt(self, textwidget):
        gettxt = self.tx.get("1.0", tk.END)
        self.textwidget.insert(tk.END, gettxt)

    def edit2(self, name):
        runpy.run_path(path_name="name")

    def find(self):
        top = Toplevel()
        label1 = tk.Label(top, text="Find").grid(row=1, column=1)
        entry1 = tk.Entry(top, width=15, bd=12, bg="cornsilk")
        entry1.grid(row=2, column=1)

        def finder():
            # remove tag 'found' from index 1 to END
            self.textwidget.tag_remove("found", "1.0", END)
            entry = entry1.get()

            if entry1:
                idx = "1.0"
                while 1:
                    # searches for desired string from index 1
                    idx = self.textwidget.search(entry, idx, nocase=1, stopindex=END)

                    if not idx:
                        break

                    # last index sum of current index and
                    # length of text
                    lastidx = "% s+% dc" % (idx, len(entry))

                    # overwrite 'Found' at idx
                    self.textwidget.tag_add("found", idx, lastidx)
                    idx = lastidx

                # mark located string as red

                self.textwidget.tag_config(
                    "found", background="purple", foreground="yellow"
                )

        self.find_btn = tk.Button(top, text="Find", bd=8, command=finder)
        self.find_btn.grid(row=8, column=1)
        entry1.focus_set()

    def replace(self):
        top = Toplevel()
        label1 = tk.Label(top, text="Find").grid(row=1, column=1)
        entry1 = tk.Entry(top, width=15, bd=12, bg="cornsilk")
        entry1.grid(row=2, column=1)
        label2 = tk.Label(top, text="Replace With ").grid(row=3, column=1)
        entry2 = tk.Entry(top, width=15, bd=12, bg="seashell")
        entry2.grid(row=5, column=1)

        def replacer():
            # remove tag 'found' from index 1 to END
            self.textwidget.tag_remove("found", "1.0", END)

            # returns to widget currently in focus
            self.fin = entry1.get()
            self.repl = entry2.get()

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

        self.replace_btn = tk.Button(top, text="Find & Replace", bd=8, command=replacer)
        self.replace_btn.grid(row=8, column=1)
        entry1.focus_set()

   

    def toggle_highlight(self, event=None):
        val = hltln.get()

        undo_highlight() if not val else highlight_line()

    def undo_highlight(self):
        self.self.textwidget.tag_remove("active_line", "1.0", tk.END)

    def update_info(self, event=None):
        # Get the current text content
        self.content = self.textwidget.get("1.0", "end-1c")

        # Count the lines, words, and characters
        lines = self.textwidget.index("end-1c").split(".")[0]
        words = len(self.content.split())
        characters = len(self.content)

        # Get the current cursor position (line and column)
        cursor_position = self.textwidget.index("insert")
        cursor_line, cursor_column = cursor_position.split(".")

        # Update the label with the new information
        self.info_label.config(
            text=f"Lines: {lines} | Words: {words} | Characters: {characters} | Cursor Position: Line {cursor_line}, Column {cursor_column}"
        )

    def format_file(self, file_path, original=False):
        try:
            with open(file_path, 'r') as file:
                original_code = file.read()

            formatted_code = autopep8.fix_code(original_code, options={'aggressive': 1})

            if original:
                base, ext = os.path.splitext(file_path)
                new_file_path = f"{base}_formatted{ext}"
                with open(new_file_path, 'w') as file:
                    file.write(formatted_code)
                self.output(f"Formatted and saved as new file: {os.path.basename(new_file_path)}")
            else:
                with open(file_path, 'w') as file:
                    file.write(formatted_code)
                self.output(f"Formatted: {os.path.basename(file_path)}")

        except Exception as e:
           mb.showerror("Error", f"An error occurred while formatting: {e}")

    def output(self, message):
        self.textwidget.insert(tk.END, message + '\n')
        self.textwidget.insert(tk.END)




    def highlight_line(self, event=None):
        start = str(self.textwidget.index(tk.INSERT)) + " linestart"
        end = str(self.textwidget.index(tk.INSERT)) + " lineend"
        self.textwidget.tag_add("sel", start, end)

        return "break"

    def highlight_word(self, event=None):
        word_pos = str(self.textwidget.index(tk.INSERT))
        start = word_pos + " wordstart"
        end = word_pos + " wordend"
        self.textwidget.tag_add("sel", start, end)

        return "break"

    def down_three_lines(self, event=None):
        current_cursor_index = str(self.textwidget.index(tk.INSERT))
        new_position = current_cursor_index + "+3l"
        self.textwidget.mark_set(tk.INSERT, new_position)

        return "break"

    def back_four_chars(self, event=None):
        current_cursor_index = str(self.textwidget.index(tk.INSERT))
        new_position = current_cursor_index + "-5c"
        self.textwidget.mark_set(tk.INSERT, new_position)

        return "break"

    def ahead_four_chars(self, event=None):
        current_cursor_index = str(self.textwidget.index(tk.INSERT))
        new_position = current_cursor_index + "+5c"
        self.textwidget.mark_set(tk.INSERT, new_position)

        return "break"

    def tag_alternating(self, event=None):
        for i in range(0, 27, 2):
            index = "1." + str(i)
            end = index + "+1c"
            self.textwidget.tag_add("odd", index, end)

        self.textwidget.tag_configure("odd", foreground="orange")

        return "break"

    def raise_selected(self, event=None):
        self.textwidget.tag_configure("raise", offset=5)
        selection = self.textwidget.tag_ranges("sel")
        self.textwidget.tag_add("raise", selection[0], selection[1])

        return "break"

    def underline_selected(self, event=None):
        self.textwidget.tag_configure("underline", underline=1)
        selection = self.textwidget.tag_ranges("sel")
        self.textwidget.tag_add("underline", selection[0], selection[1])

        return "break"

    def remove_underline(self, event=None):
        selection = self.textwidget.tag_ranges("sel")
        if selection:  # Check if there is a selection
            self.textwidget.tag_remove("underline", selection[0], selection[1])



    def downlines(self):
        self.content = "self."
        current_cursor_index = str(self.textwidget.index(tk.INSERT))
        new_position = current_cursor_index + "+1l"
        self.textwidget.mark_set(tk.INSERT, new_position)

        current_cursor_index = str(self.textwidget.index(tk.INSERT))
        new_position = current_cursor_index + "+5c"
        self.textwidget.mark_set(tk.INSERT, new_position)
        self.textwidget.insert(new_position, self.content)

        current_cursor_index = str(self.textwidget.index(tk.INSERT))
        new_position = current_cursor_index + "+1l"
        self.textwidget.mark_set(tk.INSERT, new_position)
        current_cursor_index = str(self.textwidget.index(tk.INSERT))
        new_position = current_cursor_index + "+5c"
        self.textwidget.mark_set(tk.INSERT, new_position)
        self.textwidget.insert(END, self.content)
        current_cursor_index = str(self.textwidget.index(tk.INSERT))
        new_position = current_cursor_index + "+1l"
        self.textwidget.mark_set(tk.INSERT, new_position)
        current_cursor_index = str(self.textwidget.index(tk.INSERT))
        new_position = current_cursor_index + "+5c"
        self.textwidget.mark_set(tk.INSERT, new_position)
        self.textwidget.insert(new_position, self.content)
    def indent(self, textwidget):
        selected_text = textwidget.get("sel.first", "sel.last")
        if selected_text:
            # Add four spaces to the beginning of each line
            indented_text = "\n".join(
                f"    {line}" for line in selected_text.split("\n")
            )
            textwidget.replace("sel.first", "sel.last", indented_text)

    def dedent(self,textwidget):
        selected_text = textwidget.get("sel.first", "sel.last")
        if selected_text:
            # Remove four spaces from the beginning of each line if present
            dedented_text = "\n".join(
                line[4:] if line.startswith("    ") else line
                for line in selected_text.split("\n")
            )
            textwidget.replace("sel.first", "sel.last", dedented_text)

    

  
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

    def insert_self_in_parentheses(self, textwidget):
        start_index = textwidget.index("sel.first")
        end_index = textwidget.index("sel.last")

        selected_text = textwidget.get(start_index, end_index)
        modified_lines = []

        for line in selected_text.split("\n"):
            if line.strip():
                modified_line = line.replace("()", "(self):")  # Replace () with (self)
            else:
                modified_line = line
            modified_lines.append(modified_line)

        modified_text = "\n".join(modified_lines)
        textwidget.delete(start_index, end_index)
        textwidget.insert(start_index, modified_text)
    def binding(self):
        self.textwidget.bind("<KeyRelease>", self.update_info)
        self.textwidget.bind("<Control-h>", self.highlight_line)
        self.textwidget.bind("<Control-w>", self.highlight_word)
        self.textwidget.bind("<Control-d>", self.down_three_lines)
        self.textwidget.bind("<Control-b>", self.back_four_chars)

        self.textwidget.bind("<Control-t>", self.tag_alternating)
        self.textwidget.bind("<Control-r>", self.raise_selected)
        self.textwidget.bind("<Control-u>", self.underline_selected)

   


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        menubar = MenuBar(self)
        self.config(menu=menubar)


if __name__ == "__main__":
    app = App()
    app.mainloop()
