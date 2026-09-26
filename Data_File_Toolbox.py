#!/usr/bin/env python3
"""Data File Toolbox

Combined Tkinter utility for JSON, XML, CSV and VCF files.
Uses only the Python standard library.
"""

import csv
import json
import os
import quopri
import tkinter as tk
import xml.etree.ElementTree as ET
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk
from tkinter.scrolledtext import ScrolledText

APP_TITLE = "Data File Toolbox"


def read_text_file(path):
    """Read text while tolerating common encodings."""
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            with open(path, "r", encoding=encoding, newline="") as f:
                return f.read(), encoding
        except UnicodeDecodeError:
            continue
    with open(path, "r", errors="replace") as f:
        return f.read(), "unknown"


def pretty_xml(element):
    """Indent an ElementTree in place (Python 3.9+)."""
    try:
        ET.indent(element, space="  ")
    except AttributeError:
        pass
    return ET.tostring(element, encoding="unicode")


def json_to_xml_value(parent, value, item_tag="item"):
    if isinstance(value, dict):
        for key, child_value in value.items():
            tag = str(key).strip() or "field"
            child = ET.SubElement(parent, tag)
            json_to_xml_value(child, child_value, item_tag)
    elif isinstance(value, list):
        for item in value:
            child = ET.SubElement(parent, item_tag)
            json_to_xml_value(child, item, item_tag)
    elif value is None:
        parent.set("nil", "true")
    elif isinstance(value, bool):
        parent.text = "true" if value else "false"
    else:
        parent.text = str(value)


def xml_element_to_data(element):
    """Convert XML into a readable JSON-compatible structure."""
    children = list(element)
    result = {}
    if element.attrib:
        result["@attributes"] = dict(element.attrib)

    text = (element.text or "").strip()
    if text:
        result["#text"] = text

    if children:
        grouped = {}
        for child in children:
            value = xml_element_to_data(child)
            if child.tag in grouped:
                if not isinstance(grouped[child.tag], list):
                    grouped[child.tag] = [grouped[child.tag]]
                grouped[child.tag].append(value)
            else:
                grouped[child.tag] = value
        result.update(grouped)

    if not result:
        return ""
    if list(result.keys()) == ["#text"]:
        return result["#text"]
    return result


