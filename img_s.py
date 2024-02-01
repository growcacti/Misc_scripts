import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageFilter, ImageEnhance, ImageTk
Image.MAX_IMAGE_PIXELS = None  







class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.loaded_image = None
        self.root.geometry("800x600")
       
        self.original_image = None
        self.canvas = tk.Canvas(self.root)
        self.canvas.grid(row=0, column=0, sticky="nsew")
    
        h_scroll = tk.Scrollbar(self.root, orient='horizontal', command=self.canvas.xview)
        h_scroll.grid(row=13, column=0, sticky='ew')
        v_scroll = tk.Scrollbar(self.root, orient='vertical', command=self.canvas.yview)
        v_scroll.grid(row=0, column=1, sticky='ns')

        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        # Configure grid to expand the canvas
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
        
         
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
       
        self.zoom_slider = ttk.Scale(self.root, from_=1, to_=200, orient="horizontal", command=self.on_zoom)
        self.zoom_slider.set(100)
        self.zoom_slider.grid(row=11, column=0, columnspan=3, sticky='ew')

      
        reset_zoom_button = tk.Button(self.root, text="Reset Zoom", command=self.reset_zoom)
        reset_zoom_button.grid(row=9, column=0, padx=10, pady=10)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
  


    def open_image(self):
        filetypes = [("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.ico")]
        file_path = filedialog.askopenfilename(filetypes=filetypes)
        if file_path:
            self.loaded_image = Image.open(file_path)
            self.original_image = Image.open(file_path) 
            self.display_image(self.loaded_image)

    def save_image(self):
        if self.loaded_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
            if file_path:
                self.loaded_image.save(file_path)

  
    def flip_image(self):
        if self.loaded_image:
            self.loaded_image = self.loaded_image.transpose(Image.FLIP_LEFT_RIGHT)
            self.display_image(self.loaded_image)
    def rotate_image(self):
        if self.loaded_image:
            minvalue = -360
            maxvalue = 360
            degrees = simpledialog.askinteger("Rotate", "Enter degrees to rotate (e.g., 90, 180, -90):", minvalue=minvalue, maxvalue=maxvalue)

            if degrees is not None:
                self.loaded_image = self.loaded_image.rotate(degrees)
                self.display_image(self.loaded_image)

    def blur_image(self):
        if self.loaded_image:
            self.loaded_image = self.loaded_image.filter(ImageFilter.BLUR)
            self.display_image(self.loaded_image)

    def sharpen_image(self):
        if self.loaded_image:
            enhancer = ImageEnhance.Sharpness(self.loaded_image)
            self.loaded_image = enhancer.enhance(2.0)
            self.display_image(self.loaded_image)
    def brighten(self):
        try:
            brightness = float(value)
            enhanced_image = ImageEnhance.Brightness(self.loaded_image).enhance(brightness)
            updated_image = ImageTk.PhotoImage(enhanced_image)
            brightness_scale = tk.Scale(self.root, from_=0.1, to=2.0, resolution=0.1,
                                        orient="horizontal", label="Brightness", command=self.update_brightness)
            brightness_scale.set(1.0)  
            brightness_scale.grid(row=10, column=4)

        except ValueError as e:
            print(e)

    def on_zoom(self, event=None):
        zoom_level = self.zoom_slider.get()
        self.apply_zoom(zoom_level / 100)  

    def update_brightness(self, event=None):
        brightness_value = self.brightness_scale.get()

        if self.loaded_image:  # Check if an image is loaded
            enhancer = ImageEnhance.Brightness(self.loaded_image)
            enhanced_image = enhancer.enhance(brightness_value)
            self.display_image(enhanced_image)
        else:
            print("No image loaded.")
 

    def bind_keyboard_shortcuts(self):
        self.root.bind("<Control-+>", self.zoom_in)  # Zoom in shortcut
        self.root.bind("<Control-->", self.zoom_out) # Zoom out shortcut
        self.root.bind("<Control-0>", self.reset_zoom) # Reset zoom shortcut

    def reset_zoom(self):
        self.apply_zoom(1) 

    def apply_zoom(self, zoom_factor):
        if self.loaded_image is not None:
            # Calculate the new size
            original_size = self.original_image.size
            new_size = (int(original_size[0] * zoom_factor), int(original_size[1] * zoom_factor))

            # Prevent the image from becoming too small
            if new_size[0] < MIN_WIDTH or new_size[1] < MIN_HEIGHT:
                return

            # Resize the image
            self.loaded_image = self.original_image.resize(new_size, Image.Resampling.LANCZOS)

            # Update the image display
            self.display_image(self.loaded_image)

    def on_zoom_slider_change(self, event=None):
        zoom_level = self.zoom_slider.get()
        zoom_factor = zoom_level / 100  # Assuming 100 is the default slider value
        self.apply_zoom(zoom_factor)

    def display_image(self, image):
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.tk_image, anchor='nw')

        # Update the scroll region to encompass the new image
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def update_brightness(self, event=None):
        brightness_value = float(self.brightness_scale.get())
        
        if self.loaded_image is not None:
            enhanced_image = ImageEnhance.Brightness(self.loaded_image).enhance(brightness_value)
            self.display_enhanced_image(enhanced_image)
        else:
            print("No image loaded.")

    def display_enhanced_image(self, image):
        # Update the display with the enhanced image
        tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, image=tk_image, anchor='nw')
        self.canvas.image = tk_image  # Keep a reference to avoid garbage collection
  # Constants for minimum size
MIN_WIDTH = 50  # Minimum width of the image
MIN_HEIGHT = 50  # Minimum height of the image
#Image.Resampling.LANCZOS
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
