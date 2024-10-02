import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, filedialog, messagebox, Spinbox, Scrollbar, INSERT, END, font, Toplevel
import os
import re
import calendar
from datetime import datetime
from collections import defaultdict
import time
from time import time, strftime, localtime
import shutil
import difflib
import csv
import time
#You can set the number of lines you want to see before and after the search pattern
#using the spinboxes at the bottom
class PyGrepSim:
    def __init__(self, root):
        self.root = root
        self.var_recursive = tk.BooleanVar()  # Variable for recursive option
        self.setup_gui()
        self.subpath = "/"
        self.path = os.path.join(os.path.expanduser("~"), self.subpath)
        self.ignored_extensions = ('.bmd.out', '.bmd','.bmp', '.svg', '.jpg', '.png', '.mp3', '.avi', '.mov')  # Extensions to ignore

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
        
        self.var_case_insensitive = tk.BooleanVar()  # Default is Case Sensitive
        check_case_insensitive = tk.Checkbutton(frame_options, text="Case Insensitive", variable=self.var_case_insensitive)
        check_case_insensitive.pack(side=tk.LEFT)

        # Add the recursive search check button
        check_recursive = tk.Checkbutton(frame_options, text="Recursive", variable=self.var_recursive)
        check_recursive.pack(side=tk.LEFT)
            
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
        help_button = tk.Button(self.root, text="Help", command=self.show_help)
        help_button.pack(pady=5)

    def create_text_area(self):
        self.text_area = ScrolledText(self.root,bd=7, height=25, width=120)
        self.text_area.pack(padx=5, pady=20)

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
            if not file.lower().endswith(self.ignored_extensions):
                self.filenamelist.insert(0, file)  # Insert the selected filename
   
    def save_filelist(self):
        filelist = filedialog.asksaveasfilename(defaultextension=".txt",
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
            # Use recursive search if the checkbutton is selected
            if self.var_recursive.get():
                for root, dirs, files in os.walk(self.path):
                    for filename in files:
                        if not filename.lower().endswith(self.ignored_extensions):
                            self.process_file(root, filename, re_pattern, lines_before, lines_after)
            else:
                filenames = os.listdir(self.path)
                for filename in filenames:
                    if not filename.lower().endswith(self.ignored_extensions):
                        self.process_file(self.path, filename, re_pattern, lines_before, lines_after)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def process_file(self, directory, filename, re_pattern, lines_before, lines_after):
        file_extensions = ('.txt', '.py', '.dat', '.log')
        if filename.lower().endswith(file_extensions):
            file_path = os.path.join(directory, filename)
            lines = self.try_open_file(file_path)
            if lines is None:
                print(f"Could not read the file: {file_path}")
                return
            for i, line in enumerate(lines):
                if re_pattern.search(line):
                    start = max(i - lines_before, 0)
                    end = min(i + lines_after + 1, len(lines))
                    self.text_area.insert(tk.END, f"---{filename}---\n")
                    for l in lines[start:end]:
                        self.text_area.insert(tk.END, l)
                    self.text_area.insert(tk.END, f"\n{'-'*40}\n")

    def try_open_file(self, file_path):
        encodings = ['utf-8', 'iso-8859-1', 'cp1252']
        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc, errors='ignore') as file:
                    return file.readlines()
            except UnicodeDecodeError:
                continue

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

    def show_help(self):
        help_message = (
        "PyGrepSim Help\n\n"
        "This program allows you to search for patterns in text files using regular expressions.\n\n"
        "1. Pattern: Enter the regular expression pattern to search for.\n"
        "2. Case Insensitive: Check this box to perform a case-insensitive search.\n"
        "3. Filename: Browse to select a directory containing text files.\n"
        "4. Lines Before/After: Set the number of lines to display before and after the matching pattern.\n"
        "5. Search: Click to search for the pattern in the selected directory's files.\n"
        "6. Save: Save the search results displayed in the text area.\n"
        "7. Save Filelist: Save the list of filenames that contain the matching pattern.\n"
        "8. Clear: Clear all input fields and the text area.\n\n"
        "Note: For large files, the application may become unresponsive, but it is still processing. Please wait.")
        messagebox.showinfo("Help", help_message)


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