def unfold_vcard_lines(text):
    """Join folded vCard lines (continuation lines begin with space/tab)."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    unfolded = []
    for line in lines:
        if line.startswith((" ", "\t")) and unfolded:
            unfolded[-1] += line[1:]
        else:
            unfolded.append(line)
    return unfolded


def decode_vcard_value(raw, params):
    value = raw
    if "ENCODING=QUOTED-PRINTABLE" in params.upper():
        try:
            value = quopri.decodestring(value).decode("utf-8")
        except (UnicodeDecodeError, ValueError):
            value = quopri.decodestring(value).decode("latin-1", errors="replace")
    return (value.replace("\\n", "\n")
                 .replace("\\,", ",")
                 .replace("\\;", ";")
                 .replace("\\\\", "\\"))


def parse_vcf(text):
    contacts = []
    current = None
    for raw_line in unfold_vcard_lines(text):
        line = raw_line.strip("\n")
        upper = line.upper()
        if upper == "BEGIN:VCARD":
            current = {"Name": "", "Phone": "", "Email": "", "Organization": "", "Address": "", "Notes": ""}
            continue
        if upper == "END:VCARD":
            if current is not None:
                contacts.append(current)
            current = None
            continue
        if current is None or ":" not in line:
            continue

        left, raw_value = line.split(":", 1)
        parts = left.split(";")
        prop = parts[0].upper()
        params = ";".join(parts[1:])
        value = decode_vcard_value(raw_value, params)

        if prop == "FN":
            current["Name"] = value
        elif prop == "N" and not current["Name"]:
            fields = value.split(";")
            family = fields[0] if fields else ""
            given = fields[1] if len(fields) > 1 else ""
            current["Name"] = (given + " " + family).strip()
        elif prop == "TEL":
            current["Phone"] = value if not current["Phone"] else current["Phone"] + "; " + value
        elif prop == "EMAIL":
            current["Email"] = value if not current["Email"] else current["Email"] + "; " + value
        elif prop == "ORG":
            current["Organization"] = value.replace(";", " / ")
        elif prop == "ADR":
            current["Address"] = ", ".join(x for x in value.split(";") if x)
        elif prop == "NOTE":
            current["Notes"] = value
    return contacts


def escape_vcard(value):
    return str(value).replace("\\", "\\\\").replace("\n", "\\n").replace(";", "\\;").replace(",", "\\,")


def contacts_to_vcf(contacts):
    lines = []
    for c in contacts:
        lines.extend([
            "BEGIN:VCARD",
            "VERSION:3.0",
            f"FN:{escape_vcard(c.get('Name', ''))}",
        ])
        for phone in [p.strip() for p in str(c.get("Phone", "")).split(";") if p.strip()]:
            lines.append(f"TEL:{escape_vcard(phone)}")
        for email in [e.strip() for e in str(c.get("Email", "")).split(";") if e.strip()]:
            lines.append(f"EMAIL:{escape_vcard(email)}")
        if c.get("Organization"):
            lines.append(f"ORG:{escape_vcard(c['Organization'])}")
        if c.get("Address"):
            lines.append(f"ADR:;;{escape_vcard(c['Address'])};;;;")
        if c.get("Notes"):
            lines.append(f"NOTE:{escape_vcard(c['Notes'])}")
        lines.append("END:VCARD")
    return "\n".join(lines) + ("\n" if lines else "")


class DataFileToolbox(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1100x760")
        self.minsize(850, 600)

        self.status_var = tk.StringVar(value="Ready")
        self.current_json_path = None
        self.current_xml_path = None
        self.current_csv_path = None
        self.current_vcf_path = None
        self.csv_rows = []
        self.csv_delimiter = ","
        self.contacts = []
        self.selected_contact_index = None

        self._build_menu()
        self._build_ui()

    def _build_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Open Any Supported File…", command=self.open_any)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        tools = tk.Menu(menubar, tearoff=False)
        tools.add_command(label="Validate Current JSON", command=self.validate_json)
        tools.add_command(label="Format Current JSON", command=self.format_json)
        tools.add_command(label="Format Current XML", command=self.format_xml)
        menubar.add_cascade(label="Tools", menu=tools)

        help_menu = tk.Menu(menubar, tearoff=False)
        help_menu.add_command(label="Using This Program", command=lambda: self.notebook.select(self.help_tab))
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=menubar)

    def _build_ui(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=8, pady=(8, 2))

        self.json_tab = ttk.Frame(self.notebook)
        self.xml_tab = ttk.Frame(self.notebook)
        self.csv_tab = ttk.Frame(self.notebook)
        self.vcf_tab = ttk.Frame(self.notebook)
        self.convert_tab = ttk.Frame(self.notebook)
        self.help_tab = ttk.Frame(self.notebook)
        for frame, title in [
            (self.json_tab, "JSON"), (self.xml_tab, "XML"), (self.csv_tab, "CSV"),
            (self.vcf_tab, "VCF Contacts"), (self.convert_tab, "Convert"), (self.help_tab, "Help")]:
            self.notebook.add(frame, text=title)

        self._build_json_tab()
        self._build_xml_tab()
        self._build_csv_tab()
        self._build_vcf_tab()
        self._build_convert_tab()
        self._build_help_tab()

        status = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w")
        status.grid(row=1, column=0, sticky="ew", padx=8, pady=(2, 8))

    def set_status(self, text):
        self.status_var.set(text)

    # ---------------- JSON ----------------
    def _build_json_tab(self):
        self.json_tab.rowconfigure(1, weight=1)
        self.json_tab.columnconfigure(0, weight=1)
        bar = ttk.Frame(self.json_tab)
        bar.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        buttons = [
            ("New", self.new_json), ("Open", self.open_json), ("Save", self.save_json),
            ("Save As", lambda: self.save_json(True)), ("Validate", self.validate_json),
            ("Pretty Format", self.format_json), ("Minify", self.minify_json),
            ("Add Key/Value", self.add_json_pair), ("Clear", lambda: self.json_text.delete("1.0", "end")),
        ]
        for i, (label, cmd) in enumerate(buttons):
            ttk.Button(bar, text=label, command=cmd).grid(row=0, column=i, padx=3)
        self.json_text = ScrolledText(self.json_tab, wrap="none", undo=True, font=("TkFixedFont", 10))
        self.json_text.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))

    def new_json(self):
        self.current_json_path = None
        self.json_text.delete("1.0", "end")
        self.json_text.insert("1.0", "{\n  \n}\n")
        self.set_status("New JSON document")

    def open_json(self, path=None):
        path = path or filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*")])
        if not path:
            return
        try:
            text, enc = read_text_file(path)
            data = json.loads(text)
            self.json_text.delete("1.0", "end")
            self.json_text.insert("1.0", json.dumps(data, indent=2, ensure_ascii=False))
            self.current_json_path = path
            self.notebook.select(self.json_tab)
            self.set_status(f"Loaded JSON: {path} ({enc})")
        except Exception as e:
            messagebox.showerror("JSON Error", str(e))

    def _get_json(self):
        return json.loads(self.json_text.get("1.0", "end-1c"))

    def save_json(self, save_as=False):
        try:
            data = self._get_json()
        except Exception as e:
            messagebox.showerror("Invalid JSON", f"The JSON cannot be saved until it is valid.\n\n{e}")
            return
        path = self.current_json_path
        if save_as or not path:
            path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        self.current_json_path = path
        self.set_status(f"Saved JSON: {path}")

    def validate_json(self):
        try:
            self._get_json()
            messagebox.showinfo("JSON Validation", "The JSON is valid.")
            self.set_status("JSON validation passed")
        except json.JSONDecodeError as e:
            messagebox.showerror("Invalid JSON", f"Line {e.lineno}, column {e.colno}:\n{e.msg}")

    def format_json(self):
        try:
            data = self._get_json()
            self.json_text.delete("1.0", "end")
            self.json_text.insert("1.0", json.dumps(data, indent=2, ensure_ascii=False))
            self.set_status("JSON formatted")
        except Exception as e:
            messagebox.showerror("JSON Error", str(e))

    def minify_json(self):
        try:
            data = self._get_json()
            self.json_text.delete("1.0", "end")
            self.json_text.insert("1.0", json.dumps(data, separators=(",", ":"), ensure_ascii=False))
            self.set_status("JSON minified")
        except Exception as e:
            messagebox.showerror("JSON Error", str(e))

    def add_json_pair(self):
        key = simpledialog.askstring("JSON Key", "Enter a key name:", parent=self)
        if not key:
            return
        value = simpledialog.askstring("JSON Value", "Enter a value:\n(plain text is stored as a string)", parent=self)
        if value is None:
            return
        try:
            data = self._get_json()
            if not isinstance(data, dict):
                raise ValueError("Add Key/Value works when the top level is a JSON object { ... }.")
            try:
                parsed_value = json.loads(value)
            except json.JSONDecodeError:
                parsed_value = value
            data[key] = parsed_value
            self.json_text.delete("1.0", "end")
            self.json_text.insert("1.0", json.dumps(data, indent=2, ensure_ascii=False))
        except Exception as e:
            messagebox.showerror("Cannot Add Pair", str(e))

    # ---------------- XML ----------------
    def _build_xml_tab(self):
        self.xml_tab.rowconfigure(1, weight=1)
        self.xml_tab.columnconfigure(0, weight=1)
        bar = ttk.Frame(self.xml_tab)
        bar.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        for i, (label, cmd) in enumerate([
            ("New", self.new_xml), ("Open", self.open_xml), ("Save", self.save_xml),
            ("Save As", lambda: self.save_xml(True)), ("Validate", self.validate_xml),
            ("Pretty Format", self.format_xml), ("XML Builder", self.xml_builder),
            ("Clear", lambda: self.xml_text.delete("1.0", "end")),
        ]):
            ttk.Button(bar, text=label, command=cmd).grid(row=0, column=i, padx=3)
        self.xml_text = ScrolledText(self.xml_tab, wrap="none", undo=True, font=("TkFixedFont", 10))
        self.xml_text.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))

    def new_xml(self):
        self.current_xml_path = None
        self.xml_text.delete("1.0", "end")
        self.xml_text.insert("1.0", '<?xml version="1.0" encoding="utf-8"?>\n<root>\n</root>\n')
        self.set_status("New XML document")

    def open_xml(self, path=None):
        path = path or filedialog.askopenfilename(filetypes=[("XML files", "*.xml"), ("All files", "*")])
        if not path:
            return
        try:
            text, enc = read_text_file(path)
            root = ET.fromstring(text)
            self.xml_text.delete("1.0", "end")
            self.xml_text.insert("1.0", pretty_xml(root))
            self.current_xml_path = path
            self.notebook.select(self.xml_tab)
            self.set_status(f"Loaded XML: {path} ({enc})")
        except Exception as e:
            messagebox.showerror("XML Error", str(e))

    def _get_xml_root(self):
        return ET.fromstring(self.xml_text.get("1.0", "end-1c"))

    def save_xml(self, save_as=False):
        try:
            root = self._get_xml_root()
        except Exception as e:
            messagebox.showerror("Invalid XML", str(e))
            return
        path = self.current_xml_path
        if save_as or not path:
            path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if not path:
            return
        try:
            ET.indent(root, space="  ")
        except AttributeError:
            pass
        ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
        self.current_xml_path = path
        self.set_status(f"Saved XML: {path}")

    def validate_xml(self):
        try:
            self._get_xml_root()
            messagebox.showinfo("XML Validation", "The XML is well-formed.")
            self.set_status("XML validation passed")
        except ET.ParseError as e:
            messagebox.showerror("Invalid XML", str(e))

    def format_xml(self):
        try:
            root = self._get_xml_root()
            self.xml_text.delete("1.0", "end")
            self.xml_text.insert("1.0", pretty_xml(root))
            self.set_status("XML formatted")
        except Exception as e:
            messagebox.showerror("XML Error", str(e))

    def xml_builder(self):
        dialog = tk.Toplevel(self)
        dialog.title("Simple XML Builder")
        dialog.transient(self)
        dialog.grab_set()
        ttk.Label(dialog, text="Root element:").grid(row=0, column=0, padx=8, pady=8, sticky="e")
        root_var = tk.StringVar(value="root")
        ttk.Entry(dialog, textvariable=root_var, width=25).grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        ttk.Label(dialog, text="Child rows: tag | text | attributes (key=value,key2=value2)").grid(row=1, column=0, columnspan=3, padx=8, sticky="w")
        rows_frame = ttk.Frame(dialog)
        rows_frame.grid(row=2, column=0, columnspan=3, padx=8, pady=8, sticky="nsew")
        rows = []

        def add_row():
            r = len(rows)
            tag = ttk.Entry(rows_frame, width=18)
            text = ttk.Entry(rows_frame, width=28)
            attrs = ttk.Entry(rows_frame, width=35)
            tag.grid(row=r, column=0, padx=2, pady=2)
            text.grid(row=r, column=1, padx=2, pady=2)
            attrs.grid(row=r, column=2, padx=2, pady=2)
            rows.append((tag, text, attrs))

        def build():
            name = root_var.get().strip()
            if not name:
                messagebox.showerror("Builder", "Enter a root element.", parent=dialog)
                return
            try:
                root = ET.Element(name)
                for tag_e, text_e, attr_e in rows:
                    tag = tag_e.get().strip()
                    if not tag:
                        continue
                    child = ET.SubElement(root, tag)
                    child.text = text_e.get()
                    raw_attrs = attr_e.get().strip()
                    if raw_attrs:
                        for pair in raw_attrs.split(","):
                            if "=" not in pair:
                                raise ValueError(f"Attribute must use key=value: {pair}")
                            k, v = pair.split("=", 1)
                            child.set(k.strip(), v.strip())
                self.xml_text.delete("1.0", "end")
                self.xml_text.insert("1.0", pretty_xml(root))
                self.notebook.select(self.xml_tab)
                dialog.destroy()
                self.set_status("XML created with builder")
            except Exception as e:
                messagebox.showerror("Builder Error", str(e), parent=dialog)

        ttk.Button(dialog, text="Add Child Row", command=add_row).grid(row=3, column=0, padx=8, pady=8)
        ttk.Button(dialog, text="Build XML", command=build).grid(row=3, column=1, padx=8, pady=8)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).grid(row=3, column=2, padx=8, pady=8)
        for _ in range(3):
            add_row()

    # ---------------- CSV ----------------
    def _build_csv_tab(self):
        self.csv_tab.rowconfigure(1, weight=1)
        self.csv_tab.columnconfigure(0, weight=1)
        bar = ttk.Frame(self.csv_tab)
        bar.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        for i, (label, cmd) in enumerate([
            ("Open", self.open_csv), ("Save", self.save_csv), ("Save As", lambda: self.save_csv(True)),
            ("Delimiter", self.choose_delimiter), ("Add Row", self.add_csv_row),
            ("Delete Row", self.delete_csv_row), ("Edit Cell", self.edit_csv_cell),
            ("Refresh", self.display_csv),
        ]):
            ttk.Button(bar, text=label, command=cmd).grid(row=0, column=i, padx=3)

        frame = ttk.Frame(self.csv_tab)
        frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        self.csv_tree = ttk.Treeview(frame, show="headings")
        self.csv_tree.grid(row=0, column=0, sticky="nsew")
        y = ttk.Scrollbar(frame, orient="vertical", command=self.csv_tree.yview)
        x = ttk.Scrollbar(frame, orient="horizontal", command=self.csv_tree.xview)
        y.grid(row=0, column=1, sticky="ns")
        x.grid(row=1, column=0, sticky="ew")
        self.csv_tree.configure(yscrollcommand=y.set, xscrollcommand=x.set)
        self.csv_tree.bind("<Double-1>", lambda e: self.edit_csv_cell())

    def open_csv(self, path=None):
        path = path or filedialog.askopenfilename(filetypes=[("CSV/Text tables", "*.csv *.tsv *.txt"), ("All files", "*")])
        if not path:
            return
        try:
            text, enc = read_text_file(path)
            sample = text[:4096]
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
                self.csv_delimiter = dialect.delimiter
            except csv.Error:
                self.csv_delimiter = ","
            self.csv_rows = list(csv.reader(text.splitlines(), delimiter=self.csv_delimiter))
            self.current_csv_path = path
            self.display_csv()
            self.notebook.select(self.csv_tab)
            self.set_status(f"Loaded table: {path} — delimiter {repr(self.csv_delimiter)} ({enc})")
        except Exception as e:
            messagebox.showerror("CSV Error", str(e))

    def display_csv(self):
        tree = self.csv_tree
        tree.delete(*tree.get_children())
        if not self.csv_rows:
            tree["columns"] = ()
            return
        width = max(len(row) for row in self.csv_rows)
        columns = [f"C{i+1}" for i in range(width)]
        tree["columns"] = columns
        header = self.csv_rows[0]
        for i, col in enumerate(columns):
            title = header[i] if i < len(header) and header[i] else col
            tree.heading(col, text=title)
            tree.column(col, width=140, minwidth=60, stretch=True)
        for row_index, row in enumerate(self.csv_rows[1:], start=1):
            values = row + [""] * (width - len(row))
            tree.insert("", "end", iid=str(row_index), values=values)

    def choose_delimiter(self):
        value = simpledialog.askstring("CSV Delimiter", "Enter comma, semicolon, tab, pipe, or a single character:", initialvalue={",":"comma", ";":"semicolon", "\t":"tab", "|":"pipe"}.get(self.csv_delimiter, self.csv_delimiter), parent=self)
        if not value:
            return
        names = {"comma": ",", "semicolon": ";", "tab": "\t", "pipe": "|"}
        self.csv_delimiter = names.get(value.lower(), value[0])
        self.set_status(f"CSV delimiter set to {repr(self.csv_delimiter)}")

    def save_csv(self, save_as=False):
        if not self.csv_rows:
            messagebox.showwarning("CSV", "There is no table loaded.")
            return
        path = self.current_csv_path
        if save_as or not path:
            path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*")])
        if not path:
            return
        with open(path, "w", encoding="utf-8", newline="") as f:
            csv.writer(f, delimiter=self.csv_delimiter).writerows(self.csv_rows)
        self.current_csv_path = path
        self.set_status(f"Saved table: {path}")

    def add_csv_row(self):
        if not self.csv_rows:
            cols = simpledialog.askinteger("New Table", "How many columns?", minvalue=1, initialvalue=3, parent=self)
            if not cols:
                return
            self.csv_rows = [[f"Column {i+1}" for i in range(cols)]]
        width = max(len(r) for r in self.csv_rows)
        self.csv_rows.append([""] * width)
        self.display_csv()

    def delete_csv_row(self):
        sel = self.csv_tree.selection()
        if not sel:
            messagebox.showwarning("CSV", "Select a row first.")
            return
        for iid in sorted((int(x) for x in sel), reverse=True):
            if 0 <= iid < len(self.csv_rows):
                del self.csv_rows[iid]
        self.display_csv()

    def edit_csv_cell(self):
        sel = self.csv_tree.selection()
        if not sel:
            messagebox.showwarning("CSV", "Select a row first.")
            return
        row_index = int(sel[0])
        col = simpledialog.askinteger("Edit Cell", "Column number to edit:", minvalue=1, parent=self)
        if col is None:
            return
        col_index = col - 1
        while len(self.csv_rows[row_index]) <= col_index:
            self.csv_rows[row_index].append("")
        old = self.csv_rows[row_index][col_index]
        new = simpledialog.askstring("Edit Cell", f"Row {row_index+1}, column {col}:\n", initialvalue=old, parent=self)
        if new is not None:
            self.csv_rows[row_index][col_index] = new
            self.display_csv()

    # ---------------- VCF ----------------
    def _build_vcf_tab(self):
        self.vcf_tab.rowconfigure(1, weight=1)
        self.vcf_tab.columnconfigure(0, weight=1)
        bar = ttk.Frame(self.vcf_tab)
        bar.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        for i, (label, cmd) in enumerate([
            ("Open VCF", self.open_vcf), ("Save VCF", self.save_vcf), ("Export CSV", self.export_contacts_csv),
            ("Export JSON", self.export_contacts_json), ("Add Contact", self.add_contact),
            ("Delete Contact", self.delete_contact),
        ]):
            ttk.Button(bar, text=label, command=cmd).grid(row=0, column=i, padx=3)

        pane = ttk.Panedwindow(self.vcf_tab, orient="horizontal")
        pane.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        left = ttk.Frame(pane)
        right = ttk.Frame(pane)
        pane.add(left, weight=1)
        pane.add(right, weight=2)
        left.rowconfigure(0, weight=1); left.columnconfigure(0, weight=1)
        self.contact_list = tk.Listbox(left, exportselection=False)
        self.contact_list.grid(row=0, column=0, sticky="nsew")
        self.contact_list.bind("<<ListboxSelect>>", self.show_contact)

        self.contact_vars = {name: tk.StringVar() for name in ("Name", "Phone", "Email", "Organization", "Address")}
        for r, name in enumerate(("Name", "Phone", "Email", "Organization", "Address")):
            ttk.Label(right, text=name + ":").grid(row=r, column=0, sticky="ne", padx=6, pady=6)
            ttk.Entry(right, textvariable=self.contact_vars[name], width=55).grid(row=r, column=1, sticky="ew", padx=6, pady=6)
        ttk.Label(right, text="Notes:").grid(row=5, column=0, sticky="ne", padx=6, pady=6)
        self.contact_notes = ScrolledText(right, height=8, wrap="word")
        self.contact_notes.grid(row=5, column=1, sticky="nsew", padx=6, pady=6)
        ttk.Button(right, text="Apply Changes to Selected Contact", command=self.apply_contact).grid(row=6, column=1, sticky="e", padx=6, pady=8)
        right.columnconfigure(1, weight=1); right.rowconfigure(5, weight=1)

    def open_vcf(self, path=None):
        path = path or filedialog.askopenfilename(filetypes=[("vCard files", "*.vcf"), ("All files", "*")])
        if not path:
            return
        try:
            text, enc = read_text_file(path)
            self.contacts = parse_vcf(text)
            self.current_vcf_path = path
            self.refresh_contacts()
            self.notebook.select(self.vcf_tab)
            self.set_status(f"Loaded {len(self.contacts)} contacts: {path} ({enc})")
        except Exception as e:
            messagebox.showerror("VCF Error", str(e))

    def refresh_contacts(self):
        self.contact_list.delete(0, "end")
        for i, c in enumerate(self.contacts):
            self.contact_list.insert("end", c.get("Name") or f"Contact {i+1}")

    def show_contact(self, _event=None):
        sel = self.contact_list.curselection()
        if not sel:
            return
        self.selected_contact_index = sel[0]
        c = self.contacts[self.selected_contact_index]
        for name, var in self.contact_vars.items():
            var.set(c.get(name, ""))
        self.contact_notes.delete("1.0", "end")
        self.contact_notes.insert("1.0", c.get("Notes", ""))

    def apply_contact(self):
        if self.selected_contact_index is None or self.selected_contact_index >= len(self.contacts):
            messagebox.showwarning("VCF", "Select a contact first.")
            return
        c = self.contacts[self.selected_contact_index]
        for name, var in self.contact_vars.items():
            c[name] = var.get()
        c["Notes"] = self.contact_notes.get("1.0", "end-1c")
        self.refresh_contacts()
        self.contact_list.selection_set(self.selected_contact_index)
        self.set_status("Contact updated in memory — use Save VCF to write it to disk")

    def add_contact(self):
        self.contacts.append({"Name":"New Contact", "Phone":"", "Email":"", "Organization":"", "Address":"", "Notes":""})
        self.refresh_contacts()
        idx = len(self.contacts) - 1
        self.contact_list.selection_clear(0, "end")
        self.contact_list.selection_set(idx)
        self.contact_list.see(idx)
        self.show_contact()

    def delete_contact(self):
        sel = self.contact_list.curselection()
        if not sel:
            return
        idx = sel[0]
        if messagebox.askyesno("Delete Contact", f"Delete {self.contacts[idx].get('Name','this contact')}?"):
            del self.contacts[idx]
            self.selected_contact_index = None
            self.refresh_contacts()

    def save_vcf(self):
        path = self.current_vcf_path or filedialog.asksaveasfilename(defaultextension=".vcf", filetypes=[("vCard files", "*.vcf")])
        if not path:
            return
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(contacts_to_vcf(self.contacts))
        self.current_vcf_path = path
        self.set_status(f"Saved VCF: {path}")

    def export_contacts_csv(self):
        if not self.contacts:
            messagebox.showwarning("VCF", "No contacts loaded.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not path: return
        fields = ["Name", "Phone", "Email", "Organization", "Address", "Notes"]
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader(); writer.writerows(self.contacts)
        self.set_status(f"Exported contacts to CSV: {path}")

    def export_contacts_json(self):
        if not self.contacts:
            messagebox.showwarning("VCF", "No contacts loaded.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not path: return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.contacts, f, indent=2, ensure_ascii=False)
        self.set_status(f"Exported contacts to JSON: {path}")

    # ---------------- Convert ----------------
    def _build_convert_tab(self):
        self.convert_tab.columnconfigure(0, weight=1)
        intro = ttk.Label(self.convert_tab, text="Conversion tools use the data currently loaded in the matching tab.", font=("TkDefaultFont", 11, "bold"))
        intro.grid(row=0, column=0, sticky="w", padx=12, pady=(14, 8))
        frame = ttk.LabelFrame(self.convert_tab, text="Available conversions")
        frame.grid(row=1, column=0, sticky="new", padx=12, pady=8)
        actions = [
            ("JSON → XML", self.convert_json_to_xml, "Useful for configuration files, data interchange, and systems that require XML."),
            ("JSON → CSV", self.convert_json_to_csv, "Best when the JSON is a list of similar records and you want Excel/LibreOffice rows and columns."),
            ("XML → JSON", self.convert_xml_to_json, "Makes XML easier to inspect or process in Python/web tools."),
            ("CSV → JSON", self.convert_csv_to_json, "Turns a table into records using the first row as field names."),
            ("VCF → CSV", self.export_contacts_csv, "Creates a spreadsheet-friendly contact list."),
            ("VCF → JSON", self.export_contacts_json, "Creates structured contact data for scripts or archiving."),
        ]
        for r, (label, cmd, desc) in enumerate(actions):
            ttk.Button(frame, text=label, command=cmd, width=18).grid(row=r, column=0, padx=8, pady=6, sticky="w")
            ttk.Label(frame, text=desc, wraplength=720, justify="left").grid(row=r, column=1, padx=8, pady=6, sticky="w")

    def convert_json_to_xml(self):
        try:
            data = self._get_json()
            root_name = simpledialog.askstring("Root Element", "XML root element name:", initialvalue="root", parent=self) or "root"
            root = ET.Element(root_name)
            json_to_xml_value(root, data)
            path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
            if not path: return
            try: ET.indent(root, space="  ")
            except AttributeError: pass
            ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
            self.set_status(f"Converted JSON to XML: {path}")
        except Exception as e:
            messagebox.showerror("Conversion Error", str(e))

    def convert_json_to_csv(self):
        try:
            data = self._get_json()
            if isinstance(data, dict):
                # Accept an object whose one value is a list of records.
                lists = [v for v in data.values() if isinstance(v, list) and all(isinstance(x, dict) for x in v)]
                if len(lists) == 1:
                    data = lists[0]
            if not (isinstance(data, list) and data and all(isinstance(x, dict) for x in data)):
                raise ValueError("JSON → CSV needs a list of objects/records, for example [{\"name\": \"Ann\"}, {\"name\": \"Bob\"}].")
            fields = []
            for row in data:
                for key in row:
                    if key not in fields: fields.append(key)
            path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if not path: return
            with open(path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader(); writer.writerows(data)
            self.set_status(f"Converted JSON to CSV: {path}")
        except Exception as e:
            messagebox.showerror("Conversion Error", str(e))

    def convert_xml_to_json(self):
        try:
            root = self._get_xml_root()
            data = {root.tag: xml_element_to_data(root)}
            path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if not path: return
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.set_status(f"Converted XML to JSON: {path}")
        except Exception as e:
            messagebox.showerror("Conversion Error", str(e))

    def convert_csv_to_json(self):
        if len(self.csv_rows) < 1:
            messagebox.showerror("Conversion Error", "Load a CSV file first.")
            return
        headers = self.csv_rows[0]
        records = []
        for row in self.csv_rows[1:]:
            records.append({headers[i] if i < len(headers) and headers[i] else f"column_{i+1}": value for i, value in enumerate(row)})
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not path: return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        self.set_status(f"Converted CSV to JSON: {path}")

    # ---------------- Help ----------------
    def _build_help_tab(self):
        self.help_tab.rowconfigure(0, weight=1)
        self.help_tab.columnconfigure(0, weight=1)
        help_text = ScrolledText(self.help_tab, wrap="word", padx=12, pady=12)
        help_text.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        help_text.insert("1.0", self.help_content())
        help_text.configure(state="disabled")

    def help_content(self):
        return """DATA FILE TOOLBOX — WHAT IT IS FOR

