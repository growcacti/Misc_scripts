import fitz
import tkinter as tk
from tkinter import ttk, filedialog,END,INSERT
from PIL import Image, ImageTk
import PyPDF2
import io
from PyPDF2 import PdfFileMerger
from glob import glob  # Required for pdf_merge()
import io
import os
class PDFApp:
    def __init__(self, root):
        self.root = root
        self.nb = ttk.Notebook(root)
    
        self.path = os.getcwd()
        self.zoom_level = 1
        self.page = None
        self.image_id = None

        self.f1 = ttk.Frame(self.nb)  # PDF Viewer Frame
         self.nb.add(self.f2, text="Text Extractor")

        self.canvas = tk.Canvas(self.f1)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.txt = tk.Text(self.f2)
        self.txt.pack(fill=tk.BOTH, expand=True)

        self.img_objects = []
        self.current_page = 0
        self.page = self.current_page
        self.load_button = tk.Button(self.f1, text="Load PDF", command=self.open_pdf)
        self.load_button.pack()

        self.prev_button = tk.Button(self.f1, text="Previous", command=self.previous_page)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.f1, text="Next", command=self.next_page)
        self.next_button.pack(side=tk.RIGHT)

        self.extract_button = tk.Button(root, text="Extract PDF", command=self.load_pdf_into_text_widget)
        self.extract_button.pack(pady=10)

        self.merge_button = tk.Button(root, text="Merge PDFs", command=self.pdf_merge)
        self.merge_button.pack(pady=10)
        self.f3 = ttk.Frame(self.nb)  # Image Extractor Frame
        self.nb.add(self.f3, text="Image Extractor")
        self.f4 = ttk.Frame(self.nb)  # Image Extractor Frame
   
        self.nb.add(self.f4, text="canvas")

        self.image_canvas = tk.Canvas(self.f3)
        self.image_canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas2 = tk.Canvas(self.f4, bg='white')
        self.canvas2.pack(fill=tk.BOTH, expand=tk.YES)
        self.image_extract_button = tk.Button(self.f3, text="Extract Images", command=self.extract_images_from_pdf)
        self.image_extract_button.pack(pady=10)
        self.button_zoom_in = tk.Button(self.f1, text="Zoom In", command=self.zoom_in)
        self.button_zoom_in.pack(side=tk.LEFT)
        self.button_zoom_out = tk.Button(self.f1, text="Zoom Out", command=self.zoom_out)
        self.button_zoom_out.pack(side=tk.RIGHT)
        self.f2 = ttk.Frame(self.nb)  # Text Extractor Frame

        self.nb.add(self.f1, text="PDF Viewer")
     

      
      

        self.img_objects = []
        self.current_page = 0
        self.page = self.current_page
        self.load_button = tk.Button(self.f1, text="Load PDF", command=self.open_pdf)


        self.prev_button = tk.Button(self.f1, text="Previous", command=self.previous_page)
 

        self.next_button = tk.Button(self.f1, text="Next", command=self.next_page)
        

        self.extract_button = tk.Button(self.f2, text="Extract PDF", command=self.load_pdf_into_text_widget)


             
        self.f3 = ttk.Frame(self.nb)  # Image Extractor Frame
        self.nb.add(self.f3, text="Image Extractor")
        self.f4 = ttk.Frame(self.nb)  # Image Extractor Frame
   
        self.nb.add(self.f4, text="canvas")

        self.image_canvas = tk.Canvas(self.f3)
        self.merge_button = tk.Button(self.f3, text="Merge PDFs", command=self.pdf_merge)

        self.canvas2 = tk.Canvas(self.f4, bg='white')

        self.image_extract_button = tk.Button(self.f3, text="Extract Images", command=self.extract_images_from_pdf)
   
        self.button_zoom_in = tk.Button(self.f1, text="Zoom In", command=self.zoom_in)
       
        self.button_zoom_out = tk.Button(self.f1, text="Zoom Out", command=self.zoom_out)

        self.dirpath = tk.Entry(self.f1, bd=12, bg="seashell", width=40)
        
        self.lb = tk.Listbox(
            self.f1,
            bg="cyan2",
            bd=12,
            width=35,
            height=55,
            exportselection=False,
            selectmode=tk.SINGLE,
        )
    
        self.lb.focus()
        self.lb.configure(selectmode="")

        self.curtxt = None
        self.x = self.lb.curselection()
        self.flist = os.listdir(self.path)
        self.dirpath.delete(0, END)
        self.dirpath.insert(INSERT, self.path)

        for self.item in self.flist:
            if self.item.endswith(".pdf"):
                self.lb.insert(tk.END, self.item)

                self.lb.focus()
                
        self.lb.bind("<Double-Button-1>", self.listing)
        self.lb.binddef pdf_merge(self):
        merger = PdfFileMerger()
        allpdfs = [a for a in glob("*.pdf")]
        [merger.append(pdf) for pdf in allpdfs]
        with open("Merged_pdfs.pdf", "wb") as new_file:
            merger.write(new_file)
    def extract_images_from_pdf2(file_path):
        doc = fitz.open(file_path)
        images = []
        for page_num in range(doc.page_count):
            page = doc.loself.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_objects[idx])
            ad_page(page_num)
            img_list = page.get_images(full=Tr("<<ListboxSelect>>", self.showcontent)
        self.lb.bind("<<ListboxSelect>>", lambda event: self.showcontent(event))
        
        
        
        
        self.nb.grid(row=0, column=0, sticky='nsew')
        
        self.canvas.grid(row=0, column=2,rowspan=8,columnspan=2, sticky='nsew')
        self.txt.grid(row=0, column=0, sticky='nsew')
        
        self.load_button.grid(row=1, column=0)
        self.prev_button.grid(row=2, column=0, sticky='w')
        self.next_button.grid(row=3, column=0, sticky='e')
        self.extract_button.grid(row=10, column=0)
        self.merge_button.grid(row=11, column=0)
        self.image_extract_button.grid(row=12, column=0)
        self.button_zoom_in.grid(row=6, column=0, sticky='w')
        self.button_zoom_out.grid(row=7, column=0, sticky='e')
        self.dirpath.grid(row=9, column=0, sticky='ew')
        self.lb.grid(row=0, column=1, rowspan=8, sticky='nsew')
        
        self.image_canvas.grid(row=0, column=0, sticky='nsew')
        self.canvas2.grid(row=0, column=0, sticky='nsew')

    def open_pdf(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.filepath:
            self.doc = fitz.open(self.filepath)
            self.img_objects = []
            for page in seldef pdf_merge(self):
        merger = PdfFileMerger()
        allpdfs = [a for a in glob("*.pdf")]
        [merger.append(pdf) for pdf in allpdfs]
        with open("Merged_pdfs.pdf", "wb") as new_file:
            merger.write(new_file)
    def extract_images_from_pdf2(file_path):
        doc = fitz.open(file_path)
        images = []
        for page_num in range(doc.page_count):
            page = doc.loself.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_objects[idx])
            ad_page(page_num)
            img_list = page.get_images(full=Trf.doc:
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img_tk = ImageTk.PhotoImage(image=img)
                self.img_objects.append(img_tk)
            self.display_page(0)

    def listing(self, event=None):
        x = event.widget
        try:
            x = int(self.lb.curselection()[0])
            file = self.lb.get(x)
        except IndexError:
            v = self.lb.get(x)
            v = self.lb.curselection()[0]
            file = self.lb.get(v)






    def showcontent(self, event=None):
        # Get the selected file name from the listbox
        for i in self.lb.curselection():
            file = self.lb.get(i)

        # Open the selected PDF file using fitz
        self.doc = fitz.open(file)
        self.img_objects = []  # Resetting the img_objects list

        for page in self.doc:
            # Create pixmap and image for each page
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_tk = ImageTk.PhotoImage(image=img)

            # Append the PhotoImage object to img_objects list
            self.img_objects.append(img_tk)

        # Display the first page of the newly loaded PDF
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

    def load_pdf_into_text_widget(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            extracted_text = self.extract_pdf_text(file_path)
            self.txt.delete(1.0, tk.END)
            self.txt.insert(tk.END, extracted_text)

    def extract_pdf_text(self, file_path):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)
            text = ''
            for page_num in range(reader.numPages):
                text += reader.getPage(page_num).extractText()
        return text

    def pdf_merge(self):
        merger = PdfFileMerger()
        allpdfs = [a for a in glob("*.pdf")]
        [merger.append(pdf) for pdf in allpdfs]
        with open("Merged_pdfs.pdf", "wb") as new_file:
            merger.write(new_file)
    def extract_images_from_pdf2(file_path):
        doc = fitz.open(file_path)
        images = []
        for page_num in range(doc.page_count):
            page = doc.loself.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_objects[idx])
            ad_page(page_num)
            img_list = page.get_images(full=True)
            for img_index, img in enumerate(img_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                pil_image = Image.open(io.BytesIO(image_bytes))
                images.append(pil_image)
        returself.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_objects[idx])
        self.current_page = idx


    def extract_images_from_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            extract_images_from_pdf2(file_path)    
            return
    def show_page(self, page_number):
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_objects[idx])
        self.current_page = idx
        if self.page:
            self.page = self.current_page
           
        
        self.update_image()

    def update_image(self):
        if not isinstance(self.page, fitz.Page):  # replace `fitz.Page` with the correct type if different
            print(f"Unexpected type: {type(self.page)}")
        image = self.page.get_pixmap(matrix=fitz.Matrix(self.zoom_level, self.zoom_level))
        img = Image.frombytes("RGB", [image.width, image.height], image.samples)
        self.tk_image = ImageTk.PhotoImage(image=img)
        if self.image_id:
            self.canvas.delete(self.image_id)
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_objects[idx])
    def zoom_in(self):
        self.zoom_level += 0.1
        self.update_image()

    def zoom_out(self):
        self.zoom_level -= 0.1
        if self.zoom_level <= 0:
            self.zoom_level = 0.1
    

    def newdirlist(self):
        self.path = askdirectory()
        os.chdir(self.path)
        self.flist = os.listdir(self.path)
        self.lb.delete(0, tk.END)
        self.dirpath.delete(0, END)
        self.dirpath.insert(INSERT, self.path)

        for self.item in self.flist:
            self.lb.insert(tk.END, self.item)
        return self.flist
   
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1800x900")
    app = PDFApp(root)
    root.mainloop()
