
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Spinbox, Toplevel
from tkinter.scrolledtext import ScrolledText
import os
import re
import json
import time
import shutil
import csv
import difflib
import math
from pathlib import Path
from datetime import datetime
#You can set the number of lines you want to see before and after the search pattern
#using the spinboxes at the bottom
#3rd Party Modules
#from reportlab.lib.pagesizes import letter
#from reportlab.pdfgen import canvas



class Selected_Extensions:
    def __init__(self, top):
        self.top = top
        self.listbox = tk.Listbox(self.top, selectmode=tk.SINGLE)
        self.listbox.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.entry = tk.Entry(self.top,bd=8,bg="seashell")
        self.entry.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="ew")
        tk.Label(self.top, text="<-- Entry for new file type to ignore/group (e.g., .png)").grid(row=1, column=2)
        self.add_button = tk.Button(self.top, bd=4, bg="misty rose", text="Add Item", command=self.add_item)
        self.add_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.delete_button = tk.Button(self.top, bd=4, bg="yellow", text="Delete Selected", command=self.delete_selected)
        self.delete_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.clear_button = tk.Button(self.top, bd=4, bg="azure", text="Clear List", command=self.clear_list)
        self.clear_button.grid(row=2, column=2, padx=10, pady=5, sticky="ew")
        self.save_button = tk.Button(self.top, bd=4, bg="cyan", text="Save List", command=self.save_list)
        self.save_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.load_button = tk.Button(self.top, bd=4, bg="light green", text="Load List", command=self.load_list)
        self.load_button.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.default_button = tk.Button(self.top, bd=4, bg="plum", text="Load Default List", command=self.default_list_load)
        self.default_button.grid(row=4,column = 1,padx = 10,pady = 5 ,sticky ="ew") 
        self.convert_button = tk.Button(self.top, bd=6, bg="orange", text="Convert to List", command=self.convert_to_list)
        self.convert_button.grid(row=3,column = 2,padx = 10,pady = 5 ,sticky ="ew") 
        tk.Label(self.top,text ="To ignore/group files, use the 'Convert to List' button").grid(row = 5 ,column = 2)

        # Grid expansion
        self.top.grid_rowconfigure(0 ,weight = 1)
        self.top.grid_columnconfigure(0 ,weight = 1)

    def add_item(self):
        item = self.entry.get()
        if item:
            self.listbox.insert(tk.END ,item)
            self.entry.delete(0 ,tk.END)
        else :
            messagebox.showwarning("Input Error","Please enter a valid item.")

    def delete_selected(self):
        selected = self.listbox.curselection()
        if selected :
            self.listbox.delete(selected)
        else :
            messagebox.showwarning("Selection Error","Please select an item to delete.")

    def clear_list(self):
        self.listbox.delete(0 ,tk.END)

    def save_list(self):
        items =self.listbox.get(0 ,tk.END)
        if items :
            file_path = filedialog.asksaveasfilename(defaultextension=".json" ,filetypes =[("JSON files","*.json")])
            if file_path :
                with open(file_path,'w')as f:
                    json.dump(items,f)
                messagebox.showinfo("Save Successful","List saved successfully.")
                return items
            else :
                messagebox.showwarning("Save Error","The list is empty.")

    def load_list(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                items = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            messagebox.showerror("Load Error", f"Could not load the list:\n{exc}")
            return []

        if not isinstance(items, list):
            messagebox.showerror("Load Error", "The JSON file does not contain a list.")
            return []

        self.clear_list()
        for item in items:
            self.listbox.insert(tk.END, str(item))
        return items

    def convert_to_list(self):
        items = self.listbox.get(0, tk.END)
        if items:
            converted = list(items)
            messagebox.showinfo("List Conversion", f"List: {converted}")
            return converted

        messagebox.showwarning("Conversion Error", "The list is empty.")
        return []

    def get_selected_extensions(self):
         return [item.lower()for item in self.listbox.get(0 ,tk.END)]

    def default_list_load(self):
        selectlist = [
            ".dat", ".png", ".mov", ".bmd.out", ".bmd", ".log",
            ".jpeg", ".xml", ".svg", ".bmp", ".mp3", ".avi", ".py"
        ]
        existing = {item.lower() for item in self.listbox.get(0, tk.END)}
        for item in selectlist:
            if item.lower() not in existing:
                self.listbox.insert(tk.END, item)
             
  
class PyGrepSim:
   
    def __init__(self, root):
        self.root = root

        # Initialize frame_lines_control first
        self.frame_lines_control = tk.Frame(self.root)
        self.frame_lines_control.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        self.var_recursive = tk.BooleanVar()  # Variable for recursive option
        self.var_case_insensitive = tk.BooleanVar()  # Variable for case-insensitive option
        self.var_regex = tk.BooleanVar(value=True)
        self.var_whole_word = tk.BooleanVar(value=False)

        self.setup_gui()  # Call setup_gui after initializing the required attributes

        self.subpath = "/"
        self.path = os.path.join(os.path.expanduser("~"), self.subpath)

        self.matched_files = []  # List to store matched files

        # Initialize selected_Extensions
        self.top = Toplevel(self.root)
        self.sel_ext = Selected_Extensions(self.top)
        self.top.withdraw()  # Hide the window initially

    def setup_gui(self):
        self.create_options_frame()
        self.create_file_frame()
        self.create_lines_control_frame()
        self.create_text_area()

    def create_options_frame(self):
        frame_options = tk.Frame(self.root)
        frame_options.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        tk.Label(frame_options, text="Pattern: RegEx or Exact").grid(row=0, column=0, padx=5, pady=5)
        self.entry_pattern = tk.Entry(frame_options, bd=7, bg="ivory")
        self.entry_pattern.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame_options, text="<---- In search entry  ex: AXXX or anything, If recursive checked, it might take a longer time to do search").grid(row=0, column=6, padx=5, pady=5)
        check_case_insensitive = tk.Checkbutton(frame_options, text="Case Insensitive", variable=self.var_case_insensitive)
        check_case_insensitive.grid(row=0, column=2, padx=5, pady=5)

        # Add the recursive search check button
        check_recursive = tk.Checkbutton(frame_options, text="<---Recursive (Look in all subdirectories)", variable=self.var_recursive)
        check_recursive.grid(row=0, column=3, padx=5, pady=5)
        tk.Checkbutton(frame_options, text="Regular expression", variable=self.var_regex).grid(row=0, column=4, padx=5)
        tk.Checkbutton(frame_options, text="Whole word", variable=self.var_whole_word).grid(row=0, column=5, padx=5)
        
        # Add the save path entry and browse button
        tk.Label(frame_options, text="").grid(row=1, column=0, padx=5, pady=5)
        self.entry_save_path = tk.Entry(frame_options, bd=7)
        self.entry_save_path.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(frame_options, bd=5, bg="alice blue",text="Browse, Path, saves to output location", command=self.browse_save_path).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(frame_options, text="Show Ignore list for_file extensions", bd=7, bg="pink", command=self.selected_ext).grid(row=0, column=8)
        tk.Label(frame_options, text="").grid(row=1, column=4, padx=5, pady=5)

    def create_file_frame(self):
        frame_file = tk.Frame(self.root)
        frame_file.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        tk.Label(frame_file, text="Filename:").grid(row=0, column=0, padx=5, pady=5)
        self.filenamelist = tk.Listbox(frame_file, bd=7,bg="antique white", width=50)
        self.filenamelist.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(frame_file, text="Browse Directory for Search", bd=5, bg="light blue", command=self.open_file_dialog).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(frame_file, text="Save_Filelist", bd=3, bg="azure", command=self.save_filelist).grid(row=0, column=3, padx=5, pady=5)
        tk.Button(frame_file, text="Search All", bd=6, bg="light green", command=self.search_for_pattern).grid(row=0, column=4, padx=5, pady=5)
        tk.Button(frame_file, text="Save Text Below After Search All", bd=5, bg="orange", command=self.save_file).grid(row=0, column=5, padx=5, pady=5)
        
        
        tk.Button(frame_file, text="Copy Matched Files", bd=5, bg="plum1", command=self.copy_matches).grid(row=0, column=6, padx=5, pady=5)
        tk.Button(frame_file, text="Clear All", bd=3, bg="wheat", command=self.clear_all).grid(row=0, column=7, padx=5, pady=5)
       

    def create_text_area(self):
        self.text_area = ScrolledText(self.root, bd=7, bg="navajo white", height=25, width=120)
        self.text_area.grid(row=3, column=0, padx=5, pady=5)
        tk.Label(self.root, text="<----Output text, all matched files").grid(row=3, column=5, sticky="ew")
        help_button = tk.Button(self.frame_lines_control, text="Help", command=self.show_help)
        help_button.grid(row=3, column=0, padx=5, pady=5)
        about_button = tk.Button(self.frame_lines_control, text="About", command=self.about)
        about_button.grid(row=3, column=2, padx=5, pady=5)
        reg_button = tk.Button(self.frame_lines_control, text="Regex Help", command=self.re_cheatsheet)
        reg_button.grid(row=3, column=4, padx=5, pady=5)

    def create_lines_control_frame(self):
        tk.Label(self.frame_lines_control, text="Lines before:").grid(row=0, column=0, sticky="e")
        self.spinbox_before = Spinbox(self.frame_lines_control, from_=0, to=99, width=3)
        self.spinbox_before.grid(row=0, column=1,sticky="w")
        self.spinbox_before.delete(0, tk.END)
        self.spinbox_before.insert(0, 1)  # Default value

        tk.Label(self.frame_lines_control, text="Lines after:").grid(row=0, column=2)
        self.spinbox_after = Spinbox(self.frame_lines_control, from_=0, to=99, width=3)
        self.spinbox_after.grid(row=0, column=3)
        self.spinbox_after.delete(0, tk.END)
        self.spinbox_after.insert(0, 3)  # Default value
        tk.Label(self.frame_lines_control, text="These spinboxes can be adjusted to show more information around the matching result").grid(row=2,column=0)

    def browse_save_path(self):
        path = filedialog.askdirectory()
        if path:
            self.entry_save_path.delete(0, tk.END)
            self.entry_save_path.insert(0, path)

    def open_file_dialog(self):
        path = filedialog.askdirectory()
        if not path:
            return

        self.path = path
        try:
            filelist = os.listdir(self.path)
        except OSError as exc:
            messagebox.showerror("Directory Error", f"Could not read directory:\n{exc}")
            return

        self.filenamelist.delete(0, tk.END)
        selected_extensions = self.sel_ext.get_selected_extensions()
        for filename in sorted(filelist):
            if not any(filename.lower().endswith(ext) for ext in selected_extensions):
                self.filenamelist.insert(tk.END, filename)

    def save_filelist(self):
        filelist = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("All Files", "*.*")],
                                                )
        if not filelist:
            return

        with open(filelist, "w") as output_file:
            flist = self.filenamelist.get(0, tk.END)
            output_file.write("\n".join(flist))
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
        self.matched_files.clear()

    def selected_ext(self):
        self.top.deiconify()  # Show the window

    def try_open_file(self, file_path):
        encodings = ("utf-8", "cp1252", "iso-8859-1")
        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.readlines()
            except UnicodeDecodeError:
                continue
            except OSError:
                return None
        return None

    def copy_matches(self):
        if not self.matched_files:
            messagebox.showinfo("Copy Matches", "Run a search first; there are no matched files to copy.")
            return
        self.save_matched_files()

    def save_matched_files(self):
        epoch_time = int(time.time())  # Get current epoch time to make directory
        raw_pattern = self.entry_pattern.get().strip() or "matches"
        safe_pattern = re.sub(r'[<>:"/\\|?*]+', "_", raw_pattern)[:60]
        directory_name = f"{safe_pattern}_{epoch_time}"
        save_path = self.entry_save_path.get() or os.path.expanduser("~")  # Use the provided save path or default to home directory
        full_directory_path = os.path.join(save_path, directory_name)
        os.makedirs(full_directory_path, exist_ok=True)  # Create directory in the specified location

        with open(os.path.join(full_directory_path, "filenames.txt"), "w") as file:
            for file_path in self.matched_files:
                filename = os.path.basename(file_path)
                file.write(f"{filename}\n")  # Write each filename on a new line
                # Copy each matching file to the new directory
                dst_path = os.path.join(full_directory_path, filename)  # Destination file path
                shutil.copy2(file_path, dst_path)  # Copy file to new directory

        messagebox.showinfo("Files Copied", f"Matching files and list have been copied to '{full_directory_path}'.")
    def search_for_pattern(self):
        patterns = self.entry_pattern.get().split(',')
        lines_before = int(self.spinbox_before.get())
        lines_after = int(self.spinbox_after.get())

        self.text_area.delete('1.0', tk.END)  # Clear the text area for new output
        self.matched_files.clear()  # Clear previous matched files

        try:
            raw_patterns = [p.strip() for p in patterns if p.strip()]
            if not raw_patterns:
                messagebox.showwarning("Search", "Enter at least one search pattern.")
                return
            cooked = []
            for pattern in raw_patterns:
                expression = pattern if self.var_regex.get() else re.escape(pattern)
                if self.var_whole_word.get():
                    expression = rf"\b(?:{expression})\b"
                cooked.append(expression)
            re_patterns = [re.compile(pattern, re.IGNORECASE if self.var_case_insensitive.get() else 0) for pattern in cooked]
        except re.error:
            messagebox.showerror("Invalid Pattern", "One or more entered patterns are not valid regular expressions.")
            return

        selected_extensions = self.sel_ext.get_selected_extensions()

        try:
            # Use recursive search if the checkbutton is selected
            if self.var_recursive.get():
                for root, dirs, files in os.walk(self.path):
                    for filename in files:
                        if not any(filename.lower().endswith(ext) for ext in selected_extensions):
                            self.process_file(root, filename, re_patterns, lines_before, lines_after)
            else:
                filenames = os.listdir(self.path)
                for filename in filenames:
                    if not any(filename.lower().endswith(ext) for ext in selected_extensions):
                        self.process_file(self.path, filename, re_patterns, lines_before, lines_after)

            self.text_area.insert(tk.END, f"\nSearch complete: {len(self.matched_files)} matching file(s).\n")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def process_file(self, directory, filename, re_patterns, lines_before, lines_after):
        file_extensions = ('.txt', '.py', '.dat', '.log')
        if filename.lower().endswith(file_extensions):
            file_path = os.path.join(directory, filename)
            lines = self.try_open_file(file_path)
            if lines is None:
                messagebox.showerror("Read Error", f"Could not read the file:\n{file_path}")
                return
            file_matched = False
            for i, line in enumerate(lines):
                for re_pattern in re_patterns:
                    if re_pattern.search(line):
                        if not file_matched:
                            self.matched_files.append(file_path)  # Add the file to matched files if it's not already added
                            file_matched = True
                        start = max(i - lines_before, 0)
                        end = min(i + lines_after + 1, len(lines))
                        self.text_area.insert(tk.END, f"---{filename}---\n")
                        for p in lines[start:end]:
                            self.text_area.insert(tk.END, p)
                        self.text_area.insert(tk.END, f"\n{'-'*40}\n")  # makes 40 dashed lines to separate the results
                        break  # Stop searching with other patterns if one matches

    def show_help(self):
        help_message = (
        "PyGrepSim Help\n"
        "This program allows you to search for patterns in text files using regular expressions.\n"
        "1. Pattern: Enter the regular expression pattern to search for, also see cheatsheet.\n"
        "2. Case Insensitive: Check this box to perform a case-insensitive search.\n"
        "3. Browse to select a directory  should contain text files or search will show filenames. .\n"
        "4. Lines Before/After: Set the number of lines to display before and after the matching pattern.\n"
        "5. Search All: Click to search for the pattern in the selected directory's files.\n"
        "6. Save: Save the search results displayed in the text area.\n"
        "7. Save Filelist: Save the list of filenames that contain the matching pattern.\n"
        "8. Clear: Clear all input fields and the text area.\n"
        "Note: For large files and/or recursive checked, the application may become unresponsive, but it is still processing. Please wait.\n"
        "9 The files that contain the search pattern can be sorted out and copied to a new directory that is what save path does")
        messagebox.showinfo("Help", help_message)
    def about(self):
        about_str = """ This program  was created in the hopes that it would be useful,\n  Made in 2024 \n  Python3.10
  Selected_Extensions Class:
        Manages a list of file extensions that the user can choose to ignore or group.
        Provides functionalities to add, delete, clear, save, load, and convert the list of extensions.

    PyGrepSim Class:
        A GUI tool for searching patterns within files using regular expressions.
        Supports options like case-insensitive search and recursive directory traversal.
        Allows users to specify the number of lines before and after the match to display.
        Outputs search results and can save matched files into a new directory.

    TextComparator Class:
        Provides functionalities to compare two text files.
        Highlights differences and similarities between the two files.
        Offers options to merge files based on differences or similarities.
        Can remove duplicate lines from the merged content and save the output.

    Filegroup Class:
        Allows users to search for files with specific extensions within a directory.
        Supports recursive search through subdirectories.
        Copies found files to a specified destination directory.

    Multi_Find_Replace Class:
        Facilitates find-and-replace operations across multiple text files within a directory.
        Supports recursive search through subdirectories.
        Allows users to replace found words and create a new directory with modified files.

    Concatinate_Text Class:
        Enables users to select multiple text files and merge their contents into a single file.
        Displays the merged content in a text area and allows saving it to a new file.

    FileReformatter Class:
        Processes test report files in text format to extract specific data fields.
        Reformats extracted data into a CSV logbook file.
        Displays formatted data in a text area within the GUI.

    Main Application:
        Uses tkinter's Notebook widget to create tabs for each utility.
        Initializes and sets up each utility class in its respective tab."""
        messagebox.showinfo("About", about_str)


    def re_cheatsheet(self):
        cheatsheet = r"""Py Regular Expression Cheat Sheet 
        Literal Characters: Matches the exact characters. Example: abc matches "abc".
        Metacharacters
        Matches any single character except newline(backslash n). Example: a.c matches "abc", "a1c", etc.
    ^: Matches the start of the string. Example: ^abc matches "abc" only if it's at the start of the string.
    $: Matches the end of the string.Example: abc$ matches "abc" only if it's at the end of the string.
    *: Matches 0 or more repetitions of the preceding character.Example: a* matches "", "a", "aa", etc.
    +: Matches 1 or more repetitions of the preceding character. Example: a+ matches "a", "aa", etc.
    ?: Matches 0 or 1 repetition of the preceding character.Example: a? matches "" or "a".
    {m}: Matches exactly m repetitions of the preceding character.
        Example: a{3} matches "aaa".
    {m,n}: Matches between m and n repetitions of the preceding character. Example: a{2,4} matches "aa", "aaa", or "aaaa".

    Character Classes
    [abc]: Matches any one of the characters a, b, or c. Example: [abc] matches "a", "b", or "c".
    [^abc]: Matches any character except a, b, or c. Example: [^abc] matches any character except "a", "b", or "c".
    [a-z]: Matches any lowercase letter. Example: [a-z] matches "a", "b", "c", ..., "z".
    \d: Matches any digit, equivalent to [0-9]. Example: \d matches "0", "1", ..., "9".
    \D: Matches any non-digit. Example: \D matches any character except "0", "1", ..., "9".
    \w: Matches any word character (alphanumeric plus underscore), equivalent to [a-zA-Z0-9_].
     Example: \w matches "a", "b", ..., "z", "A", ..., "Z", "0", ..., "9", "_".
    \W: Matches any non-word character.  Example: \W matches any character except "a", ..., "z", "A", ..., "Z", "0", ..., "9", "_".
    \s: Matches any whitespace character. Example: \s matches space, tab, newline, etc.
    \S: Matches any non-whitespace character. Example: \S matches any character except space, tab, newline, etc.

    Grouping and Alternation
        (abc): Matches "abc" and groups it.
        Example: (abc) matches "abc".
        a|b: Matches either "a" or "b".
        Example: a|b matches "a" or "b".

    Escaping
     \: Escapes a metacharacter \n = newline
        Example: \. matches a literal period.
    Anchors
        \b: Matches a word boundary.
        Example: \bword\b matches "word" only if it is a whole word.
    \B: Matches a non-word boundary.
        Example: \Bword\B matches "word" only if it is not a whole word.

    Lookahead and Lookbehind
    (?=...): Positive lookahead.
    Example: a(?=b) matches "a" only if followed by "b".
    (?!...): Negative lookahead.
        Example: a(?!b) matches "a" only if not followed by "b".
    (?<=...): Positive lookbehind.
        Example: (?<=a)b matches "b" only if preceded by "a".
    (?<!...): Negative lookbehind.
        Example: (?<!a)b matches "b" only if not preceded by "a".
"""
        messagebox.showinfo("Reg Ex Help", cheatsheet)        




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
        self.info_frame = ttk.Frame(self.parent)
        self.info_frame.grid(row=0, column=3, rowspan=2, sticky="ns")
        self.text1 = ScrolledText(self.txtfrm1,bd=6)
        self.text1.grid(row=0, column=0, sticky="nsew")
        self.text2 = ScrolledText(self.txtfrm2,bd=6)
        self.text2.grid(row=0, column=0, sticky="nsew")
        self.output_text = tk.Text(self.txtfrm3,bd=7, height=15)
        self.output_text.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.info_text = ScrolledText(self.info_frame,bd=4, width=30, height=20)
        self.info_text.grid(row=0, column=0, sticky="nsew")
         # Create buttons
        tk.Button(self.btfr, bd=4, bg="seashell3", text="Load Files", command=self.load_files).grid(row=0, column=0, sticky="w")
        tk.Button(self.btfr, bd=4, bg="light green", text="Compare", command=self.compare_files).grid(row=1, column=0, sticky="w")
        tk.Button(self.btfr, bd=4, bg="light blue", text="Merge with Differences", command=self.merge_with_differences).grid(row=2, column=0, sticky="w")
        tk.Button(self.btfr, bd=4, bg="cyan", text="Merge with Similarities", command=self.merge_with_similarities).grid(row=3, column=0, sticky="w")
        tk.Button(self.btfr, bd=4, bg="orange", text="Remove Duplicates", command=self.remove_duplicates).grid(row=4, column=0, sticky="w")
        tk.Button(self.btfr, bd=4, bg="alice blue", text="Clear All", command=self.clear_textwidgets).grid(row=5, column=0, sticky="w")
        tk.Button(self.btfr, bd=4, bg="tan", text="Clear Text1 & Text2", command=self.clear_compare_widgets).grid(row=6, column=0, sticky="w")
        tk.Button(self.btfr, bd=4, bg="light pink", text="Clear Output Text", command=self.clear_compared).grid(row=7, column=0, sticky="w")
        tk.Button(self.btfr, bd=4, bg="light yellow", text="Clear Info Only", command=self.clear_info).grid(row=8, column=0, sticky="w")
        tk.Button(self.btfr, bd=4, bg="wheat", text="Save Output", command=self.save_output).grid(row=9, column=0, sticky="w")


        self.infotxt1 =  TextWidgetInfo(self.txtfrm1, self.text1)
        self.infotxt2 =  TextWidgetInfo(self.txtfrm2, self.text2)
        self.outtxtinfo =TextWidgetInfo(self.txtfrm3, self.output_text)

    def clear_compared(self):
        self.output_text.delete("1.0", tk.END)
        
    def clear_info(self):
        self.info_text.configure(state='normal')
        self.info_text.delete("1.0", tk.END)


        
    def clear_textwidgets(self):
        self.text1.delete("1.0", tk.END)
        self.text2.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.info_text.configure(state='normal')
        self.info_text.delete("1.0", tk.END)
       

    def clear_compare_widgets(self):
        # Clear only the text widgets used for comparing files
        self.text1.delete("1.0", tk.END)
        self.text2.delete("1.0", tk.END)

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
        content1 = self.text1.get("1.0", tk.END).splitlines()
        content2 = self.text2.get("1.0", tk.END).splitlines()

        self.text1.delete("1.0", tk.END)
        self.text2.delete("1.0", tk.END)

        diff_count = 0
        matching_lines = 0
        diff_line_numbers = []

        for i, (line1, line2) in enumerate(zip(content1, content2), start=1):
            if line1 != line2:
                diff_count += 1
                diff_line_numbers.append(i)
                self.text1.insert(tk.END, line1 + "\n", "diff")
                self.text2.insert(tk.END, line2 + "\n", "diff")
            else:
                matching_lines += 1
                self.text1.insert(tk.END, line1 + "\n")
                self.text2.insert(tk.END, line2 + "\n")

        # Add remaining lines if lengths differ
        extra_lines1 = content1[len(content2):]
        extra_lines2 = content2[len(content1):]
        for line in extra_lines1:
            self.text1.insert(tk.END, line + "\n", "diff")
            diff_count += 1
        for line in extra_lines2:
            self.text2.insert(tk.END, line + "\n", "diff")
            diff_count += 1

        self.text1.tag_configure("diff", background="wheat1")
        self.text2.tag_configure("diff", background="sky blue")

        # Sequence similarity handles inserted/deleted lines better than positional zip alone.
        similarity_percentage = difflib.SequenceMatcher(None, content1, content2).ratio() * 100

        # Display comparison stats
        self.info_text.configure(state='normal')
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, f"Total Lines in File 1: {len(content1)}\n")
        self.info_text.insert(tk.END, f"Total Lines in File 2: {len(content2)}\n")
        self.info_text.insert(tk.END, f"Number of Differences: {diff_count}\n")
        self.info_text.insert(tk.END, f"Similarity Percentage: {similarity_percentage:.2f}%\n")
        self.info_text.insert(tk.END, "Line Numbers with Differences: \n")
        self.info_text.insert(tk.END, ", ".join(map(str, diff_line_numbers)))
        self.info_text.configure(state='disabled')

    def merge_with_differences(self):
        content1 = self.text1.get("1.0", tk.END).splitlines()
        content2 = self.text2.get("1.0", tk.END).splitlines()

        merged_content = list(dict.fromkeys(content1 + content2))
        merged_text = "\n".join(merged_content)

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, merged_text)

    def merge_with_similarities(self):
        content1 = self.text1.get("1.0", tk.END).splitlines()
        content2 = self.text2.get("1.0", tk.END).splitlines()

        similar_content = [line for line in content1 if line in content2]
        merged_text = "\n".join(similar_content)

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, merged_text)

    def remove_duplicates(self):
        content = self.output_text.get("1.0", tk.END).splitlines()
        unique_content = list(dict.fromkeys(content))
        unique_text = "\n".join(unique_content)

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, unique_text)

    def save_output(self):
        output_file = filedialog.asksaveasfilename(
            title="Save Output",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if output_file:
            with open(output_file, "w") as f:
                content = self.output_text.get("1.0", tk.END)
                f.write(content)



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
        self.sel_ext = None  # Initialize Selected_Extensions instance as None
        self.exts = []
        
        self.drv_label = tk.Label(self.parent, text="Drive Path:")
        self.drv_label.grid(row=0, column=0, padx=10, pady=10)
        self.dlabel = tk.Label(self.parent, text="Set the extention first then browse to see the list of files")
        self.dlabel.grid(row=6, column=1, padx=10, pady=10)
        self.drv_entry = tk.Entry(self.parent, bd=7,width=50)
        self.drv_entry.grid(row=0, column=1, padx=10, pady=10)
        self.drv_entry.bind('<KeyRelease>', lambda event: self.adjust_width(self.drv_entry))
        
        self.filelist = tk.Listbox(self.parent, bd=8, bg="alice blue", height=35, width=30)
        self.filelist.grid(row=0, column=6)
        
        self.drv_browse_button = tk.Button(self.parent,bd=6, text="2nd Browse Start", command=self.browse_drv)
        self.drv_browse_button.grid(row=0, column=2, padx=10, pady=10)
        
        self.ext_label = tk.Label(self.parent, text="File Extension: eg .txt")
        self.ext_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.set_ext_button = tk.Button(self.parent, bd=5,bg="yellow",text="1st Set Selected Extensions", command=self.set_extensions)
        self.set_ext_button.grid(row=3, column=2, padx=10, pady=10)
        
        self.dest_label = tk.Label(self.parent, text="Destination Path:")
        self.dest_label.grid(row=2, column=0, padx=10, pady=10)
        
        self.dest_entry = tk.Entry(self.parent, bd=7, width=50)
        self.dest_entry.grid(row=2,column = 1,padx = 10,pady = 10)
        self.dest_entry.bind('<KeyRelease>', lambda event: self.adjust_width(self.dest_entry))
        
        self.dest_browse_button=tk.Button(self.parent ,bd = 5 ,text ="Browse Destination" ,command=self.browse_dest) 
        self.dest_browse_button.grid(row = 2,column = 2,padx = 10,pady = 10)

        self.dest_browse_button_mkdir=tk.Button(self.parent ,bd = 5 ,bg ="light green" ,text ="Browse with Mkdir" ,command=self.browse_dest2) 
        self.dest_browse_button_mkdir.grid(row = 2,column = 3,padx = 10,pady = 10)

        self.recursive_checkbutton=tk.Checkbutton(self.parent,text ="Recursive Search",variable=self.recursive) 
        self.recursive_checkbutton.grid(row = 3,column = 1)

        self.search_button=tk.Button(self.parent,text ="Search and Copy",command=self.search_and_copy) 
        self.search_button.grid(row = 4,column = 1,padx = 10 ,pady = 10)

    def set_extensions(self):
         top=Toplevel(self.parent) 
         if not hasattr(self,'sel_ext') or not isinstance(self.sel_ext ,Selected_Extensions):
             # Create a new instance of Selected_Extensions if it doesn't exist
             self.sel_ext = Selected_Extensions(top)

    def browse_drv(self):
         drv_path=filedialog.askdirectory() 
         if drv_path:
             file_exts_or_groups=self.sel_ext.get_selected_extensions() if self.sel_ext else [] 
             self.drv_entry.delete(0 ,tk.END) 
             self.drv_entry.insert(0 ,drv_path)
             self.filelist.delete(0, tk.END) 
             for file in os.listdir(drv_path):
                 if not any(file.lower().endswith(ext) for ext in file_exts_or_groups): 
                     continue
                 # Insert the selected filename into the listbox
                 self.filelist.insert(tk.END,file)             

    def browse_dest(self):
         dest_path=filedialog.askdirectory() 
         if dest_path:
             self.dest_entry.delete(0 ,tk.END) 
             self.dest_entry.insert(0 ,dest_path)

    def browse_dest2(self):
         dest_path=filedialog.askdirectory()
         if not dest_path:
             return

         # Get the current epoch time
         epoch_time=str(int(time.time()))

         # Create a new directory name using the epoch time
         new_dir_name="dir4data" + epoch_time

         # Combine the selected directory path with the new directory name
         new_dest_path=os.path.join(dest_path,new_dir_name)

         # Check if the directory exists and if not create it
         if not os.path.exists(new_dest_path):
             os.makedirs(new_dest_path)

         # Clear the entry widget and insert the new destination path
         self.dest_entry.delete(0,'end')
         self.dest_entry.insert(0,new_dest_path)

    def search_and_copy(self):
         drv_path=self.drv_entry.get() 
         dest_path=self.dest_entry.get() 
         is_recursive=self.recursive.get()

         if not drv_path or not dest_path:
             messagebox.showerror("Error","All fields are required")
             return

         if not os.path.exists(drv_path):
             messagebox.showerror("Error","Drive Path does not exist")
             return

         if not os.path.exists(dest_path):
             messagebox.showerror("Error","Destination Path does not exist")
             return

         # Get selected extensions from Selected_Extensions instance
         file_exts_or_groups=self.sel_ext.get_selected_extensions() 

         files_copied=self.recursive_search_and_copy(drv_path,dest_path,file_exts_or_groups) if is_recursive else \
                      self.non_recursive_search_and_copy(drv_path,dest_path,file_exts_or_groups)

         messagebox.showinfo("Success",f"Copied {files_copied} files to {dest_path}")

    def recursive_search_and_copy(self,path,dest,file_exts_or_groups): 
          files_copied = 0
          for parent_dir,_dirs,_files in os.walk(path):
              for file in _files:
                  full_file_path=os.path.join(parent_dir,file) 
                  if any(file.lower().endswith(ext) for ext in file_exts_or_groups) and os.path.isfile(full_file_path):
                      self._copy_unique(full_file_path,dest) 
                      files_copied +=1
          return files_copied

    def non_recursive_search_and_copy(self,path,dest,file_exts_or_groups): 
          files_copied = 0
          for file in os.listdir(path):
              full_file_path=os.path.join(path,file) 
              if any(file.lower().endswith(ext) for ext in file_exts_or_groups) and os.path.isfile(full_file_path):
                  self._copy_unique(full_file_path,dest) 
                  files_copied +=1
          return files_copied


    @staticmethod
    def _copy_unique(source, destination_dir):
        """Copy without silently overwriting a same-named file."""
        base = os.path.basename(source)
        stem, ext = os.path.splitext(base)
        target = os.path.join(destination_dir, base)
        counter = 1
        while os.path.exists(target):
            target = os.path.join(destination_dir, f"{stem}_{counter}{ext}")
            counter += 1
        shutil.copy2(source, target)
        return target
    def adjust_width(self, entry):
          text_length=len(entry.get()) +1 # Adding extra space for padding
          entry.config(width=text_length)



class Multi_Find_Replace:
    """Find/replace text across files, safely by default.

    Normal mode writes modified copies to a timestamped output directory.
    Destructive mode overwrites originals only after explicit confirmation.
    """

    DEFAULT_TEXT_EXTENSIONS = (
        ".txt,.csv,.log,.dat,.py,.ini,.cfg,.conf,.json,.xml,.rtf,.md"
    )

    def __init__(self, parent):
        self.parent = parent
        self.recursive_search = tk.BooleanVar(value=True)
        self.destructive_mode = tk.BooleanVar(value=False)
        self.create_backup = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value="Ready - safe copy mode")
        self.data = []
        self.setup_gui()

    def setup_gui(self):
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(2, weight=1)

        self.control_frame = tk.Frame(self.parent)
        self.control_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nw")

        tk.Button(
            self.control_frame, bd=7, text="Select Directory",
            command=self.select_directory
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.directory_label = tk.Label(
            self.control_frame, text="Select a directory", fg="blue",
            wraplength=420, justify="left"
        )
        self.directory_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        tk.Checkbutton(
            self.control_frame, text="Recursive Search",
            variable=self.recursive_search
        ).grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.setup_find_replace_entries()

        tk.Label(self.control_frame, text="Skip first lines:").grid(
            row=5, column=0, sticky="e", padx=10
        )
        self.skip_lines_spinbox = tk.Spinbox(
            self.control_frame, from_=0, to=100000, width=8
        )
        self.skip_lines_spinbox.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        tk.Label(self.control_frame, text="Text extensions:").grid(
            row=6, column=0, sticky="e", padx=10
        )
        self.extensions_entry = tk.Entry(self.control_frame, width=44)
        self.extensions_entry.grid(row=6, column=1, padx=10, pady=5, sticky="ew")
        self.extensions_entry.insert(0, self.DEFAULT_TEXT_EXTENSIONS)
        tk.Label(
            self.control_frame,
            text="Comma separated. Use * to allow every file type.",
            fg="gray30"
        ).grid(row=7, column=0, columnspan=2, padx=10, sticky="w")

        mode_frame = tk.LabelFrame(self.control_frame, text="Replace Safety Mode", padx=8, pady=6)
        mode_frame.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        tk.Checkbutton(
            mode_frame,
            text="Overwrite original files (DESTRUCTIVE)",
            variable=self.destructive_mode,
            command=self.update_mode_display
        ).grid(row=0, column=0, sticky="w")

        self.backup_check = tk.Checkbutton(
            mode_frame,
            text="Create .bak backup before overwriting",
            variable=self.create_backup
        )
        self.backup_check.grid(row=1, column=0, sticky="w")

        self.mode_label = tk.Label(
            mode_frame,
            text="SAFE: modified copies are written to a new output folder.",
            justify="left", wraplength=400
        )
        self.mode_label.grid(row=2, column=0, sticky="w", pady=(5, 0))

        button_frame = tk.Frame(self.control_frame)
        button_frame.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        tk.Button(
            button_frame, bd=6, text="Find Only",
            command=lambda: self.find_in_files(replace=False)
        ).grid(row=0, column=0, padx=5, sticky="ew")

        tk.Button(
            button_frame, bd=6, bg="light green", text="Replace",
            command=lambda: self.find_in_files(replace=True)
        ).grid(row=0, column=1, padx=5, sticky="ew")

        tk.Button(
            self.control_frame, text="Clear Results", command=self.clear_results
        ).grid(row=10, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.status_label = tk.Label(
            self.control_frame, textvariable=self.status_var,
            anchor="w", justify="left", wraplength=420
        )
        self.status_label.grid(row=11, column=0, columnspan=2, padx=10, pady=8, sticky="ew")

        result_frame = tk.Frame(self.parent)
        result_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        result_frame.grid_rowconfigure(1, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)

        tk.Label(
            result_frame,
            text="Matching files / operation results"
        ).grid(row=0, column=0, sticky="w")

        self.list_box = tk.Listbox(result_frame, bd=5, width=90, height=28)
        self.list_box.grid(row=1, column=0, sticky="nsew")
        scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=self.list_box.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.list_box.configure(yscrollcommand=scrollbar.set)

        self.update_mode_display()

    def setup_find_replace_entries(self):
        tk.Label(self.control_frame, text="Find:").grid(row=3, column=0, sticky="e", padx=10)
        self.find_entry = tk.Entry(self.control_frame, bd=5, width=44)
        self.find_entry.grid(row=3, column=1, padx=10, pady=4, sticky="ew")

        tk.Label(self.control_frame, text="Replace with:").grid(row=4, column=0, sticky="e", padx=10)
        self.replace_entry = tk.Entry(self.control_frame, bd=5, width=44)
        self.replace_entry.grid(row=4, column=1, padx=10, pady=4, sticky="ew")

    def update_mode_display(self):
        if self.destructive_mode.get():
            self.backup_check.config(state="normal")
            self.mode_label.config(
                text="DESTRUCTIVE: originals will be overwritten after a confirmation."
            )
            self.status_var.set("Destructive overwrite mode selected - confirmation required")
        else:
            self.backup_check.config(state="disabled")
            self.mode_label.config(
                text="SAFE: modified copies are written to a new output folder."
            )
            self.status_var.set("Ready - safe copy mode")

    def clear_results(self):
        self.list_box.delete(0, tk.END)
        self.status_var.set("Results cleared")

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_label.config(text=directory)
            self.status_var.set(f"Selected: {directory}")

    def _allowed_extensions(self):
        raw = self.extensions_entry.get().strip()
        if not raw or raw == "*":
            return None

        extensions = []
        for item in raw.split(","):
            ext = item.strip().lower()
            if not ext:
                continue
            if not ext.startswith("."):
                ext = "." + ext
            extensions.append(ext)
        return tuple(extensions) or None

    @staticmethod
    def _read_text_file(path):
        # newline="" keeps the source file's CRLF/LF line endings intact.
        for encoding in ("utf-8", "cp1252", "iso-8859-1"):
            try:
                with open(path, "r", encoding=encoding, newline="") as fh:
                    return fh.readlines(), encoding
            except UnicodeDecodeError:
                continue
            except OSError:
                return None, None
        return None, None

    @staticmethod
    def _atomic_write(path, lines, encoding):
        temp_path = path + ".multitool_tmp"
        try:
            with open(temp_path, "w", encoding=encoding, newline="") as fh:
                fh.writelines(lines)
            os.replace(temp_path, path)
        except Exception:
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except OSError:
                pass
            raise

    def _confirm_destructive_replace(self, find_word, replace_word):
        backup_text = (
            "A .bak backup WILL be created first."
            if self.create_backup.get()
            else "NO backup will be created."
        )
        return messagebox.askyesno(
            "Confirm Destructive Replace",
            "You selected DESTRUCTIVE mode.\n\n"
            "Matching ORIGINAL files will be overwritten.\n"
            f"Find: {find_word!r}\n"
            f"Replace with: {replace_word!r}\n\n"
            f"{backup_text}\n\n"
            "Continue?",
            icon="warning"
        )

    def find_in_files(self, replace=False):
        directory = self.directory_label.cget("text")
        if not directory or directory == "Select a directory" or not os.path.isdir(directory):
            messagebox.showerror("Error", "Please select a valid directory.")
            return

        find_word = self.find_entry.get()
        if not find_word:
            messagebox.showerror("Error", "Please enter text to find.")
            return

        replace_word = self.replace_entry.get() if replace else ""
        try:
            skip_lines = max(0, int(self.skip_lines_spinbox.get()))
        except ValueError:
            messagebox.showerror("Error", "Skip first lines must be a whole number.")
            return

        destructive = bool(replace and self.destructive_mode.get())
        if destructive and not self._confirm_destructive_replace(find_word, replace_word):
            self.status_var.set("Destructive replacement cancelled")
            return

        allowed_extensions = self._allowed_extensions()
        self.list_box.delete(0, tk.END)

        output_directory = None
        if replace and not destructive:
            output_directory = os.path.join(directory, f"replace_{int(time.time())}")
            try:
                os.makedirs(output_directory, exist_ok=False)
            except OSError as exc:
                messagebox.showerror("Output Error", f"Could not create output directory:\n{exc}")
                return

        matches = 0
        changed_files = 0
        skipped_files = 0
        errors = 0
        self.status_var.set("Searching...")
        self.parent.update_idletasks()

        if self.recursive_search.get():
            walker = os.walk(directory)
        else:
            try:
                names = os.listdir(directory)
            except OSError as exc:
                messagebox.showerror("Error", f"Could not read directory:\n{exc}")
                return
            walker = [(directory, [], names)]

        output_abs = os.path.abspath(output_directory) if output_directory else None

        for root, dirs, files in walker:
            # Do not walk into previous/new replacement output directories.
            dirs[:] = [d for d in dirs if not d.startswith("replace_")]
            if output_abs and os.path.abspath(root).startswith(output_abs + os.sep):
                continue

            for filename in files:
                if filename.endswith(".multitool_tmp") or filename.endswith(".bak"):
                    continue
                if allowed_extensions and not filename.lower().endswith(allowed_extensions):
                    continue

                source_path = os.path.join(root, filename)
                if not os.path.isfile(source_path):
                    continue

                lines, encoding = self._read_text_file(source_path)
                if lines is None:
                    skipped_files += 1
                    continue

                searchable = lines[skip_lines:]
                if not any(find_word in line for line in searchable):
                    continue

                matches += 1
                self.list_box.insert(tk.END, source_path)

                if not replace:
                    continue

                new_lines = lines[:skip_lines] + [
                    line.replace(find_word, replace_word) for line in searchable
                ]

                try:
                    if destructive:
                        if self.create_backup.get():
                            backup_path = source_path + ".bak"
                            shutil.copy2(source_path, backup_path)
                        self._atomic_write(source_path, new_lines, encoding)
                        self.list_box.insert(tk.END, "    UPDATED ORIGINAL")
                    else:
                        relative_path = os.path.relpath(source_path, directory)
                        destination_path = os.path.join(output_directory, relative_path)
                        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                        with open(destination_path, "w", encoding=encoding, newline="") as fh:
                            fh.writelines(new_lines)
                        try:
                            shutil.copystat(source_path, destination_path)
                        except OSError:
                            pass
                        self.list_box.insert(tk.END, f"    COPY -> {destination_path}")
                    changed_files += 1
                except OSError as exc:
                    errors += 1
                    self.list_box.insert(tk.END, f"    ERROR: {exc}")

                if matches % 25 == 0:
                    self.status_var.set(f"Searching... {matches} matching file(s) found")
                    self.parent.update_idletasks()

        if not replace:
            summary = f"Found text in {matches} file(s)."
        elif destructive:
            summary = (
                f"Found text in {matches} file(s).\n"
                f"Updated {changed_files} original file(s).\n"
                f"Errors: {errors}. Skipped unreadable files: {skipped_files}."
            )
        else:
            summary = (
                f"Found text in {matches} file(s).\n"
                f"Wrote {changed_files} modified copy/copies to:\n{output_directory}\n\n"
                "The original files were not changed.\n"
                f"Errors: {errors}. Skipped unreadable files: {skipped_files}."
            )

        self.status_var.set(summary.replace("\n", "  "))
        messagebox.showinfo("Find/Replace Complete", summary)


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
                    try:
                        with open(file_path, "r", encoding="utf-8") as input_file:
                            file_content = input_file.read()
                    except UnicodeDecodeError:
                        with open(file_path, "r", encoding="cp1252") as input_file:
                            file_content = input_file.read()
                    self.txtout.insert(tk.END, file_content)
                    output_file.write(file_content)
                    output_file.write("\n")  # add a newline between files
                       
            messagebox.showinfo('Success', f'Files have been merged and saved as {output_filename}')
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {e}')

    def clearall(self):
        self.txtout.delete("1.0", tk.END)
        self.listbox.delete(0, tk.END)


class DataWorkbench:
    """Preview, reorganize, and convert CSV, JSON, and Touchstone S2P data."""

    TOUCHSTONE_COLUMNS = (
        "frequency", "S11_real", "S11_imag", "S21_real", "S21_imag",
        "S12_real", "S12_imag", "S22_real", "S22_imag"
    )

    def __init__(self, parent):
        self.parent = parent
        self.rows = []
        self.columns = []
        self.source_path = ""
        self.source_type = ""
        self.status = tk.StringVar(value="Open a CSV, JSON, or S2P file to begin.")
        self._build_ui()

    def _build_ui(self):
        controls = tk.Frame(self.parent)
        controls.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        tk.Button(controls, text="Open Data File", bd=6, command=self.open_file).grid(
            row=0, column=0, columnspan=2, sticky="ew", pady=3
        )
        self.file_label = tk.Label(controls, text="No file selected", wraplength=330, justify="left")
        self.file_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=3)

        tk.Label(controls, text="Keep columns (comma separated):").grid(row=2, column=0, sticky="w")
        self.columns_entry = tk.Entry(controls, width=48)
        self.columns_entry.grid(row=3, column=0, columnspan=2, sticky="ew", pady=3)
        tk.Label(controls, text="Leave blank to keep every column.", fg="gray30").grid(
            row=4, column=0, columnspan=2, sticky="w"
        )

        tk.Label(controls, text="Sort by column:").grid(row=5, column=0, sticky="w", pady=(8, 0))
        self.sort_column = ttk.Combobox(controls, state="readonly", width=28)
        self.sort_column.grid(row=6, column=0, sticky="ew", pady=3)
        self.remove_duplicates = tk.BooleanVar(value=False)
        tk.Checkbutton(controls, text="Remove duplicate rows", variable=self.remove_duplicates).grid(
            row=6, column=1, sticky="w"
        )
        tk.Button(controls, text="Apply Reorganization", bg="light blue", command=self.reorganize).grid(
            row=7, column=0, columnspan=2, sticky="ew", pady=5
        )
        tk.Button(controls, text="Add RF Mag / dB / Phase Columns", bg="khaki1", command=self.add_rf_columns).grid(
            row=8, column=0, columnspan=2, sticky="ew", pady=5
        )

        tk.Label(controls, text="Save as:").grid(row=9, column=0, sticky="w", pady=(8, 0))
        self.output_format = ttk.Combobox(controls, values=("CSV", "JSON", "S2P"), state="readonly", width=12)
        self.output_format.set("CSV")
        self.output_format.grid(row=9, column=1, sticky="w", pady=(8, 0))
        tk.Button(controls, text="Save / Convert", bg="light green", bd=6, command=self.save_data).grid(
            row=10, column=0, columnspan=2, sticky="ew", pady=5
        )
        tk.Label(controls, textvariable=self.status, wraplength=360, justify="left").grid(
            row=11, column=0, columnspan=2, sticky="w", pady=5
        )

        preview_frame = tk.Frame(self.parent)
        preview_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)
        tk.Label(preview_frame, text="Data preview (first 500 rows)").grid(row=0, column=0, sticky="w")
        self.preview = ttk.Treeview(preview_frame, show="headings", height=28)
        self.preview.grid(row=1, column=0, sticky="nsew")
        yscroll = ttk.Scrollbar(preview_frame, orient="vertical", command=self.preview.yview)
        yscroll.grid(row=1, column=1, sticky="ns")
        xscroll = ttk.Scrollbar(preview_frame, orient="horizontal", command=self.preview.xview)
        xscroll.grid(row=2, column=0, sticky="ew")
        self.preview.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        preview_frame.grid_rowconfigure(1, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)

    @staticmethod
    def _read_text(path):
        for encoding in ("utf-8-sig", "utf-8", "cp1252", "iso-8859-1"):
            try:
                with open(path, "r", encoding=encoding, newline="") as handle:
                    return handle.read()
            except UnicodeDecodeError:
                continue
        raise ValueError("The file could not be decoded as text.")

    @staticmethod
    def _flatten(value, prefix=""):
        if isinstance(value, dict):
            result = {}
            for key, child in value.items():
                child_prefix = f"{prefix}.{key}" if prefix else str(key)
                result.update(DataWorkbench._flatten(child, child_prefix))
            return result
        return {prefix or "value": value}

    def _read_json(self, text):
        value = json.loads(text)
        if isinstance(value, list):
            return [self._flatten(item) if isinstance(item, dict) else {"value": item} for item in value]
        if isinstance(value, dict):
            # A dictionary of records is common in exported data files.
            if value and all(isinstance(item, dict) for item in value.values()):
                return [self._flatten(item) for item in value.values()]
            return [self._flatten(value)]
        return [{"value": value}]

    def _read_csv(self, text):
        try:
            dialect = csv.Sniffer().sniff(text[:4096], delimiters=",;\t|")
        except csv.Error:
            dialect = csv.excel
        return [dict(row) for row in csv.DictReader(text.splitlines(), dialect=dialect)]

    def _read_s2p(self, text):
        unit_scale = {"HZ": 1, "KHZ": 1e3, "MHZ": 1e6, "GHZ": 1e9}
        scale, parameter_format = 1e9, "MA"
        values = []
        for raw_line in text.splitlines():
            line = raw_line.split("!", 1)[0].strip()
            if not line:
                continue
            if line.startswith("#"):
                options = line[1:].upper().split()
                if options and options[0] in unit_scale:
                    scale = unit_scale[options[0]]
                if "RI" in options:
                    parameter_format = "RI"
                elif "DB" in options:
                    parameter_format = "DB"
                elif "MA" in options:
                    parameter_format = "MA"
                continue
            try:
                values.extend(float(item) for item in line.split())
            except ValueError as exc:
                raise ValueError(f"Invalid S2P numeric data: {raw_line}") from exc

        rows = []
        while len(values) >= 9:
            record, values = values[:9], values[9:]
            row = {"frequency": record[0] * scale}
            for name, first, second in zip(("S11", "S21", "S12", "S22"), record[1::2], record[2::2]):
                if parameter_format == "RI":
                    real, imaginary = first, second
                else:
                    magnitude = 10 ** (first / 20) if parameter_format == "DB" else first
                    angle = second * 3.141592653589793 / 180
                    real, imaginary = magnitude * __import__("math").cos(angle), magnitude * __import__("math").sin(angle)
                row[f"{name}_real"] = real
                row[f"{name}_imag"] = imaginary
            rows.append(row)
        if values:
            raise ValueError("S2P data ended with an incomplete frequency record.")
        return rows

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[
            ("Supported data", "*.csv *.json *.s2p"), ("CSV", "*.csv"),
            ("JSON", "*.json"), ("Touchstone S2P", "*.s2p"), ("All files", "*.*")
        ])
        if not path:
            return
        try:
            text = self._read_text(path)
            extension = os.path.splitext(path)[1].lower()
            if extension == ".json":
                rows, source_type = self._read_json(text), "JSON"
            elif extension == ".s2p":
                rows, source_type = self._read_s2p(text), "S2P"
            else:
                rows, source_type = self._read_csv(text), "CSV"
            if not rows:
                raise ValueError("The selected file contains no data rows.")
        except (OSError, ValueError, json.JSONDecodeError, csv.Error) as exc:
            messagebox.showerror("Open Data File", f"Could not parse the file:\n{exc}")
            return
        self.rows, self.source_path, self.source_type = rows, path, source_type
        self.columns = list(dict.fromkeys(key for row in rows for key in row))
        self.columns_entry.delete(0, tk.END)
        self.columns_entry.insert(0, ", ".join(self.columns))
        self.sort_column.configure(values=("", *self.columns))
        self.sort_column.set("")
        self.file_label.config(text=path)
        self.status.set(f"Loaded {len(rows)} row(s) from {source_type}. Fields: {len(self.columns)}.")
        self.refresh_preview()

    def refresh_preview(self):
        self.preview.delete(*self.preview.get_children())
        self.preview["columns"] = self.columns
        for column in self.columns:
            self.preview.heading(column, text=column)
            self.preview.column(column, width=max(100, min(220, len(column) * 12)), stretch=True)
        for row in self.rows[:500]:
            self.preview.insert("", tk.END, values=[str(row.get(column, "")) for column in self.columns])

    def add_rf_columns(self):
        """For S-parameter RI columns, calculate magnitude, dB, and phase."""
        if not self.rows:
            messagebox.showwarning("RF Columns", "Open a data file first.")
            return
        added = []
        for name in ("S11", "S21", "S12", "S22"):
            rk, ik = f"{name}_real", f"{name}_imag"
            if rk not in self.columns or ik not in self.columns:
                continue
            for row in self.rows:
                try:
                    real, imag = float(row[rk]), float(row[ik])
                    mag = math.hypot(real, imag)
                    row[f"{name}_mag"] = mag
                    row[f"{name}_dB"] = 20 * math.log10(mag) if mag > 0 else float("-inf")
                    row[f"{name}_phase_deg"] = math.degrees(math.atan2(imag, real))
                except (TypeError, ValueError):
                    row[f"{name}_mag"] = row[f"{name}_dB"] = row[f"{name}_phase_deg"] = ""
            added.extend((f"{name}_mag", f"{name}_dB", f"{name}_phase_deg"))
        if not added:
            messagebox.showinfo("RF Columns", "No S11/S21/S12/S22 real/imaginary column pairs were found.")
            return
        for col in added:
            if col not in self.columns:self.columns.append(col)
        self.columns_entry.delete(0, tk.END); self.columns_entry.insert(0, ", ".join(self.columns))
        self.sort_column.configure(values=("", *self.columns))
        self.status.set(f"Added {len(added)} RF derived columns.")
        self.refresh_preview()

    def reorganize(self):
        if not self.rows:
            messagebox.showwarning("Reorganize Data", "Open a data file first.")
            return
        requested = [item.strip() for item in self.columns_entry.get().split(",") if item.strip()]
        if requested:
            unknown = [item for item in requested if item not in self.columns]
            if unknown:
                messagebox.showerror("Reorganize Data", f"Unknown column(s): {', '.join(unknown)}")
                return
            self.columns = requested
            self.rows = [{column: row.get(column, "") for column in self.columns} for row in self.rows]
        if self.remove_duplicates.get():
            unique, seen = [], set()
            for row in self.rows:
                key = tuple(str(row.get(column, "")) for column in self.columns)
                if key not in seen:
                    seen.add(key)
                    unique.append(row)
            self.rows = unique
        column = self.sort_column.get()
        if column:
            def sort_key(row):
                value = row.get(column, "")
                try:
                    return (0, float(value))
                except (TypeError, ValueError):
                    return (1, str(value).lower())
            self.rows.sort(key=sort_key)
        self.status.set(f"Reorganized {len(self.rows)} row(s).")
        self.refresh_preview()

    def save_data(self):
        if not self.rows:
            messagebox.showwarning("Save Data", "Open a data file first.")
            return
        output_type = self.output_format.get()
        extension = {"CSV": ".csv", "JSON": ".json", "S2P": ".s2p"}[output_type]
        path = filedialog.asksaveasfilename(defaultextension=extension, filetypes=[(output_type, f"*{extension}")])
        if not path:
            return
        try:
            if output_type == "CSV":
                with open(path, "w", encoding="utf-8", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=self.columns, extrasaction="ignore")
                    writer.writeheader()
                    writer.writerows(self.rows)
            elif output_type == "JSON":
                with open(path, "w", encoding="utf-8") as handle:
                    json.dump(self.rows, handle, indent=2, ensure_ascii=False, default=str)
            else:
                required = set(self.TOUCHSTONE_COLUMNS)
                if not required.issubset(self.columns):
                    missing = ", ".join(column for column in self.TOUCHSTONE_COLUMNS if column not in self.columns)
                    raise ValueError(f"S2P output requires these columns: {missing}")
                with open(path, "w", encoding="utf-8", newline="\n") as handle:
                    handle.write("! Created by Multi Tool Suite Data Workbench\n# Hz S RI R 50\n")
                    for row in self.rows:
                        handle.write(" ".join(str(row[column]) for column in self.TOUCHSTONE_COLUMNS) + "\n")
            self.status.set(f"Saved {len(self.rows)} row(s) as {output_type}: {path}")
            messagebox.showinfo("Save Data", f"Saved {len(self.rows)} row(s) to:\n{path}")
        except (OSError, ValueError, csv.Error) as exc:
            messagebox.showerror("Save Data", f"Could not save the file:\n{exc}")



