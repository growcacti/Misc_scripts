import PyPDF2
import fitz
import os
import tkinter as tk
from tkinter import ttk, filedialog
import tkinter as tk
from PyPDF2 import PdfFileReader
import fitz
from PIL import Image, ImageTk



root=tk.Tk()
nb = ttk.Notebook(root)
class PDFViewer:
    def __init__(self, root):
        self.root = root
        self.nb = ttk.Notebook(root)
        self.nb.pack()
        self.f1 = ttk.Frame(self.nb)
        self.f1.pack()
        self.f2 = tkk.Frame(self.nb)
        self.f2.pack()
        self.f3 = ttk.Frame(self.nb)
        self.f3.pack()
        self.nb.add(self.f1, text="pdf")
        self.nb.add(self.f2, text="text result")
        self.nb.add(self.f3, text="Results")                   
        self.canvas = tk.Canvas(self.f1)
        self.canvas.pack()
        self.txt= tk.Text(self.f2)
        self.txt.pack
        self.lb = tk.Listbox(self.f3)
        self.lb.pack()
        self.current_page = 0
        self.img_objects = []
        self.filepath = os.getcwd()
        self.filename = self.filepath
        self.e1 =tk.Entry(self.f1, bd=5,bg="azure")
        self.e1.pack()
        self.e2 =tk.Entry(self.f1, bd=5,bg="azure")
        self.e2.pack()
        self.e3 =tk.Entry(self.f1, bd=5,bg="azure")
        self.e3.pack()
        self.pdf_button = tk.Button(self.f1, text="Open PDF", command=self.open_pdf)
        self.pdf_button.pack()
        self.pdfbut1 =  tk.Button(self.f1, text="search", command = lambda :self.search_pdf(self.e2.get(), self.e3.get())
        self.pdfbut1.pack()
        self.pdfbut2 =  tk.Button(self.f1, text="search hilite extract", command= lambda : self.highlight_and_extract(self.e1.get(),self.e2.get(),self.e3.get())
        self.pdfbut2.pack()
      
    def open_pdf(self):
        idir = os.getcwd()
        self.filepath = filedialog.askopenfilename(
            initialdir=idir, filetypes=[("PDF files", "*.pdf")]
        )
        e1.insert("end", self.filepath)
        if self.filepath:
            doc = fitz.open(self.filepath)
            pdf = PdfFileReader(self.filepath)
            num_pages = pdf.getNumPages()

            for page_num in range(num_pages):
                page = doc[page_num]
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img_tk = ImageTk.PhotoImage(image=img)
                self.img_objects.append(img_tk)

            self.display_page(0)

            self.prev_button = tk.Button(
                self.self.f1, text="Previous", command=self.previous_page
            )
            prev_button.pack(side=tk.LEFT)

            next_button = tk.Button(self.f1, text="Next", command=self.next_page)
            next_button.pack(side=tk.RIGHT)

            self.canvas.pack(fill=tk.BOTH, expand=True)

    def display_page(self, page_index):
        self.current_page = page_index
        self.canvas.delete("all")
        img_tk = self.img_objects[page_index]
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

    def next_page(self):
        if self.current_page < len(self.img_objects) - 1:
            self.current_page += 1
            self.display_page(self.current_page)

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page(self.current_page)



    def search_pdf(self,file_name, search_term):
        # Open the PDF with PyPDF2 and search
        self.pdf_file = open(file_name, 'rb')
        self.pdf_reader = PyPDF2.PdfFileReader(self.pdf_file)
        self.pages_with_text = []
        
        for page_num in range(self.pdf_reader.numPages):
            page = self.pdf_reader.getPage(page_num)
            text = page.extractText()
            if search_term in text:
                pages_with_text.append(page_num)

        self.pdf_file.close()
        return pages_with_text

    def highlight_and_extract(self,file_name, search_term, pages_with_text):
        # Open the PDF with PyMuPDF
        pdf_document = fitz.open(file_name)
        
        extracted_texts = []

        for page_num in pages_with_text:
            page = pdf_document[page_num]

            # Search the text in the page
            text_instances = page.searchFor(search_term)

            for inst in text_instances:
                # Highlight the text
                highlight = page.addHighlightAnnot(inst)
                extracted_texts.append(inst[4])

            # You can also save the updated PDF with highlighted text if you want
            # pdf_document.save("highlighted.pdf")

        pdf_document.close()
        return extracted_texts

def main():
    pv = PDFViewer(root)
    
    search_term = "desired_text"
    
    pages_with_text = search_pdf(file_name, search_term)
    
    if not pages_with_text:
        print("Search term not found.")
        pv.txt.insert("1.0", "Not Found")
        
        return

    extracted_texts = highlight_and_extract(file_name, search_term, pages_with_text)
    for text in extracted_texts:
        print(text)
        pv.txt.insert("1.0", text)

if __name__ == "__main__":
    
    main()
    root.mainloop()
