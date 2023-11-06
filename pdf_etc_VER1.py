import os
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import fitz
import PyPDF2


class PDFViewer:
    def __init__(self, root):
        self.root = root
        self.nb = ttk.Notebook(root)
        self.nb.pack(fill=tk.BOTH, expand=True)

        self.f1 = ttk.Frame(self.nb)
        self.f2 = ttk.Frame(self.nb)

        self.nb.add(self.f1, text="PDF Viewer")
        self.nb.add(self.f2, text="Extracted Text")

        self.canvas = tk.Canvas(self.f1)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.txt = tk.Text(self.f2)
        self.txt.pack(fill=tk.BOTH, expand=True)

        self.img_objects = []
        self.current_page = 0

        self.load_button = tk.Button(self.f1, text="Load PDF", command=self.open_pdf)
        self.load_button.pack()

        self.prev_button = tk.Button(
            self.f1, text="Previous", command=self.previous_page
        )
        self.prev_button.pack(side=tk.LEFT)

        self.load_button2 = tk.Button(
            root, text="Extract PDF", command=self.load_pdf_into_text_widget
        )
        self.load_button2.pack(pady=10)
        self.next_button = tk.Button(self.f1, text="Next", command=self.next_page)
        self.next_button.pack(side=tk.RIGHT)

    ##        self.search_entry = tk.Entry(self.f1)
    ##        self.search_entry.pack(side=tk.LEFT)
    ##
    ##        self.search_button = tk.Button(self.f1, text="Search & Extract", command=self.search_and_extract)
    ##        self.search_button.pack(side=tk.RIGHT)

    def open_pdf(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.filepath:
            self.doc = fitz.open(self.filepath)
            self.img_objects = []
            for page in self.doc:
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img_tk = ImageTk.PhotoImage(image=img)
                self.img_objects.append(img_tk)
            self.display_page(0)

    def display_page(self, idx):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_objects[idx])
        self.current_page = idx

    def next_page(self):
        if self.current_page < len(self.img_objects) - 1:
            self.display_page(self.current_page + 1)

    def previous_page(self):
        if self.current_page > 0:
            self.display_page(self.current_page - 1)

    def search_and_extract(self):
        search_term = self.search_entry.get()
        if not search_term:
            return

        extracted_texts = []
        for page_num, page in enumerate(self.doc):
            text_instances = page.search_for(search_term)
            for inst in text_instances:
                highlight = page.add_highlight_annot(inst)
                extracted_texts.append(page.get_text("text", clip=inst))

        self.doc.save("highlighted.pdf", garbage=4, deflate=True, clean=True)

        for text in extracted_texts:
            self.txt.insert(tk.END, text + "\n")

        # Refresh the current page to show highlights
        self.display_page(self.current_page)

    def load_pdf_into_text_widget(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            extracted_text = self.extract_text_from_pdf(file_path)
            self.txt.insert(tk.END, extracted_text)

    def extract_text_from_pdf(self, pdf_path):
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page_num in range(reader.numPages):
                text += reader.getPage(page_num).extractText()
        return text


root = tk.Tk()
root.geometry("800x600")
pdf = PDFViewer(root)
root.mainloop()
