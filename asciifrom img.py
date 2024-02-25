import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont

class ImgToAsciiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to ASCII Art Converter")

        # Button to open image
        tk.Button(self.root, text="Open Image", command=self.open_image).pack()

        # Button to save ASCII art
        tk.Button(self.root, text="Save ASCII Art", command=self.save_ascii).pack()

    def open_image(self):
        filetypes = [("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.ico")]
        self.inputImageFileName = filedialog.askopenfilename(filetypes=filetypes)

    def save_ascii(self):
        self.outputTextFileName = filedialog.asksaveasfilename(defaultextension=".txt")
        if self.inputImageFileName and self.outputTextFileName:
            self.convert_to_ascii()

    def convert_to_ascii(self):
        font = ImageFont.truetype("LiberationMono-Regular.ttf", 12)  # Adjust the path and font size

        # Get the size of a single character using getbbox
        bbox = font.getbbox('A')  # Using 'A' as an example character
        chrx = bbox[2] - bbox[0]  # Width of the character
        chry = bbox[3] - bbox[1]  # Height of the character

        weights = self.calculate_weights(font, chrx, chry)

        image = Image.open(self.inputImageFileName)
        imgx, imgy = image.size
        imgx, imgy = int(imgx / chrx), int(imgy / chry)
        image = image.resize((imgx, imgy), Image.BICUBIC)
        image = image.convert("L")
        pixels = image.load()

        with open(self.outputTextFileName, "w") as output:
            for y in range(imgy):
                for x in range(imgx):
                    w = float(pixels[x, y]) / 255
                    wf, k = -1.0, -1
                    for i, weight in enumerate(weights):
                        if abs(weight - w) <= abs(wf - w):
                            wf, k = weight, i
                    output.write(chr(k + 32))
                output.write("\n")



    def calculate_weights(self, font):
        weights = []
        for i in range(32, 127):
            chrImage = font.getmask(chr(i))
            bbox = chrImage.getbbox()  # (left, top, right, bottom)
        if bbox:  # Check if bbox is not None
             chrx = bbox[2] - bbox[0]  # Width of the character
             chry = bbox[3] - bbox[1]  # Height of the character
             ctr = sum(chrImage.getpixel((x, y)) > 0 for y in range(chry) for x in range(chrx))
             weights.append(float(ctr) / (chrx * chry))
        else:
            weights.append(0)  # In case bbox is None, append a default weight
            return weights


if __name__ == "__main__":
    root = tk.Tk()
    app = ImgToAsciiApp(root)
    root.mainloop()