This program puts several small file utilities into one application. It is meant for opening, checking, editing, creating and converting structured data without having to remember several separate programs.

QUICK START
1. Choose the tab for the file type: JSON, XML, CSV, or VCF Contacts.
2. Open a file, make changes, and use Save or Save As.
3. Use the Convert tab when you need the same information in another format.
4. Watch the status bar at the bottom for the last action performed.

JSON TAB
JSON is common in configuration files, APIs, program settings and saved application data.
• Validate — checks whether the punctuation and structure are legal JSON. This is useful when a program reports that a settings file is invalid.
• Pretty Format — adds indentation and line breaks so nested data is easy to read.
• Minify — removes unnecessary spaces. Useful when compact files are desired.
• Add Key/Value — adds a setting to a top-level JSON object. Values such as 12, true, false, null, lists and objects are recognized when entered as valid JSON; ordinary text is stored as a string.

XML TAB
XML is used by older programs, configuration files, data exchange, documents and many industry formats.
• Validate — checks that the XML is well-formed: matching tags, legal nesting, etc.
• Pretty Format — indents the hierarchy so parent/child relationships are easier to see.
• XML Builder — makes a simple XML document without manually typing angle brackets. Enter a root name, then child tag, text and optional attributes such as id=5,type=radio.

CSV TAB
CSV is ideal for rows and columns and is easy to open in Excel or LibreOffice Calc.
• The program tries to detect comma, semicolon, tab or pipe delimiters automatically.
• Delimiter — lets you override the separator manually.
• The first row is treated as the column header.
• Double-click a row, or use Edit Cell, to change a field.
• Add Row / Delete Row are useful for small table corrections without opening a spreadsheet.

