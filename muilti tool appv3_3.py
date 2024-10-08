import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, messagebox, Spinbox, Scrollbar, INSERT, END, font, Toplevel
from tkinter import ttk
import os
import re
from collections import defaultdict
import time
import shutil

#You can set the number of lines you want to see before and after the search pattern
#using the spinboxes at the bottom
class PyGrepSim:
    def __init__(self, root):
      
        self.root = root
        self.setup_gui()
        self.subpath = "/"       
        self.path= os.path.join(os.path.expanduser("~"), self.subpath)
        
        
    def setup_gui(self):
        self.create_options_frame()
        self.create_file_frame()
        self.create_text_area()
        self.create_lines_control_frame()

    def create_options_frame(self):
        frame_options = tk.Frame(self.root)
        frame_options.pack(pady=5)

        tk.Label(frame_options, text="Pattern: RegEx").pack(side=tk.LEFT)
        self.entry_pattern = tk.Entry(frame_options, bd=7)
        self.entry_pattern.pack(side=tk.LEFT, padx=5)
        tk.Label(frame_options, text="Large files you will get 'not respondeing' But you only need to wait").pack(side=tk.BOTTOM)
        self.var_case_insensitive = tk.BooleanVar() #Default is Case Sensitive
        check_case_insensitive = tk.Checkbutton(frame_options, text="Case Insensitive", variable=self.var_case_insensitive)
        check_case_insensitive.pack(side=tk.LEFT)
        
    def create_file_frame(self):
        frame_file = tk.Frame(self.root)
        frame_file.pack(pady=5)

        tk.Label(frame_file, text="Filename:").pack(side=tk.LEFT)
        self.filenamelist = tk.Listbox(frame_file, bd=7,width=50)
        self.filenamelist.pack(side=tk.LEFT, padx=5)

        tk.Button(frame_file, text="Browse", bd=5,bg="light blue", command=self.open_file_dialog).pack(side=tk.LEFT)
        tk.Button(frame_file, text="Save", bd=5,bg="orange", command=self.save_file).pack(side=tk.RIGHT)
        tk.Button(frame_file, text="Save_Filelist",bd=3, bg="azure", command=self.save_filelist).pack(side=tk.RIGHT)
        tk.Button(frame_file, text="Search",bd=6, bg="light green", command=self.search_for_pattern).pack(side=tk.RIGHT,pady=30)
        tk.Button(frame_file, text="Clear", bd=3,bg="wheat",command=self.clear_all).pack(side=tk.LEFT,pady=30)
       
    def create_text_area(self):
        self.text_area = tk.Text(self.root,bd=7, height=15, width=80)
        self.text_area.pack(padx=10, pady=5)

    def create_lines_control_frame(self):
        frame_lines_control = tk.Frame(self.root)
        frame_lines_control.pack(pady=5)

        tk.Label(frame_lines_control, text="Lines before:").pack(side=tk.LEFT)
        self.spinbox_before = Spinbox(frame_lines_control, from_=0, to=99, width=3)
        self.spinbox_before.pack(side=tk.LEFT)

        tk.Label(frame_lines_control, text="Lines after:").pack(side=tk.LEFT)
        self.spinbox_after = Spinbox(frame_lines_control, from_=0, to=99, width=3)
        self.spinbox_after.pack(side=tk.LEFT)



          
        
    def open_file_dialog(self):
        self.path = filedialog.askdirectory()
        filelist = os.listdir(self.path)
        self.filenamelist.delete(0, tk.END)  # Clear the entry field
        for file in filelist:
            self.filenamelist.insert(0, file)  # Insert the selected filename



    
    def save_filelist(self):
        filelist = filedialog .asksaveasfilename(defaultextension=".txt",
                                     filetypes=[("All Files", "*.*")],
                                         )
        if not filelist:
            return

        with open(filelist, "w") as output_file:
            flist = self.filenamelist.get(0, tk.END)
            strflist = str(flist)
            output_file.write(strflist)
            return flist

    def save_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("All Files", "*.*")],
                                 )
        if not filename:
            return
        with open(filename, "w") as output_file:
            text = self.text_area.get(1.0, tk.END)
            output_file.write(text)
            output_file.close()
            return 

    def clear_all(self):
        self.text_area.delete('1.0', tk.END)
        self.filenamelist.delete(0, tk.END)
        self.entry_pattern.delete(0, tk.END)
    def search_for_pattern(self):
        pattern = self.entry_pattern.get()
        lines_before = int(self.spinbox_before.get())
        lines_after = int(self.spinbox_after.get())
        self.text_area.delete('1.0', tk.END)  # Clear the text area for new output

        try:
            re_pattern = re.compile(pattern, re.IGNORECASE if self.var_case_insensitive.get() else 0)
        except re.error:
            messagebox.showerror("Invalid Pattern", "The entered pattern is not a valid regular expression.")
            return

        try:
            # Ensure that self.path is a string representing the path , e.g., r"C:\Users\..."
            # Because in windows you could get a unicode error c:\users  "\u" is a unicode escape, should be ok we use /
            filenames = os.listdir(self.path)
            for filename in filenames:
                file_path = os.path.join(self.path, filename)  # Correctly join the directory path and filename helps bring it all together
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    for i, line in enumerate(lines):       # associate the lines with line numbers behind the scenens
                        if re_pattern.search(line):
                            start = max(i - lines_before, 0)
                            end = min(i + lines_after + 1, len(lines))
                            self.text_area.insert(tk.END, f"---{filename}---\n")
                            for l in lines[start:end]:
                                self.text_area.insert(tk.END, l)
                            self.text_area.insert(tk.END, f"\n{'-'*40}\n")
        except SyntaxError as syn: 
            print(syn)
            self.text_area.insert(tk.END, "File not found. Please check the path and try again.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")




        matching_filenames = []  # List to store filenames that match the pattern

        try:          
            for filename in filenames:
                file_path = os.path.join(self.path, filename)
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    for i, line in enumerate(lines):
                        if re_pattern.search(line):
                            if filename not in matching_filenames:
                                matching_filenames.append(filename)  # Add filename to list if it matches to  use to save later on
                            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        if matching_filenames:
            self.save_filenames(matching_filenames)  # Save matching filenames after search

    def save_filenames(self, filenames):
        epoch_time = int(time.time())  # Get current epoch time to make directory
        directory_name = f"file_search_results_{epoch_time}"  # Create directory name & add to that directory name using epoch time
        os.makedirs(directory_name, exist_ok=True)  # Create directory in the present

        with open(os.path.join(directory_name, "filenames.txt"), "w") as file:
            for filename in filenames:
                file.write(f"{filename}\n")  # Write each filename on a new line
                 # Copy each matching file to the new directory
                src_path = os.path.join(self.path, filename)  # Source file path
                dst_path = os.path.join(directory_name, filename)  # Destination file path
                shutil.copy2(src_path, dst_path)  # Copy file to new directory

        messagebox.showinfo("Files Copied", f"Matching files and list have been copied to '{directory_name}'.")