if __name__ == '__main__':
    root = tk.Tk()
    root.title("Multi Tool Suite 2.0")
    root.geometry("1250x780")
    root.minsize(950, 650)

    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=False)
    filemenu.add_command(label="Exit", command=root.destroy)
    menubar.add_cascade(label="File", menu=filemenu)
    helpmenu = tk.Menu(menubar, tearoff=False)
    helpmenu.add_command(label="About Multi Tool Suite 2.0", command=lambda: messagebox.showinfo(
        "About", "Multi Tool Suite 2.0\nTkinter / Python standard library\nSearch, compare, group, replace, merge and reorganize data."))
    menubar.add_cascade(label="Help", menu=helpmenu)
    root.config(menu=menubar)

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both', padx=4, pady=4)
    tabs = []
    for title in ('PyGrepSim', 'Text Compare', 'Group Files', 'Find / Replace', 'Concatenate Text', 'Data Workbench'):
        frame = tk.Frame(notebook)
        notebook.add(frame, text=title)
        tabs.append(frame)
    PyGrepSim(tabs[0]); TextComparator(tabs[1]); Filegroup(tabs[2]); Multi_Find_Replace(tabs[3]); Concatinate_Text(tabs[4]); DataWorkbench(tabs[5])

    status = tk.StringVar(value="Ready")
    statusbar = tk.Label(root, textvariable=status, anchor="w", relief="sunken", bd=1)
    statusbar.pack(fill="x", side="bottom")
    def tab_changed(event=None):
        status.set(f"Ready — {notebook.tab(notebook.select(), 'text')}")
    notebook.bind('<<NotebookTabChanged>>', tab_changed)
    root.mainloop()
