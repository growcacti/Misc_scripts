import tkinter as tk
from tkinter import ttk, INSERT,END,font
from tkinter import messagebox as mb
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
from string import punctuation
from tkinter.font import Font, families

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


#####################################################################
######################################################################


class TextWidget_Info:
    def __init__(self, parent, textwidget):
        self.parent = parent
        self.tx = textwidget
        self.info_label = tk.Label(self.parent, text="Lines: 0  \n | Words: 0   \n| Characters: 0 \n| Cursor Position: Line 1   , Column 0       ")
        self.info_label.grid(row=30, column=0)

        # Bind to text change and cursor movement events
        self.tx.bind("<KeyRelease>", self.update_info)
        self.tx.bind("<ButtonRelease-1>", self.update_info)
        self.tx.bind("<<Modified>>", self.on_text_modified)
        self.tx.bind("<ButtonRelease-2>", self.update_info)
    def on_text_modified(self, event):
        if self.tx.edit_modified():
            self.update_info(event)
            self.tx.edit_modified(False)

    def update_info(self, event=None):
        # Get the current text content
        content = self.tx.get("1.0", "end-1c")

        # Count the lines, words, and characters
        lines = self.tx.index("end-1c").split(".")[0]
        words = len(content.split())
        characters = len(content)

        # Get the current cursor position (line and column)
        cursor_position = self.tx.index("insert")
        cursor_line, cursor_column = cursor_position.split(".")

        # Update the label with the new information
        self.info_label.config(
            text=f"Lines: {lines}   \n| Words: {words}       \n| Characters: {characters}     \n | Cursor Position: Line {cursor_line}, Column {cursor_column}"
        )

############################################################################
###############################################################
class FontBar():
    def __init__(self, parent,text):
        
        self.path = os.getcwd()
        self.text = text
        self.parent = parent
        self.fram = tk.Frame(self.parent)
        self.fram.grid(row=0, column=0, sticky="w")  # Align with the frame
       
        self.fram2 = ttk.Frame(self.parent)
        self.fram2.grid(row=3,column=0)
        self.toolbarfrm = tk.Frame(self.fram, width=10, height=100)
        self.toolbarfrm.grid(row=0, column=0, columnspan=5, sticky="w")