class FileComparator:
    def __init__(self, root):
        self.root = root
        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.root, text="Template File:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_template = tk.Entry(self.root, width=50)
        self.entry_template.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_template).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(self.root, text="File to Compare:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_compare = tk.Entry(self.root, width=50)
        self.entry_compare.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_compare).grid(row=1, column=2, padx=5, pady=5)

        tk.Button(self.root, text="Compare", command=self.compare_files).grid(row=2, column=1, padx=5, pady=20)

    def browse_template(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("JSON Files", "*.json"), ("XML Files", "*.xml"), ("All Files", "*.*")])
        if file_path:
            self.entry_template.delete(0, tk.END)
            self.entry_template.insert(0, file_path)

    def browse_compare(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("JSON Files", "*.json"), ("XML Files", "*.xml"), ("All Files", "*.*")])
        if file_path:
            self.entry_compare.delete(0, tk.END)
            self.entry_compare.insert(0, file_path)

    def compare_files(self):
        template_path = self.entry_template.get()
        compare_path = self.entry_compare.get()

        if not template_path or not compare_path:
            messagebox.showwarning("Input Error", "Please select both template and compare files.")
            return

        try:
            with open(template_path, 'r') as template_file:
                template_strings = set(line.strip() for line in template_file.readlines())

            with open(compare_path, 'r') as compare_file:
                compare_strings = set(line.strip() for line in compare_file.readlines())

            matched = template_strings & compare_strings
            unmatched = compare_strings - template_strings

            self.save_results(matched, unmatched)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_results(self, matched, unmatched):
        matched_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Save Matched Results", filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("JSON Files", "*.json"), ("XML Files", "*.xml"), ("All Files", "*.*")])
        if matched_path:
            with open(matched_path, 'w') as matched_file:
                matched_file.write("\n".join(matched))

        unmatched_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Save Unmatched Results", filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("JSON Files", "*.json"), ("XML Files", "*.xml"), ("All Files", "*.*")])
        if unmatched_path:
            with open(unmatched_path, 'w') as unmatched_file:
                unmatched_file.write("\n".join(unmatched))

        messagebox.showinfo("Success", "Files compared and results saved.")

