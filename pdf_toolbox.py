#!/usr/bin/env python3
"""PDF Toolbox with optional OCR for scanned or image-only PDF pages."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from io import BytesIO
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    PdfReader = PdfWriter = None

try:
    import fitz  # PyMuPDF renders PDF pages without a separate Poppler install.
    import pytesseract
    from PIL import Image
except ImportError:
    fitz = pytesseract = Image = None

try:
    from reportlab.lib.pagesizes import A4, LETTER, LEGAL
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    from xml.sax.saxutils import escape
except ImportError:
    SimpleDocTemplate = None


APP_TITLE = "JH PDF Toolbox"


def parse_page_spec(spec: str, max_pages: int) -> list[int]:
    """Return zero-based unique indexes from a spec such as ``1,3,5-8``."""
    if not spec.strip():
        raise ValueError("Enter pages such as 1,3,5-8.")
    pages, seen = [], set()
    for part in spec.split(","):
        match = re.fullmatch(r"\s*(\d+)(?:\s*-\s*(\d+))?\s*", part)
        if not match:
            raise ValueError("Invalid page selection: {0}".format(part))
        start, end = int(match.group(1)), int(match.group(2) or match.group(1))
        for number in range(min(start, end), max(start, end) + 1):
            if not 1 <= number <= max_pages:
                raise ValueError("Page {0} is outside 1-{1}.".format(number, max_pages))
            if number not in seen:
                pages.append(number - 1)
                seen.add(number)
    return pages


class PDFToolbox(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1050x760")
        self.minsize(880, 600)
        self.last_output = None
        self.merge_files = []
        self.status_var = tk.StringVar(value="Ready")
        self._build_ui()
        self._warn_missing_dependencies()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        outer = ttk.Frame(self, padding=10)
        outer.grid(sticky="nsew")
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(1, weight=1)
        ttk.Label(outer, text="PDF Toolbox", font=("TkDefaultFont", 16, "bold")).grid(row=0, column=0, sticky="w")
        self.tabs = ttk.Notebook(outer)
        self.tabs.grid(row=1, column=0, sticky="nsew", pady=(8, 0))
        self._build_extract_tab()
        self._build_text_to_pdf_tab()
        self._build_merge_tab()
        self._build_split_tab()
        self._build_page_tools_tab()
        self._build_info_tab()
        bottom = ttk.Frame(outer)
        bottom.grid(row=2, column=0, sticky="ew", pady=(8, 0))
        bottom.columnconfigure(0, weight=1)
        ttk.Label(bottom, textvariable=self.status_var).grid(row=0, column=0, sticky="w")
        ttk.Button(bottom, text="Open Last Output", command=self.open_last_output).grid(row=0, column=1, padx=4)
        ttk.Button(bottom, text="Exit", command=self.destroy).grid(row=0, column=2)

    def _tab(self, name):
        tab = ttk.Frame(self.tabs, padding=12)
        tab.columnconfigure(1, weight=1)
        self.tabs.add(tab, text=name)
        return tab

    @staticmethod
    def _path_row(parent, row, label, variable, command, button="Browse..."):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=(0, 8), pady=5)
        ttk.Entry(parent, textvariable=variable).grid(row=row, column=1, sticky="ew", pady=5)
        ttk.Button(parent, text=button, command=command).grid(row=row, column=2, padx=(8, 0), pady=5)

    def _build_extract_tab(self):
        tab = self._tab("PDF to Text / OCR")
        tab.rowconfigure(7, weight=1)
        self.extract_input = tk.StringVar()
        self.extract_output = tk.StringVar()
        self.use_ocr = tk.BooleanVar(value=True)
        self.ocr_language = tk.StringVar(value="eng")
        self.ocr_dpi = tk.IntVar(value=300)
        self.tesseract_path = tk.StringVar()
        ttk.Label(tab, text="Extract selectable PDF text, with OCR fallback for scanned pages.", font=("TkDefaultFont", 11, "bold")).grid(row=0, column=0, columnspan=3, sticky="w")
        self._path_row(tab, 1, "PDF file:", self.extract_input, self.choose_extract_input)
        self._path_row(tab, 2, "Text output:", self.extract_output, self.choose_extract_output, "Save As...")
        ttk.Checkbutton(tab, text="OCR pages that have no extractable text", variable=self.use_ocr).grid(row=3, column=1, sticky="w", pady=4)
        options = ttk.Frame(tab)
        options.grid(row=4, column=1, sticky="w", pady=4)
        ttk.Label(options, text="Language:").grid(row=0, column=0)
        ttk.Entry(options, textvariable=self.ocr_language, width=10).grid(row=0, column=1, padx=(4, 12))
        ttk.Label(options, text="Render DPI:").grid(row=0, column=2)
        ttk.Spinbox(options, from_=150, to=600, textvariable=self.ocr_dpi, width=6).grid(row=0, column=3, padx=(4, 0))
        self._path_row(tab, 5, "Tesseract executable (optional):", self.tesseract_path, self.choose_tesseract, "Browse...")
        actions = ttk.Frame(tab)
        actions.grid(row=6, column=1, sticky="w", pady=6)
        ttk.Button(actions, text="Preview", command=lambda: self.extract_pdf(preview=True)).grid(row=0, column=0)
        ttk.Button(actions, text="Extract Text", command=lambda: self.extract_pdf(preview=False)).grid(row=0, column=1, padx=6)
        self.extract_preview = ScrolledText(tab, wrap="word")
        self.extract_preview.grid(row=7, column=0, columnspan=3, sticky="nsew", pady=(4, 0))

    def _build_text_to_pdf_tab(self):
        tab = self._tab("Text to PDF")
        self.text_input, self.text_output = tk.StringVar(), tk.StringVar()
        self.text_size, self.text_font = tk.StringVar(value="Letter"), tk.IntVar(value=11)
        self._path_row(tab, 0, "Text file:", self.text_input, self.choose_text_input)
        self._path_row(tab, 1, "PDF output:", self.text_output, self.choose_text_output, "Save As...")
        ttk.Label(tab, text="Page size:").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Combobox(tab, textvariable=self.text_size, values=("Letter", "A4", "Legal"), width=10, state="readonly").grid(row=2, column=1, sticky="w")
        ttk.Label(tab, text="Font size:").grid(row=3, column=0, sticky="w", pady=5)
        ttk.Spinbox(tab, from_=8, to=24, textvariable=self.text_font, width=6).grid(row=3, column=1, sticky="w")
        ttk.Button(tab, text="Create PDF", command=self.text_to_pdf).grid(row=4, column=1, sticky="w", pady=8)

    def _build_merge_tab(self):
        tab = self._tab("Merge PDFs")
        tab.rowconfigure(1, weight=1)
        self.merge_output = tk.StringVar()
        controls = ttk.Frame(tab)
        controls.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 6))
        for text, command in (("Add PDFs...", self.add_merge_files), ("Remove", self.remove_merge_files), ("Move Up", lambda: self.move_merge_file(-1)), ("Move Down", lambda: self.move_merge_file(1))):
            ttk.Button(controls, text=text, command=command).pack(side="left", padx=(0, 5))
        self.merge_list = tk.Listbox(tab, selectmode="extended")
        self.merge_list.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self._path_row(tab, 2, "Output PDF:", self.merge_output, self.choose_merge_output, "Save As...")
        ttk.Button(tab, text="Merge PDFs", command=self.merge_pdfs).grid(row=3, column=1, sticky="w", pady=8)

    def _build_split_tab(self):
        tab = self._tab("Split PDF")
        self.split_input, self.split_folder = tk.StringVar(), tk.StringVar()
        self.split_mode, self.split_value = tk.StringVar(value="Every page"), tk.StringVar(value="1-3,4-6")
        self._path_row(tab, 0, "PDF file:", self.split_input, self.choose_split_input)
        self._path_row(tab, 1, "Output folder:", self.split_folder, self.choose_split_folder, "Choose Folder...")
        ttk.Label(tab, text="Method:").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Combobox(tab, textvariable=self.split_mode, values=("Every page", "Page ranges"), state="readonly").grid(row=2, column=1, sticky="w")
        ttk.Label(tab, text="Ranges (when used):").grid(row=3, column=0, sticky="w", pady=5)
        ttk.Entry(tab, textvariable=self.split_value).grid(row=3, column=1, sticky="ew")
        ttk.Button(tab, text="Split PDF", command=self.split_pdf).grid(row=4, column=1, sticky="w", pady=8)

    def _build_page_tools_tab(self):
        tab = self._tab("Page Tools")
        self.page_input, self.page_output = tk.StringVar(), tk.StringVar()
        self.page_action, self.page_selection, self.rotation = tk.StringVar(value="Extract"), tk.StringVar(value="1"), tk.IntVar(value=90)
        self._path_row(tab, 0, "PDF file:", self.page_input, self.choose_page_input)
        self._path_row(tab, 1, "Output PDF:", self.page_output, self.choose_page_output, "Save As...")
        ttk.Label(tab, text="Action:").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Combobox(tab, textvariable=self.page_action, values=("Extract", "Delete", "Rotate", "Reverse all"), state="readonly").grid(row=2, column=1, sticky="w")
        ttk.Label(tab, text="Pages:").grid(row=3, column=0, sticky="w", pady=5)
        ttk.Entry(tab, textvariable=self.page_selection).grid(row=3, column=1, sticky="ew")
        ttk.Label(tab, text="Rotation:").grid(row=4, column=0, sticky="w", pady=5)
        ttk.Combobox(tab, textvariable=self.rotation, values=(90, 180, 270), width=8, state="readonly").grid(row=4, column=1, sticky="w")
        ttk.Button(tab, text="Apply", command=self.apply_page_tool).grid(row=5, column=1, sticky="w", pady=8)

    def _build_info_tab(self):
        tab = self._tab("PDF Info")
        tab.rowconfigure(2, weight=1)
        self.info_input = tk.StringVar()
        self._path_row(tab, 0, "PDF file:", self.info_input, self.choose_info_input)
        ttk.Button(tab, text="Read Information", command=self.read_info).grid(row=1, column=1, sticky="w", pady=6)
        self.info_text = ScrolledText(tab, wrap="word")
        self.info_text.grid(row=2, column=0, columnspan=3, sticky="nsew")

    def _warn_missing_dependencies(self):
        missing = []
        if PdfReader is None:
            missing.append("pypdf")
        if SimpleDocTemplate is None:
            missing.append("reportlab")
        if fitz is None:
            missing.extend(("pymupdf", "pytesseract", "pillow"))
        if missing:
            self.after(100, lambda: messagebox.showwarning(
                "Optional dependencies missing",
                "Install:\npython -m pip install " + " ".join(missing),
            ))

    def need_pypdf(self):
        if PdfReader is None:
            messagebox.showerror("Missing pypdf", "Install with:\npython -m pip install pypdf")
            return False
        return True

    def configure_ocr(self):
        if fitz is None or pytesseract is None or Image is None:
            raise RuntimeError("OCR needs PyMuPDF, pytesseract, and Pillow. Install:\npython -m pip install pymupdf pytesseract pillow")
        executable = self.tesseract_path.get().strip()
        if executable:
            if not Path(executable).is_file():
                raise RuntimeError("The selected Tesseract executable does not exist.")
            pytesseract.pytesseract.tesseract_cmd = executable
        try:
            pytesseract.get_tesseract_version()
        except Exception as exc:
            raise RuntimeError("Tesseract OCR was not found. Install it or select tesseract.exe.\n\n{0}".format(exc)) from exc

    # File pickers
    def choose_extract_input(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.extract_input.set(path)
            self.extract_output.set(str(Path(path).with_suffix(".txt")))

    def choose_extract_output(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if path: self.extract_output.set(path)

    def choose_tesseract(self):
        path = filedialog.askopenfilename(title="Select tesseract.exe", filetypes=[("Tesseract", "tesseract.exe"), ("All files", "*.*")])
        if path: self.tesseract_path.set(path)

    def choose_text_input(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if path:
            self.text_input.set(path)
            self.text_output.set(str(Path(path).with_suffix(".pdf")))

    def choose_text_output(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if path: self.text_output.set(path)

    def choose_merge_output(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if path: self.merge_output.set(path)

    def choose_split_input(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.split_input.set(path)
            self.split_folder.set(str(Path(path).with_name(Path(path).stem + "_split")))

    def choose_split_folder(self):
        path = filedialog.askdirectory()
        if path: self.split_folder.set(path)

    def choose_page_input(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.page_input.set(path)
            self.page_output.set(str(Path(path).with_name(Path(path).stem + "_edited.pdf")))

    def choose_page_output(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if path: self.page_output.set(path)

    def choose_info_input(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path: self.info_input.set(path)

    # PDF text extraction with optional page-level OCR fallback.
    def extract_pdf(self, preview=False):
        if not self.need_pypdf(): return
        try:
            source = Path(self.extract_input.get())
            if not source.is_file(): raise ValueError("Choose a valid PDF file.")
            if self.use_ocr.get(): self.configure_ocr()
            reader = PdfReader(str(source))
            document = fitz.open(str(source)) if self.use_ocr.get() else None
            chunks, ocr_pages = [], []
            for number, page in enumerate(reader.pages, 1):
                text = (page.extract_text() or "").strip()
                if not text and document is not None:
                    pixmap = document[number - 1].get_pixmap(matrix=fitz.Matrix(self.ocr_dpi.get() / 72, self.ocr_dpi.get() / 72), alpha=False)
                    image = Image.open(BytesIO(pixmap.tobytes("png")))
                    text = pytesseract.image_to_string(image, lang=self.ocr_language.get().strip() or "eng").strip()
                    ocr_pages.append(number)
                chunks.append("===== Page {0} =====\n{text}".format(number, text=text))
            if document: document.close()
            result = "\n\n".join(chunks)
            self.extract_preview.delete("1.0", "end")
            self.extract_preview.insert("1.0", result[:100000])
            detail = " OCR used on page(s): " + ", ".join(map(str, ocr_pages)) if ocr_pages else ""
            if not preview:
                output = Path(self.extract_output.get() or source.with_suffix(".txt"))
                output.write_text(result, encoding="utf-8")
                self.extract_output.set(str(output)); self.last_output = output
                messagebox.showinfo("Complete", "Text saved to:\n{0}{1}".format(output, detail))
            self.status_var.set("Processed {0} page(s).{1}".format(len(reader.pages), detail))
        except Exception as exc:
            messagebox.showerror("PDF to Text / OCR", str(exc))

    def text_to_pdf(self):
        if SimpleDocTemplate is None:
            messagebox.showerror("Missing ReportLab", "Install with:\npython -m pip install reportlab"); return
        try:
            source = Path(self.text_input.get())
            if not source.is_file(): raise ValueError("Choose a valid text file.")
            output = Path(self.text_output.get() or source.with_suffix(".pdf"))
            sizes = {"Letter": LETTER, "A4": A4, "Legal": LEGAL}
            doc = SimpleDocTemplate(str(output), pagesize=sizes[self.text_size.get()], leftMargin=.65*inch, rightMargin=.65*inch, topMargin=.65*inch, bottomMargin=.65*inch)
            style = ParagraphStyle("Text", parent=getSampleStyleSheet()["BodyText"], fontSize=self.text_font.get(), leading=self.text_font.get()*1.3)
            story = [Paragraph(escape(line) or "&nbsp;", style) for line in source.read_text(encoding="utf-8", errors="replace").splitlines()]
            doc.build(story or [Spacer(1, 1)])
            self.last_output = output; self.status_var.set("Created " + output.name)
            messagebox.showinfo("Complete", "PDF saved to:\n" + str(output))
        except Exception as exc: messagebox.showerror("Text to PDF", str(exc))

    def add_merge_files(self):
        for raw in filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")]):
            path = Path(raw)
            if path not in self.merge_files: self.merge_files.append(path); self.merge_list.insert("end", str(path))

    def remove_merge_files(self):
        for index in reversed(self.merge_list.curselection()): del self.merge_files[index]; self.merge_list.delete(index)

    def move_merge_file(self, offset):
        selected = self.merge_list.curselection()
        if len(selected) != 1: return
        old, new = selected[0], selected[0] + offset
        if 0 <= new < len(self.merge_files):
            self.merge_files[old], self.merge_files[new] = self.merge_files[new], self.merge_files[old]
            self.merge_list.delete(0, "end")
            for item in self.merge_files: self.merge_list.insert("end", str(item))
            self.merge_list.selection_set(new)

    def merge_pdfs(self):
        if not self.need_pypdf(): return
        try:
            if len(self.merge_files) < 2: raise ValueError("Add at least two PDF files.")
            output = Path(self.merge_output.get())
            if not output.name: raise ValueError("Choose an output PDF.")
            writer = PdfWriter()
            for path in self.merge_files: writer.append(str(path))
            with output.open("wb") as file: writer.write(file)
            writer.close(); self.last_output = output; self.status_var.set("Created " + output.name)
        except Exception as exc: messagebox.showerror("Merge PDFs", str(exc))

    @staticmethod
    def write_pages(reader, indexes, output):
        writer = PdfWriter()
        for index in indexes: writer.add_page(reader.pages[index])
        with output.open("wb") as file: writer.write(file)
        writer.close()

    def split_pdf(self):
        if not self.need_pypdf(): return
        try:
            source = Path(self.split_input.get())
            if not source.is_file(): raise ValueError("Choose a valid PDF file.")
            output = Path(self.split_folder.get()); output.mkdir(parents=True, exist_ok=True)
            reader, made = PdfReader(str(source)), 0
            groups = ([ [index] for index in range(len(reader.pages)) ] if self.split_mode.get() == "Every page" else [parse_page_spec(item, len(reader.pages)) for item in self.split_value.get().split(",")])
            for number, indexes in enumerate(groups, 1):
                self.write_pages(reader, indexes, output / "{0}_{1:03d}.pdf".format(source.stem, number)); made += 1
            self.last_output = output; self.status_var.set("Created {0} PDF file(s)".format(made))
        except Exception as exc: messagebox.showerror("Split PDF", str(exc))

    def apply_page_tool(self):
        if not self.need_pypdf(): return
        try:
            source = Path(self.page_input.get())
            if not source.is_file(): raise ValueError("Choose a valid PDF file.")
            output = Path(self.page_output.get() or source.with_name(source.stem + "_edited.pdf"))
            reader, writer = PdfReader(str(source)), PdfWriter()
            action = self.page_action.get(); selected = parse_page_spec(self.page_selection.get(), len(reader.pages)) if action != "Reverse all" else []
            if action == "Extract": indexes = selected
            elif action == "Delete": indexes = [i for i in range(len(reader.pages)) if i not in set(selected)]
            elif action == "Reverse all": indexes = list(reversed(range(len(reader.pages))))
            else:
                indexes = list(range(len(reader.pages)))
                for index in selected: reader.pages[index].rotate(self.rotation.get())
            if not indexes: raise ValueError("The operation would create an empty PDF.")
            for index in indexes: writer.add_page(reader.pages[index])
            with output.open("wb") as file: writer.write(file)
            writer.close(); self.last_output = output; self.status_var.set("Created " + output.name)
        except Exception as exc: messagebox.showerror("Page Tools", str(exc))

    def read_info(self):
        if not self.need_pypdf(): return
        try:
            source = Path(self.info_input.get())
            if not source.is_file(): raise ValueError("Choose a valid PDF file.")
            reader = PdfReader(str(source)); metadata = reader.metadata or {}
            lines = ["File: " + str(source), "Pages: " + str(len(reader.pages)), "Encrypted: " + str(reader.is_encrypted), "", "Metadata:"]
            lines.extend("{0}: {1}".format(key, value) for key, value in metadata.items())
            self.info_text.delete("1.0", "end"); self.info_text.insert("1.0", "\n".join(lines))
        except Exception as exc: messagebox.showerror("PDF Info", str(exc))

    def open_last_output(self):
        if not self.last_output or not self.last_output.exists(): messagebox.showinfo("Open Output", "No output has been created yet."); return
        try:
            if sys.platform.startswith("win"): os.startfile(self.last_output)
            elif sys.platform == "darwin": subprocess.Popen(["open", str(self.last_output)])
            else: subprocess.Popen(["xdg-open", str(self.last_output)])
        except OSError as exc: messagebox.showerror("Open Output", str(exc))


if __name__ == "__main__":
    PDFToolbox().mainloop()
