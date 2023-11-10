import tkinter as tk
from tkinter import ttk, filedialog, Canvas, Frame
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import os,sys




class TkinterApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x900")
        self.root.title("TK GUI Generator HPC Engineering")
        self.path = os.getcwd()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0)

        self.frm1 = ttk.Frame(self.notebook, width=2100, height=1080)
        self.notebook.add(self.frm1, text="Control")
        self.txfrm =  ttk.Frame(self.frm1, width=100, height=45)
        self.txfrm.grid(row=0,column=1)
       
        self.frm2 = ttk.Frame(self.notebook, width=2100, height=1080)
        self.notebook.add(self.frm2, text="View")
        self.frm1.grid_columnconfigure(0, weight=3)  # Expand first column
        self.frm2.grid_columnconfigure(0, weight=1)  # Expand first column
        self.btfrm =  ttk.Frame(self.frm2, width=5, height=20)
        self.btfrm.grid(row=0,column=0)
        # Assuming you want the text frame and button frame side by side
        self.txfrm.grid(row=0, column=1, sticky="ew")  
        self.btfrm.grid(row=0, column=0, sticky="nsew")  # sticky "nsew" makes the widget expand in all directions
##
        # Then configure column weights to allow the frames to expand and fill space
        self.frm1.grid_columnconfigure(0, weight=0, uniform="group1")
        self.frm1.grid_columnconfigure(1, weight=0, uniform="group1")

        # For the buttons, make sure they align vertically but in the same column
       

        # You may also want to configure the row weights if you want them to expand vertically
        self.btfrm.grid_rowconfigure(0, weight=0)
        self.btfrm.grid_rowconfigure(1, weight=0)

        # And set the frame to expand within its grid cell, if it's not already done elsewhere in your code
        self.btfrm.grid(sticky="nsew")
        self.txfrm.grid(sticky="ew")

        # Assuming self.frm1 is in a cell of another grid, you may need to configure that grid to allow expansion as well
        self.notebook.grid_rowconfigure(0, weight=0)  # Replace parent_widget with actual variable
        self.notebook.grid_columnconfigure(0, weight=0)  # Replace parent_widget with actual variable


       
        
        

        self.wkcurdir = os.getcwd()

        # Initialize counts for widgets
        self.ecount = 1
        self.btcount = 1
        self.notecount = 1
        self.btncount = 1
        self.btncount2 = 1
        self.labelcount = 1
        self.canvascount = 1
        self.lboxcount = 1
        self.rowcount = 1
        self.columncount = 1
        self.combocount = 1
        self.spincount = 1
        self.textcount = 1
        self.slidercount = 1
        self.scrollcount = 1
        self.projectcount = 1
      
        self.text = ScrolledText(self.frm1, height=44,width=120)
        self.text.grid(row=0, column=0,sticky="w") 
 
        sb1 = SideButtonframe(self.frm1,self.text)
        self.create_widgets()
        
    def create_widgets(self):
       

      
        # Buttons
        
        self.b1 = tk.Button(self.btfrm, text="Entry Widget", command=self.e_code)
        self.b1.grid(row=1, column=0, sticky="ew")
        self.b2 = tk.Button(self.btfrm, text="Insert Button row", command=self.button_code1)
        self.b2.grid(row=2, column=0, sticky="ew")
        self.b55 = tk.Button(self.btfrm, text="Insert Button column", command=self.button_code2)
        self.b55.grid(row=3, column=0, sticky="ew")
        self.b4 = tk.Button(self.btfrm, text="Insert label row", command=self.label_code1)
        self.b4.grid(row=4, column=0, sticky="ew")
        self.b5 = tk.Button(self.btfrm, text="List Box", command=self.listbox_code)
        self.b5.grid(row=24, column=0, sticky="ew")
        self.b6 = tk.Button(self.btfrm, text="Menu1", command=self.menu1_code)
        self.b6.grid(row=26, column=0, sticky="ew")
        self.b7 = tk.Button(self.btfrm, text="Menu2", command=self.menu2_code)
        self.b7.grid(row=28, column=0, sticky="ew")
        self.b8 = tk.Button(self.btfrm, text="Canvas", command=self.canvas_code)
        self.b8.grid(row=29, column=0, sticky="ew")
        self.b9 = tk.Button(self.btfrm, text="Combobox", command=self.combo_code)
        self.b9.grid(row=30, column=0, sticky="ew")
        self.bba = tk.Button(self.btfrm, text="Spinbox", command=self.spin_code)
        self.bba.grid(row=31, column=0, sticky="ew")
        self.bb1 = tk.Button(self.btfrm, text="Text Box", command=self.text_code)
        self.bb1.grid(row=32, column=0, sticky="ew")
        self.b14 = tk.Button(self.btfrm, text="insert label col", command=self.label_code2)
        self.b14.grid(row=34, column=0, sticky="ew")
        self.b15 = tk.Button(self.btfrm, text="Slider Widget", command=self.slider)
        self.b15.grid(row=35, column=0, sticky="ew")
        self.b16 = tk.Button(self.btfrm, text="Scroll Bar", command=self.scrollbar)
        self.b16.grid(row=36, column=0, sticky="ew")
        self.b17 = tk.Button(self.btfrm, text="Clear Code Box", command=self.cleartext)
        self.b17.grid(row=37,column=0)
        self.b18 = tk.Button(self.btfrm, text="Restart 1st Code Block", command=self.st_str)
        self.b18.grid(row=38, column=0, sticky="ew")
        self.b19 = tk.Button(self.btfrm, text="Finish & Save", command=self.save_code)
        self.b19.grid(row=39, column=0, sticky="ew")
        self.b20 = tk.Button(self.btfrm, text="Open File", command=self.open_code)
        self.b20.grid(row=40, column=0, sticky="ew")
        # ... and so on for the rest of your buttons
        
    def st_str(self):
        start_str = """#! /usr/bin/python3\n
import tkinter as tk
from tkinter import ttk
# proj_str
root = tk.Tk()
root.title(\"Tkinter widget helper\")
class App:
    def __init__(self, root):
         self.root = root
         self.root.geometry('900x900')
         self.root.title('TK GUI Generator HPC Engineering')
         self.notebook = ttk.Notebook(self.root)
         self.frm1 = tk.Frame(self.notebook, height=300, width=300)
         self.frm1.grid(row=0, rowspan=10, column=5, columnspan=10)
         self.frm2 = tk.Frame(self.notebook, height=300, width=300)
         self.frm2.grid(row=0, column=0, sticky="ew", rowspan=5, columnspan=5)"""
        self.text.insert("1.0", start_str)

    def e_code(self):
        w_str = """
        display1 = tk.StringVar()
        self.entry1 = tk.Entry(root,
            textvariable=display1,
            justif SideButtonframey='right',
            bg='orange')
        self.entry1.grid(row=3, column=4)
        self.entry1["font"] = "arial 12 bold"
        """
        w_str2 = w_str.replace("b1", "b" + str(self.btncount))
        w_str3 = w_str2.replace("row=1", "row=" + str(self.rowcount))
        self.text.insert(tk.END, w_str3)
        self.btncount += 1
        self.rowcount += 1


       
    def run(self):
        self.root.mainloop()
    def button_code1(self):
       w_str = """
        self.b1 = tk.Button(self.root,text="new",
            #command=None,

            )
        self.b1.grid(row=1, column=2)
"""
   
    def button_code2(self):

        w_str = """
    self.btn1 = tk.Button(self.root,
                #relief=tk.FLAT,
                compound=tk.LEFT,
                text="new",
                #command=None,

                )
    btn1.grid(row=2, column=1)
    """
        w_str2 = w_str.replace("btn1", "btn" + str(self.btncount2))
        w_str3 = w_str2.replace("column=1", "column=" + str(self.columncount))
        self.text.insert(tk.END, w_str3)
        self.btncount2 += 1
        self.columncount += 1


    def label_code1(self):
        
        label_str = """
    label1 = tk.Label(root, text="---")
    label1.grid(row=4, column=2) """
        label_str2 = label_str.replace("label1", "label" + str(self.labelcount))
        label_str3 = label_str2.replace("row=1", "row=" + str(self.rowcount))
        self.text.insert(tk.END, label_str3)
        self.labelcount += 1
        self.rowcount += 1


    def label_code2(self):
  
        label_str = """
    label1 = tk.Label(self.root, text="label") 
    label1.grid(row=5, column=2) """
        label_str2 = label_str.replace("label1", "label" + str(self.labelcount))
        label_str3 = label_str2.replace("column=1", "column=" + str(self.columncount))
        self.text.insert(tk.END, label_str3)
        self.labelcount += 1
        self.columncount += 1


    def listbox_code(self):
   
        lbox_str = """
    self.lbox1=tk.Listbox(root, width=80, height=25)
    self.lbox1.grid(row=9, coloumn=3)  """
        lbox_str2 = lbox_str.replace("self.lbox1", "self.lbox" + str(self.lboxcount))
        self.text.insert(tk.END, lbox_str2)
        self.lboxcount += 1


    def menu1_code(self):
        menu1_str = """
    root.option_add('*tearOff',False)
        menubar = Menu(root)
        root.config(menu = menubar)
        File = Menu(menubar)
        Edit = Menu(menubar)
        Help_ = Menu(menubar)
        menubar.add_cascade( menu = File , label = 'File')
        menubar.add_cascade( menu = Edit , label = 'Edit')
        menubar.add_cascade( menu = Help_, label = 'Help')
        File.add_command( label = 'New', command = lambda: print(" New File"))
        File.add_separator()
        File.add_command( label = 'Open',command = lambda: print("Open File"))
        File.add_separator()
        save = Menu(File)
        File.add_cascade( menu = save , label ='Save')
        save.add_command(label ='Save_as', command = lambda: print(" Save as"))
        save.add_command(label ='Save_all',command = lambda: print(" Save all"))
        """
        self.text.insert(tk.END, menu1_str)


    def menu2_code(self):
        menu2_str = """
    def open(self):
    messagebox.shorootfo('From My Computer','Your File has been Opened')
    def close(self):
    messagebox.shorootfo('From My Computer','Your File has been Closed')
    def nothing(self):
    messagebox.shorootfo('From My Computer','Are You Feeling Well')

    menubar = Menu(root)

    filemenu = Menu(menubar)
    filemenu.add_command(label="Open File",command=open)
    filemenu.add_command(label="New File",command=nothing)
    filemenu.add_separator()
    filemenu.add_command(label="Save",command=nothing)
    filemenu.add_command(label="Save As",command=nothing)
    filemenu.add_separator()
    filemenu.add_command(label="Close",command=close)
    filemenu.add_command(label="Close Tab",command=nothing)
    filemenu.add_command(label="Close rootdow",command=nothing)
    filemenu.add_separator()
    filemenu.add_command(label="Exit",command=root.quit)

    menubar.add_cascade(label="File", menu = filemenu)

    editmenu = Menu(menubar)
    editmenu.add_command(label="Undo",command=nothing)
    editmenu.add_command(label="Redo",command=nothing)
    editmenu.add_separator()
    editmenu.add_command(label="Copy",command=nothing)
    editmenu.add_command(label="Paste",command=nothing)
    editmenu.add_separator()
    editmenu.add_command(label="Columns",command=nothing)
    editmenu.add_command(label="Lines",command=nothing)
    editmenu.add_command(label="Text",command=nothing)
    editmenu.add_separator()
    editmenu.add_command(label="Exit",command=root.quit)

    menubar.add_cascade(label="Edit", menu = editmenu)

    root.config(menu = menubar)
    """
        self.text.insert(tk.END, menu2_str)


    def canvas_code(self):

        canvas_str = """
    self.canvas1 = Canvas(self.root)
    self.canvas.grid(row=1, column=1)
        canvas.config(width = 700 , height = 800)

        line = canvas.create_line(40,70, 79,140 , fill ='red', width = 7)

        """

        canvas_str2 = canvas_str.replace("self.canvas1", "self.canvas" + str(self.canvascount))
        self.text.insert(tk.END, canvas_str2)
        self.canvascount += 1


    def combo_code(self):
        global combo_str, combocount
        combo_str = """
    self.cbox1 = ttk.Combobox(self.root, values=["Value1", "value2, "value3"])
    self.cbox1.grid(column=0, row=1)"""
        combo_str2 = combo_str.replace("self.cbox1", "self.cbox" + str(self.combocount))
        self.text.insert(tk.END, combo_str2)
        self.combocount += 1


    def spin_code(self):

        spin_str = """
    sp1 = tk.Spinbox(root, from_=1.0, to=1000.0, increment=0.1)
        sp1.grid(row=1, column=0)"""
        spin_str2 = spin_str.replace("sp1", "sp" + str(self.spincount))
        self.text.insert(tk.END, spin_str2)
        self.spincount += 1


    def text_code(self):
    
        txt_str = """
    self.txt1 = tk.Text(root, height=60, width=150, bg='white')
    self.txt1.insert('1.0', tk.END)
    self.txt1.grid(row=02
    , column=3)"""
        txt_str2 = txt_str.replace("self.txt1", "self.txt" + str(self.textcount))
        self.text.insert(tk.END, txt_str2)
        self.textcount += 1


    def slider(self):

        sld_str = """self.current_value = tk.DoubleVar()
                    self.slider1 = ttk.Scale(self.root,
                    from_=0,
                    to=100,
                    orient='horizontal',
                    variable=current_value)
                    self.slider.grid(row=1, column=1)"""                    
        sld_str2 = slidar_str.replace("slider1", "slider" + str(self.slidercount))
        self.text.insert(tk.END, slider_str2)
        self.slidercount += 1
    

    def scrollbar(self):
       
        # scrollcount not goint to add counter for this yet
        scr_str1 = """
    self.scrollbar = tk.Scrollbar(self.root,command=text.yview)
    self.scrollbar.grid(row=0, column=1, sticky='ns')

    self.text['yscrollcommand'] = scrollbar.set
    """
        self.text.insert(tk.END, scr_str1)


    def scrolled_txt(self):
        scr_str = """class ScrolledText(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)

        # Create the scrollbar
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create the Text widget
        self.text = tk.Text(self, wrap=tk.WORD, yscrollcommand=self.scrollbar.set, *args, **kwargs)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure the scrollbar to scroll the Text widget
        self.scrollbar.config(command=self.text.yview)

    def insert(self, index, chars, *args):
        self.text.insert(index, chars, *args)

    def delete(self, first, last=None):
        self.text.delete(first, last)

    # You can add more methods if needed to proxy to the Text widget

stext = ScrolledText(root)
stext.pack(fill=tk.BOTH, expand=True)
stext.insert(tk.END, "This is a combined Text and Scrollbar widget.\n" * 20)

root.mainloop()

"""

    def restartstr(self):
        self.text.insert(tk.END, start_str)


    def cleartext(self):
        self.text.delete("1.0", tk.END)


    def open_code(self):
        # file type
        filetypes = [
            ("Python files", "*.py"),
            ("text files", "*.txt"),
            ("All files", "*.*"),
        ]
        # show the open file dialog
        f = filedialog.askopenfile(filetypes=filetypes)
        # read the text file and show its content on the Text
        self.text.insert("1.0", f.readlines())
        


    def save_code(self):

        stop_str = """ root = tk.Tk()
    app = App(root)
    app.mainloop()"""
        self.text.insert(tk.END, stop_str)
        filetypes = [
            ("Python files", "*.py"),
            ("Text files", "*.txt"),
            ("All files", "*.*"),
        ]
        self.save_file()
    def open_file(self):
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
        self.text.delete(1.0, tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.read()
            self.text.insert(tk.END, text)

    def save_file(self):
        """Save the current file as a new file."""
        filepath = asksaveasfilename(
            defaultextension="self.txt",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = self.text.get(1.0, tk.END)
            output_file.write(text)
       
class SideButtonframe:
    def __init__(self, parent, text):
        self.text = text
        self.parent = parent
        self.text.tag_configure("highlight", background="cornsilk")
        self.sfr = tk.Frame(self.parent, width=2)
        self.sfr.grid(row=20, column=0, sticky="w")
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
        self.method_combobox.grid(row=0, column=1)

        # Create a button to initiate the selected method
        self.execute_button = tk.Button(
            self.sfr, text="Execute", bd=2, command=self.execute_method
        )
        self.execute_button.grid(row=1, column=1)

        self.update_info()
        indent_spaces = tk.StringVar()
        indent_spinbox = ttk.Spinbox(
            self.sfr, from_=1, to=10, textvariable=indent_spaces, width=3
        )
        indent_spinbox.set("4")  # Default indent spaces
        indent_spinbox.grid(row=2, column=1)

    def execute_method(self):
        selected_method = self.method_combobox.get()

        if selected_method == "Open":
            self.open_file(self.text)
        elif selected_method == "Save As...":
            self.save_file(self.text)
        elif selected_method == "Clear":
            self.clear(self.text)
        elif selected_method == "Change FG Color":
            self.changeFg(self.text)
        elif selected_method == "Change BG Color":
            self.changeBg(self.text)
        elif selected_method == "Select All":
            self.text.event_generate("<<SelectAll>>")
        elif selected_method == "Cut":
            self.text.event_generate("<<Cut>>")
        elif selected_method == "Copy":
            self.text.event_generate("<<Copy>>")
        elif selected_method == "Paste":
            self.text.event_generate("<<Paste>>")
        elif selected_method == "Undo":
            self.undo()
        elif selected_method == "Redo":
            self.redo()
        elif selected_method == "Insert Self":
            self.insert_self(self.text)
        elif selected_method == "Highlighted Insert Self":
            self.insert_selfs(self.text)
        elif selected_method == "Find & Replace":
            self.finder(self.text)
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
        self.content = self.text.get("1.0", "end-1c")
        self.label = tk.Label(self.sfr, text="             ").grid(row=18, column=0)
        self.label1 = tk.Label(self.sfr, text="             ").grid(row=19, column=0)
        lines = self.text.index("end-1c").split(".")[0]
        words = len(self.content.split())
        characters = len(self.content)
        self.info_label = tk.Label(
            self.sfr, text="Lines: 0 | Words: 0 |\n Characters: 0"
        )
        self.info_label.grid(row=4, column=1)
        # Get the current text content
        self.content = self.text.get("1.0", "end-1c")

        # Count the lines, words, and characters

        self.info_label.config(
            text=f"Lines: {lines} |  \n Words: {words} |\n Characters: {characters}"
        )

        # Update the label with the information

    def finder(self, text):
        self.text = text
        fr = FindReplaceWidget(self.text)

    def changeBg(self, text):
        (triple, hexstr) = askcolor()
        if hexstr:
            text.config(bg=hexstr)

    def changeFg(self, text):
        (triple, hexstr) = askcolor()
        if hexstr:
            text.config(fg=hexstr)

    def clear(self, text):
        self.text = text
        self.text.delete("1.0", tk.END)

    def open_file(self, text):
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
        text.delete(1.0, tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.read()
            text.insert(tk.END, text)

    def save_file(self, text):
        """Save the current file as a new file."""
        filepath = asksaveasfilename(
            defaultextension="self.txt",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = text.get(1.0, tk.END)
            output_file.write(text)

    def undo(self):
        try:
            self.text.edit_undo()
        except:
            print("No previous action")

    def redo(self):
        try:
            self.text.edit_redo()
        except:
            print("No previous action")

    def copy(self, event=None):
        self.clipboard_clear()
        text = self.text.get("sel.first", "sel.last")
        self.clipboard_append(text)

    def cut(self, event):
        self.copy()
        self.delete("sel.first", "sel.last")

    def paste(self, event):
        text = self.selection_get(selection="CLIPBOARD")
        self.insert("insert", text)

    def select_all(self, event=None):
        self.text.tag_add("sel", "1.0", tk.END)
        return "break"

    def indent2(self, event=None):
        # Get the current line and its content
        index = self.text.index("insert linestart")
        line = self.text.get(index, index + "lineend")

        # Check if the line starts with specific keywords
        keywords = ["if", "elif", "else", "while", "for", "def", "class"]
        if any(line.startswith(keyword) for keyword in keywords):
            # Insert four spaces at the start of the new line
            self.text.insert("insert", " " * 4)

    def auto_indent(self, event=None):
        self.text = event.widget

        # get leading whitespace from current line

    def apply_indent_dedent():
        sel_start, sel_end = text.tag_ranges(tk.SEL)
        if sel_start and sel_end:
            text.tag_add("indent", sel_start, sel_end)
            self.text.get("insert linestart", "insert")
            match = re.match(r"^(\s+)", line)
            whitespace = match.group(0) if match else ""

            # insert the newline and the whitespace
            self.text.insert("insert", f"\n{whitespace}")

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
        selected_text = text.get("sel.first", "sel.last")
        if selected_text:
            # Add four spaces to the beginning of each line
            indented_text = "\n".join(
                f"    {line}" for line in selected_text.split("\n")
            )
            text.replace("sel.first", "sel.last", indented_text)

    def dedent(self):
        selected_text = text.get("sel.first", "sel.last")
        if selected_text:
            # Remove four spaces from the beginning of each line if present
            dedented_text = "\n".join(
                line[4:] if line.startswith("    ") else line
                for line in selected_text.split("\n")
            )
            text.replace("sel.first", "sel.last", dedented_text)

    def highlight(self):
        selected_text = text.get("sel.first", "sel.last")
        if selected_text:
            text.tag_add("highlight", "sel.first", "sel.last")

    def apply_indent_dedent(self):
        sel_start, sel_end = text.tag_ranges(tk.SEL)
        if sel_start and sel_end:
            text.tag_add("indent", sel_start, sel_end)

    def insert_self(self, text):
        self.text = text
        start_index = self.text.index("sel.first")
        end_index = self.text.index("sel.last")

        selected_text = self.text.get(start_index, end_index)
        modified_text = "\n".join(
            [
                "self." + line if line.strip() else line
                for line in selected_text.split("\n")
            ]
        )

        self.text.delete(start_index, end_index)
        self.text.insert(start_index, modified_text)

    def insert_selfs(self, text):
        self.text = text

        start_index = self.text.index("sel.first")
        end_index = self.text.index("sel.last")

        selected_text = self.text.get(start_index, end_index)
        modified_lines = [
            "self." + line.strip() if line.strip() else line
            for line in selected_text.split("\n")
        ]
        modified_text = "\n".join(modified_lines)

        self.text.delete(start_index, end_index)
        self.text.insert(start_index, modified_text)

    def insert_self_in_parentheses(self, text):
        start_index = self.text.index("sel.first")
        end_index = self.text.index("sel.last")

        selected_text = self.text.get(start_index, end_index)
        modified_lines = []

        for line in selected_text.split("\n"):
            if line.strip():
                modified_line = line.replace("()", "(self)")  # Replace () with (self)
            else:
                modified_line = line
            modified_lines.append(modified_line)

        modified_text = "\n".join(modified_lines)
        self.text.delete(start_index, end_index)
        self.text.insert(start_index, modified_text)

    def bindings(self):
        self.text.bind("<Return>", self.auto_indent)
        self.text.bind("<Key>", self.update_info)
        self.text.bind("<<Selection>>", self.update_info)

    def quit(self):
        sys.exit(0)




if __name__ == "__main__":
    root = tk.Tk()
    app = TkinterApp(root)
    app.run()