##        self.shortcutbar = tk.Frame(self.fram2, height=10, width=80)
##        self.shortcutbar.grid(row=0, column=1, columnspan=5, sticky="ew")
        self.font_config()

    def font_config(self):
        self.toolbar = tk.Canvas(self.toolbarfrm, bg="seashell")
        self.toolbar.grid(row=0, column=0, columnspan=5, sticky="ew")
        self.toolbar.config(width=300, height=60)
        self.values = [n for n in range(2, 120, 2)]

        self.font_family = tk.StringVar(
            self.toolbar
        )  # string variable for storing value of font options from user
        self.fontbox = ttk.Combobox(
            self.toolbar, width=50, textvariable=self.font_family, state="readonly"
        )  # combobox
        self.fontbox["values"] = values=families()
        self.fontbox.set("Liberation Serif")
        self.fontbox.grid(row=0, column=0)
        # font box ends here

        # font size box
        self.size = tk.IntVar(self.toolbar)
        self.fontsize = ttk.Combobox(
            self.toolbar, width=20, values=self.values, textvariable=self.size
        )

        self.size.set(12)
        self.fontsize.grid(row=0, column=1)

        self.current_font_family = self.font_family
        self.current_font_size = self.size
        self.text.configure(font=("Liberation Serif", 12))
        self.fontbox.bind("<<ComboboxSelected>>", lambda event: self.change_font)
        self.fontsize.bind("<<ComboboxSelected>>", lambda event: self.change_font_size)
        self.fontbox.bind("<ButtonRelease-1>", lambda event: self.change_font)

        self.font_btn = tk.Button(
            self.toolbar,
            text=" Set Font",
            bd=3,
            bg="blue violet",
            command=lambda: self.change_fonttype(
                self.fontbox.get(), self.fontsize.get()
            ),
        )
        self.font_btn.grid(row=1, column=0)
        self.font_btn2 = tk.Button(
            self.toolbar,
            text="set size Font",
            bd=3,
            bg="blue violet",
            command=lambda: self.change_font_size(self.fontsize.get()),
        )
        self.font_btn2.grid(row=1, column=1)
        self.color_btn = tk.Button(
            self.toolbar,
            text="Font color",
            bd=2,
            bg="goldenrod",
            command=lambda: self.change_font_color(),
        )
        self.color_btn.grid(row=1, column=2)
        self.bold_btn = tk.Button(
            self.toolbar, text="B", bd=3, bg="violet red", command=self.change_bold
        )
        self.bold_btn.grid(row=1, column=3)
        self.bold_btn2 = tk.Button(
            self.toolbar,
            text="All B",
            bd=2,
            bg="violet red",
            command=self.changeall_bold,
        )
        self.bold_btn2.grid(row=0, column=3)
        self.italic_btn = tk.Button(
            self.toolbar, text="i", bd=3, bg="lawn green", command=self.change_italic
        )
        self.italic_btn.grid(row=1, column=4)
        self.italic_btn2 = tk.Button(
            self.toolbar,
            text="All i",
            bd=3,
            bg="lawn green",
            command=self.changeall_italic,
        )
        self.italic_btn2.grid(row=0, column=4)
        self.underline_btn = tk.Button(
            self.toolbar, text="_", bd=3, bg="yellow", command=self.underline_text
        )
        self.underline_btn.grid(row=1, column=5)
        self.underline_btn2 = tk.Button(
            self.toolbar,
            text="All _",command=self.changeall_underline,
        )
        self.underline_btn2.grid(row=0, column=5)
        self.align_left_btn = tk.Button(
            self.toolbar, text="LT",command=self.align_left
        )
        self.align_left_btn.grid(row=1, column=6)
        self.align_center_btn = tk.Button(
            self.toolbar, text="CT", bd=3, bg="cyan", command=self.align_center
        )
        self.align_center_btn.grid(row=1, column=7)
        self.align_right_btn = tk.Button(
            self.toolbar, text="RT", bd=3, bg="light pink", command=self.align_right
        )
        self.align_right_btn.grid(row=1, column=8)
        self.clear_btn = tk.Button(
            self.toolbar, text="clear", bd=3, bg="light pink", command=self.clear
        )
        self.clear_btn.grid(row=0, column=8)
        # function to change font family

    def change_font(self, event=None):
        self.current_font_family = font_family.get()
        self.text.configure(font=(self.current_font_family, self.current_font_size))
        self.fontsize.bind(
            "<<ComboboxSelected>>", lambda event: self.change_font_size()
        )
        self.fontbox.bind("<<ComboboxSelected>>", lambda event,: self.change_font())

    def change_fonttype(self, type, size):
        self.type = self.fontbox.get()
        self.size = self.fontsize.get()
        self.text.configure(font=(self.type, self.size))

    # change font size
    def change_font_size(self, size, event=None):
        self.fontbox.bind("<<ComboboxSelected>>", lambda event: self.change_font_size)
        self.size = size
        self.current_font_size = self.fontsize.get()
        self.text.configure(font=(self.fontbox.get(), self.size))
        self.fontbox.bind("<<ComboboxSelected>>", lambda event: self.change_font_size)

    def change_bold(self, event=None):
        """toggle only selected text"""
        try:
            self.current_tags = self.text.tag_names("sel.first")
            if "bold" in self.current_tags:
                self.text.tag_remove("bold", "sel.first", "sel.last")
            else:
                self.text.tag_add("bold", "sel.first", "sel.last")
                bold_font = tk.font.Font(self.text, self.text.cget("font"))
                bold_font.configure(weight="bold")
                self.text.tag_configure("bold", font=bold_font)
        except tk.TclError as ex:
            print(ex)

    # change to italic
    def change_italic(self, event=None):
        """making italic the selected text"""
        try:
            self.current_tags = self.text.tag_names("sel.first")
            if "italic" in self.current_tags:
                self.text.tag_remove("italic", "sel.first", "sel.last")
            else:
                self.text.tag_add("italic", "sel.first", "sel.last")
                italic_font = tk.font.Font(self.text, self.text.cget("font"))
                italic_font.configure(slant="italic")
                self.text.tag_configure("italic", font=italic_font)
        except tk.TclError:
            pass

    def underline_text(self, event=None):
        try:
            self.current_tags = self.text.tag_names("sel.first")
            if "underline" in self.current_tags:
                self.text.tag_remove("underline", "sel.first", "sel.last")
            else:
                self.text.tag_add("underline", "sel.first", "sel.last")
                underline_font = tk.font.Font(self.text, self.text.cget("font"))
                underline_font.configure(underline=1)
                self.text.tag_configure("underline", font=underline_font)
        except tk.TclError:
            pass

    # change font color
    def change_font_color(self, event=None):
        try:
            (rgb, hx) = tk.colorchooser.askcolor()
            self.text.tag_add("color", "sel.first", "sel.last")
            self.text.tag_configure("color", foreground=hx)
            # self.text.tag_configure(rgb, foreground=hx)
        except tk.TclError as ex:
            print(ex)

    # left alignment
    def align_left(self, event=None):
        text_content = self.text.get(1.0, "end")
        self.text.tag_config("left", justify=tk.LEFT)
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.INSERT, text_content, "left")

    # center alignment
    def align_center(self, event=None):
        text_content = self.text.get(1.0, "end")
        self.text.tag_config("center", justify=tk.CENTER)
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.INSERT, text_content, "center")

    # text alignment right
    def align_right(self, event=None):
        text_content = self.text.get(1.0, "end")
        self.text.tag_config("right", justify=tk.RIGHT)
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.INSERT, text_content, "right")

    def changeall_bold(self):
        self.text.tag_add("bold", "1.0", "end")
        bold_font = tk.font.Font(self.text, self.text.cget("font"))
        bold_font.configure(weight="bold")
        self.text.tag_configure("bold", font=bold_font)

    def changeall_italic(self):
        self.text.tag_add("italic", "1.0", "end")
        italic_font = tk.font.Font(self.text, self.text.cget("font"))
        italic_font.configure(slant="italic")
        self.text.tag_configure("italic", font=italic_font)

    def changeall_underline(self):
        self.text.tag_add("underline", "1.0", "end")
        underline_font = tk.font.Font(self.text, self.text.cget("font"))
        underline_font.configure(underline=1)
        self.text.tag_configure("underline", font=underline_font)

    def destory(self):
        self.fram.grid_forget()

    def clear(self):
        self.text.delete("1.0", tk.END)
