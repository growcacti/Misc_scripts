import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import re

class TextManipulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Manipulation App with Menu")

        # Add a Menu
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        # File Menu
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Load Text", command=self.load_text)
        file_menu.add_command(label="Save Text", command=self.save_text)
        self.menu.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tk.Menu(self.menu, tearoff=0)
        edit_menu.add_command(label="Find and Replace", command=self.find_and_replace)
        edit_menu.add_command(label="Word Count", command=self.word_count)
        edit_menu.add_command(label="Character Count", command=self.character_count)
        edit_menu.add_command(label="Line Count", command=self.line_count)
        edit_menu.add_command(label="Regex Search", command=self.regex_search)
        self.menu.add_cascade(label="Edit", menu=edit_menu)

        # Text widget for displaying text
        self.text_widget = tk.Text(root, wrap='word', height=15, width=60)
        self.text_widget.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Load Text Button
        self.load_button = tk.Button(root, text="Load Text", command=self.load_text)
        self.load_button.grid(row=1, column=0, padx=5, pady=5)

        # Save Text Button
        self.save_button = tk.Button(root, text="Save Text", command=self.save_text)
        self.save_button.grid(row=1, column=1, padx=5, pady=5)

        # Reverse Text Button
        self.reverse_button = tk.Button(root, text="Reverse Text", command=self.reverse_text)
        self.reverse_button.grid(row=2, column=0, padx=5, pady=5)

        # Convert to Uppercase Button
        self.uppercase_button = tk.Button(root, text="To Uppercase", command=self.to_uppercase)
        self.uppercase_button.grid(row=2, column=1, padx=5, pady=5)

        # Convert to Lowercase Button
        self.lowercase_button = tk.Button(root, text="To Lowercase", command=self.to_lowercase)
        self.lowercase_button.grid(row=2, column=2, padx=5, pady=5)

        # Remove Whitespace Button
        self.trim_button = tk.Button(root, text="Trim Whitespace", command=self.trim_whitespace)
        self.trim_button.grid(row=2, column=3, padx=5, pady=5)

    def load_text(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.text_widget.delete(1.0, tk.END)
                    self.text_widget.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def save_text(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    content = self.text_widget.get(1.0, tk.END)
                    file.write(content)
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def reverse_text(self):
        content = self.text_widget.get(1.0, tk.END).strip()
        reversed_content = content[::-1]
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, reversed_content)

    def to_uppercase(self):
        content = self.text_widget.get(1.0, tk.END).strip()
        upper_content = content.upper()
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, upper_content)

    def to_lowercase(self):
        content = self.text_widget.get(1.0, tk.END).strip()
        lower_content = content.lower()
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, lower_content)

    def trim_whitespace(self):
        content = self.text_widget.get(1.0, tk.END)
        trimmed_content = content.strip()
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, trimmed_content)

    def find_and_replace(self):
        find_str = simpledialog.askstring("Find", "Enter the word to find:")
        replace_str = simpledialog.askstring("Replace", "Enter the word to replace:")
        if find_str and replace_str:
            content = self.text_widget.get(1.0, tk.END)
            new_content = content.replace(find_str, replace_str)
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, new_content)

    def word_count(self):
        content = self.text_widget.get(1.0, tk.END).strip()
        words = len(content.split())
        messagebox.showinfo("Word Count", f"Total Words: {words}")

    def character_count(self):
        content = self.text_widget.get(1.0, tk.END).strip()
        characters = len(content)
        messagebox.showinfo("Character Count", f"Total Characters: {characters}")

    def line_count(self):
        content = self.text_widget.get(1.0, tk.END).strip()
        lines = content.count('\n') + 1
        messagebox.showinfo("Line Count", f"Total Lines: {lines}")

    def regex_search(self):
        pattern = simpledialog.askstring("Regex Search", "Enter the regex pattern:")
        if pattern:
            content = self.text_widget.get(1.0, tk.END)
            matches = re.findall(pattern, content)
            messagebox.showinfo("Regex Search", f"Matches found: {matches}" if matches else "No matches found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextManipulationApp(root)
    root.mainloop()