class Filegroup:
    def __init__(self, gtab):
        self.parent = gtab
        self.recursive = tk.BooleanVar()
        self.drv_label = tk.Label(self.parent, text="Drive Path:")
        self.drv_label.grid(row=0, column=0, padx=10, pady=10)
        self.drv_entry = tk.Entry(self.parent, width=50)
        self.drv_entry.grid(row=0, column=1, padx=10, pady=10)
        self.drv_browse_button = tk.Button(self.parent, text="Browse", command=self.browse_drv)
        self.drv_browse_button.grid(row=0, column=2, padx=10, pady=10)
        self.ext_label = tk.Label(self.parent, text="File Extension: eg .txt")
        self.ext_label.grid(row=1, column=0, padx=10, pady=10)
        self.ext_entry = tk.Entry(self.parent, bd=7,width=50)
        self.ext_entry.grid(row=1, column=1, padx=10, pady=10)
        self.dest_label = tk.Label(self.parent, text="Destination Path:")
        self.dest_label.grid(row=2, column=0, padx=10, pady=10)
        self.dest_entry = tk.Entry(self.parent, bd=7,width=50)
        self.dest_entry.grid(row=2, column=1, padx=10, pady=10)
        self.dest_browse_button = tk.Button(self.parent,bd=5, text="Browse", command=self.browse_dest)
        self.dest_browse_button.grid(row=2, column=2, padx=10, pady=10)
        self.dest_browse_button = tk.Button(self.parent,bd=5, bg="light green", text="Browsewith MKdir", command=self.browse_dest2)
        self.dest_browse_button.grid(row=2, column=3, padx=10, pady=10)
        self.recursive_checkbutton = tk.Checkbutton(self.parent, text="Recursive Search", variable=self.recursive)
        self.recursive_checkbutton.grid(row=3, column=1, padx=10, pady=10)
        self.search_button = tk.Button(self.parent, text="Search and Copy", command=self.search_and_copy)
        self.search_button.grid(row=4, column=1, padx=10, pady=10)

    def browse_drv(self):
        drv_path = filedialog.askdirectory()
        self.drv_entry.insert(0, drv_path)

    def browse_dest(self):
        dest_path = filedialog.askdirectory()
        self.dest_entry.insert(0, dest_path)
  
    def browse_dest2(self):
        dest_path = filedialog.askdirectory()
        
        # Get the current epoch time
        epoch_time = str(int(time.time()))
        
        # Create a new directory name using the epoch time
        new_dir_name = "result_" + epoch_time
        
        # Combine the selected directory path with the new directory name
        new_dest_path = os.path.join(dest_path, new_dir_name)
        
        # Check if the directory exists, and if not, create it
        if not os.path.exists(new_dest_path):
            os.makedirs(new_dest_path)
        
        # Clear the entry widget and insert the new destination path
        self.dest_entry.delete(0, 'end')
        self.dest_entry.insert(0, new_dest_path)
    def search_and_copy(self):
        drv_path = self.drv_entry.get()
        file_ext = self.ext_entry.get()
        dest_path = self.dest_entry.get()
        is_recursive = self.recursive.get()
        
        if not drv_path or not file_ext or not dest_path:
            messagebox.showerror("Error", "All fields are required")
            return
        
        if not os.path.exists(drv_path):
            messagebox.showerror("Error", "drv Path does not exist")
            return
        
        if not os.path.exists(dest_path):
            messagebox.showerror("Error", "Destination Path does not exist")
            return

        if is_recursive:
            files_copied = self.recursive_search_and_copy(drv_path, file_ext, dest_path)
        else:
            files_copied = self.non_recursive_search_and_copy(drv_path, file_ext, dest_path)

        messagebox.showinfo("Success", f"Copied {files_copied} files to {dest_path}")

    def recursive_search_and_copy(self, search_path, file_ext, dest_path):
        files_copied = 0
        for parent, _, files in os.walk(search_path):
            for file in files:
                if file.endswith(file_ext):
                    full_file_path = os.path.join(parent, file)
                    shutil.copy(full_file_path, dest_path)
                    files_copied += 1
        return files_copied

    def non_recursive_search_and_copy(self, search_path, file_ext, dest_path):
        files_copied = 0
        for file in os.listdir(search_path):
            full_file_path = os.path.join(search_path, file)
            if os.path.isfile(full_file_path) and file.endswith(file_ext):
                shutil.copy(full_file_path, dest_path)
                files_copied += 1
        return files_copied

