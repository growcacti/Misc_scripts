from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import math

def create_image_grid(image_dir, output_image):
    images = []
    for filename in os.listdir(image_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img = Image.open(os.path.join(image_dir, filename))
            images.append(img)
    
    if not images:
        raise ValueError("No images found in the directory.")
    
    num_images = len(images)
    grid_size = math.ceil(math.sqrt(num_images))
    
    img_width, img_height = images[0].size
    output_width = grid_size * img_width
    output_height = grid_size * img_height

    new_image = Image.new('RGB', (output_width, output_height))

    for index, img in enumerate(images):
        row = index // grid_size
        col = index % grid_size
        x = col * img_width
        y = row * img_height
        new_image.paste(img, (x, y))

    new_image.save(output_image)

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        entry_dir.delete(0, tk.END)
        entry_dir.insert(0, directory)

def generate_grid():
    image_dir = entry_dir.get()
    output_image = entry_output.get()
    try:
        create_image_grid(image_dir, output_image)
        messagebox.showinfo("Success", "Image grid created successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Image Grid Creator")

# Directory selection
tk.Label(root, text="Image Directory:").grid(row=0, column=0, padx=10, pady=5)
entry_dir = tk.Entry(root, width=50,bd=11,bg='wheat')
entry_dir.grid(row=0, column=1, padx=10, pady=5)
btn_browse = tk.Button(root, text="Browse", bd=5,bg='light green',command=select_directory)
btn_browse.grid(row=0, column=2, padx=10, pady=5)

# Output image name
tk.Label(root, text="Output Image:").grid(row=1, column=0, padx=10, pady=5)
entry_output = tk.Entry(root, width=50,bd=11,bg='seashell2')
entry_output.grid(row=1, column=1, padx=10, pady=5)
tk.Label(root, text="make sure to use .png on output").grid(row=9, column=1, padx=10, pady=5)

# Generate button
btn_generate = tk.Button(root, text="Generate Image Grid", command=generate_grid)
btn_generate.grid(row=2, column=0, columnspan=3, pady=20)

# Start the main event loop
root.mainloop()