#####################################################################################
#####################################################################################   
###############################################################################

class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        self.parent = parent
        self.bar_frm = tk.Frame(self.parent, width=500, height=50)
        self.bar_frm.grid(row=0, column=0, sticky="ew")
        self.parent.columnconfigure(0, weight=1)  # This makes the column expandable
        
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.grid(row=4, column=0)
        self.frm1 = ttk.Frame(self.notebook, width=2100, height=1000)
        self.notebook.add(self.frm1, text="View")
        self.txtfrm = tk.Frame(self.frm1, width=200, height=40)
        self.txtfrm.grid(row=0, column=2)
        self.tx = ScrolledText(self.txtfrm, bg="white", bd=12, height=35,width=250,)
        self.tx.grid(row=0, column=2,sticky="w")
        self.textwidget = self.tx
        self.fontbar = FontBar(self.bar_frm, self.textwidget)
      
        self.path = os.getcwd()
        self.lbfrm = tk.Frame(self.frm1, width=5, height=30)
        self.lbfrm.grid(row=0, column=1)
        self.lb = tk.Listbox(self.lbfrm, bg="cyan2", bd=12, width=35, height=35, exportselection=False, selectmode=tk.SINGLE,)
        self.lb.grid(row=0, column=0)
        self.lb.focus()
        self.lb.configure(selectmode="")
        self.lb.bind("<Double-Button-1>", self.listing)
        self.lb.bind("<<ListboxSelect>>", self.showcontent)
        self.lb.bind("<Double-Button-2>", lambda event: self.run(self.lb))
        self.lb.bind("<<ListboxSelect>>", lambda event: self.listing(event))
        self.curtxt = None
        self.x = self.lb.curselection()
        self.fr_buttons = tk.Frame(self.frm1, relief=tk.RAISED)
        self.fr_buttons.grid(row=0,column=0,sticky="ns")
        self.btn_1 = tk.Button(self.fr_buttons, text="change dir", bd=3,command=self.newdirlist)
        self.btn_1.grid(row=1, column=0)
        self.btn_2 = tk.Button(self.fr_buttons,text="refresh dir list",bd=3,command=self.makedirlist)
        self.btn_2.grid(row=2, column=0)
        self.btn_3 = tk.Button(self.fr_buttons, text="---",bd=3, command=lambda:None)
        self.btn_3.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.btn_grab = tk.Button(self.fr_buttons, text="Send to Editor Tab",bd=6, command=self.ggtxt)
        self.btn_grab.grid(row=4, column=0)
        self.btn_grab2 = tk.Button(self.fr_buttons, text="Send to Text Tab", bd=6,command=self.ggtxt2)
        self.btn_grab2.grid(row=6,column=0)
        self.dirpath = tk.Entry(self.fr_buttons, bd=10, width=40)
        self.dirpath.grid(row=7,column=0)
        self.dirpath.insert(0, self.path)
        self.frm2 = ttk.Frame(self.notebook, width=2100, height=1000)
        self.notebook.add(self.frm2, text="Text")
        self.text1 = ScrolledText(self.frm2, height=30, width=60, bg="white", bd=10)
        self.text1.grid(row=4, column=1, sticky="nsew")
        self.text1.insert("1.0", "end-1c")
        self.frm3 = ttk.Frame(self.notebook, width=2100, height=1080)
        self.notebook.add(self.frm3, text="Editor")
        self.frm4 = ttk.Frame(self.notebook, width=2100, height=1080)
        self.notebook.add(self.frm4, text="Compare Text")
        self.textcompare = TextFileComparator(self.frm4)
        self.textcompare.run()
        self.frm5 = ttk.Frame(self.notebook, width=2100, height=1080)
        self.notebook.add(self.frm5, text="Unicode View")
        uni = UnicodeListGeneratorApp(self.frm5)
        self.frm6 = ttk.Frame(self.notebook, width=2100, height=1080)
        self.notebook.add(self.frm6, text="6")
        self.frm7 = ttk.Frame(self.notebook, width=2100, height=1080)
        self.notebook.add(self.frm7, text="7")

        self.frm8 = ttk.Frame(self.notebook, width=2100, height=1080)
        self.notebook.add(self.frm8, text="8")
        self.frm9 = ttk.Frame(self.notebook, width=2100, height=1080)
        self.notebook.add(self.frm9, text="9")
        self.text2 = ScrolledText(self.frm3, height=40, width=100, bg="white", bd=10)
        self.text2.grid(row=5, column=1, sticky="nsew")
        self.text2.insert("1.0", "end-1c")
