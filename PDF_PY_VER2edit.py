import fitz
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import PyPDF2
import io
from PyPDF2 import PdfFileMerger
from glob import glob  # Required for pdf_merge()
import io

class PDFApp:
    def __init__(self, root):
        self.root = root
        self.nb = ttk.Notebook(root)
   
       
        self.zoom_level = 1
        self.page = None
        self.image_id = None

        self.f1 = ttk.Frame(self.nb)  # PDF Viewer Frame
        self.f2 = ttk.Frame(self.nb)  # Text Extractor Frame

        self.nb.add(self.f1, text="PDF Viewer")
        self.nb.add(self.f2, text="Text Extractor")

        self.canvas = tk.Canvas(self.f1)
   

        self.txt = tk.Text(self.f2)
      

        self.img_objects = []
        self.current_page = 0
        self.page = self.current_page
        self.load_button = tk.Button(self.f1, text="Load PDF", command=self.open_pdf)
    
        self.prev_button = tk.Button(self.f1, text="Previous", command=self.previous_page)


        self.next_button = tk.Button(self.f1, text="Next", command=self.next_page)


        self.extract_button = tk.Button(root, text="Extract PDF", command=self.load_pdf_into_text_widget)


        self.merge_button = tk.Button(root, text="Merge PDFs", command=self.pdf_merge)
  
        self.f3 = ttk.Frame(self.nb)  # Image Extractor Frame
        self.nb.add(self.f3, text="Image Extractor")
        self.f4 = ttk.Frame(self.nb)  # Image Extractor Frame
   
        self.nb.add(self.f4, text="canvas")

        self.image_canvas = tk.Canvas(self.f3)
     
        self.canvas2 = tk.Canvas(self.f4, bg='white')
  
        self.image_extract_button = tk.Button(self.f3, text="Extract Images", command=self.extract_images_from_pdf)
  
        self.button_zoom_in = tk.Button(self.f1, text="Zoom In", command=self.zoom_in)

        self.button_zoom_out = tk.Button(self.f1, text="Zoom Out", command=self.zoom_out)
 
    # Changes start here
        self.nb.grid(row=0, column=0, sticky="nsew")

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.txt.grid(row=0, column=0, sticky="nsew")

        self.load_button.grid(row=1, column=0)
        self.prev_button.grid(row=2, column=0, sticky="w")
        self.next_button.grid(row=2, column=1, sticky="e")

        self.extract_button.grid(row=1, column=0, pady=10)
        self.merge_button.grid(row=2, column=0, pady=10)

        self.image_canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas2.grid(row=0, column=0, sticky="nsew")
        self.image_extract_button.grid(row=1, column=0, pady=10)

        self.button_zoom_in.grid(row=3, column=0, sticky="w")
        self.button_zoom_out.grid(row=3, column=1, sticky="e")

        # Configure rows and columns weight for resizing
        self.f1.grid_rowconfigure(0, weight=1)
        self.f1.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)


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
        self.current_page = idx
        self.update_image()  # Now this calls the correct update_image method

    def zoom_in(self):
        self.zoom_level += 0.1  # or any other factor you find suitable
        self.update_image()

    def zoom_out(self):
        self.zoom_level -= 0.1  # or any other factor you find suitable
        if self.zoom_level <= 0.1:
            self.zoom_level = 0.1  # Prevent zoom_level from going to 0 or negative
        self.update_image()

    # ... [Other methods remain unchanged]


    def update_image(self):
        page = self.doc.load_page(self.current_page)  # This line gets the correct page object
        zoom_matrix = fitz.Matrix(self.zoom_level, self.zoom_level)
        pix = page.get_pixmap(matrix=zoom_matrix)  # corrected line
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)




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
        return images


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
 

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1800x900")
    app = PDFApp(root)
    root.mainloop()
