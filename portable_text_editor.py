import tkinter as tk
from tkinter import Menu, simpledialog, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import re

class TextEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Text Editor with Pattern Replacement')
        
        # Text editor area
        self.text_area = ScrolledText(root, undo=True)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # Menu setup
        menu = Menu(root)
        root.config(menu=menu)
        
        # File menu
        file_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open...", command=self.load_file)
        file_menu.add_command(label="Save As...", command=self.save_file)
        file_menu.add_separator()
        
        # Edit menu
        edit_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Replace After Pattern...", command=self.replace_after_pattern)
        edit_menu.add_command(label="Replace Before Pattern...", command=self.replace_before_pattern)
        
        # Regex operations menu
        regex_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Regex", menu=regex_menu)
        regex_menu.add_command(label="Regex Substitute...", command=self.regex_substitute)
    
    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", file.read())
    
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get("1.0", tk.END))
    
    def get_pattern_and_replacement(self, prompt):
        pattern = simpledialog.askstring("Input", f"Enter pattern {prompt}:")
        if not pattern:
            return None, None
        replacement = simpledialog.askstring("Input", "Enter replacement text:")
        return pattern, replacement
    
    def replace_after_pattern(self):
        pattern, replacement = self.get_pattern_and_replacement("to replace after (inclusive)")
        if pattern is not None:
            modified_text = re.sub(f"{pattern}.*", f"{pattern}{replacement}", self.text_area.get("1.0", tk.END))
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", modified_text)
    
    def replace_before_pattern(self):
        pattern, replacement = self.get_pattern_and_replacement("to replace before (exclusive)")
        if pattern is not None:
            modified_text = re.sub(f".*{pattern}", f"{replacement}{pattern}", self.text_area.get("1.0", tk.END), count=1)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", modified_text)
    
    def regex_substitute(self):
        pattern, replacement = self.get_pattern_and_replacement("for regex substitute")
        if pattern is not None:
            modified_text = re.sub(pattern, replacement, self.text_area.get("1.0", tk.END))
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", modified_text)

# Main window
root = tk.Tk()
app = TextEditorApp(root)
root.mainloop()
