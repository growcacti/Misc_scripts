import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json

class FileStatAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("File and Directory Analyzer")
        
        # Frame for Path Selection and Buttons
        top_frame = tk.Frame(root)
        top_frame.pack(padx=10, pady=10, fill=tk.X)
        
        self.path_entry = tk.Entry(top_frame, width=50)
        self.path_entry.pack(side=tk.LEFT, expand=True, padx=(0, 5))
        
        self.browse_button = tk.Button(top_frame, text="Browse...", command=self.browse_directory)
        self.browse_button.pack(side=tk.LEFT)
        
        # Frame for Actions
        action_frame = tk.Frame(root)
        action_frame.pack(padx=10, pady=5, fill=tk.X)
        
        self.scan_button = tk.Button(action_frame, text="Scan Directory", command=self.scan_directory)
        self.scan_button.pack(side=tk.LEFT, expand=True)
        
        self.save_button = tk.Button(action_frame, text="Save Results", command=self.save_results)
        self.save_button.pack(side=tk.LEFT, expand=True)
        
        self.load_button = tk.Button(action_frame, text="Load Results", command=self.load_results)
        self.load_button.pack(side=tk.LEFT, expand=True)
        
        # Text Display
        self.result_text = tk.Text(root, height=15, width=80)
        self.result_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, directory)

    def scan_directory(self):
        directory = self.path_entry.get()
        if not os.path.isdir(directory):
            messagebox.showerror("Error", "The specified path is not a directory.")
            return
        
        file_count = 0
        dir_count = 0
        total_size = 0
        
        for root, dirs, files in os.walk(directory):
            dir_count += len(dirs)
            file_count += len(files)
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    total_size += os.path.getsize(file_path)
        
        result = {
            "Directory": directory,
            "Total Files": file_count,
            "Total Directories": dir_count,
            "Total Size (Bytes)": total_size,
            "Total Size (Readable)": self.size_format(total_size)
        }
        self.display_result(result)
        self.current_result = result

    def display_result(self, result):
        self.result_text.delete(1.0, tk.END)
        for key, value in result.items():
            self.result_text.insert(tk.END, f"{key}: {value}\n")
    
    def size_format(self, size, suffix="B"):
        for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
            if abs(size) < 1024.0:
                return f"{size:3.1f} {unit}{suffix}"
            size /= 1024.0
        return f"{size:.1f} Yi{suffix}"
    
    def save_results(self):
        if not hasattr(self, 'current_result'):
            messagebox.showerror("Error", "No results to save.")
            return
        with open("file_stats.json", "w") as file:
            json.dump(self.current_result, file)
        messagebox.showinfo("Save Successful", "Results have been saved to file_stats.json.")
    
    def load_results(self):
        try:
            with open("file_stats.json", "r") as file:
                result = json.load(file)
            self.display_result(result)
            messagebox.showinfo("Load Successful", "Results have been loaded.")
        except FileNotFoundError:
            messagebox.showerror("File Not Found", "The file_stats.json file does not exist.")
        except json.JSONDecodeError:
            messagebox.showerror("Load Error", "Error decoding the results.")

root = tk.Tk()
app = FileStatAnalyzer(root)
root.mainloop()
