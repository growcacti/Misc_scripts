import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import re





class RegexpTab:
    def __init__(self, frm1):
        self.frm1 = frm1
        self.frame = ttk.Frame(self.frm1)
        self.frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(self.frame, text="Match:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.match_entry = tk.Entry(self.frame)
        self.match_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(self.frame, text="Replace:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.replace_entry = tk.Entry(self.frame)
        self.replace_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        self.apply_button = tk.Button(self.frame, text="Apply", command=self.apply_regexp)
        self.apply_button.grid(row=2, column=1, sticky="e", padx=5, pady=5)

        # Configure the frame's column 1 to expand and fill space
        self.frame.columnconfigure(1, weight=1)

    def apply_regexp(self):
        pattern = self.match_entry.get()
        replace_pattern = self.replace_entry.get()
        # Logic to apply the regex to the selected files in the file listbox
        print(f"Applying regex: {pattern} -> {replace_pattern}")

# Other classes like CaseTab, Replace, etc., should also be defined similarly.
class Add_To_String:  
    
    def __init__(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text="Add (7)")
        self.lf.grid(column=4, row=0, rowspan=2, sticky="nsew")

        # Variable defs
        self.prefix = tk.StringVar()
        self.insert_this = tk.StringVar()
        self.at_pos = tk.IntVar()
        self.suffix = tk.StringVar()
        self.word_space = tk.BooleanVar()

        # Prefix, entry
        ttk.Label(self.lf, text="Prefix").grid(column=0, row=0, sticky="ew")
        self.prefix_entry = ttk.Entry(self.lf, width=5, textvariable=self.prefix)
        self.prefix_entry.grid(column=1, row=0, sticky="ew")

        # Insert, entry
        ttk.Label(self.lf, text="Insert").grid(column=0, row=1, sticky="ew")
        self.insert_this_entry = ttk.Entry(
            self.lf, width=5, textvariable=self.insert_this
        )
        self.insert_this_entry.grid(column=1, row=1, sticky="ew")

        # Insert char(s) at position, spinbox
        ttk.Label(self.lf, text="At pos.").grid(column=0, row=2, sticky="ew")
        self.at_pos_spin = ttk.Spinbox(
            self.lf,
            width=3,
            from_=-MAX_NAME_LEN,
            to=MAX_NAME_LEN,
            textvariable=self.at_pos,
        )
        self.at_pos_spin.grid(column=1, row=2)
        self.at_pos.set(0)

        # Suffix, entry
        ttk.Label(self.lf, text="Suffix").grid(column=0, row=3, sticky="ew")
        self.suffix_entry = ttk.Entry(self.lf, width=5, textvariable=self.suffix)
        self.suffix_entry.grid(column=1, row=3, sticky="ew")

        # Word space, checkbutton
        self.word_space_check = ttk.Checkbutton(
            self.lf, text="Word Space", variable=self.word_space
        )
        self.word_space_check.grid(column=0, row=4)

        # Reset, button
        self.reset_button = ttk.Button(
            self.lf, width=2, text="R", command=self.resetWidget
        )
        self.reset_button.grid(column=20, row=20, sticky="w", padx=2, pady=2)

        self.bindEntries()

    def prefixGet(self, *args, **kwargs):
        return self.prefix.get()

    def insertThisGet(self, *args, **kwargs):
        return self.insert_this.get()

    def atPosGet(self, *args, **kwargs):
        return self.at_pos.get()

    def suffixGet(self, *args, **kwargs):
        return self.suffix.get()

    def wordSpaceGet(self, *args, **kwargs):
        return self.word_space.get()

class ReNamerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bulk File Renamer")
        self.directory = tk.StringVar()
        self.prefix = tk.StringVar()
        self.suffix = tk.StringVar()
        self.search_text = tk.StringVar()
        self.replace_text = tk.StringVar()

        self.setup_gui()

    def setup_gui(self):
        # Create the notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Directory selection
        dir_frame = ttk.Frame(self.notebook)
        self.notebook.add(dir_frame, text="Directory & Files")
        tk.Label(dir_frame, text="Directory:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        tk.Entry(dir_frame, textvariable=self.directory, width=50).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(dir_frame, text="Browse", command=self.browse_directory).grid(row=0, column=2, padx=10, pady=10)

        # File list display
        self.file_listbox = tk.Listbox(dir_frame, selectmode=tk.MULTIPLE, width=80, height=15)
        self.file_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Add the basic renaming controls
        self.add_basic_controls(dir_frame)

        # Add tabs for the additional features
        self.add_tabs()

        # Action buttons
        tk.Button(self.root, text="Rename Files", command=self.rename_files).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        tk.Button(self.root, text="Exit", command=self.root.quit).grid(row=1, column=1, padx=10, pady=10, sticky=tk.E)

    def add_basic_controls(self, parent_frame):
        # Prefix and Suffix addition
        tk.Label(parent_frame, text="Prefix:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        tk.Entry(parent_frame, textvariable=self.prefix, width=20).grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        tk.Button(parent_frame, text="Add Prefix", command=self.add_prefix).grid(row=2, column=2, padx=10, pady=5, sticky=tk.W)

        tk.Label(parent_frame, text="Suffix:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        tk.Entry(parent_frame, textvariable=self.suffix, width=20).grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)
        tk.Button(parent_frame, text="Add Suffix", command=self.add_suffix).grid(row=3, column=2, padx=10, pady=5, sticky=tk.W)

        # Search and Replace
        tk.Label(parent_frame, text="Search:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        tk.Entry(parent_frame, textvariable=self.search_text, width=20).grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)
        tk.Label(parent_frame, text="Replace:").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
        tk.Entry(parent_frame, textvariable=self.replace_text, width=20).grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)
        tk.Button(parent_frame, text="Replace", command=self.replace_text_in_files).grid(row=5, column=2, padx=10, pady=5, sticky=tk.W)

    def add_tabs(self):
        # Add other feature tabs here
        self.add_regexp_tab()
        self.add_case_tab()
        self.add_replace_tab()
        self.add_numbering_tab()
        self.add_to_string_tab()
        self.add_shift_chars_tab()
        self.add_remove_tab()
        self.add_extension_replace_tab()
        self.add_name_basic_tab()

    def add_regexp_tab(self):
        frm1 = ttk.Frame(self.notebook)
        self.notebook.add(frm1, text="RegExp")
        RegexpTab(frm1)

    def add_case_tab(self):
        frm2 = ttk.Frame(self.notebook)
        self.notebook.add(frm2, text="Case")
        CaseTab(frm2)

    def add_replace_tab(self):
        frm3 = ttk.Frame(self.notebook)
        self.notebook.add(frm3, text="Replace")
        Replace(frm3)

    def add_numbering_tab(self):
        frm4 = ttk.Frame(self.notebook)
        self.notebook.add(frm4, text="Numbering")
        Numbering(frm4)

    def add_add_to_string_tab(self):
        frm5 = ttk.Frame(self.notebook)
        self.notebook.add(frm5, text="Add To String")
        Add_To_String(frm5)

    def add_shift_chars_tab(self):
        frm6 = ttk.Frame(self.notebook)
        self.notebook.add(frm6, text="Shift Chars")
        Shift_Chars(frm6)

    def add_remove_tab(self):
        frm7 = ttk.Frame(self.notebook)
        self.notebook.add(frm7, text="Remove")
        RemoveTab(frm7)

    def add_extension_replace_tab(self):
        frm8 = ttk.Frame(self.notebook)
        self.notebook.add(frm8, text="Extension Replace")
        ExtensionReplaceTab(frm8)

    def add_name_basic_tab(self):
        frm9 = ttk.Frame(self.notebook)
        self.notebook.add(frm9, text="Name Basic")
        NameBasic(frm9)

    # The following methods are the existing basic functionality.
    def browse_directory(self):
        dir_name = filedialog.askdirectory()
        if dir_name:
            self.directory.set(dir_name)
            self.update_file_list()

    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        directory = self.directory.get()
        for filename in os.listdir(directory):
            self.file_listbox.insert(tk.END, filename)

    def add_prefix(self):
        prefix = self.prefix.get()
        if not prefix:
            messagebox.showerror("Error", "Please enter a prefix.")
            return

        for i in range(self.file_listbox.size()):
            filename = self.file_listbox.get(i)
            new_name = prefix + filename
            self.file_listbox.delete(i)
            self.file_listbox.insert(i, new_name)

    def add_suffix(self):
        suffix = self.suffix.get()
        if not suffix:
            messagebox.showerror("Error", "Please enter a suffix.")
            return

        for i in range(self.file_listbox.size()):
            filename = self.file_listbox.get(i)
            name, ext = os.path.splitext(filename)
            new_name = name + suffix + ext
            self.file_listbox.delete(i)
            self.file_listbox.insert(i, new_name)

    def replace_text_in_files(self):
        search = self.search_text.get()
        replace = self.replace_text.get()
        if not search:
            messagebox.showerror("Error", "Please enter text to search for.")
            return

        for i in range(self.file_listbox.size()):
            filename = self.file_listbox.get(i)
            new_name = filename.replace(search, replace)
            self.file_listbox.delete(i)
            self.file_listbox.insert(i, new_name)

    def rename_files(self):
        directory = self.directory.get()
        if not directory:
            messagebox.showerror("Error", "Please select a directory.")
            return

        for i in range(self.file_listbox.size()):
            old_name = self.file_listbox.get(i)
            new_name = self.file_listbox.get(i)
            old_path = os.path.join(directory, old_name)
            new_path = os.path.join(directory, new_name)
            os.rename(old_path, new_path)

        messagebox.showinfo("Success", "Files renamed successfully!")
        self.update_file_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = ReNamerGUI(root)
    root.mainloop()
