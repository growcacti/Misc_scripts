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
import csv

class PyGrepSim:
    def __init__(self, root):
        self.root = root
        self.var_recursive = tk.BooleanVar()  # Variable for recursive option
        self.setup_gui()
        self.subpath = "/"
        self.path = os.path.join(os.path.expanduser("~"), self.subpath)

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
            # Use recursive search if the checkbutton is selected
            if self.var_recursive.get():
                for root, dirs, files in os.walk(self.path):
                    for filename in files:
                        self.process_file(root, filename, re_pattern, lines_before, lines_after)
            else:
                filenames = os.listdir(self.path)
                for filename in filenames:
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

if __name__ == '__main__':
    root = tk.Tk()
    pysim = PyGrepSim(root)
    root.mainloop()
