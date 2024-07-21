import tkinter as tk
from tkinter import filedialog, messagebox
import json
import lz4.block
import os

class JsonToHtmlConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON to HTML Converter")
        tk.Label(self.root, text="Select JSON File:").grid(row=0, column=0, padx=5, pady=5)
        self.json_entry = tk.Entry(self.root, width=50)
        self.json_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_json).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(self.root, text="Convert and Save as HTML", command=self.convert_and_save).grid(row=1, column=1, padx=5, pady=20)
        tk.Button(self.root, text="lz4 block extention", command=self.read_jsonlz4).grid(row=3, column=1, padx=5, pady=20)
    def browse_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        if file_path:
            self.json_entry.delete(0, tk.END)
            self.json_entry.insert(0, file_path)

    def convert_and_save(self):
        json_path = self.json_entry.get()
        if not json_path:
            messagebox.showwarning("Input Error", "Please select a JSON file.")
            return
        
        try:
            with open(json_path, 'r') as json_file:
                json_data = json.load(json_file)
            
            html_data = self.json_to_html(json_data)
            
            save_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html"), ("All Files", "*.*")])
            if save_path:
                with open(save_path, 'w') as html_file:
                    html_file.write(html_data)
                messagebox.showinfo("Success", "File successfully saved as HTML.")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def json_to_html(self, json_data):
        html_content = '<html>\n<head>\n<title>JSON to HTML</title>\n</head>\n<body>\n'
        html_content += self.dict_to_html(json_data)
        html_content += '\n</body>\n</html>'
        return html_content

    def dict_to_html(self, data, level=0):
        html_content = ""
        indent = "  " * level
        if isinstance(data, dict):
            html_content += f'{indent}<ul>\n'
            for key, value in data.items():
                html_content += f'{indent}  <li><strong>{key}:</strong> {self.dict_to_html(value, level + 1)}</li>\n'
            html_content += f'{indent}</ul>\n'
        elif isinstance(data, list):
            html_content += f'{indent}<ul>\n'
            for item in data:
                html_content += f'{indent}  <li>{self.dict_to_html(item, level + 1)}</li>\n'
            html_content += f'{indent}</ul>\n'
        else:
              html_content += str(data)
        return html_content


    def read_jsonlz4(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        self.json_entry.delete(0, tk.END)
        self.json_entry.insert(0, file_path)
        try:
            with open(file_path, 'rb') as file:
                # The first 8 bytes are a magic number for Mozilla's JSONLZ4 format
                file.read(8)
                compressed_data = file.read()
                decompressed_data = lz4.block.decompress(compressed_data)
                json_data = json.loads(decompressed_data)
                html_data = self.json_to_html(json_data)
                
                save_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html"), ("All Files", "*.*")])
                if save_path:
                    with open(save_path, 'w') as html_file:
                        html_file.write(html_data)
                    messagebox.showinfo("Success", "File successfully saved as HTML.")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return json_data

   
   

if __name__ == '__main__':
    root = tk.Tk()
    app = JsonToHtmlConverter(root)
    root.mainloop()
