import tkinter as tk
from tkinter import filedialog, messagebox
import json
from PIL import Image, ImageDraw

def load_tileset(tileset_image, tile_width, tile_height):
    tileset = Image.open(tileset_image)
    tiles = []
    for y in range(0, tileset.height, tile_height):
        for x in range(0, tileset.width, tile_width):
            tile = tileset.crop((x, y, x + tile_width, y + tile_height))
            tiles.append(tile)
    return tiles

def render_map(map_file, tileset_image, output_image):
    with open(map_file, 'r') as f:
        map_data = json.load(f)
    
    tileset = load_tileset(tileset_image, map_data['tilewidth'], map_data['tileheight'])
    
    map_width = map_data['width'] * map_data['tilewidth']
    map_height = map_data['height'] * map_data['tileheight']
    output_img = Image.new('RGBA', (map_width, map_height))
    
    for layer in map_data['layers']:
        if layer['type'] == 'tilelayer':
            for y in range(layer['height']):
                for x in range(layer['width']):
                    tile_index = layer['data'][y * layer['width'] + x] - 1
                    if tile_index >= 0:
                        tile = tileset[tile_index]
                        output_img.paste(tile, (x * map_data['tilewidth'], y * map_data['tileheight']))
    
    output_img.save(output_image)

def select_map_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    map_file_path.set(file_path)

def select_tileset_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    tileset_image_path.set(file_path)

def save_output_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    output_image_path.set(file_path)

def render():
    try:
        render_map(map_file_path.get(), tileset_image_path.get(), output_image_path.get())
        messagebox.showinfo("Success", "Map rendered successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Tkinter GUI
root = tk.Tk()
root.title("Map Renderer")

map_file_path = tk.StringVar()
tileset_image_path = tk.StringVar()
output_image_path = tk.StringVar()

tk.Label(root, text="Map File:").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=map_file_path, width=50).grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse...", command=select_map_file).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Tileset Image:").grid(row=1, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=tileset_image_path, width=50).grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse...", command=select_tileset_image).grid(row=1, column=2, padx=5, pady=5)

tk.Label(root, text="Output Image:").grid(row=2, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=output_image_path, width=50).grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text="Browse...", command=save_output_image).grid(row=2, column=2, padx=5, pady=5)

tk.Button(root, text="Render Map", command=render).grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()
