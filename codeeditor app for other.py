import tkinter as tk
from tkinter import filedialog

class CodeEditorApp:
    def __init__(self, root):
        self.root = root
        root.title("Code Editor")

        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        # Create ListBox
        self.list_box = tk.Listbox(self.root)
        self.list_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create Text widget
        self.text_widget = tk.Text(self.root)
        self.text_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create Insert Code button
        self.insert_button = tk.Button(self.root, text="Insert Code", command=self.insert_code)
        self.insert_button.pack()

    def create_menu(self):
        # Create a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Add File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Load File", command=self.load_file)
        self.file_menu.add_command(label="Save", command=self.save_file)

    def insert_code(self):
        selected_indices = self.list_box.curselection()
        if selected_indices:
            selected_line = self.list_box.get(selected_indices[0])
            self.text_widget.insert(tk.END, f"{selected_line}\n")

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                self.list_box.delete(0, tk.END)
                for line in file:
                    self.list_box.insert(tk.END, line.strip())

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_widget.get("1.0", tk.END))

# Create the main window and pass it to the CodeEditorApp class
root = tk.Tk()
app = CodeEditorApp(root)
root.mainloop()