VCF CONTACTS TAB
VCF/vCard files are used to transfer contacts between phones, email programs and address books.
• Open VCF — reads common vCard 3.x data without requiring an extra Python package.
• Select a contact to edit name, phone, email, organization, address and notes.
• Apply Changes updates the contact in memory. Use Save VCF to write the changes back to disk.
• Export CSV is useful for reviewing contacts in a spreadsheet.
• Export JSON is useful for programming, backup inspection or additional processing.

CONVERT TAB
JSON → XML: useful when another program requires XML.
JSON → CSV: useful for turning a list of records into spreadsheet rows.
XML → JSON: useful when XML is difficult to inspect or when a Python/web workflow prefers JSON.
CSV → JSON: useful for turning spreadsheet-like records into structured program data.
VCF → CSV/JSON: useful for examining or processing phone/address-book contacts.

SAVE VS. SAVE AS
Save writes back to the currently opened file. Save As asks for a new filename, which is safer when experimenting. For important files, keeping the original and saving a copy is recommended.

VALIDATION VS. CONVERSION
Validation only checks whether the file structure is legal; it does not prove that another specific program will accept every field. Conversion changes representation and can sometimes lose format-specific details. For example, XML attributes and repeated elements do not have an exact one-to-one equivalent in every JSON/CSV structure.