##        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.frm4 = ttk.Frame(self.notebook, width=2100, height=1080)
        self.notebook.add(self.frm4, text="PEP8")
        self.autopep8 = AutoPEP8Formatter(self.frm4)
        self.info1 = TextWidget_Info(self.frm1, self.tx)
        self.info2 = TextWidget_Info(self.frm2, self.text1)
        self.info3 = TextWidget_Info(self.frm3, self.text2)
        self.textwidgets = [self.tx, self.text1, self.text2]
        self.fontbar = FontBar(self.bar_frm,self.textwidget)
        self.menubar = tk.Menu(self.parent, tearoff=False)
        
        self.file_menu = tk.Menu(self.menubar)
        self.edit_menu = tk.Menu(self.menubar)
        self.view_menu = tk.Menu(self.menubar)
        self.cursor_menu = tk.Menu(self.menubar)
        self.format_menu = tk.Menu(self.menubar)
        self.tool_menu = tk.Menu(self.menubar)

        
        self.lb.bind("<Double-Button-1>", self.listing)
        self.lb.bind("<<ListboxSelect>>", self.showcontent)
        self.lb.bind("<<ListboxSelect>>", lambda event: self.listing(event))
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
        self.file_menu.add_command(label="Exit", underline=1, command=self.exit_application)
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
            label="Ahead_four_chars",
            underline=1,
            command=lambda: self.ahead_four_chars(),
            )
        self.cursor_menu.add_command(
            label="Highlight_line", underline=1, command=lambda: self.highlight_line()
            )
        self.cursor_menu.add_command(
            label="Back_four_chars", underline=1, command=lambda: self.back_four_chars()
            )
        self.cursor_menu.add_command(
            label="Down_three_lines",
            underline=1,
            command=lambda: self.down_three_lines(),)

        self.cursor_menu.add_command(
            label="Down_six_lines",
            underline=1,
            command=lambda: self.down_six_lines(),
        )

        
        self.cursor_menu.add_command(
            label="Downlines", underline=1, command=lambda: self.downlines()
            )
        self.cursor_menu.add_command(
            label="Tag alternating",
            underline=1,
            command=self.tag_alternating,
            )
       
        self.cursor_menu.add_command(
            label="Cursor to top of page",
            underline=1,
            command=self.cursor_to_top,)
        self.cursor_menu.add_command(
            label="Cursor to bottom",
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
        self.binding()
        self.makedirlist()
        self.update_info()
##################################################################
#######################METHODS##########################################


    def update_info(self):
       
        self.info1.update_info()
        self.info2.update_info()
        self.info3.update_info()
            

    def makedirlist(self):
        self.path = os.getcwd()
        self.flist = os.listdir(self.path)
        self.dirpath.delete(0, END)
        self.dirpath.insert(INSERT, self.path)
       
        for self.item in self.flist:
            if self.item.endswith(".py" or ".txt"):
                self.lb.insert(tk.END, self.item)

                self.lb.focus()
    def newdirlist(self):
        self.path = askdirectory()
        os.chdir(self.path)
        self.flist = os.listdir(self.path)
        self.lb.delete(0, tk.END)
        self.dirpath.delete(0, END)
        self.flist = os.listdir(self.path)
       
        self.dirpath.insert(INSERT, self.path)
        for self.item in self.flist:
           if self.item.endswith(".py") or self.item.endswith(".txt"):
               self.lb.insert(tk.END, self.item)
               self.lb.focus()
               return self.path, self.flist                



    def listing(self, event=None):
        self.flist = os.listdir(self.path)
        self.dirpath.delete(0, END)
        self.dirpath.insert(INSERT, self.path)

        for self.item in self.flist:
            if self.item.endswith(".py" or ".txt"):
                self.lb.insert(tk.END, self.item)

                self.lb.focus()

        
        if event:
            x = int(self.lb.curselection()[0]) if self.lb.curselection() else None
        else:
            # No event, use the first item as default or handle no selection
            x = 0 if self.lb.size() > 0 else None
        if x is not None:
            file = self.lb.get(x)
            with open(file, "r") as file:
                content = file.read()
                self.tx.delete("1.0", tk.END)
                self.tx.insert(tk.END, content)
        else:
            self.tx.delete("1.0", tk.END)
            self.tx.insert(tk.END, "Please select a file to display its content.")

                      

   

    def showcontent(self, x, event=None):
        for i in self.lb.curselection():
            file = self.lb.get(i)
            with open(file, "r") as file:
                file = file.read()
                self.textwidget.delete("1.0", tk.END)
                self.textwidget.insert(tk.END, file)
                return

    def ggtxt(self):
      
        gettxt = self.tx.get("1.0", tk.END)
        self.text2.delete("1.0", tk.END)
        self.text2.insert(tk.END, gettxt)

    
    def ggtxt2(self):
      
        gettxt = self.tx.get("1.0", tk.END)
        self.text1.delete("1.0", tk.END)
        self.text1.insert(tk.END, gettxt)

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



       

    def on_tab_changed(self, event=None):
        # Get the currently selected tab index
        selected_index = self.notebook.index(self.notebook.select())

        # Assign the corresponding text widget to self.textwidget
        if selected_index == 0:  # Assuming this index corresponds to self.frm1
            self.textwidget = self.tx
        elif selected_index == 1:  # Assuming this index corresponds to self.frm2
            self.textwidget = self.text1
        elif selected_index == 2:  # Assuming this index corresponds to self.frm3
            self.textwidget = self.text2
        else:
            self.textwidget = None  # or any default widget
    def can_respond(self, widget):
        # Check if the widget is enabled
        if str(widget['state']) == 'disabled':
            return False

        # Check if the widget is visible
        if not widget.winfo_ismapped():
            return False

        # Check for specific content conditions
        content = widget.get("1.0", "end-1c")
        if some_specific_condition(content):  # Replace with your condition
            return False

        # Check if the widget has focus
        if widget is not self.focus_get():
            return False

        return True


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

    def exit_application(self):
        """ Method to exit application """
        self.parent.destroy()

        sys.exit()
           

    def readlines(self):
        filepath = askopenfilename(filetypes=[("All Files", "*.*")])
        if not filepath:
            return
        self.textwidget.delete("1.0", tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.readlines()
            self.textwidget.insert(tk.END, text)
            return filepath2

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

            
            self.textwidget.tag_config("found", foreground="green", background="yellow")

        self.replace_btn = tk.Button(top, text="Find & Replace", bd=8, command=replacer)
        self.replace_btn.grid(row=8, column=1)
        entry1.focus_set()

   

    def toggle_highlight(self, event=None):
        val = hltln.get()

        undo_highlight() if not val else highlight_line()

    def undo_highlight(self):
        self.self.textwidget.tag_remove("active_line", "1.0", tk.END)

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

    def down_six_lines(self, event=None):
        current_cursor_index = str(self.textwidget.index(tk.INSERT))
        new_position = current_cursor_index + "+6l"
        self.textwidget.mark_set(tk.INSERT, new_position)

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
        self.textwidget.bind("<KeyRelease>",self.info1.on_text_modified)
        self.tx.bind("<KeyRelease>",self.info2.on_text_modified)
##        self.textwidget.bind("<KeyRelease>"),self.info3.on_text_modified)
        self.textwidget.bind("<Control-h>", self.highlight_line)
        self.textwidget.bind("<Control-w>", self.highlight_word)
        self.textwidget.bind("<Control-d>", self.down_three_lines)
        self.textwidget.bind("<Control-b>", self.back_four_chars)
        self.textwidget.bind("<Control-t>", self.tag_alternating)
       
class TextFileComparator:
    def __init__(self, parent):
        self.parent = parent
        self.text1 = None
        self.text2 = None
        self.output_text = None
        self.btfr = ttk.Frame(parent, width=10, height=10)
        self.btfr.grid(row=0, column=0)
        self.txtfrm1 = ttk.Frame(self.parent, width=60, height=60)
        self.txtfrm1.grid(row=0, column=1)
        self.txtfrm2 = ttk.Frame(self.parent, width=60, height=60)
        self.txtfrm2.grid(row=0, column=2)
        self.txtfrm3 = ttk.Frame(self.parent, width=50, height=15)
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
            self.btfr, text="Clear All", command=self.clear_textwidgets
        )
        clear_button.grid(row=4, column=0, sticky="w")

    def clear_textwidgets(self):
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
            self.parent, text="Lines: 0 | Words: 0 |\n Characters: 0"
        )
        self.info_label.grid(row=20, column=0)
        lines = self.text2.index("end-1c").split(".")[0]
        words = len(self.content.split())
        characters = len(self.content)
        self.info_label2 = tk.Label(
            self.parent, text="Lines: 0 | Words: 0 |\n Characters: 0"
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


class TextFileComparator:
    def __init__(self, parent):
        self.parent = parent
        self.text1 = None
        self.text2 = None
        self.output_text = None
        self.btfr = ttk.Frame(parent, width=10, height=10)
        self.btfr.grid(row=0, column=0)
        self.txtfrm1 = ttk.Frame(self.parent, width=60, height=60)
        self.txtfrm1.grid(row=0, column=1)
        self.txtfrm2 = ttk.Frame(self.parent, width=60, height=60)
        self.txtfrm2.grid(row=0, column=2)
        self.txtfrm3 = ttk.Frame(self.parent, width=50, height=15)
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
            self.btfr, text="Clear All", command=self.clear_textwidgets
        )
        clear_button.grid(row=4, column=0, sticky="w")

    def clear_textwidgets(self):
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
            self.parent, text="Lines: 0 | Words: 0 |\n Characters: 0"
        )
        self.info_label.grid(row=20, column=0)
        lines = self.text2.index("end-1c").split(".")[0]
        words = len(self.content.split())
        characters = len(self.content)
        self.info_label2 = tk.Label(
            self.parent, text="Lines: 0 | Words: 0 |\n Characters: 0"
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


class UnicodeListGeneratorApp:
    def __init__(self, parent):
        self.parent = parent
        listbox_font = font.Font(family="Helvetica", size=48)     
        # Create and place labels, entries, and button
        start_label = ttk.Label(self.parent, text="Start (hex):")
        start_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

        end_label = ttk.Label(self.parent, text="End (hex):")
        end_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

        self.start_entry = ttk.Entry(self.parent, width=10)
        self.start_entry.grid(row=1, column=1, padx=10, pady=5)

        self.end_entry = ttk.Entry(self.parent, width=10)
        self.end_entry.grid(row=2, column=1, padx=10, pady=5)

        generate_button = ttk.Button(self.parent, text="Generate", command=self.generate_unicode)
        generate_button.grid(row=3, column=0, columnspan=2, pady=10)

        save_button = ttk.Button(self.parent, text="Save to File", command=self.save_to_file)
        save_button.grid(row=3, column=4)

        clear_button = ttk.Button(self.parent, text="Clear list", command=self.clear)
        clear_button.grid(row=3, column=6, pady=10)

        # Create and place listbox for output
        self.output_listbox = tk.Listbox(self.parent, width=20, height=15)
        self.output_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        self.output_listbox2 = tk.Listbox(self.parent, width=10, height=5, font=listbox_font)
        self.output_listbox2.grid(row=4, column=4, padx=10, pady=5)
        scrollbar = tk.Scrollbar(self.parent, orient="vertical")
        scrollbar.grid(row=4, column=5, sticky='ns')

        # Attach the scrollbar to both listboxes
        self.output_listbox.config(yscrollcommand=scrollbar.set)
        self.output_listbox2.config(yscrollcommand=scrollbar.set)

        # Update both listboxes when the scrollbar is moved
        def sync_scroll(*args):
            self.output_listbox.yview(*args)
            self.output_listbox2.yview(*args)

        scrollbar.config(command=sync_scroll)
    def generate_unicode(self):
        start_hex = self.start_entry.get()
        end_hex = self.end_entry.get()

        # Convert hex strings to integers
        start_int = int(start_hex, 16)
        end_int = int(end_hex, 16)

        # Clear the listbox
        self.output_listbox.delete(0, tk.END)
        self.output_listbox2.delete(0, tk.END)

        # Add characters to the listbox
        for code_point in range(start_int, end_int + 1):
            char = chr(code_point)
            hex_value = f"{code_point:04X}"
            self.output_listbox.insert(tk.END, f"U+{hex_value}: {char}")
            self.output_listbox2.insert(tk.END, f"        {char}")

    def save_to_file(self):
        # Choose where to save the file
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                  filetypes=[("Text files", "*.txt"),
                                                             ("All files", "*.*")])
        if not file_path:  # if the user cancels the save
            return

        with open(file_path, 'w', encoding='utf-8') as file:
            for item in self.output_listbox.get(0, tk.END):
                file.write(item + ',' + '\n')

    def clear(self):
        self.output_listbox.delete(0, tk.END)
        



class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        menubar = MenuBar(self)
        self.config(menu=menubar)


if __name__ == "__main__":
    app = App()
    app.mainloop()