class TextComparator:
    def __init__(self, txttab):
        self.parent = txttab
        self.output_text = None
        self.btfr = ttk.Frame(self.parent, width=10, height=10)
        self.btfr.grid(row=0, column=0)
        self.txtfrm1 = ttk.Frame(self.parent, width=60, height=60)
        self.txtfrm1.grid(row=0, column=1)
        self.txtfrm2 = ttk.Frame(self.parent, width=60, height=60)
        self.txtfrm2.grid(row=0, column=2)
        self.txtfrm3 = ttk.Frame(self.parent, width=50, height=15)
        self.txtfrm3.grid(row=12, column=0, columnspan=4)
        self.text1 = ScrolledText(self.txtfrm1)
        self.text1.grid(row=0, column=0, sticky="nsew")
        self.text2 = ScrolledText(self.txtfrm2)
        self.text2.grid(row=0, column=0, sticky="nsew")
        self.output_text = tk.Text(self.txtfrm3, height=15)
        self.output_text.grid(row=1, column=0, columnspan=2, sticky="nsew")
        load_button = tk.Button(self.btfr, text="Load Files", command=self.load_files)
        load_button.grid(row=2, column=0, sticky="w")
        compare_button = tk.Button(
            self.btfr, text="Compare", command=self.compare_files
        )
        compare_button.grid(row=3, column=0, sticky="w")
        clear_button = tk.Button(
            self.btfr, text="Clear All", command=self.clear_textwidgets
        )
        clear_button.grid(row=4, column=0, sticky="w")
        self.infotxt1 =  TextWidgetInfo(self.txtfrm1, self.text1)
        self.infotxt2 =  TextWidgetInfo(self.txtfrm2, self.text2)
        self.outtxtinfo =TextWidgetInfo(self.txtfrm3, self.output_text)
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
        self.text1.tag_configure("diff", background="wheat1")
        self.text2.tag_configure("diff", background="sky blue")

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
        self.content = self.textwidget.get("1.0", "end-1c")
        self.infotxt1.update()
        self.infotxt2.update()
        self.outtxtinfo.update()

class TextWidgetInfo:
    def __init__(self, parent, textwidget):
        self.parent = parent
        self.textwidget = textwidget
        self.info_label = tk.Label(self.parent, text="Lines: 0  \n | Words: 0   \n| Characters: 0 \n| Cursor Position: Line 1   , Column 0       ")
        self.info_label.grid(row=30, column=0)
        self.update_info()
        self.textwidget.bind("<KeyRelease>", self.update_info)
        self.textwidget.bind("<ButtonRelease-1>", self.update_info)
        self.textwidget.bind("<<Modified>>", self.on_text_modified)
        self.textwidget.bind("<ButtonRelease-2>", self.update_info)
    def on_text_modified(self, event):
        if self.textwidget.edit_modified():
            self.update_info(event)
            self.textwidget.edit_modified(False)

    def update_info(self, event=None):
        # Get the current text content
        content = self.textwidget.get("1.0", "end-1c")
        lines = self.textwidget.index("end-1c").split(".")[0]
        words = len(content.split())
        characters = len(content)
        # Get the current cursor position (line and column)
        cursor_position = self.textwidget.index("insert")
        cursor_line, cursor_column = cursor_position.split(".")

        # Update the label with the new information
        self.info_label.config(
            text=f"Lines: {lines}   \n| Words: {words}       \n| Characters: {characters}     \n | Cursor Position: Line {cursor_line}, Column {cursor_column}"
        )


if __name__ == '__main__':
    root = tk.Tk()
    notebook = ttk.Notebook(root)
    notebook.pack(expand=1, fill='both')

    # Add PyGrepSim Tab
    pygrep_tab = tk.Frame(notebook)
    notebook.add(pygrep_tab, text='PyGrepSim')
    PyGrepSim(pygrep_tab)

    # Add File Comparator Tab
    file_comparator_tab = tk.Frame(notebook)
    notebook.add(file_comparator_tab, text='File Comparator')
    FileComparator(file_comparator_tab)
    txttab = tk.Frame(notebook)
    notebook.add(txttab, text="Text Compare")
    TextComparator(txttab)    
    root.mainloop()