WHY THIS COMBINED VERSION IS MORE USEFUL
• One window instead of many separate scripts.
• Standard-library only: Tkinter, json, csv, ElementTree and quopri.
• Built-in help explains not only the buttons but why each format/tool is useful.
• File validation before saving helps prevent damaged JSON/XML.
• Conversion tools are grouped in one place.
• VCF contacts can be inspected without installing vobject.
• Status messages show what happened and which file was used.

SAFETY TIP
When editing irreplaceable configuration, contact, or data files, use Save As first. Conversion is best treated as creating a new file rather than replacing the source.
"""

    def show_about(self):
        messagebox.showinfo("About", f"{APP_TITLE}\n\nCombined JSON, XML, CSV and VCF editor/converter.\nStandard-library Python/Tkinter application.")

    def open_any(self):
        path = filedialog.askopenfilename(filetypes=[
            ("Supported files", "*.json *.xml *.csv *.tsv *.vcf"),
            ("JSON", "*.json"), ("XML", "*.xml"), ("CSV", "*.csv *.tsv"),
            ("VCF", "*.vcf"), ("All files", "*")])
        if not path:
            return
        ext = Path(path).suffix.lower()
        if ext == ".json": self.open_json(path)
        elif ext == ".xml": self.open_xml(path)
        elif ext in (".csv", ".tsv", ".txt"): self.open_csv(path)
        elif ext == ".vcf": self.open_vcf(path)
        else: messagebox.showwarning("Unsupported", f"I do not know which editor to use for {ext or 'this file'}.")


if __name__ == "__main__":
    app = DataFileToolbox()
    app.mainloop()
