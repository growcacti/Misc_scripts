import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import os
from datetime import datetime

class FileExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('File Explorer')
        self.root.geometry('1000x600')  # Adjust size as needed

        self.path = os.getcwd()
        self.output_folder = ''

        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        # Directory Tree Frame
        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')
        self.pathdir = tk.Entry(self.tree_frame, width=50, bd=10, bg='alice blue')
        self.pathdir.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.tree = ttk.Treeview(self.tree_frame, columns=('Directory Structure',), show='tree')
        self.tree.grid(row=1, column=0, sticky='nsew')

        self.tree_scroll = ttk.Scrollbar(self.tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.config(yscrollcommand=self.tree_scroll.set)
        self.tree_scroll.grid(row=1, column=1, sticky='ns')

        # File Information List Frame
        self.list_frame = ttk.Frame(self.root)
        self.list_frame.grid(row=0, column=1, padx=10, pady=5, sticky='nsew')
        self.root.grid_columnconfigure(1, weight=1)

        # File List Labels
        self.file_list_label = ttk.Label(self.list_frame, text='Filename')
        self.file_list_label.grid(row=0, column=0, padx=5, pady=5)

        self.file_size_list_label = ttk.Label(self.list_frame, text='Size (KB)')
        self.file_size_list_label.grid(row=0, column=1, padx=5, pady=5)

        self.file_date_list_label = ttk.Label(self.list_frame, text='Modification Date')
        self.file_date_list_label.grid(row=0, column=2, padx=5, pady=5)

        self.file_type_list_label = ttk.Label(self.list_frame, text='Type')
        self.file_type_list_label.grid(row=0, column=3, padx=5, pady=5)

        # File Listboxes
        self.file_list = tk.Listbox(self.list_frame, width=30, height=20)
        self.file_list.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        self.file_size = tk.Listbox(self.list_frame, width=20, height=20)
        self.file_size.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

        self.file_date = tk.Listbox(self.list_frame, width=30, height=20)
        self.file_date.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

        self.file_type = tk.Listbox(self.list_frame, width=20, height=20)
        self.file_type.grid(row=1, column=3, padx=5, pady=5, sticky='nsew')

        self.list_frame.grid_rowconfigure(1, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)

        # Main Options Frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='ew')

        tk.Label(self.main_frame, text='').grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.main_frame, text='Refresh', command=self.refresh_view).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.main_frame.grid_columnconfigure(1, weight=1)

    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label='Select Directory', command=self.select_directory)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

    def select_directory(self):
        self.pathdir.delete(0, tk.END)
        self.path = filedialog.askdirectory()
        if self.path:
            self.pathdir.insert(0, self.path)
            self.populate_treeview(self.path)
            self.populate_file_info(self.path)

    def populate_treeview(self, root_path):
        self.tree.delete(*self.tree.get_children())  # Clear existing items in the Treeview
        for entry in os.scandir(root_path):
            if entry.is_dir():
                self.tree.insert('', 'end', entry.path, text=entry.name)

    def populate_file_info(self, dir_path):
        self.file_list.delete(0, tk.END)
        self.file_size.delete(0, tk.END)
        self.file_date.delete(0, tk.END)
        self.file_type.delete(0, tk.END)

        for file in os.scandir(dir_path):
            if file.is_file():
                self.file_list.insert(tk.END, file.name)
                self.file_size.insert(tk.END, f"{os.path.getsize(file.path) / 1024:.2f}")
                self.file_date.insert(tk.END, datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'))
                self.file_type.insert(tk.END, file.name.split('.')[-1] if '.' in file.name else 'Unknown')

    def refresh_view(self):
        if self.path:
            self.populate_file_info(self.path)

if __name__ == '__main__':
    root = tk.Tk()
    app = FileExplorerApp(root)
    root.mainloop()
