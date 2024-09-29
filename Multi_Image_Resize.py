import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image
import os
import time

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Resizer")
        self.select_button = tk.Button(root, text="Select Folder and Resize Images", command=self.select_folder)
        self.select_button.pack(pady=20)

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            resize_factor = simpledialog.askfloat("Resize Factor", "Enter resize factor (e.g., 0.8 for 80%):", minvalue=0.1, maxvalue=1.0)
            if resize_factor:
                self.resize_images(folder_selected, resize_factor)

    def resize_images(self, input_folder, resize_factor):
        epoch_time = str(int(time.time()))
        output_folder = os.path.join(input_folder, f'resized_output_{epoch_time}')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for file in os.listdir(input_folder):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(input_folder, file)
                try:
                    with Image.open(img_path) as img:
                        # Resizing the image
                        new_size = tuple(int(dim * resize_factor) for dim in img.size)
                        resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                        # Saving the resized image
                        resized_img.save(os.path.join(output_folder, file))
                        print(f"Resized and saved: {file}")
                except Exception as e:
                    print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()
