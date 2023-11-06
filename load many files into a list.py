import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class PDFLoader:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window
        self.filepaths = []  # List to hold selected file paths

    def load_files(self):
        while True:
            filepath = filedialog.askopenfilename(title="Select PDF file",
                                                  filetypes=[("PDF files", "*.pdf")])
            if filepath:
                self.filepaths.append(filepath)
                user_response = messagebox.askyesno("Question", "Do you want to add more files?")
                if not user_response:
                    break
            else:
                break  # User cancelled the file dialog

        # Now self.filepaths contains the paths of all selected files

    def process_files(self):
        for filepath in self.filepaths:
            doc = fitz.open(filepath)
            # ... do something with the document ...

pdf_loader = PDFLoader()
pdf_loader.load_files()
pdf_loader.process_files()