class DatePicker_Calculator:
    def __init__(self, parent):
        self.parent = parent
        self.now = datetime.now().strftime("%m %d %Y %H %M %S")
        month, day, year, hour, minute, second = self.now.split()
        self.current_time = strftime('%H:%M:%S', localtime())

        # Entry frame using grid
        self.efrm = tk.Frame(self.parent, width=180, height=15)
        self.efrm.grid(row=0, column=0)
         

        # Spinboxes for hour, minute, second
        self.hour_var = tk.StringVar(value=hour)
        self.hour_spin = ttk.Spinbox(self.efrm, from_=0, to=23, width=2, textvariable=self.hour_var)
        self.hour_spin.grid(row=0, column=5)

        self.minute_var = tk.StringVar(value=minute)
        self.minute_spin = ttk.Spinbox(self.efrm, from_=0, to=59, width=2, textvariable=self.minute_var)
        self.minute_spin.grid(row=0, column=6)

        self.second_var = tk.StringVar(value=second)
        self.second_spin = ttk.Spinbox(self.efrm, from_=0, to=59, width=2, textvariable=self.second_var)
        self.second_spin.grid(row=0, column=7)

        tk.Label(self.efrm, text="T1 Entry").grid(row=0,column=0)
        self.et1 = tk.Entry(self.efrm, bd=7)
        self.et1.grid(row=0, column=1)
        tk.Label(self.efrm, text="T2 Entry").grid(row=1,column=0)
        self.et2 = tk.Entry(self.efrm, bd=7)
        self.et2.grid(row=1, column=1)
        tk.Label(self.efrm, text="").grid(row=1,column=2)
        tk.Label(self.efrm, text="Date Selection").grid(row=0,column=4)
        self.et11 = tk.Entry(self.efrm, bd=7,width=60)
        self.et11.grid(row=1, column=4, columnspan=2)
        tk.Label(self.efrm, text="Time Difference").grid(row=3,column=4)
        self.et22 = tk.Entry(self.efrm, bd=7,width=60)
        self.et22.grid(row=2, column=4, columnspan=2)
        self.et3 = tk.Entry(self.efrm, bd=7)
        
        tk.Label(self.efrm, text="Date1").grid(row=0,column=7)
        self.et3.grid(row=1, column=7)
        tk.Label(self.efrm, text="Date2").grid(row=3,column=7)
        self.et4 = tk.Entry(self.efrm, bd=7)
        self.et4.grid(row=4, column=7)
        tk.Label(self.efrm, text="Date Diff").grid(row=0,column=10)
        self.output=tk.Text(self.efrm,width=25,height=4)
        self.output.grid(row=0,column=12)
        tk.Label(self.efrm, text="Current Epoch Time").grid(row=0,column=16)
        self.et7 = tk.Entry(self.efrm, bd=7,font=("Helvetica", 14))
        self.et7.grid(row=0, column=17)
        tk.Label(self.efrm, text="Current Time").grid(row=1,column=16)
        self.et8 = tk.Entry(self.efrm, bd=7,font=("Helvetica", 14))
        self.et8.grid(row=1, column=17)
        #tk.Label(self.efrm, text="").grid(row=1,column=0)
        self.current_month = datetime.now().month  # Corrected to datetime.now().month
        self.current_year = datetime.now().year    # Corrected to datetime.now().year
        self.current_time = strftime('%H:%M:%S', localtime())
        self.epoch_time = int(time.time())  
        nav_frame = tk.Frame(self.parent, width=40, height=40)
        nav_frame.grid(row=1, column=0, pady=10)

        b1=tk.Button(self.efrm, text="Time1",bd=4, command=self.insert1)
        b1.grid(row=10, column=0)
        b2=tk.Button(self.efrm, text="Time2",bd=4, command=self.insert2)
        b2.grid(row=11, column=0)
        b3=tk.Button(self.efrm, text="Calculate Diff",bd=6,command=self.hour_diff)
        b3.grid(row=10, column=1)
        b4=tk.Button(self.efrm, text="Date1", bd=4,command=self.date1)
        b4.grid(row=10, column=12)    
        b5=tk.Button(self.efrm, text="Date2", bd=4,command=self.date2)
        b5.grid(row=11, column=12)
        b6=tk.Button(self.efrm, text="Calculate Date Diff",bd=7, command=self.date_diff)
        b6.grid(row=10, column=15)
        bt12=tk.Button(self.efrm, text="Clear Entries",bd=5, command=self.clear)
        bt12.grid(row=10, column=20)
        self.month_pick = tk.Entry(self.efrm, bd=9,width=20)
        self.month_pick.grid(row=20, column=4)
        self.day_pick = tk.Entry(self.efrm, bd=9,width=20)
        self.day_pick.grid(row=20, column=5)


        # Previous month button
        self.day_buttons = []
        prev_month_btn = tk.Button(nav_frame, text="< Prev",bd=6, command=self.prev_month)
        prev_month_btn.grid(row=0, column=0)

        # Month/Year label
        self.month_year_label = tk.Label(nav_frame, text="", font=("Helvetica", 16))
        self.month_year_label.grid(row=20, column=1)

        # Next month button
        next_month_btn = tk.Button(nav_frame, text="Next >",bd=6, command=self.next_month)
        next_month_btn.grid(row=0, column=2)

        # Calendar frame using grid
        self.calendar_frame = tk.Frame(self.parent)
        self.calendar_frame.grid(row=2, column=0, rowspan=2,columnspan=2)
        
        # Display the current month calendar
        self.display_calendar(self.current_year, self.current_month)
    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.display_prev(self.current_year, self.current_month)

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.display_next(self.current_year, self.current_month)
    def display_calendar(self, year, month):
        self.month_year_label.config(text=f"{calendar.month_name[month]} {year}")
        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(weekdays):
            tk.Label(self.calendar_frame, text=day).grid(row=0, column=i)

        # Fill in the days of the month
        month_days = calendar.monthcalendar(year, month)
        month_days = calendar.monthcalendar(year, month)

        self.day_buttons.clear()  # Make sure to clear the list before adding new buttons
        for row_index, week in enumerate(month_days):
            for col_index, day in enumerate(week):
                if day == 0:
                    # Create a blank label for alignment if the day is 0 (empty cell)
                    lbl = tk.Label(self.calendar_frame, text="")
                    lbl.grid(row=row_index + 1, column=col_index)
                    continue
                btn = tk.Button(self.calendar_frame, text=str(day), bd=16, width=3, height=2,bg="alice blue",font=("Helvetica", 14),
                                command=lambda m=month, d=day, y=year: self.update(m, d, y))
                btn.grid(row=row_index + 1, column=col_index)
                self.day_buttons.append(btn)  # Add the button to the list

    def display_prev(self, year, month):
        self.clear_calendar()
        self.display_calendar(year, month)

    def display_next(self, year, month):
        self.clear_calendar()
        self.display_calendar(year, month)

    
    def update_clock(self):
        self.time = f"{self.hour_var.get()}:{self.minute_var.get()}:{self.second_var.get()}"
        
        self.current_time = strftime('%H:%M:%S', localtime())
        self.epoch_time = int(time.time())
        self.et7.delete(0, END)
        self.et8.delete(0, END)
        self.et7.insert(END, self.epoch_time)  # Corrected the typo 'eself.poch_time'
        self.et8.insert(END, self.current_time)  # Corrected the typo 'cuurent_time'
        self.parent.after(1000, self.update_clock)
    def update(self, month, day, year):
        weekday_dict = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 
                     4: "Friday", 5: "Saturday", 6: "Sunday"}

          # Create a date object from the year, month, and day
        months_dict = {'January': 1, 'February': 2,'March': 3, 'April': 4,'May': 5,
                  'June': 6,'July': 7, 'August': 8, 'September': 9,'October': 10,
                  'November': 11,'December': 12}

        # Create a date object from the year, month, and day
        self.date_obj = datetime(year, month, day)
        formatted_date = self.date_obj.strftime("%m-%d-%Y")  # Format the date as "month-day-year"

        # Get the day of the week as an integer (Monday is 0, Sunday is 6)
        day_of_week_int = self.date_obj.weekday()

        # Use the day_of_week_int to get the day name from weekday_dict
        day_of_week_name = weekday_dict[day_of_week_int]

        # Get the month name from the month number
        month_name = calendar.month_name[month]

        # Update the daypick entry with the day of the week name
        self.day_pick.delete(0, tk.END)
        self.day_pick.insert(tk.END, day_of_week_name)

        # Update the month_pick entry with the month name
        self.month_pick.delete(0, tk.END)
        self.month_pick.insert(tk.END, month_name)

        # Update the date Entry with the formatted date
        self.et11.delete(0, tk.END)
        self.et11.insert(tk.END, formatted_date)

    def insert1(self):
        self.time = f"{self.hour_var.get()}:{self.minute_var.get()}:{self.second_var.get()}"
        self.et1.delete(0, END)
        self.et1.insert(END, self.time)
        
    def insert2(self):
        self.time = f"{self.hour_var.get()}:{self.minute_var.get()}:{self.second_var.get()}"
        self.et2.delete(0, END)
        self.et2.insert(END, self.time)
    def date1(self):
        dateone = self.et11.get()
        self.et3.delete(0, END)
        self.et3.insert(END, dateone)


    def date2(self):
        datetwo = self.et11.get()
        self.et4.delete(0, END)
        self.et4.insert(END, datetwo)
    def hour_diff(self):
        hhmmss = "%H:%M:%S"
        try:
            self.et11.delete(0, END)
            print(self.et1.get())
            print(self.et2.get())
            start_time = datetime.strptime(self.et1.get(), hhmmss).time()
            end_time = datetime.strptime(self.et2.get(), hhmmss).time()
            # Calculate the difference in seconds
            difference_in_seconds = (datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).total_seconds()
            # Convert seconds to hours and minutes
            hours, remainder = divmod(difference_in_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            result = f"Time difference: {int(hours)} hours  {int(minutes)} minutes and {int(seconds)} Seconds"
       
            self.et22.delete(0, END)
            
            self.et22.insert(END, result)
        except ValueError:
            self.et22.delete(0, END)
  
    def date_diff(self):
        date_format = "%m-%d-%Y"  # Date format without time
        try:
            self.day_buttions = []
            start_date_str = self.et3.get()
            end_date_str = self.et4.get()
            start_date = datetime.strptime(start_date_str, date_format)
            end_date = datetime.strptime(end_date_str, date_format)

            # Initialize counters for years and months
            years, months = 0, 0
            
            # Increment years until the year of the end date is reached
            while (start_date.year + years) < end_date.year:
                years += 1
            
            # After counting years, adjust the start date
            year_adjusted_start_date = start_date.replace(year=start_date.year + years)
            
            # Increment months until the month of the end date is reached or passed
            while year_adjusted_start_date.replace(month=year_adjusted_start_date.month + months) < end_date:
                months += 1
                if year_adjusted_start_date.month + months > 12:  # Loop back to January
                    months -= 12
                    years += 1
            
            # After counting months, adjust the start date again
            month_adjusted_start_date = year_adjusted_start_date.replace(month=year_adjusted_start_date.month + months)
            
            # Calculate the remaining days
            remaining_days = (end_date - month_adjusted_start_date).days
            rmdays = abs(remaining_days)
            # Correct for the month overshooting
            if month_adjusted_start_date > end_date:
                months -= 1
                if months < 0:  # If months go negative, loop back to December and decrement years
                    months = 11
                    years -= 1
                # Recalculate remaining days with corrected month
                month_adjusted_start_date = month_adjusted_start_date.replace(month=month_adjusted_start_date.month - 1)
                remaining_days = (end_date - month_adjusted_start_date).days
                rmdays = abs(remaining_days)

            # Format the result
            result = f"Date difference: {years} years, {months} months and {rmdays} days"
            print(result)
            self.output.delete("1.0", END)
            self.output.insert(END, result)
        except ValueError:
            self.output.delete("1.0", END)
            self.output.insert(END, "Invalid date format. Please use MM-DD-YYYY")
    def clear(self):
        self.et1.delete(0, END)
        self.et2.delete(0, END)
        self.et3.delete(0, END)
        self.et4.delete(0, END)
        self.et11.delete(0, END)
        self.et22.delete(0, END)     
        self.output.delete("1.0", END)
    def find_day(self, month,day,year):
        daynum = calendar.weekday(year, month, day)
        # Modify days list to start with Sunday as 0
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday"]
        return days[daynum]   
    def clear_calendar(self):
        for button in self.day_buttons:
            button.grid_forget()  # This will remove the button from the grid
            button.destroy()      # This will destroy the button widget
        self.day_buttons.clear()




class File_Diff:
    def __init__(self, parent):
        self.parent = parent
        self.nb2 = ttk.Notebook(self.parent)
        self.nb2.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")      
        self.tab_input = ttk.Frame(self.nb2)
        self.tab_file1 = ttk.Frame(self.nb2)
        self.tab_file2 = ttk.Frame(self.nb2)
        self.tab_diff = ttk.Frame(self.nb2)
        self.nb2.add(self.tab_input, text="Setup")
        self.nb2.add(self.tab_file1, text="File 1")
        self.nb2.add(self.tab_file2, text="File 2")
        self.nb2.add(self.tab_diff, text="Differences")
        self.txt_file1 = ScrolledText(self.tab_file1, wrap=tk.WORD)
        self.txt_file1.grid(row=1, column=0)
        self.txtinfo1 = TextWidgetInfo(self.tab_file1, self.txt_file1)
        self.txt_file2 = ScrolledText(self.tab_file2, wrap=tk.WORD)
        self.txt_file2.grid(row=1, column=0)
        self.txtinfo2 = TextWidgetInfo(self.tab_file2, self.txt_file2)
        self.btn_select_file1 = tk.Button(self.tab_input, text="Select File 1", command=self.select_file1)
        self.btn_select_file1.grid(row=1, column=0, padx=10, pady=10)
        self.btn_select_file2 = tk.Button(self.tab_input, text="Select File 2", command=self.select_file2)
        self.btn_select_file2.grid(row=4, column=0, padx=10, pady=10)
        self.btn_compare_files = tk.Button(self.tab_input, text="Compare Files", command=self.compare_files)
        self.btn_compare_files.grid(row=11, column=0, columnspan=2, padx=10, pady=10)
        # Labels to display selected file paths
        self.lbl_file1_path = tk.Label(self.tab_input, text="No File Selected")
        self.lbl_file1_path.grid(row=2, column=0, padx=10, pady=10)
        self.lbl_file2_path = tk.Label(self.tab_input, text="No File Selected")
        self.lbl_file2_path.grid(row=5, column=0, padx=10, pady=10)
        tk.Label(self.tab_input,text="@@ and Blue text is location differences").grid(row=7, column=0)
        tk.Label(self.tab_input,text=" -   Red text is removed or missing differences, example would be stuff not in file2 just file 1, unique to file1").grid(row=8, column=0)
        tk.Label(self.tab_input,text="+ Green is addition differences thing that are in file2 that don't match file 1 unigue to file2 ").grid(row=9, column=0)
        tk.Label(self.tab_input,text="These are displayed in the diff tab").grid(row=10, column=0)      
        self.btn_save_differences = tk.Button(self.tab_input, text="Save Differences", command=self.save_differences)
        self.btn_save_differences.grid(row=10, column=1, columnspan=2, padx=10, pady=10)
        self.txt_differences = ScrolledText(self.tab_diff, wrap=tk.WORD)
        self.txt_differences.grid(row=1, column=0)
        self.txtinfo3 = TextWidgetInfo(self.tab_diff, self.txt_differences)
        self.btn_clear_all = tk.Button(self.tab_input, text="Clear All", command=self.clear_all)
        self.btn_clear_all.grid(row=11, column=1, columnspan=2, padx=10, pady=10)

    def clear_all(self):
        # Clear all Text widgets
        self.txt_differences.delete('1.0', tk.END)
        self.txt_file1.delete('1.0', tk.END)
        self.txt_file2.delete('1.0', tk.END)

        # Reset file selection labels
        self.lbl_file1_path.config(text="No File Selected")
        self.lbl_file2_path.config(text="No File Selected")

    def select_file1(self):
        file_path = filedialog.askopenfilename()
        self.lbl_file1_path.config(text=file_path)
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.txt_file1.delete('1.0', tk.END)
                self.txt_file1.insert(tk.END, content)

    def select_file2(self):
        file_path = filedialog.askopenfilename()
        self.lbl_file2_path.config(text=file_path)
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.txt_file2.delete('1.0', tk.END)
                self.txt_file2.insert(tk.END, content)



    def save_differences(self):
        # Open save file dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            # Write the contents of the Text widget to the file
            with open(file_path, "w") as file:
                file.write(self.txt_differences.get("1.0", tk.END))
    def compare_files(self):
        file1_path = self.lbl_file1_path.cget("text")
        file2_path = self.lbl_file2_path.cget("text")

        if file1_path != "No File Selected" and file2_path != "No File Selected":
            with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
                file1_lines = file1.readlines()
                file2_lines = file2.readlines()

            # Implement the comparison logic
            self.compare_and_display(file1_lines, file2_lines)

    def compare_and_display(self, file1_lines, file2_lines):
        # Increase the number of context lines for better visibility
        context_lines = 10  # You can adjust this number as needed
        diff = list(difflib.unified_diff(file1_lines, file2_lines, lineterm='', n=context_lines))
        
        # Clear the Text widget before displaying new content
        self.txt_differences.delete('1.0', tk.END)

        if diff:
            # Enhanced formatting for readability
            for line in diff:
                # You can add more formatting here if needed
                self.txt_differences.insert(tk.END, line + '\n')
        else:
            # Display message if no differences are found
            self.txt_differences.insert(tk.END, "No differences found.")

    def compare_and_display(self, file1_lines, file2_lines):
        context_lines = 3 
        diff = list(difflib.unified_diff(file1_lines, file2_lines, lineterm=''))
        self.txt_differences.delete('1.0', tk.END)
        if diff:
            for line in diff:
                if line.startswith('@@'):
                    self.txt_differences.insert(tk.END, line + '\n', 'location')
                elif line.startswith('+'):
                    self.txt_differences.insert(tk.END, line + '\n', 'add')
                elif line.startswith('-'):
                    self.txt_differences.insert(tk.END, line + '\n', 'remove')
                else:
                    self.txt_differences.insert(tk.END, line + '\n')

            # Tag configuration for better visibility
            self.txt_differences.tag_config('location', foreground='blue')
            self.txt_differences.tag_config('add', foreground='green')
            self.txt_differences.tag_config('remove', foreground='red')


class Multi_Find_Replace:
    def __init__(self, parent):
        self.parent = parent
        self.recursive_search = tk.BooleanVar(value=True)  # Variable to control recursion

        # GUI Components
        self.setup_gui()

    def setup_gui(self):
        # Frame for control widgets
        self.control_frame = tk.Frame(self.parent)
        self.control_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nw')

        # Select Directory Button
        select_button = tk.Button(self.control_frame, text="Select Directory", command=self.select_directory)
        select_button.grid(row=0, column=0, padx=10, pady=5)

        # Directory Label
        self.directory_label = tk.Label(self.control_frame, text="Select a directory", fg="blue")
        self.directory_label.grid(row=1, column=0, padx=10, pady=5)

        # Recursive Search Checkbutton
        self.recursive_checkbutton = tk.Checkbutton(self.control_frame, text="Recursive Search", variable=self.recursive_search)
        self.recursive_checkbutton.grid(row=2, column=0, padx=10, pady=5)

        # Find and Replace Entries
        self.setup_find_replace_entries()

        # Buttons
        self.setup_buttons()

        # Skip Lines Spinbox
        tk.Label(self.control_frame, text="Skip Lines:").grid(row=6, column=0, sticky='e', padx=10)
        self.skip_lines_spinbox = tk.Spinbox(self.control_frame, from_=0, to=10, width=5)
        self.skip_lines_spinbox.grid(row=6, column=1, padx=10, pady=5)

        # List Box
        self.list_box = tk.Listbox(self.parent, width=80, height=20)
        self.list_box.grid(row=0, column=2, rowspan=6, padx=10, pady=10)

    def setup_find_replace_entries(self):
        tk.Label(self.control_frame, text="Find:").grid(row=3, column=0, sticky='e', padx=10)
        self.find_entry = tk.Entry(self.control_frame)
        self.find_entry.grid(row=3, column=1, padx=10)

        tk.Label(self.control_frame, text="Replace With:").grid(row=4, column=0, sticky='e', padx=10)
        self.replace_entry = tk.Entry(self.control_frame)
        self.replace_entry.grid(row=4, column=1, padx=10)

    def setup_buttons(self):
        find_button = tk.Button(self.control_frame, text="Find", command=self.find_in_files)
        find_button.grid(row=5, column=1, padx=10, pady=10)
        replace_button = tk.Button(self.control_frame, text="Replace", command=lambda: self.find_in_files(True))
        replace_button.grid(row=6, column=1, padx=10, pady=10)
        skiplines_button = tk.Button(self.control_frame, text="Skip # Line Replace", command=self.skip_line_replace)
        skiplines_button.grid(row=7, column=1, padx=10, pady=10)

    def select_directory(self):
        directory = filedialog.askdirectory()
        self.directory_label.config(text=directory)

    def skip_line_replace(self):
        skip_lines = int(self.skip_lines_spinbox.get())
        self.find_in_files(True, skip_lines)

    def find_in_files(self, replace=False, skip_lines=0):
        directory = self.directory_label.cget("text")
        find_word = self.find_entry.get()
        replace_word = self.replace_entry.get() if replace else None
        recursive = self.recursive_search.get()

        # Create a unique directory name with 'replace' and epoch time
        unique_dir_name = f"replace_{int(time.time())}"
        new_directory = os.path.join(directory, unique_dir_name)
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)

        self.list_box.delete(0, tk.END)  # Clear existing entries in the list box

        if recursive:
            walker = os.walk(directory)
        else:
            walker = [(directory, [], os.listdir(directory))]

        for parent, dirs, files in walker:
            extlist = ['.txt', '.py', '.rtf', '.TXT']
            for file in files:
                if file.endswith(tuple(extlist)):
                    file_path = os.path.join(parent, file)
                    new_file_path = os.path.join(new_directory, file)  # New file path in the new directory
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.readlines()
                    except UnicodeDecodeError:
                        try:
                            with open(file_path, 'r', encoding='ISO-8859-1') as f:
                                content = f.readlines()
                        except Exception as e:
                            messagebox.showerror("Error", f"An error occurred while processing {file_path}: {e}")
                            continue
                    
                    # Process content with skipping lines if needed
                    new_content = []
                    for i, line in enumerate(content):
                        if replace and replace_word and (i >= skip_lines):
                            new_line = line.replace(find_word, replace_word)
                            new_content.append(new_line)
                        else:
                            new_content.append(line)
                    count = ''.join(new_content).count(replace_word if replace else find_word)
                    
                    if count > 0:
                        # Write the replaced content to the new file path
                        with open(new_file_path, 'w', encoding='utf-8') as f:
                            f.writelines(new_content)
                        self.list_box.insert(tk.END, f"{file}: Replaced {count} occurrences in new directory")
                    else:
                        # Even if no occurrences, copy the original file
                        shutil.copyfile(file_path, new_file_path)



