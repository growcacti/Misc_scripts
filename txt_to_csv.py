import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path


class TxtCsvConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("TXT to CSV Data Builder")
        self.root.geometry("1050x720")
        self.root.minsize(850, 600)

        self.current_rows = []
        self.current_delimiter = ","

        # -------------------------------------------------
        # Variables
        # -------------------------------------------------

        self.input_file_var = tk.StringVar()
        self.input_folder_var = tk.StringVar()

        self.mode_var = tk.StringVar(value="file")
        self.recursive_var = tk.BooleanVar(value=True)

        self.separator_var = tk.StringVar(value="Auto Detect")

        self.remove_chars_var = tk.StringVar()
        self.find_var = tk.StringVar()
        self.replace_var = tk.StringVar()

        self.trim_var = tk.BooleanVar(value=True)
        self.skip_blank_var = tk.BooleanVar(value=True)

        self.status_var = tk.StringVar(value="Ready")

        # -------------------------------------------------
        # Main layout
        # -------------------------------------------------

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        self.create_input_section()
        self.create_notebook()
        self.create_bottom_section()

    # =====================================================
    # INPUT AREA
    # =====================================================

    def create_input_section(self):

        frame = ttk.LabelFrame(
            self.root,
            text="Input"
        )

        frame.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="ew"
        )

        frame.columnconfigure(1, weight=1)

        ttk.Radiobutton(
            frame,
            text="Single TXT File",
            variable=self.mode_var,
            value="file",
            command=self.update_mode
        ).grid(
            row=0,
            column=0,
            padx=8,
            pady=5,
            sticky="w"
        )

        ttk.Entry(
            frame,
            textvariable=self.input_file_var
        ).grid(
            row=0,
            column=1,
            padx=8,
            pady=5,
            sticky="ew"
        )

        self.file_button = ttk.Button(
            frame,
            text="Browse File",
            command=self.select_file
        )

        self.file_button.grid(
            row=0,
            column=2,
            padx=8,
            pady=5
        )

        ttk.Radiobutton(
            frame,
            text="Folder / Batch",
            variable=self.mode_var,
            value="folder",
            command=self.update_mode
        ).grid(
            row=1,
            column=0,
            padx=8,
            pady=5,
            sticky="w"
        )

        ttk.Entry(
            frame,
            textvariable=self.input_folder_var
        ).grid(
            row=1,
            column=1,
            padx=8,
            pady=5,
            sticky="ew"
        )

        self.folder_button = ttk.Button(
            frame,
            text="Browse Folder",
            command=self.select_folder
        )

        self.folder_button.grid(
            row=1,
            column=2,
            padx=8,
            pady=5
        )

        ttk.Checkbutton(
            frame,
            text="Search subfolders recursively",
            variable=self.recursive_var
        ).grid(
            row=2,
            column=1,
            padx=8,
            pady=5,
            sticky="w"
        )

    # =====================================================
    # NOTEBOOK
    # =====================================================

    def create_notebook(self):

        self.notebook = ttk.Notebook(self.root)

        self.notebook.grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            sticky="nsew"
        )

        self.setup_tab = ttk.Frame(self.notebook)
        self.clean_tab = ttk.Frame(self.notebook)
        self.preview_tab = ttk.Frame(self.notebook)

        self.notebook.add(
            self.setup_tab,
            text="Conversion Setup"
        )

        self.notebook.add(
            self.clean_tab,
            text="Cleaning"
        )

        self.notebook.add(
            self.preview_tab,
            text="Preview"
        )

        self.create_setup_tab()
        self.create_clean_tab()
        self.create_preview_tab()

    # =====================================================
    # SETUP TAB
    # =====================================================

    def create_setup_tab(self):

        tab = self.setup_tab

        tab.columnconfigure(1, weight=1)

        ttk.Label(
            tab,
            text="Column Separator:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=15,
            sticky="w"
        )

        separator_box = ttk.Combobox(
            tab,
            textvariable=self.separator_var,
            state="readonly",
            values=[
                "Auto Detect",
                "Comma",
                "Tab",
                "Semicolon",
                "Pipe"
            ],
            width=20
        )

        separator_box.grid(
            row=0,
            column=1,
            padx=10,
            pady=15,
            sticky="w"
        )

        ttk.Label(
            tab,
            text=(
                "Auto Detect examines the TXT file and attempts "
                "to determine how the columns are separated."
            )
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            padx=10,
            pady=5,
            sticky="w"
        )

        ttk.Separator(
            tab,
            orient="horizontal"
        ).grid(
            row=2,
            column=0,
            columnspan=3,
            padx=10,
            pady=15,
            sticky="ew"
        )

        ttk.Checkbutton(
            tab,
            text="Trim spaces around each value",
            variable=self.trim_var
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            padx=10,
            pady=7,
            sticky="w"
        )

        ttk.Checkbutton(
            tab,
            text="Skip blank lines",
            variable=self.skip_blank_var
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            padx=10,
            pady=7,
            sticky="w"
        )

        ttk.Button(
            tab,
            text="Analyze / Preview File",
            command=self.preview_file
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            padx=10,
            pady=20,
            sticky="w"
        )

    # =====================================================
    # CLEANING TAB
    # =====================================================

    def create_clean_tab(self):

        tab = self.clean_tab
        tab.columnconfigure(1, weight=1)

        ttk.Label(
            tab,
            text="Characters to remove:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        ttk.Entry(
            tab,
            textvariable=self.remove_chars_var
        ).grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="ew"
        )

        ttk.Label(
            tab,
            text='Example: * removes all "*" characters.'
        ).grid(
            row=1,
            column=1,
            padx=10,
            pady=2,
            sticky="w"
        )

        ttk.Separator(
            tab,
            orient="horizontal"
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            padx=10,
            pady=15,
            sticky="ew"
        )

        ttk.Label(
            tab,
            text="Find:"
        ).grid(
            row=3,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        ttk.Entry(
            tab,
            textvariable=self.find_var
        ).grid(
            row=3,
            column=1,
            padx=10,
            pady=10,
            sticky="ew"
        )

        ttk.Label(
            tab,
            text="Replace with:"
        ).grid(
            row=4,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        ttk.Entry(
            tab,
            textvariable=self.replace_var
        ).grid(
            row=4,
            column=1,
            padx=10,
            pady=10,
            sticky="ew"
        )

        ttk.Label(
            tab,
            text=(
                "The Find/Replace operation is performed before "
                "the line is split into spreadsheet columns."
            )
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="w"
        )

    # =====================================================
    # PREVIEW TAB
    # =====================================================

    def create_preview_tab(self):

        tab = self.preview_tab

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(0, weight=1)

        tree_frame = ttk.Frame(tab)

        tree_frame.grid(
            row=0,
            column=0,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        self.preview_tree = ttk.Treeview(
            tree_frame,
            show="headings"
        )

        self.preview_tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        y_scroll = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=self.preview_tree.yview
        )

        y_scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        x_scroll = ttk.Scrollbar(
            tree_frame,
            orient="horizontal",
            command=self.preview_tree.xview
        )

        x_scroll.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        self.preview_tree.configure(
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

    # =====================================================
    # BOTTOM CONTROLS
    # =====================================================

    def create_bottom_section(self):

        frame = ttk.Frame(self.root)

        frame.grid(
            row=2,
            column=0,
            padx=10,
            pady=10,
            sticky="ew"
        )

        frame.columnconfigure(1, weight=1)

        ttk.Button(
            frame,
            text="Convert",
            command=self.convert
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        ttk.Label(
            frame,
            textvariable=self.status_var
        ).grid(
            row=0,
            column=1,
            padx=15,
            sticky="w"
        )

        ttk.Button(
            frame,
            text="Exit",
            command=self.root.destroy
        ).grid(
            row=0,
            column=2,
            padx=5
        )

    # =====================================================
    # FILE/FOLDER SELECTION
    # =====================================================

    def select_file(self):

        filename = filedialog.askopenfilename(
            title="Select TXT File",
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )

        if filename:
            self.input_file_var.set(filename)
            self.mode_var.set("file")
            self.preview_file()

    def select_folder(self):

        folder = filedialog.askdirectory(
            title="Select Folder"
        )

        if folder:
            self.input_folder_var.set(folder)
            self.mode_var.set("folder")

    def update_mode(self):
        pass

    # =====================================================
    # CLEANING
    # =====================================================

    def clean_line(self, line):

        # Remove requested characters
        remove_chars = self.remove_chars_var.get()

        for char in remove_chars:
            line = line.replace(char, "")

        # Find / Replace
        find_text = self.find_var.get()

        if find_text:
            line = line.replace(
                find_text,
                self.replace_var.get()
            )

        return line

    # =====================================================
    # DELIMITER DETECTION
    # =====================================================

    def detect_delimiter(self, text):

        choice = self.separator_var.get()

        manual = {
            "Comma": ",",
            "Tab": "\t",
            "Semicolon": ";",
            "Pipe": "|"
        }

        if choice in manual:
            return manual[choice]

        try:
            dialect = csv.Sniffer().sniff(
                text,
                delimiters=",\t;|"
            )

            return dialect.delimiter

        except csv.Error:

            # Count separators if Sniffer fails
            candidates = {
                ",": text.count(","),
                "\t": text.count("\t"),
                ";": text.count(";"),
                "|": text.count("|")
            }

            best = max(
                candidates,
                key=candidates.get
            )

            if candidates[best] == 0:
                return ","

            return best

    # =====================================================
    # READ TXT FILE
    # =====================================================

    def read_txt_file(self, filename):

        with open(
            filename,
            "r",
            encoding="utf-8",
            errors="replace"
        ) as infile:

            lines = infile.readlines()

        cleaned_lines = []

        for line in lines:

            line = line.rstrip("\r\n")

            if self.skip_blank_var.get():
                if not line.strip():
                    continue

            line = self.clean_line(line)

            cleaned_lines.append(line)

        sample = "\n".join(
            cleaned_lines[:30]
        )

        delimiter = self.detect_delimiter(sample)

        rows = []

        reader = csv.reader(
            cleaned_lines,
            delimiter=delimiter
        )

        for row in reader:

            if self.trim_var.get():
                row = [
                    value.strip()
                    for value in row
                ]

            rows.append(row)

        return rows, delimiter

    # =====================================================
    # PREVIEW
    # =====================================================

    def preview_file(self):

        filename = self.input_file_var.get().strip()

        if not filename:

            if self.mode_var.get() == "folder":

                folder = self.input_folder_var.get().strip()

                if folder:
                    files = self.get_txt_files(folder)

                    if files:
                        filename = str(files[0])

            if not filename:
                messagebox.showwarning(
                    "Preview",
                    "Select a TXT file first."
                )
                return

        try:

            rows, delimiter = self.read_txt_file(
                filename
            )

            self.current_rows = rows
            self.current_delimiter = delimiter

            self.show_preview(rows[:100])

            separator_name = self.delimiter_name(
                delimiter
            )

            self.status_var.set(
                f"Detected separator: {separator_name} | "
                f"{len(rows)} rows"
            )

            self.notebook.select(
                self.preview_tab
            )

        except Exception as error:

            messagebox.showerror(
                "Preview Error",
                str(error)
            )

    # =====================================================
    # SHOW TABLE
    # =====================================================

    def show_preview(self, rows):

        self.preview_tree.delete(
            *self.preview_tree.get_children()
        )

        if not rows:
            return

        max_columns = max(
            len(row)
            for row in rows
        )

        columns = [
            f"Column {number}"
            for number in range(
                1,
                max_columns + 1
            )
        ]

        self.preview_tree["columns"] = columns

        for column in columns:

            self.preview_tree.heading(
                column,
                text=column
            )

            self.preview_tree.column(
                column,
                width=140,
                minwidth=60
            )

        for row in rows:

            padded = row + (
                [""] *
                (max_columns - len(row))
            )

            self.preview_tree.insert(
                "",
                "end",
                values=padded
            )

    # =====================================================
    # CONVERSION
    # =====================================================

    def convert(self):

        if self.mode_var.get() == "file":
            self.convert_single_file()

        else:
            self.convert_folder()

    def convert_single_file(self):

        filename = self.input_file_var.get().strip()

        if not filename:

            messagebox.showwarning(
                "No File",
                "Please select a TXT file."
            )

            return

        input_path = Path(filename)

        output_filename = filedialog.asksaveasfilename(
            title="Save CSV",
            initialfile=input_path.stem + ".csv",
            defaultextension=".csv",
            filetypes=[
                ("CSV Files", "*.csv")
            ]
        )

        if not output_filename:
            return

        try:

            rows, delimiter = self.read_txt_file(
                input_path
            )

            self.write_csv(
                output_filename,
                rows
            )

            self.status_var.set(
                f"Created: {output_filename}"
            )

            messagebox.showinfo(
                "Finished",
                "CSV file created successfully."
            )

        except Exception as error:

            messagebox.showerror(
                "Conversion Error",
                str(error)
            )

    # =====================================================
    # BATCH CONVERSION
    # =====================================================

    def convert_folder(self):

        folder = self.input_folder_var.get().strip()

        if not folder:

            messagebox.showwarning(
                "No Folder",
                "Please select a folder."
            )

            return

        source_folder = Path(folder)

        files = self.get_txt_files(
            source_folder
        )

        if not files:

            messagebox.showinfo(
                "No Files",
                "No TXT files were found."
            )

            return

        output_folder = (
            source_folder /
            "CSV_Output"
        )

        output_folder.mkdir(
            exist_ok=True
        )

        converted = 0
        failed = []

        for txt_file in files:

            try:

                rows, delimiter = self.read_txt_file(
                    txt_file
                )

                if self.recursive_var.get():

                    relative = txt_file.relative_to(
                        source_folder
                    )

                    relative_parent = relative.parent

                    destination_folder = (
                        output_folder /
                        relative_parent
                    )

                    destination_folder.mkdir(
                        parents=True,
                        exist_ok=True
                    )

                else:

                    destination_folder = output_folder

                output_file = (
                    destination_folder /
                    (txt_file.stem + ".csv")
                )

                self.write_csv(
                    output_file,
                    rows
                )

                converted += 1

                self.status_var.set(
                    f"Converting {converted} of "
                    f"{len(files)}"
                )

                self.root.update_idletasks()

            except Exception as error:

                failed.append(
                    f"{txt_file}: {error}"
                )

        message = (
            f"Conversion complete.\n\n"
            f"TXT files found: {len(files)}\n"
            f"Successfully converted: {converted}\n"
            f"Failed: {len(failed)}\n\n"
            f"Output folder:\n{output_folder}"
        )

        messagebox.showinfo(
            "Batch Finished",
            message
        )

        self.status_var.set(
            f"Finished - {converted} files converted"
        )

    # =====================================================
    # FIND TXT FILES
    # =====================================================

    def get_txt_files(self, folder):

        folder = Path(folder)

        if self.recursive_var.get():

            files = list(
                folder.rglob("*.txt")
            )

        else:

            files = list(
                folder.glob("*.txt")
            )

        # Avoid accidentally processing output folders
        files = [
            file
            for file in files
            if "CSV_Output" not in file.parts
        ]

        return sorted(files)

    # =====================================================
    # WRITE CSV
    # =====================================================

    def write_csv(self, filename, rows):

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as outfile:

            writer = csv.writer(
                outfile,
                quoting=csv.QUOTE_MINIMAL
            )

            writer.writerows(rows)

    # =====================================================
    # DISPLAY DELIMITER NAME
    # =====================================================

    def delimiter_name(self, delimiter):

        names = {
            ",": "Comma",
            "\t": "Tab",
            ";": "Semicolon",
            "|": "Pipe"
        }

        return names.get(
            delimiter,
            repr(delimiter)
        )


# =========================================================
# START PROGRAM
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = TxtCsvConverter(root)

    root.mainloop()
