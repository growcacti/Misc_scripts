import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageFilter, ImageEnhance, ImageTk

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.loaded_image = None
        self.root.geometry("800x600")
        self.create_gui()
    
    def create_gui(self):
        # Use grid layout
        self.label = tk.Label(self.root)
        self.label.grid(row=0, column=0, columnspan=2)

##        self.rotate_scale = tk.Scale(self.root, from_=-360, to=360, resolution=1, orient="horizontal", label="Rotate Degrees")
##        self.rotate_scale.set(0)
##        self.rotate_scale.grid(row=1, column=0, columnspan=2)
##
     
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Save As", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(menu)
        menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Flip", command=self.flip_image)
        edit_menu.add_command(label="Rotate", command=self.rotate_image)
        edit_menu.add_command(label="Blur", command=self.blur_image)
        edit_menu.add_command(label="Sharpen", command=self.sharpen_image)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.ico")])
        if file_path:
            self.loaded_image = Image.open(file_path)
            self.update_image()

    def save_image(self):
        if self.loaded_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
            if file_path:
                self.loaded_image.save(file_path)

    def update_image(self):
        if self.loaded_image:
            photo = ImageTk.PhotoImage(self.loaded_image)
            self.label.config(image=photo)
            self.label.image = photo

    def flip_image(self):
        if self.loaded_image:
            self.loaded_image = self.loaded_image.transpose(Image.FLIP_LEFT_RIGHT)
            self.update_image()
    def rotate_image(self):
        if self.loaded_image:
            degrees = self.rotate_scale.get()  # Get the value from the scale widget
            self.loaded_image = self.loaded_image.rotate(degrees)
            self.update_image()
    def blur_image(self):
        if self.loaded_image:
            self.loaded_image = self.loaded_image.filter(ImageFilter.BLUR)
            self.update_image()

    def sharpen_image(self):
        if self.loaded_image:
            enhancer = ImageEnhance.Sharpness(self.loaded_image)
            self.loaded_image = enhancer.enhance(2.0)
            self.update_image()


    def brighten(self):
        try:
            brightness = float(value)
            enhanced_image = ImageEnhance.Brightness(original_image).enhance(brightness)
            updated_image = ImageTk.PhotoImage(enhanced_image)
            label.config(image=updated_image)
            label.image = updated_image
            brightness_scale = tk.Scale(root, from_=0.1, to=2.0, resolution=0.1, orient="horizontal", label="Brightness", command=update_brightness)
            brightness_scale.set(1.0)  # Initial brightness value
            brightness_scale.grid(row=10,column=4)

        except ValueError as e:
            print(e)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
