import tkinter as tk
from tkinter import filedialog
from PIL import Image
import pytesseract
Image.MAX_IMAGE_PIXELS = None 
def select_image_and_extract_text():
    # Open a dialog to select an image file
    file_path = filedialog.askopenfilename()
    if file_path:
        # Use Pillow to open the image
        img = Image.open(file_path)

        # Use pytesseract to extract text
        extracted_text = pytesseract.image_to_string(img)

        # Display the extracted text in the text widget
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, extracted_text)

# Create the main window
root = tk.Tk()
root.title("Text Extractor from Image")

# Create a text widget
text_widget = tk.Text(root, height=40, width=300)
text_widget.pack(pady=10)

# Create a button to select an image
select_button = tk.Button(root, text="Select Image", command=select_image_and_extract_text)
select_button.pack(pady=5)
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Adjust the path as per your Tesseract installation
# Run the application
root.mainloop()