class Concatinate_Text:
    def __init__(self, parent):

        self.parent = parent
        self.selected_files = []
        self.listbox = tk.Listbox(self.parent, width=80, bd=7, bg="snow", selectmode='multiple')
        self.listbox.grid(row=1, column=1)
        self.txtout = ScrolledText(self.parent, bd=7, bg="alice blue", width=80,height=35)
        self.txtout.grid(row=14, column=2)
        # Button to select files
        self.select_button = tk.Button(self.parent, bd=5, bg="lavender", text='Select Files', command=self.select_files)
        self.select_button.grid(row=10, column=2)
        # Button to clear Listbox & Textbox
        self.clear_button = tk.Button(self.parent, bd=5, bg ="light blue", text='Clear', command=self.clearall)
        self.clear_button.grid(row=10, column=3)
        # Button to merge files
        self.merge_button = tk.Button(self.parent, bd=7, bg="light green", text='Merge Files', command=self.merge_files)
        self.merge_button.grid(row=11, column=2)

    def select_files(self):
        file_paths = filedialog.askopenfilenames(title='Select files to merge')
        if file_paths:
            self.selected_files = file_paths
            self.listbox.delete(0, tk.END)
            for path in file_paths:
                self.listbox.insert(tk.END, path)

    def merge_files(self):
        if not self.selected_files:
            messagebox.showwarning('Warning', 'No files selected.')
            return

        epoch_time = int(time.time())
        output_filename = f"{epoch_time}.txt"
        output_directory = filedialog.askdirectory(title='Select Output Directory')

        if not output_directory:
            messagebox.showwarning('Warning', 'No output directory selected.')
            return

        output_path = os.path.join(output_directory, output_filename)

        try:
            with open(output_path, 'w') as output_file:
                self.txtout.delete("1.0", tk.END)
                for file_path in self.selected_files:
                    with open(file_path, 'r') as input_file:
                        file_content = input_file.read()
                        self.txtout.insert(tk.END, file_content)
                        output_file.write(file_content)
                        output_file.write("\n")  # Optional: add a newline between files
                       
            messagebox.showinfo('Success', f'Files have been merged and saved as {output_filename}')
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {e}')

    def clearall(self):
        self.txtout.delete("1.0", tk.END)
        self.listbox.delete(0, tk.END)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("JH Multi Tool Suite")
    notebook = ttk.Notebook(root)
    notebook.pack(expand=1, fill='both')

    # Add PyGrepSim Tab
    pygrep_tab = tk.Frame(notebook)
    notebook.add(pygrep_tab, text='PyGrepSim')
    PyGrepSim(pygrep_tab)

    # Add File Comparator Tab
    file_comparator_tab = tk.Frame(notebook)
    notebook.add(file_comparator_tab, text='File Split Compare')
    FileComparator(file_comparator_tab)
    txttab = tk.Frame(notebook)
    notebook.add(txttab, text="Text Compare")
    TextComparator(txttab)
    
    gtab = tk.Frame(notebook)
    notebook.add(gtab, text="GroupFile")
    Filegroup(gtab)
    mtab = tk.Frame(notebook)

    dtab= tk.Frame(notebook)
    notebook.add(dtab, text="Datetime")
    dp = DatePicker_Calculator(dtab)
   


    diff = tk.Frame(notebook)
    notebook.add(diff, text="File Diff")
    df = File_Diff(diff)

    mfr = tk.Frame(notebook)
    notebook.add(mfr, text="Find Replace Files Save")
    replace_save = Multi_Find_Replace(mfr)



    merge = tk.Frame(notebook)
    notebook.add(merge, text="Concatinate Text")
    cat = Concatinate_Text(merge)
  

    root.after(500,dp.update_clock)
    root.mainloop()
